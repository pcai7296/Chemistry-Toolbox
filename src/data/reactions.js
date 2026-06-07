import { generatedReactions } from "./generatedReactions.js"

const curatedReactions = [
  {
    id: "rxn_h2so4_naoh",
    formulas: ["H2SO4", "NaOH", "Na2SO4", "H2O"],
    equation: "H2SO4 + 2NaOH -> Na2SO4 + 2H2O",
    type: "中和反应",
    conditions: "常温",
    phenomenon: "放热"
  },
  {
    id: "rxn_h2so4_bacl2",
    formulas: ["H2SO4", "BaCl2", "BaSO4", "HCl"],
    equation: "H2SO4 + BaCl2 -> BaSO4↓ + 2HCl",
    type: "复分解反应",
    conditions: "溶液中",
    phenomenon: "生成白色沉淀"
  },
  {
    id: "rxn_h2so4_cuo",
    formulas: ["H2SO4", "CuO", "CuSO4", "H2O"],
    equation: "CuO + H2SO4 -> CuSO4 + H2O",
    type: "酸与碱性氧化物反应",
    conditions: "加热更明显",
    phenomenon: "黑色固体溶解，溶液变蓝"
  },
  {
    id: "rxn_h2so4_zn",
    formulas: ["Zn", "H2SO4", "ZnSO4", "H2"],
    equation: "Zn + H2SO4 -> ZnSO4 + H2↑",
    type: "置换反应",
    conditions: "稀硫酸",
    phenomenon: "有气泡产生"
  },
  {
    id: "rxn_h2so4_caco3",
    formulas: ["CaCO3", "H2SO4", "CaSO4", "CO2", "H2O"],
    equation: "CaCO3 + H2SO4 -> CaSO4 + CO2↑ + H2O",
    type: "复分解反应",
    conditions: "常温",
    phenomenon: "有气泡产生"
  },
  {
    id: "rxn_hcl_naoh",
    formulas: ["HCl", "NaOH", "NaCl", "H2O"],
    equation: "HCl + NaOH -> NaCl + H2O",
    type: "中和反应",
    conditions: "常温",
    phenomenon: "放热"
  },
  {
    id: "rxn_hcl_na2co3",
    formulas: ["Na2CO3", "HCl", "NaCl", "CO2", "H2O"],
    equation: "Na2CO3 + 2HCl -> 2NaCl + CO2↑ + H2O",
    type: "复分解反应",
    conditions: "常温",
    phenomenon: "有气泡产生"
  },
  {
    id: "rxn_hcl_caco3",
    formulas: ["CaCO3", "HCl", "CaCl2", "CO2", "H2O"],
    equation: "CaCO3 + 2HCl -> CaCl2 + CO2↑ + H2O",
    type: "复分解反应",
    conditions: "常温",
    phenomenon: "有气泡产生"
  },
  {
    id: "rxn_hcl_zn",
    formulas: ["Zn", "HCl", "ZnCl2", "H2"],
    equation: "Zn + 2HCl -> ZnCl2 + H2↑",
    type: "置换反应",
    conditions: "常温",
    phenomenon: "有气泡产生"
  },
  {
    id: "rxn_hcl_fe",
    formulas: ["Fe", "HCl", "FeCl2", "H2"],
    equation: "Fe + 2HCl -> FeCl2 + H2↑",
    type: "置换反应",
    conditions: "常温",
    phenomenon: "有气泡产生，溶液浅绿色"
  },
  {
    id: "rxn_cuso4_naoh",
    formulas: ["CuSO4", "NaOH", "Cu(OH)2", "Na2SO4"],
    equation: "CuSO4 + 2NaOH -> Cu(OH)2↓ + Na2SO4",
    type: "复分解反应",
    conditions: "溶液中",
    phenomenon: "生成蓝色沉淀"
  },
  {
    id: "rxn_co2_caoh2",
    formulas: ["CO2", "Ca(OH)2", "CaCO3", "H2O"],
    equation: "CO2 + Ca(OH)2 -> CaCO3↓ + H2O",
    type: "复分解反应",
    conditions: "澄清石灰水",
    phenomenon: "石灰水变浑浊"
  },
  {
    id: "rxn_co2_naoh",
    formulas: ["CO2", "NaOH", "Na2CO3", "H2O"],
    equation: "CO2 + 2NaOH -> Na2CO3 + H2O",
    type: "非金属氧化物与碱反应",
    conditions: "常温",
    phenomenon: "无明显现象"
  },
  {
    id: "rxn_caoh2_na2co3",
    formulas: ["Ca(OH)2", "Na2CO3", "CaCO3", "NaOH"],
    equation: "Ca(OH)2 + Na2CO3 -> CaCO3↓ + 2NaOH",
    type: "复分解反应",
    conditions: "溶液中",
    phenomenon: "生成白色沉淀"
  },
  {
    id: "rxn_nh3_hcl",
    formulas: ["NH3", "HCl", "NH4Cl"],
    equation: "NH3 + HCl -> NH4Cl",
    type: "化合反应",
    conditions: "常温",
    phenomenon: "产生白烟"
  },
  {
    id: "rxn_h2_o2",
    formulas: ["H2", "O2", "H2O"],
    equation: "2H2 + O2 -> 2H2O",
    type: "化合反应",
    conditions: "点燃",
    phenomenon: "放热，发出淡蓝色火焰"
  },
  {
    id: "rxn_c_o2",
    formulas: ["C", "O2", "CO2"],
    equation: "C + O2 -> CO2",
    type: "化合反应",
    conditions: "点燃，氧气充足",
    phenomenon: "放热"
  },
  {
    id: "rxn_co_o2",
    formulas: ["CO", "O2", "CO2"],
    equation: "2CO + O2 -> 2CO2",
    type: "氧化反应",
    conditions: "点燃",
    phenomenon: "放热，火焰呈蓝色"
  },
  {
    id: "rxn_fe_cuso4",
    formulas: ["Fe", "CuSO4", "FeSO4", "Cu"],
    equation: "Fe + CuSO4 -> FeSO4 + Cu",
    type: "置换反应",
    conditions: "溶液中",
    phenomenon: "铁表面析出红色铜，溶液由蓝变浅绿"
  },
  {
    id: "rxn_agno3_nacl",
    formulas: ["AgNO3", "NaCl", "AgCl", "NaNO3"],
    equation: "AgNO3 + NaCl -> AgCl↓ + NaNO3",
    type: "复分解反应",
    conditions: "溶液中",
    phenomenon: "生成白色沉淀"
  }
]

function normalizeEquation(value) {
  const normalized = (value || "").replace(/\s+/g, "").replace(/＝/g, "->").replace(/=/g, "->")
  const parts = normalized.split("->")
  if (parts.length !== 2) {
    return normalized.toLowerCase()
  }
  const left = parts[0].split("+").filter(Boolean).sort().join("+")
  const right = parts[1].split("+").filter(Boolean).sort().join("+")
  return (left + "->" + right).toLowerCase()
}

const seenEquations = {}
const mergedReactions = []

for (let i = 0; i < curatedReactions.length; i += 1) {
  const reaction = curatedReactions[i]
  const key = normalizeEquation(reaction.equation)
  if (!seenEquations[key]) {
    seenEquations[key] = true
    mergedReactions.push(reaction)
  }
}

for (let i = 0; i < generatedReactions.length; i += 1) {
  const reaction = generatedReactions[i]
  const key = normalizeEquation(reaction.equation)
  if (!seenEquations[key]) {
    seenEquations[key] = true
    mergedReactions.push(reaction)
  }
}

export const reactions = mergedReactions
