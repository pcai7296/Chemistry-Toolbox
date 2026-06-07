import { reactions } from "../data/reactions.js"

function normalizeFormula(value) {
  return (value || "").replace(/\s+/g, "").toLowerCase()
}

function buildNormalizedSet(formulas) {
  const result = {}
  for (let i = 0; i < formulas.length; i += 1) {
    result[normalizeFormula(formulas[i])] = true
  }
  return result
}

export function searchReactionsByPair(formulaA, formulaB) {
  const left = normalizeFormula(formulaA)
  const right = normalizeFormula(formulaB)

  if (!left || !right) {
    return []
  }

  return reactions.filter((reaction) => {
    const normalizedSet = buildNormalizedSet(reaction.formulas || [])
    return normalizedSet[left] && normalizedSet[right]
  })
}

export function formatFormula(value) {
  return (value || "").replace(/\s+/g, "")
}
