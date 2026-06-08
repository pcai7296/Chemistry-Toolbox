import { reactions, normalizeEquation } from "../data/reactions.js"
import { generatedReactionText } from "../data/generatedReactionText.js"

function normalizeFormula(value) {
  const normalized = (value || "").replace(/\s+/g, "").toLowerCase()
  return normalized.replace(/\^(\d*[+-])$/, "$1")
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

  const results = []
  const seenEquations = {}

  for (let i = 0; i < reactions.length; i += 1) {
    const reaction = reactions[i]
    const normalizedSet = buildNormalizedSet(reaction.formulas || [])
    if (normalizedSet[left] && normalizedSet[right]) {
      const key = normalizeEquation(reaction.equation)
      seenEquations[key] = true
      results.push(reaction)
    }
  }

  searchGeneratedReactionText(left, right, seenEquations, results)
  return results
}

function searchGeneratedReactionText(left, right, seenEquations, results) {
  const source = generatedReactionText || ""
  let start = 0
  let index = 0

  while (start < source.length) {
    let end = source.indexOf("\n", start)
    if (end === -1) {
      end = source.length
    }

    const line = source.slice(start, end)
    const divider = line.indexOf("\t")
    if (divider > 0) {
      const formulas = line.slice(0, divider)
      const equation = line.slice(divider + 1)
      if (lineContainsFormulaPair(formulas, left, right)) {
        const key = normalizeEquation(equation)
        if (!seenEquations[key]) {
          seenEquations[key] = true
          results.push({
            id: "generated_" + index,
            formulas: formulas.split(","),
            equation,
            type: "",
            conditions: "",
            phenomenon: ""
          })
        }
      }
    }

    start = end + 1
    index += 1
  }
}

function lineContainsFormulaPair(formulas, left, right) {
  const values = formulas.split(",")
  let hasLeft = false
  let hasRight = false

  for (let i = 0; i < values.length; i += 1) {
    const formula = normalizeFormula(values[i])
    if (formula === left) {
      hasLeft = true
    }
    if (formula === right) {
      hasRight = true
    }
    if (hasLeft && hasRight) {
      return true
    }
  }

  return false
}

export function formatFormula(value) {
  return (value || "").replace(/\s+/g, "")
}
