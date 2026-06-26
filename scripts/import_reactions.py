from __future__ import annotations

import json
import os
import re
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOURCE_PDF = Path(os.environ["USERPROFILE"]) / "Downloads" / "最全高中化学方程式分类汇总.pdf"
SOURCE_TXT = Path(os.environ["USERPROFILE"]) / "Downloads" / "最全高中化学方程式分类汇总.txt"
OUTPUT_JS = ROOT / "src" / "data" / "generatedReactionText.js"
OUTPUT_INDEX_JS = ROOT / "src" / "data" / "generatedReactionIndex.js"

EQUATION_FIXES = {
    "K2CO3+CaCl2->CaCO3↓+2KC": "K2CO3+CaCl2 -> CaCO3↓+2KCl",
    "Be+2HCl->BaCl2+H2↑": "Be+2HCl -> BeCl2+H2↑",
    "Be+2NaOH->Na2BO2+H2↑": "Be+2NaOH -> Na2BeO2+H2↑",
    "Be(OH)2+2NaOH->Na2BO2+2H2O": "Be(OH)2+2NaOH -> Na2BeO2+2H2O",
    "3Hg+8HNO3->3Hg(NO3)2+2NO2↑+4H2O": "3Hg+8HNO3 -> 3Hg(NO3)2+2NO↑+4H2O",
    "Hg+4HNO3->Hg(NO3)2+2NO2↑+2H2": "Hg+4HNO3 -> Hg(NO3)2+2NO2↑+2H2O",
}


def is_header_or_noise(line: str) -> bool:
    if not line:
        return True
    if "高中化学方程式总结，第" in line:
        return True
    if line in {"目录", "高", "中", "化", "学", "方", "程", "式", "总", "结"}:
        return True
    if re.fullmatch(r"第[一二三四五六七八九十]+部分.*", line):
        return True
    if re.fullmatch(r"[一二三四五六七八九十]+[、 ].*", line):
        return True
    if re.fullmatch(r"\d+\..*", line):
        return True
    if re.fullmatch(r"[^\w\u4e00-\u9fff]*", line):
        return True
    if "……………………" in line:
        return True
    return False


def is_chemicalish(line: str) -> bool:
    text = line.strip()
    if not text:
        return False
    return bool(re.search(r"[A-Z][a-z]?\d*", text))


def can_join_multiline(left: str, right: str) -> bool:
    left = left.strip()
    right = right.strip()
    if not left or not right:
        return False
    if any(sign in left for sign in ["＝", "=", "→"]) or any(sign in right for sign in ["＝", "=", "→"]):
        return False
    left_like_reactants = ("+" in left) or bool(re.match(r"^\d+[A-Z][A-Za-z0-9\(\)\[\]·\.]*$", left))
    right_like_products = "+" in right
    if not left_like_reactants or not right_like_products:
        return False
    return True


def strip_notes(text: str) -> str:
    result = text
    result = result.replace(" ", "")
    result = result.replace("　", "")
    result = result.replace("→", "＝")
    result = result.replace("=", "＝")
    result = result.replace("⇌", "＝")
    result = result.replace("【", "").replace("】", "")
    result = re.sub(r"（[^）]*）", "", result)
    result = re.sub(r"\((?=[^)]*[\u4e00-\u9fff])[^)]*\)", "", result)
    result = re.sub(r"（.*$", "", result)
    result = re.sub(r"\((?=.*[\u4e00-\u9fff]).*$", "", result)
    result = re.sub(r"\(([glsaq])\)", "", result)
    result = result.replace("．", ".").replace("•", "·")
    result = result.replace("；", "")
    return result.strip()


def has_unreliable_pdf_text(text: str) -> bool:
    if not text:
        return True
    if any(mark in text for mark in ["\uf02d", "\uf02b", "ΔH", "kJ", "mol-1", "——", "—", "≡", "："]):
        return True
    if re.search(r"[\u4e00-\u9fff]", text):
        return True
    return False


def normalize_equation(text: str) -> str:
    cleaned = strip_notes(text)
    if cleaned.count("＝") != 1:
        return ""
    left, right = cleaned.split("＝", 1)
    left = left.strip(" =")
    right = right.strip(" =")
    if not left or not right:
        return ""
    equation = f"{left} -> {right}"
    if has_unreliable_pdf_text(equation):
        return ""
    compact = equation.replace(" ", "")
    return EQUATION_FIXES.get(compact, equation)


def split_tokens(side: str) -> list[str]:
    return [token for token in side.split("+") if token]


def clean_formula(token: str) -> str:
    value = token.strip()
    value = re.sub(r"^\d+(?=[A-Z\(])", "", value)
    value = value.replace("↑", "").replace("↓", "")
    value = re.sub(r"\((?=[^)]*[\u4e00-\u9fff])[^)]*\)", "", value)
    value = re.sub(r"（[^）]*）", "", value)
    value = value.strip()
    return value


def extract_formulas(equation: str) -> list[str]:
    left, right = equation.split("->", 1)
    values: list[str] = []
    seen: set[str] = set()
    for token in split_tokens(left) + split_tokens(right):
        formula = clean_formula(token)
        if not formula:
            continue
        if has_unreliable_pdf_text(formula):
            continue
        if not re.search(r"[A-Z]", formula):
            continue
        if formula in seen:
            continue
        seen.add(formula)
        values.append(formula)
    return values


