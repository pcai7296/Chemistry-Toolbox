import { reactions, normalizeEquation } from "../data/reactions.js"
import { generatedReactionText } from "../data/generatedReactionText.js"

function normalizeFormula(value) {
  const normalized = (value || "").replace(/\s+/g, "").toLowerCase()
  return normalized.replace(/\^(\d*[+-])$/, "$1")
}

function parseGeneratedReactions() {
  const source = generatedReactionText || ""
  const results = []
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
      results.push({
        id: "generated_" + index,
        formulas: formulas.split(","),
        equation,
        type: "",
        conditions: "",
        phenomenon: "",
        generated: true
      })
    }

    start = end + 1
    index += 1
  }

  return results
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

const searchableReactions = reactions.concat(parseGeneratedReactions())
const formulaIndex = buildFormulaIndex(searchableReactions)

export function searchReactionsByPair(formulaA, formulaB) {
  const left = normalizeFormula(formulaA)
  const right = normalizeFormula(formulaB)

  if (!left || !right) {
    return []
  }

  const leftMatches = formulaIndex[left] || []
  const rightMatches = formulaIndex[right] || []
  const rightSet = left === right ? null : buildMatchSet(rightMatches)
  const results = []
  const seenEquations = {}

  for (let i = 0; i < leftMatches.length; i += 1) {
    const reaction = leftMatches[i]
    const id = reaction.id || ("reaction_" + i)
    if (rightSet && !rightSet[id]) {
      continue
    }

    const key = normalizeEquation(reaction.equation)
    if (reaction.generated) {
      if (seenEquations[key]) {
        continue
      }
      seenEquations[key] = true
    } else {
      seenEquations[key] = true
    }

    results.push(reaction)
  }

  return results
}

export function formatFormula(value) {
  return (value || "").replace(/\s+/g, "")
}
