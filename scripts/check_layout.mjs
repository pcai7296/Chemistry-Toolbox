import { createScreenLayout } from "../src/services/screenProfile.js"

const CASES = [
  [192, 490, "pill"],
  [212, 520, "pill"],
  [280, 456, "rounded-portrait"],
  [336, 480, "rounded-portrait"],
  [390, 450, "rounded-square"],
  [432, 514, "rounded-square"],
  [466, 466, "round"]
]

function assertWithin(name, left, width, screenWidth, errors) {
  if (left < 0) {
    errors.push(`${name} left ${left} < 0`)
  }
  if (width <= 0) {
    errors.push(`${name} width ${width} <= 0`)
  }
  if (left + width > screenWidth) {
    errors.push(`${name} right ${left + width} > ${screenWidth}`)
  }
}

function checkLayout(width, height, shape) {
  const layout = createScreenLayout(width, height, shape)
  const errors = []

  assertWithin("content", layout.contentLeft, layout.contentWidth, width, errors)
  assertWithin("card", layout.cardLeft, layout.cardWidth, width, errors)
  assertWithin("narrow", layout.narrowLeft, layout.narrowWidth, width, errors)
  assertWithin("topButton", layout.topButtonLeft, layout.topButtonWidth, width, errors)
  assertWithin("title", layout.titleLeft, layout.titleWidth, width, errors)
  assertWithin("query", layout.queryLeft, layout.queryWidth, width, errors)
  assertWithin("pagination", layout.paginationLeft, layout.paginationWidth, width, errors)
  assertWithin("keyboardTopbar", layout.keyboardTopbarLeft, layout.keyboardTopbarWidth, width, errors)
  assertWithin("keyboardSearch", layout.keyboardTopbarLeft + layout.keyboardSearchLeft, layout.keyboardSearchWidth, width, errors)
  assertWithin("keyboardPreview", layout.keyboardTopbarLeft + layout.keyboardPreviewLeft, layout.keyboardPreviewWidth, width, errors)
  assertWithin("keyboardGroup", layout.keyboardTopbarLeft + layout.keyboardGroupLeft, layout.keyboardGroupWidth, width, errors)
  assertWithin("keyboardNumber", layout.keyboardTopbarLeft + layout.keyboardNumberLeft, layout.keyboardNumberWidth, width, errors)
  assertWithin("keyboardDelete", layout.keyboardTopbarLeft + layout.keyboardDeleteLeft, layout.keyboardDeleteWidth, width, errors)
  assertWithin("qr", layout.qrLeft, layout.qrSize, width, errors)

  if (layout.headerHeight + layout.bottomSafe >= height) {
    errors.push(`vertical safe areas too large: header ${layout.headerHeight}, bottom ${layout.bottomSafe}, height ${height}`)
  }
  if (layout.resultsListTopPadding < layout.headerHeight) {
    errors.push(`results list top padding ${layout.resultsListTopPadding} < header ${layout.headerHeight}`)
  }
  if (layout.shape === "round" && layout.bottomSafe < 24) {
    errors.push(`round bottomSafe ${layout.bottomSafe} is too small`)
  }
  if (layout.keyboardGroupWidth !== layout.keyboardNumberWidth || layout.keyboardGroupWidth !== layout.keyboardDeleteWidth) {
    errors.push(`keyboard button widths differ: ${layout.keyboardGroupWidth}/${layout.keyboardNumberWidth}/${layout.keyboardDeleteWidth}`)
  }

  return { layout, errors }
}

let failed = false

for (const [width, height, shape] of CASES) {
  const { layout, errors } = checkLayout(width, height, shape)
  const summary = `${width}x${height} ${layout.shape} card=${layout.cardLeft}+${layout.cardWidth} pager=${layout.paginationLeft}+${layout.paginationWidth} keyboard=${layout.keyboardTopbarLeft}+${layout.keyboardTopbarWidth}`
  if (errors.length > 0) {
    failed = true
    console.error(`FAIL ${summary}`)
    for (const error of errors) {
      console.error(`  - ${error}`)
    }
  } else {
    console.log(`OK ${summary}`)
  }
}

if (failed) {
  process.exit(1)
}
