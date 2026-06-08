import { formatEquationSideText, formatInputFormula } from "../src/services/formulaFormat.js"

const CASES = [
  ["input", "H2SO4", "H₂SO₄", formatInputFormula],
  ["input", "SO4^2-", "SO₄²⁻", formatInputFormula],
  ["input", "NH4^+", "NH₄⁺", formatInputFormula],
  ["equation", "2H2 + O2", "2H₂ + O₂", formatEquationSideText],
  ["equation", "NaCl+H2SO4", "NaCl + H₂SO₄", formatEquationSideText]
]

let failed = false

for (const [type, source, expected, formatter] of CASES) {
  const actual = formatter(source)
  if (actual !== expected) {
    failed = true
    console.error(`FAIL ${type} ${source}: expected ${expected}, got ${actual}`)
  } else {
    console.log(`OK ${type} ${source}: ${actual}`)
  }
}

if (failed) {
  process.exit(1)
}
