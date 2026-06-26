from __future__ import annotations

import json
import math
import re
from itertools import product
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TEXT_OUTPUT = ROOT / "src" / "data" / "generatedReactionText.js"
INDEX_OUTPUT = ROOT / "src" / "data" / "generatedReactionIndex.js"

COMMONNESS_RANK = {"高": 0, "中": 1, "低": 2}
VISIBILITY_RANK = {"明显": 0, "一般": 1, "不明显": 2}


def clean_formula_token(value: str) -> str:
    return re.sub(r"^\d+", "", value.replace("↑", "").replace("↓", "").strip())


def parse_formula(formula: str) -> dict[str, int]:
    value = clean_formula_token(formula)
    value = value.replace("·", "")
    stack: list[dict[str, int]] = [{}]
    index = 0

    while index < len(value):
        char = value[index]
        if char == "(":
            stack.append({})
            index += 1
            continue
        if char == ")":
            index += 1
            start = index
            while index < len(value) and value[index].isdigit():
                index += 1
            multiplier = int(value[start:index] or "1")
            group = stack.pop()
            for element, count in group.items():
                stack[-1][element] = stack[-1].get(element, 0) + count * multiplier
            continue
        if char.isupper():
            start = index
            index += 1
            if index < len(value) and value[index].islower():
                index += 1
            element = value[start:index]
            start = index
            while index < len(value) and value[index].isdigit():
                index += 1
            count = int(value[start:index] or "1")
            stack[-1][element] = stack[-1].get(element, 0) + count
            continue
        index += 1

    return stack[0]


