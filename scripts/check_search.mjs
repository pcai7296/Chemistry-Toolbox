import { searchReactionsByPair } from "../src/services/chemSearch.js"

const CASES = [
  ["HCl", "NaCl", 3],
  ["NaOH", "HCl", 1],
  ["H2SO4", "NaCl", 2],
  ["CO2", "NaOH", 2],
  ["Fe", "HCl", 1]
]

let failed = false

for (const [left, right, minCount] of CASES) {
  const forward = searchReactionsByPair(left, right)
  const reverse = searchReactionsByPair(right, left)
  const first = forward[0] ? forward[0].equation : "无结果"

  if (forward.length < minCount) {
    failed = true
    console.error(`FAIL ${left}+${right}: expected at least ${minCount}, got ${forward.length}`)
  } else if (forward.length !== reverse.length) {
    failed = true
    console.error(`FAIL ${left}+${right}: forward ${forward.length}, reverse ${reverse.length}`)
  } else {
    console.log(`OK ${left}+${right}: ${forward.length}, first=${first}`)
  }
}

if (failed) {
  process.exit(1)
}
