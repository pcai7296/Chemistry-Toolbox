import { searchReactionsByPair } from "../src/services/chemSearch.js"
import { generatedEquations, generatedFormulaIndex, generatedMetadata } from "../src/data/generatedReactionIndex.js"

const CASES = [
  ["HCl", "NaCl", 3],
  ["NaOH", "HCl", 1, "HCl + NaOH -> NaCl + H2O"],
  ["H2SO4", "NaCl", 2],
  ["CO2", "NaOH", 2],
  ["Fe", "HCl", 1]
]

const GENERATED_CASES = [
  ["Na", "O2"],
  ["Na2O", "SO3"],
  ["H2S", "Cl2"]
]

let failed = false

function reportFailure(message) {
  failed = true
  console.error(message)
}

for (const [formula, indexes] of Object.entries(generatedFormulaIndex)) {
  if (!Array.isArray(indexes)) {
    reportFailure(`FAIL index ${formula}: value is not an array`)
    continue
  }

  let previous = -1
  for (const index of indexes) {
    if (!Number.isInteger(index) || index < 0 || index >= generatedEquations.length) {
      reportFailure(`FAIL index ${formula}: invalid reaction index ${index}`)
    } else if (index <= previous) {
      reportFailure(`FAIL index ${formula}: indexes are not strictly ascending`)
    }
    previous = index
  }
}

if (generatedEquations.length < 1500) {
  reportFailure(`FAIL generated count: expected at least 1500, got ${generatedEquations.length}`)
}

if (generatedMetadata.length !== generatedEquations.length) {
  reportFailure(`FAIL generated metadata: expected ${generatedEquations.length}, got ${generatedMetadata.length}`)
}

for (const [left, right, minCount, expectedFirst] of CASES) {
  const forward = searchReactionsByPair(left, right)
  const reverse = searchReactionsByPair(right, left)
  const first = forward[0] ? forward[0].equation : "无结果"

  if (forward.length < minCount) {
    reportFailure(`FAIL ${left}+${right}: expected at least ${minCount}, got ${forward.length}`)
  } else if (forward.length !== reverse.length) {
    reportFailure(`FAIL ${left}+${right}: forward ${forward.length}, reverse ${reverse.length}`)
  } else if (expectedFirst && first !== expectedFirst) {
    reportFailure(`FAIL ${left}+${right}: expected first ${expectedFirst}, got ${first}`)
  } else {
    console.log(`OK ${left}+${right}: ${forward.length}, first=${first}`)
  }
}

for (const [left, right] of GENERATED_CASES) {
  const results = searchReactionsByPair(left, right)
  if (!results.some((item) => item.generated)) {
    reportFailure(`FAIL generated ${left}+${right}: no generated result`)
  } else {
    console.log(`OK generated ${left}+${right}: ${results.length}`)
  }
}

const metadataResult = searchReactionsByPair("AgNO3", "NaCl").find((item) => item.phenomenon)
if (!metadataResult) {
  reportFailure("FAIL metadata AgNO3+NaCl: no visible metadata result")
} else {
  console.log(`OK metadata AgNO3+NaCl: ${metadataResult.phenomenon}`)
}

if (failed) {
  process.exit(1)
}
