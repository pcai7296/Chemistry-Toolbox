export const SUBSCRIPT_MAP = {
  "0": "₀",
  "1": "₁",
  "2": "₂",
  "3": "₃",
  "4": "₄",
  "5": "₅",
  "6": "₆",
  "7": "₇",
  "8": "₈",
  "9": "₉"
}

export const SUPERSCRIPT_MAP = {
  "0": "⁰",
  "1": "¹",
  "2": "²",
  "3": "³",
  "4": "⁴",
  "5": "⁵",
  "6": "⁶",
  "7": "⁷",
  "8": "⁸",
  "9": "⁹",
  "+": "⁺",
  "-": "⁻"
}

export function splitCharge(raw) {
  const value = raw || ""
  const match = value.match(/^(.*?)(\^(\d*)([+-]))$/)
  if (match) {
    return {
      body: match[1],
      chargeDigits: match[3] || "",
      chargeSign: match[4] || "",
      chargeRaw: match[2] || ""
    }
  }
  return {
    body: value,
    chargeDigits: "",
    chargeSign: "",
    chargeRaw: ""
  }
}

function formatCharge(parts) {
  let charge = ""
  const chargeText = (parts.chargeDigits || "") + (parts.chargeSign || "")
  for (let i = 0; i < chargeText.length; i += 1) {
    const char = chargeText[i]
    charge += SUPERSCRIPT_MAP[char] || char
  }
  return charge
}

export function formatInputFormula(raw) {
  const parts = splitCharge(raw)
  let body = ""
  for (let i = 0; i < parts.body.length; i += 1) {
    const char = parts.body[i]
    body += SUBSCRIPT_MAP[char] || char
  }
  return body + formatCharge(parts)
}

export function formatEquationFormula(raw) {
  const parts = splitCharge(raw)
  let body = ""
  for (let i = 0; i < parts.body.length; i += 1) {
    const char = parts.body[i]
    const prev = i > 0 ? parts.body[i - 1] : ""
    const shouldSubscript = /[0-9]/.test(char) && (/[A-Za-z\)\]]/.test(prev) || /[0-9]/.test(prev))
    body += shouldSubscript ? (SUBSCRIPT_MAP[char] || char) : char
  }
  return body + formatCharge(parts)
}

export function formatEquationSideText(side) {
  const tokens = (side || "").split("+")
  const result = []
  for (let i = 0; i < tokens.length; i += 1) {
    const token = tokens[i].trim()
    if (!token) {
      continue
    }
    const match = token.match(/^(\d+)(.*)$/)
    if (match && match[2]) {
      result.push(match[1] + formatEquationFormula(match[2]))
    } else {
      result.push(formatEquationFormula(token))
    }
  }
  return result.join(" + ")
}

export function estimateFormulaPreviewWidth(text) {
  const value = text || ""
  let width = 0
  for (let i = 0; i < value.length; i += 1) {
    const code = value.charCodeAt(i)
    const char = value[i]
    if (char === " ") {
      width += 9
    } else if (char === "/" || char === "·" || char === "." || char === "+" || char === "-") {
      width += 14
    } else if (SUBSCRIPT_MAP[char] || SUPERSCRIPT_MAP[char] || code >= 0x2080 && code <= 0x209F || code >= 0x2070 && code <= 0x209F) {
      width += 16
    } else if (code > 0x2E80) {
      width += 32
    } else if (char >= "A" && char <= "Z") {
      width += 22
    } else {
      width += 18
    }
  }
  return Math.max(32, width + 14)
}