def normalize_formula(value: str) -> str:
    normalized = re.sub(r"\s+", "", value or "").lower()
    return re.sub(r"\^(\d*[+-])$", r"\1", normalized)


def load_source_text() -> str:
    if SOURCE_PDF.exists():
        try:
            from pypdf import PdfReader

            reader = PdfReader(str(SOURCE_PDF))
            pages = []
            for page in reader.pages:
                pages.append(page.extract_text() or "")
            return "\n".join(pages)
        except Exception:
            pass
    return SOURCE_TXT.read_text(encoding="utf-8")


def load_existing_generated_reactions() -> list[dict]:
    if not OUTPUT_JS.exists():
        return []

    source = OUTPUT_JS.read_text(encoding="utf-8")
    match = re.search(r"export const generatedReactionText = (.*)\s*$", source, re.S)
    if not match:
        return []

    payload = match.group(1).strip()
    if payload.endswith(";"):
        payload = payload[:-1]

    text = json.loads(payload)
    reactions: list[dict] = []
    for index, line in enumerate(text.splitlines()):
        divider = line.find("\t")
        if divider <= 0:
            continue
        formulas = [formula for formula in line[:divider].split(",") if formula]
        equation = line[divider + 1 :]
        if len(formulas) < 2 or not equation:
            continue
        reactions.append(
            {
                "id": f"generated_{index}",
                "formulas": formulas,
                "equation": equation,
                "type": "",
                "conditions": "",
                "phenomenon": "",
                "source": "generatedReactionText.js",
            }
        )
    return reactions


def build_candidates(lines: list[str]) -> list[str]:
    candidates: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line or is_header_or_noise(line):
            i += 1
            continue

        if "＝" in line or "=" in line or "→" in line:
            combined = line
            if combined.rstrip().endswith(("＝", "=")) and i + 1 < len(lines) and is_chemicalish(lines[i + 1]):
                combined = combined + lines[i + 1].strip()
                i += 1
            candidates.append(combined)
            i += 1
            continue

        if i + 1 < len(lines):
            nxt = lines[i + 1].strip()
            if can_join_multiline(line, nxt):
                candidates.append(f"{line}＝{nxt}")
                i += 2
                continue

        i += 1
    return candidates


def load_reactions() -> list[dict]:
    try:
        text = load_source_text()
    except FileNotFoundError:
        existing_reactions = load_existing_generated_reactions()
        if existing_reactions:
            return existing_reactions
        raise

    lines = text.splitlines()
    candidates = build_candidates(lines)

    reactions: list[dict] = []
    seen_equations: set[str] = set()

    for candidate in candidates:
        equation = normalize_equation(candidate)
        if not equation:
            continue
        formulas = extract_formulas(equation)
        if len(formulas) < 2:
            continue
        if equation in seen_equations:
            continue
        seen_equations.add(equation)

        digest = hashlib.md5(equation.encode("utf-8")).hexdigest()[:10]
        reactions.append(
            {
                "id": f"pdf_{digest}",
                "formulas": formulas,
                "equation": equation,
                "type": "",
                "conditions": "",
                "phenomenon": "",
                "source": "最全高中化学方程式分类汇总.pdf",
            }
        )

    return reactions


def write_output(reactions: list[dict]) -> None:
    lines = []
    for reaction in reactions:
        formulas = ",".join(reaction["formulas"])
        equation = reaction["equation"]
        lines.append(f"{formulas}\t{equation}")
    payload = json.dumps("\n".join(lines), ensure_ascii=False)
    OUTPUT_JS.write_text(f"export const generatedReactionText = {payload}\n", encoding="utf-8")


def build_formula_index(reactions: list[dict]) -> dict[str, list[int]]:
    index: dict[str, list[int]] = {}
    for reaction_index, reaction in enumerate(reactions):
        added: set[str] = set()
        for formula in reaction["formulas"]:
            normalized = normalize_formula(formula)
            if not normalized or normalized in added:
                continue
            added.add(normalized)
            index.setdefault(normalized, []).append(reaction_index)
    return dict(sorted(index.items()))


def write_index_output(reactions: list[dict]) -> None:
    equations = [reaction["equation"] for reaction in reactions]
    formula_index = build_formula_index(reactions)
    equations_payload = json.dumps(equations, ensure_ascii=False, separators=(",", ":"))
    index_payload = json.dumps(formula_index, ensure_ascii=False, separators=(",", ":"))
    OUTPUT_INDEX_JS.write_text(
        "export const generatedEquations = "
        + equations_payload
        + "\nexport const generatedFormulaIndex = "
        + index_payload
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    reactions = load_reactions()
    write_output(reactions)
    write_index_output(reactions)
    from build_reaction_database import main as build_reaction_database

    build_reaction_database()
    print(f"Generated {len(reactions)} source reactions -> {OUTPUT_JS}, {OUTPUT_INDEX_JS}")


if __name__ == "__main__":
    main()