def balance_reaction(reactants: list[str], products: list[str], max_coeff: int = 18) -> tuple[int, ...] | None:
    species = reactants + products
    counts = [parse_formula(item) for item in species]
    elements = sorted({element for count in counts for element in count})
    reactant_count = len(reactants)

    for coeffs in product(range(1, max_coeff + 1), repeat=len(species)):
        valid = True
        for element in elements:
            left = 0
            right = 0
            for index, count in enumerate(counts):
                value = coeffs[index] * count.get(element, 0)
                if index < reactant_count:
                    left += value
                else:
                    right += value
            if left != right:
                valid = False
                break
        if valid:
            divisor = coeffs[0]
            for coeff in coeffs[1:]:
                divisor = math.gcd(divisor, coeff)
            return tuple(coeff // divisor for coeff in coeffs)
    return None


def format_species(formula: str, coefficient: int, mark: str = "") -> str:
    prefix = "" if coefficient == 1 else str(coefficient)
    return prefix + formula + mark


def format_equation(
    reactants: list[str],
    products: list[str],
    coeffs: tuple[int, ...],
    product_marks: dict[str, str] | None = None,
) -> str:
    product_marks = product_marks or {}
    left = " + ".join(format_species(formula, coeffs[index]) for index, formula in enumerate(reactants))
    offset = len(reactants)
    right = " + ".join(
        format_species(formula, coeffs[offset + index], product_marks.get(formula, ""))
        for index, formula in enumerate(products)
    )
    return left + " -> " + right


def is_polyatomic(formula: str) -> bool:
    return formula in {
        "NH4",
        "OH",
        "NO3",
        "SO4",
        "SO3",
        "CO3",
        "HCO3",
        "PO4",
        "CH3COO",
        "SiO3",
        "ClO",
        "ClO3",
        "MnO4",
        "CrO4",
    }


def ion_part(formula: str, count: int) -> str:
    if count == 1:
        return formula
    if is_polyatomic(formula):
        return "(" + formula + ")" + str(count)
    return formula + str(count)


def combine(cation: dict, anion: dict) -> str:
    cation_charge = cation["charge"]
    anion_charge = abs(anion["charge"])
    divisor = math.gcd(cation_charge, anion_charge)
    cation_count = anion_charge // divisor
    anion_count = cation_charge // divisor
    return ion_part(cation["formula"], cation_count) + ion_part(anion["formula"], anion_count)


def acid_formula(anion: dict) -> str:
    custom = {
        "Cl": "HCl",
        "Br": "HBr",
        "I": "HI",
        "F": "HF",
        "NO3": "HNO3",
        "ClO": "HClO",
        "CH3COO": "CH3COOH",
    }
    if anion["formula"] in custom:
        return custom[anion["formula"]]
    return "H" + (str(abs(anion["charge"])) if abs(anion["charge"]) > 1 else "") + anion["formula"]


def hydroxide_formula(cation: dict) -> str:
    return combine(cation, {"formula": "OH", "charge": -1})


def normalize_equation(value: str) -> str:
    normalized = re.sub(r"\s+", "", value).replace("＝", "->").replace("=", "->")
    parts = normalized.split("->")
    if len(parts) != 2:
        return normalized.lower()
    left = "+".join(sorted(item for item in parts[0].split("+") if item))
    right = "+".join(sorted(item for item in parts[1].split("+") if item))
    return (left + "->" + right).lower()


def normalize_formula(value: str) -> str:
    normalized = re.sub(r"\s+", "", value or "").lower()
    return re.sub(r"\^(\d*[+-])$", r"\1", normalized)


def reaction_formulas(reactants: list[str], products: list[str]) -> list[str]:
    values: list[str] = []
    seen: set[str] = set()
    for formula in reactants + products:
        cleaned = clean_formula_token(formula)
        if cleaned in {"CO2", "H2O"}:
            pass
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            values.append(cleaned)
    return values


def make_record(
    reactants: list[str],
    products: list[str],
    meta: dict,
    product_marks: dict[str, str] | None = None,
    max_coeff: int = 18,
) -> dict | None:
    coeffs = balance_reaction(reactants, products, max_coeff)
    if not coeffs:
        return None
    equation = format_equation(reactants, products, coeffs, product_marks)
    return {
        "formulas": reaction_formulas(reactants, products),
        "equation": equation,
        "type": meta.get("type", ""),
        "conditions": meta.get("conditions", ""),
        "phenomenon": meta.get("phenomenon", ""),
        "commonness": meta.get("commonness", ""),
        "visibility": meta.get("visibility", ""),
        "source": meta.get("source", "规则生成"),
    }


def load_existing_reactions() -> list[dict]:
    if not TEXT_OUTPUT.exists():
        return []
    source = TEXT_OUTPUT.read_text(encoding="utf-8")
    match = re.search(r"export const generatedReactionText = (.*)\s*$", source, re.S)
    if not match:
        return []
    payload = match.group(1).strip()
    if payload.endswith(";"):
        payload = payload[:-1]
    text = json.loads(payload)
    reactions = []
    for line in text.splitlines():
        divider = line.find("\t")
        if divider <= 0:
            continue
        formulas = [clean_formula_token(item) for item in line[:divider].split(",") if clean_formula_token(item)]
        equation = line[divider + 1 :].strip()
        reactions.append({
            "formulas": formulas,
            "equation": equation,
            "type": "",
            "conditions": "",
            "phenomenon": "",
            "commonness": "",
            "visibility": "",
            "source": "generatedReactionText.js",
        })
    return reactions


def is_clean_equation(reaction: dict) -> bool:
    equation = reaction["equation"]
    if "->" not in equation:
        return False
    left, right = equation.split("->", 1)
    if not left.strip() or not right.strip():
        return False
    if left.strip().startswith("+") or right.strip().startswith("+"):
        return False
    if left.strip().endswith("+") or right.strip().endswith("+"):
        return False
    if not re.search(r"[A-Z]", left) or not re.search(r"[A-Z]", right):
        return False
    if re.search(r"->\s*\d+\s*$", equation):
        return False
    if len(reaction.get("formulas", [])) < 2:
        return False
    if any(fragment in equation for fragment in ["-> 2", "-> 3"]) and not re.search(r"->\s*\d+[A-Z(]", equation):
        return False
    return True


def infer_existing_metadata(reaction: dict) -> dict:
    equation = reaction["equation"]
    next_reaction = dict(reaction)
    if "↓" in equation:
        next_reaction["type"] = "复分解反应"
        next_reaction["conditions"] = "溶液中"
        next_reaction["phenomenon"] = "生成沉淀"
        next_reaction["commonness"] = "中"
        next_reaction["visibility"] = "明显"
    elif "↑" in equation:
        next_reaction["conditions"] = "常温或加热"
        next_reaction["phenomenon"] = "有气体生成"
        next_reaction["commonness"] = "中"
        next_reaction["visibility"] = "明显"
    elif "O2" in equation and "CO2" in equation and "H2O" in equation:
        next_reaction["type"] = "氧化反应"
        next_reaction["conditions"] = "点燃"
        next_reaction["phenomenon"] = "燃烧放热"
        next_reaction["commonness"] = "中"
        next_reaction["visibility"] = "明显"
    return next_reaction


CATIONS = {
    "Na": {"formula": "Na", "charge": 1, "name": "钠"},
    "K": {"formula": "K", "charge": 1, "name": "钾"},
    "Li": {"formula": "Li", "charge": 1, "name": "锂"},
    "NH4": {"formula": "NH4", "charge": 1, "name": "铵"},
    "Ag": {"formula": "Ag", "charge": 1, "name": "银"},
    "Mg": {"formula": "Mg", "charge": 2, "name": "镁"},
    "Ca": {"formula": "Ca", "charge": 2, "name": "钙"},
    "Ba": {"formula": "Ba", "charge": 2, "name": "钡"},
    "Zn": {"formula": "Zn", "charge": 2, "name": "锌"},
    "Cu": {"formula": "Cu", "charge": 2, "name": "铜"},
    "Fe2": {"formula": "Fe", "charge": 2, "name": "亚铁"},
    "Fe3": {"formula": "Fe", "charge": 3, "name": "铁"},
    "Al": {"formula": "Al", "charge": 3, "name": "铝"},
    "Pb": {"formula": "Pb", "charge": 2, "name": "铅"},
}

ANIONS = {
    "Cl": {"formula": "Cl", "charge": -1},
    "Br": {"formula": "Br", "charge": -1},
    "I": {"formula": "I", "charge": -1},
    "F": {"formula": "F", "charge": -1},
    "NO3": {"formula": "NO3", "charge": -1},
    "OH": {"formula": "OH", "charge": -1},
    "ClO": {"formula": "ClO", "charge": -1},
    "CH3COO": {"formula": "CH3COO", "charge": -1},
    "SO4": {"formula": "SO4", "charge": -2},
    "SO3": {"formula": "SO3", "charge": -2},
    "CO3": {"formula": "CO3", "charge": -2},
    "HCO3": {"formula": "HCO3", "charge": -1},
    "S": {"formula": "S", "charge": -2},
    "SiO3": {"formula": "SiO3", "charge": -2},
    "PO4": {"formula": "PO4", "charge": -3},
    "ClO3": {"formula": "ClO3", "charge": -1},
    "MnO4": {"formula": "MnO4", "charge": -1},
    "CrO4": {"formula": "CrO4", "charge": -2},
}


def generate_rule_reactions() -> list[dict]:
    records: list[dict] = []
    strong_acids = ["Cl", "NO3", "SO4"]
    acids = ["Cl", "NO3", "SO4", "CO3", "SO3", "PO4", "F", "Br", "I", "CH3COO", "S", "SiO3", "ClO"]
    bases = ["Na", "K", "Li", "Ca", "Ba", "Mg", "Al", "Zn", "Cu", "Fe2", "Fe3"]

    for acid_key in acids:
        for base_key in bases:
            acid = ANIONS[acid_key]
            base = CATIONS[base_key]
            acid_value = acid_formula(acid)
            base_value = hydroxide_formula(base)
            salt = combine(base, acid)
            commonness = "高" if acid_key in strong_acids and base_key in {"Na", "K", "Ca", "Ba"} else "中"
            record = make_record(
                [acid_value, base_value],
                [salt, "H2O"],
                {
                    "type": "中和反应",
                    "conditions": "酸碱接触，常温",
                    "phenomenon": "放热" if commonness == "高" else "酸碱中和，现象通常不明显",
                    "commonness": commonness,
                    "visibility": "一般" if commonness == "高" else "不明显",
                    "source": "高中反应规则生成",
                },
            )
            if record:
                records.append(record)

    carbon_cations = ["Na", "K", "Li", "NH4", "Ca", "Ba", "Mg", "Zn", "Cu", "Fe2", "Ag", "Pb"]
    for cation_key in carbon_cations:
        cation = CATIONS[cation_key]
        for acid_key in acids:
            acid = ANIONS[acid_key]
            salt = combine(cation, acid)
            for carbonate_key in ["CO3", "HCO3"]:
                carbonate = combine(cation, ANIONS[carbonate_key])
                record = make_record(
                    [carbonate, acid_formula(acid)],
                    [salt, "CO2", "H2O"],
                    {
                        "type": "复分解反应",
                        "conditions": "加入酸，常温",
                        "phenomenon": "有气泡产生，生成二氧化碳",
                        "commonness": "高" if acid_key in strong_acids and cation_key in {"Na", "Ca", "Ba"} else "中",
                        "visibility": "明显",
                        "source": "高中反应规则生成",
                    },
                    {"CO2": "↑"},
                )
                if record:
                    records.append(record)

    gas_anions = [
        ("SO3", "SO2", "有刺激性气味气体生成"),
        ("S", "H2S", "有臭鸡蛋气味气体生成"),
    ]
    for anion_key, gas, phenomenon in gas_anions:
        for cation_key in ["Na", "K", "NH4", "Mg", "Fe2", "Zn", "Cu", "Pb"]:
            cation = CATIONS[cation_key]
            salt_reactant = combine(cation, ANIONS[anion_key])
            for acid_key in strong_acids + ["CH3COO", "Br", "I"]:
                acid = ANIONS[acid_key]
                salt_product = combine(cation, acid)
                record = make_record(
                    [salt_reactant, acid_formula(acid)],
                    [salt_product, gas],
                    {
                        "type": "复分解反应",
                        "conditions": "加入酸，常温",
                        "phenomenon": phenomenon,
                        "commonness": "中",
                        "visibility": "明显",
                        "source": "高中反应规则生成",
                    },
                    {gas: "↑"},
                )
                if record:
                    records.append(record)

    precipitates = [
        ("Ag", "Cl", "白色沉淀", "高"),
        ("Ag", "Br", "淡黄色沉淀", "中"),
        ("Ag", "I", "黄色沉淀", "中"),
        ("Ag", "CO3", "浅黄色沉淀", "中"),
        ("Ag", "PO4", "黄色沉淀", "中"),
        ("Ag", "CrO4", "砖红色沉淀", "低"),
        ("Ba", "SO4", "白色沉淀", "高"),
        ("Ba", "CO3", "白色沉淀", "高"),
        ("Ba", "SO3", "白色沉淀", "中"),
        ("Ba", "CrO4", "黄色沉淀", "低"),
        ("Ca", "CO3", "白色沉淀", "高"),
        ("Ca", "SO3", "白色沉淀", "中"),
        ("Mg", "OH", "白色沉淀", "中"),
        ("Al", "OH", "白色胶状沉淀", "高"),
        ("Zn", "OH", "白色沉淀", "中"),
        ("Cu", "OH", "蓝色沉淀", "高"),
        ("Fe2", "OH", "白色沉淀迅速变灰绿色", "高"),
        ("Fe3", "OH", "红褐色沉淀", "高"),
        ("Cu", "S", "黑色沉淀", "中"),
        ("Pb", "S", "黑色沉淀", "中"),
        ("Ag", "S", "黑色沉淀", "中"),
        ("Zn", "S", "白色沉淀", "低"),
        ("Pb", "CrO4", "黄色沉淀", "低"),
    ]
    for cation_key, anion_key, color, commonness in precipitates:
        precipitate = combine(CATIONS[cation_key], ANIONS[anion_key])
        for counter_cation_key in ["Na", "K", "NH4"]:
            for counter_anion_key in ["NO3", "CH3COO"]:
                reactant_one = combine(CATIONS[cation_key], ANIONS[counter_anion_key])
                reactant_two = combine(CATIONS[counter_cation_key], ANIONS[anion_key])
                product_two = combine(CATIONS[counter_cation_key], ANIONS[counter_anion_key])
                record = make_record(
                    [reactant_one, reactant_two],
                    [precipitate, product_two],
                    {
                        "type": "复分解反应",
                        "conditions": "溶液中",
                        "phenomenon": "生成" + color,
                        "commonness": commonness,
                        "visibility": "明显",
                        "source": "高中沉淀规则生成",
                    },
                    {precipitate: "↓"},
                )
                if record:
                    records.append(record)

    hydroxide_cations = ["Mg", "Al", "Zn", "Cu", "Fe2", "Fe3"]
    for cation_key in hydroxide_cations:
        cation = CATIONS[cation_key]
        precipitate = combine(cation, ANIONS["OH"])
        color = {
            "Mg": "白色沉淀",
            "Al": "白色胶状沉淀",
            "Zn": "白色沉淀",
            "Cu": "蓝色沉淀",
            "Fe2": "白色沉淀迅速变灰绿色",
            "Fe3": "红褐色沉淀",
        }[cation_key]
        for anion_key in ["Cl", "NO3", "SO4"]:
            for base_key in ["Na", "K", "Ba"]:
                record = make_record(
                    [combine(cation, ANIONS[anion_key]), hydroxide_formula(CATIONS[base_key])],
                    [precipitate, combine(CATIONS[base_key], ANIONS[anion_key])],
                    {
                        "type": "复分解反应",
                        "conditions": "加入碱溶液",
                        "phenomenon": "生成" + color,
                        "commonness": "高" if cation_key in {"Cu", "Fe3", "Al"} else "中",
                        "visibility": "明显",
                        "source": "高中沉淀规则生成",
                    },
                    {precipitate: "↓"},
                )
                if record:
                    records.append(record)

    ammonium_anions = ["Cl", "NO3", "SO4", "CO3", "SO3", "PO4", "F", "Br", "I", "CH3COO"]
    for anion_key in ammonium_anions:
        ammonium_salt = combine(CATIONS["NH4"], ANIONS[anion_key])
        for base_key in ["Na", "K", "Ca", "Ba"]:
            base = CATIONS[base_key]
            record = make_record(
                [ammonium_salt, hydroxide_formula(base)],
                [combine(base, ANIONS[anion_key]), "NH3", "H2O"],
                {
                    "type": "复分解反应",
                    "conditions": "加热或与强碱混合",
                    "phenomenon": "有刺激性气味气体生成",
                    "commonness": "高" if anion_key == "Cl" else "中",
                    "visibility": "明显",
                    "source": "高中铵盐规则生成",
                },
                {"NH3": "↑"},
            )
            if record:
                records.append(record)

    metal_order = ["Mg", "Al", "Zn", "Fe2", "Pb", "Cu", "Ag"]
    metal_formulas = {"Fe2": "Fe"}
    for metal_index, metal_key in enumerate(metal_order[:4]):
        metal = CATIONS[metal_key]
        metal_formula = metal_formulas.get(metal_key, metal["formula"])
        for target_key in metal_order[metal_index + 1 :]:
            target = CATIONS[target_key]
            target_formula = metal_formulas.get(target_key, target["formula"])
            for anion_key in ["Cl", "NO3", "SO4", "CH3COO"]:
                record = make_record(
                    [metal_formula, combine(target, ANIONS[anion_key])],
                    [combine(metal, ANIONS[anion_key]), target_formula],
                    {
                        "type": "置换反应",
                        "conditions": "金属与盐溶液接触",
                        "phenomenon": "较活泼金属表面析出较不活泼金属",
                        "commonness": "高" if {metal_key, target_key} == {"Fe2", "Cu"} else "中",
                        "visibility": "明显" if target_key in {"Cu", "Ag"} else "一般",
                        "source": "金属活动性规则生成",
                    },
                )
                if record:
                    records.append(record)

    for metal_key in ["Mg", "Al", "Zn", "Fe2"]:
        metal = CATIONS[metal_key]
        metal_formula = metal_formulas.get(metal_key, metal["formula"])
        for acid_key in strong_acids + ["CH3COO", "Br", "I"]:
            acid = ANIONS[acid_key]
            record = make_record(
                [metal_formula, acid_formula(acid)],
                [combine(metal, acid), "H2"],
                {
                    "type": "置换反应",
                    "conditions": "稀酸，常温",
                    "phenomenon": "有气泡产生，生成氢气",
                    "commonness": "高" if metal_key in {"Zn", "Fe2"} and acid_key in {"Cl", "SO4"} else "中",
                    "visibility": "明显",
                    "source": "金属活动性规则生成",
                },
                {"H2": "↑"},
            )
            if record:
                records.append(record)

    oxide_cations = ["Na", "K", "Li", "Mg", "Ca", "Ba", "Zn", "Cu", "Fe2", "Fe3", "Al", "Pb"]
    for cation_key in oxide_cations:
        cation = CATIONS[cation_key]
        oxide = combine(cation, {"formula": "O", "charge": -2})
        for acid_key in acids:
            acid = ANIONS[acid_key]
            record = make_record(
                [oxide, acid_formula(acid)],
                [combine(cation, acid), "H2O"],
                {
                    "type": "复分解反应",
                    "conditions": "酸与金属氧化物接触",
                    "phenomenon": "固体逐渐溶解，生成盐和水",
                    "commonness": "高" if cation_key in {"Cu", "Fe3", "Ca"} and acid_key in strong_acids else "中",
                    "visibility": "一般",
                    "source": "氧化物反应规则生成",
                },
            )
            if record:
                records.append(record)

    acidic_oxides = [
        ("CO2", "CO3", "非金属氧化物被碱吸收"),
        ("SO2", "SO3", "有刺激性气味气体被吸收"),
        ("SO3", "SO4", "非金属氧化物与碱反应"),
        ("SiO2", "SiO3", "固体与强碱反应"),
    ]
    for oxide, anion_key, phenomenon in acidic_oxides:
        for base_key in ["Na", "K", "Li", "Ca", "Ba"]:
            base = CATIONS[base_key]
            record = make_record(
                [oxide, hydroxide_formula(base)],
                [combine(base, ANIONS[anion_key]), "H2O"],
                {
                    "type": "非金属氧化物与碱反应",
                    "conditions": "碱溶液中",
                    "phenomenon": phenomenon,
                    "commonness": "高" if oxide in {"CO2", "SO2"} and base_key in {"Na", "Ca", "Ba"} else "中",
                    "visibility": "一般" if oxide != "SO2" else "明显",
                    "source": "氧化物反应规则生成",
                },
            )
            if record:
                records.append(record)

    oxygen_reactions = [
        ("Na", "Na2O", "钠燃烧生成氧化钠", "高"),
        ("K", "K2O", "钾燃烧生成氧化钾", "中"),
        ("Li", "Li2O", "锂燃烧生成氧化锂", "中"),
        ("Mg", "MgO", "剧烈燃烧，发出耀眼白光", "高"),
        ("Al", "Al2O3", "燃烧生成白色固体", "高"),
        ("Zn", "ZnO", "燃烧生成白色固体", "中"),
        ("Fe", "Fe3O4", "剧烈燃烧，火星四射", "高"),
        ("Cu", "CuO", "红色固体变黑", "高"),
        ("C", "CO2", "充分燃烧，发光放热", "高"),
        ("C", "CO", "不充分燃烧，生成一氧化碳", "中"),
        ("S", "SO2", "燃烧产生蓝紫色火焰和刺激性气味", "高"),
        ("P", "P2O5", "燃烧产生大量白烟", "高"),
        ("H2", "H2O", "淡蓝色火焰，放热", "高"),
        ("CO", "CO2", "蓝色火焰，放热", "高"),
    ]
    for reactant, product_formula, phenomenon, commonness in oxygen_reactions:
        record = make_record(
            [reactant, "O2"],
            [product_formula],
            {
                "type": "化合反应",
                "conditions": "点燃",
                "phenomenon": phenomenon,
                "commonness": commonness,
                "visibility": "明显",
                "source": "氧化反应规则生成",
            },
        )
        if record:
            records.append(record)

    water_metal_reactions = [
        ("Na", "NaOH", "剧烈反应，有气泡产生", "高"),
        ("K", "KOH", "剧烈反应，有气泡产生", "高"),
        ("Li", "LiOH", "反应较缓，有气泡产生", "中"),
        ("Ca", "Ca(OH)2", "有气泡产生，溶液变浑浊", "高"),
        ("Ba", "Ba(OH)2", "有气泡产生", "中"),
    ]
    for metal, hydroxide, phenomenon, commonness in water_metal_reactions:
        record = make_record(
            [metal, "H2O"],
            [hydroxide, "H2"],
            {
                "type": "置换反应",
                "conditions": "与水接触，常温",
                "phenomenon": phenomenon,
                "commonness": commonness,
                "visibility": "明显",
                "source": "活泼金属反应规则生成",
            },
            {"H2": "↑"},
        )
        if record:
            records.append(record)

    oxide_water_reactions = [
        ("Na2O", "NaOH", "白色固体溶解，溶液呈碱性", "高"),
        ("K2O", "KOH", "固体溶解，溶液呈碱性", "中"),
        ("Li2O", "LiOH", "固体溶解，溶液呈碱性", "中"),
        ("CaO", "Ca(OH)2", "放热，生成熟石灰", "高"),
        ("BaO", "Ba(OH)2", "固体与水反应生成碱", "中"),
        ("CO2", "H2CO3", "二氧化碳溶于水生成碳酸", "高"),
        ("SO2", "H2SO3", "刺激性气体溶于水", "高"),
        ("SO3", "H2SO4", "剧烈放热，生成硫酸", "中"),
        ("P2O5", "H3PO4", "白色固体吸水生成磷酸", "中"),
    ]
    for oxide, product_formula, phenomenon, commonness in oxide_water_reactions:
        record = make_record(
            [oxide, "H2O"],
            [product_formula],
            {
                "type": "化合反应",
                "conditions": "与水接触",
                "phenomenon": phenomenon,
                "commonness": commonness,
                "visibility": "明显" if commonness == "高" else "一般",
                "source": "氧化物反应规则生成",
            },
        )
        if record:
            records.append(record)

    halide_cations = ["Na", "K", "NH4", "Mg", "Ca", "Ba", "Zn", "Fe2"]
    halogen_replacements = [
        ("Cl2", "Br", "Cl", "Br2", "溶液由无色变橙黄色"),
        ("Cl2", "I", "Cl", "I2", "溶液颜色加深，生成碘"),
        ("Br2", "I", "Br", "I2", "溶液颜色加深，生成碘"),
    ]
    for halogen, source_anion_key, product_anion_key, product_halogen, phenomenon in halogen_replacements:
        for cation_key in halide_cations:
            cation = CATIONS[cation_key]
            record = make_record(
                [halogen, combine(cation, ANIONS[source_anion_key])],
                [combine(cation, ANIONS[product_anion_key]), product_halogen],
                {
                    "type": "置换反应",
                    "conditions": "卤素单质通入盐溶液",
                    "phenomenon": phenomenon,
                    "commonness": "高" if cation_key in {"Na", "K"} else "中",
                    "visibility": "明显",
                    "source": "卤素活动性规则生成",
                },
            )
            if record:
                records.append(record)

    for cation_key in ["Na", "K", "Li"]:
        cation = CATIONS[cation_key]
        record = make_record(
            [combine(cation, ANIONS["NO3"])],
            [combine(cation, {"formula": "NO2", "charge": -1}), "O2"],
            {
                "type": "分解反应",
                "conditions": "加热",
                "phenomenon": "硝酸盐受热分解，放出氧气",
                "commonness": "中",
                "visibility": "一般",
                "source": "热分解规则生成",
            },
            {"O2": "↑"},
        )
        if record:
            records.append(record)

    for cation_key in ["Mg", "Ca", "Ba", "Zn", "Cu", "Fe2", "Fe3", "Al", "Pb", "Ag"]:
        cation = CATIONS[cation_key]
        oxide = combine(cation, {"formula": "O", "charge": -2})
        record = make_record(
            [combine(cation, ANIONS["NO3"])],
            [oxide, "NO2", "O2"],
            {
                "type": "分解反应",
                "conditions": "加热",
                "phenomenon": "产生红棕色气体，并放出氧气",
                "commonness": "中",
                "visibility": "明显",
                "source": "热分解规则生成",
            },
            {"NO2": "↑", "O2": "↑"},
            36,
        )
        if record:
            records.append(record)

    for cation_key in ["Na", "K", "Ca", "Ba"]:
        cation = CATIONS[cation_key]
        record = make_record(
            [combine(cation, ANIONS["ClO3"])],
            [combine(cation, ANIONS["Cl"]), "O2"],
            {
                "type": "分解反应",
                "conditions": "加热，二氧化锰催化",
                "phenomenon": "放出氧气",
                "commonness": "高" if cation_key == "K" else "中",
                "visibility": "明显",
                "source": "热分解规则生成",
            },
            {"O2": "↑"},
        )
        if record:
            records.append(record)

    direct_nonmetal_reactions = [
        ("Cl2", "Cl", "燃烧或加热，生成氯化物"),
        ("Br2", "Br", "加热或接触，生成溴化物"),
        ("I2", "I", "加热，生成碘化物"),
        ("S", "S", "加热，生成硫化物"),
    ]
    for reagent, anion_key, phenomenon in direct_nonmetal_reactions:
        for cation_key in ["Na", "K", "Mg", "Ca", "Al", "Zn", "Fe2", "Cu"]:
            cation = CATIONS[cation_key]
            metal_formula = "Fe" if cation_key == "Fe2" else cation["formula"]
            record = make_record(
                [metal_formula, reagent],
                [combine(cation, ANIONS[anion_key])],
                {
                    "type": "化合反应",
                    "conditions": "加热或点燃",
                    "phenomenon": phenomenon,
                    "commonness": "中",
                    "visibility": "明显",
                    "source": "单质化合规则生成",
                },
            )
            if record:
                records.append(record)

    organics = []
    for carbon in range(1, 31):
        organics.append(("C" + (str(carbon) if carbon > 1 else "") + "H" + str(2 * carbon + 2), "烷烃燃烧"))
        if carbon >= 2:
            organics.append(("C" + str(carbon) + "H" + str(2 * carbon), "烯烃燃烧"))
            organics.append(("C" + str(carbon) + "H" + str(2 * carbon - 2), "炔烃燃烧"))
        if carbon <= 20:
            organics.append(("C" + (str(carbon) if carbon > 1 else "") + "H" + str(2 * carbon + 2) + "O", "醇类燃烧"))
    for formula, reaction_type in organics:
        record = make_record(
            [formula, "O2"],
            ["CO2", "H2O"],
            {
                "type": "氧化反应",
                "conditions": "点燃",
                "phenomenon": reaction_type + "，发光放热",
                "commonness": "高" if formula in {"CH4", "C2H5OH", "C3H8"} else "低",
                "visibility": "明显",
                "source": "燃烧通式生成",
            },
            {"CO2": "↑"},
            36,
        )
        if record:
            records.append(record)

    for cation_key in ["Ca", "Ba", "Mg", "Zn", "Cu", "Fe2", "Pb"]:
        cation = CATIONS[cation_key]
        carbonate = combine(cation, ANIONS["CO3"])
        oxide = combine(cation, {"formula": "O", "charge": -2})
        record = make_record(
            [carbonate],
            [oxide, "CO2"],
            {
                "type": "分解反应",
                "conditions": "高温",
                "phenomenon": "固体分解，生成二氧化碳",
                "commonness": "中",
                "visibility": "一般",
                "source": "热分解规则生成",
            },
            {"CO2": "↑"},
        )
        if record:
            records.append(record)

    for cation_key in ["Mg", "Cu", "Fe2", "Fe3", "Zn", "Al", "Ca"]:
        cation = CATIONS[cation_key]
        hydroxide = hydroxide_formula(cation)
        oxide = combine(cation, {"formula": "O", "charge": -2})
        record = make_record(
            [hydroxide],
            [oxide, "H2O"],
            {
                "type": "分解反应",
                "conditions": "加热",
                "phenomenon": "固体受热分解",
                "commonness": "中",
                "visibility": "一般",
                "source": "热分解规则生成",
            },
        )
        if record:
            records.append(record)

    return records


def dedupe_and_sort(reactions: list[dict]) -> list[dict]:
    result = []
    seen: set[str] = set()
    for reaction in reactions:
        if not is_clean_equation(reaction):
            continue
        key = normalize_equation(reaction["equation"])
        if key in seen:
            continue
        seen.add(key)
        result.append(reaction)
    return sorted(
        result,
        key=lambda item: (
            COMMONNESS_RANK.get(item.get("commonness") or "低", 3),
            VISIBILITY_RANK.get(item.get("visibility") or "不明显", 3),
            item.get("equation", ""),
        ),
    )


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


def write_outputs(reactions: list[dict]) -> None:
    text_lines = []
    for reaction in reactions:
        text_lines.append(",".join(reaction["formulas"]) + "\t" + reaction["equation"])
    TEXT_OUTPUT.write_text(
        "export const generatedReactionText = "
        + json.dumps("\n".join(text_lines), ensure_ascii=False)
        + "\n",
        encoding="utf-8",
    )

    metadata = []
    for reaction in reactions:
        values = [
            reaction.get("type", ""),
            reaction.get("conditions", ""),
            reaction.get("phenomenon", ""),
            reaction.get("commonness", ""),
            reaction.get("visibility", ""),
        ]
        metadata.append(values if any(values) else [])
    INDEX_OUTPUT.write_text(
        "export const generatedEquations = "
        + json.dumps([reaction["equation"] for reaction in reactions], ensure_ascii=False, separators=(",", ":"))
        + "\nexport const generatedMetadata = "
        + json.dumps(metadata, ensure_ascii=False, separators=(",", ":"))
        + "\nexport const generatedFormulaIndex = "
        + json.dumps(build_formula_index(reactions), ensure_ascii=False, separators=(",", ":"))
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    existing = [infer_existing_metadata(item) for item in load_existing_reactions()]
    expanded = generate_rule_reactions()
    reactions = dedupe_and_sort(expanded + existing)
    write_outputs(reactions)
    with_meta = sum(1 for item in reactions if item.get("type") or item.get("conditions") or item.get("phenomenon"))
    print(f"Built {len(reactions)} reactions ({with_meta} with metadata) -> {INDEX_OUTPUT}")


if __name__ == "__main__":
    main()
