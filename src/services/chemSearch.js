import { reactions, normalizeEquation } from "../data/reactions.js"
import { generatedEquations, generatedFormulaIndex, generatedMetadata } from "../data/generatedReactionIndex.js"

function normalizeFormula(value) {
  const normalized = (value || "").replace(/\s+/g, "").toLowerCase()
  return normalized.replace(/\^(\d*[+-])$/, "$1")
}

function addToIndex(index, formula, reaction) {
  const normalized = normalizeFormula(formula)
  if (!normalized) {
    return
  }
  if (!index[normalized]) {
    index[normalized] = []
  }
  index[normalized].push(reaction)
}

function buildFormulaIndex(items) {
  const index = {}
  for (let i = 0; i < items.length; i += 1) {
    const reaction = items[i]
    const formulas = reaction.formulas || []
    const added = {}
    for (let j = 0; j < formulas.length; j += 1) {
      const normalized = normalizeFormula(formulas[j])
      if (normalized && !added[normalized]) {
        added[normalized] = true
        addToIndex(index, normalized, reaction)
      }
    }
  }
  return index
}

function buildMatchSet(items) {
  const result = {}
  for (let i = 0; i < items.length; i += 1) {
    result[items[i].id || ("reaction_" + i)] = true
  }
  return result
}

function buildEquationSet(items) {
  const result = {}
  for (let i = 0; i < items.length; i += 1) {
    result[normalizeEquation(items[i].equation)] = true
  }
  return result
}

function intersectSortedIndexes(leftItems, rightItems) {
  const results = []
  let leftIndex = 0
  let rightIndex = 0

  while (leftIndex < leftItems.length && rightIndex < rightItems.length) {
    const leftValue = leftItems[leftIndex]
    const rightValue = rightItems[rightIndex]
    if (leftValue === rightValue) {
      results.push(leftValue)
      leftIndex += 1
      rightIndex += 1
    } else if (leftValue < rightValue) {
      leftIndex += 1
    } else {
      rightIndex += 1
    }
  }

  return results
}

function createGeneratedReaction(index) {
  const metadata = generatedMetadata[index] || {}
  const isArrayMetadata = metadata instanceof Array
  return {
    id: "generated_" + index,
    equation: generatedEquations[index] || "",
    type: isArrayMetadata ? (metadata[0] || "") : (metadata.type || ""),
    conditions: isArrayMetadata ? (metadata[1] || "") : (metadata.conditions || ""),
    phenomenon: isArrayMetadata ? (metadata[2] || "") : (metadata.phenomenon || ""),
    commonness: isArrayMetadata ? (metadata[3] || "") : (metadata.commonness || ""),
    visibility: isArrayMetadata ? (metadata[4] || "") : (metadata.visibility || ""),
    generated: true
  }
}

const formulaIndex = buildFormulaIndex(reactions)
const curatedEquationKeys = buildEquationSet(reactions)

export function searchReactionsByPair(formulaA, formulaB) {
  const left = normalizeFormula(formulaA)
  const right = normalizeFormula(formulaB)

  if (!left || !right) {
    return []
  }

  const results = []
  const seenEquations = {}
  const leftMatches = formulaIndex[left] || []
  const rightMatches = formulaIndex[right] || []
  const rightSet = left === right ? null : buildMatchSet(rightMatches)

  for (let i = 0; i < leftMatches.length; i += 1) {
    const reaction = leftMatches[i]
    const id = reaction.id || ("reaction_" + i)
    if (rightSet && !rightSet[id]) {
      continue
    }

    const key = normalizeEquation(reaction.equation)
    seenEquations[key] = true
    results.push(reaction)
  }

  const leftGenerated = generatedFormulaIndex[left] || []
  const rightGenerated = generatedFormulaIndex[right] || []
  const generatedMatches = left === right ? leftGenerated : intersectSortedIndexes(leftGenerated, rightGenerated)

  for (let i = 0; i < generatedMatches.length; i += 1) {
    const reactionIndex = generatedMatches[i]
    const equation = generatedEquations[reactionIndex]
    if (!equation) {
      continue
    }

    const key = normalizeEquation(equation)
    if (seenEquations[key] || curatedEquationKeys[key]) {
      continue
    }

    seenEquations[key] = true
    results.push(createGeneratedReaction(reactionIndex))
  }

  return results
}

export function formatFormula(value) {
  return (value || "").replace(/\s+/g, "")
}
