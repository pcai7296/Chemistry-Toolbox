const KNOWN_PROFILES = [
  {
    key: "pill_192_490",
    width: 192,
    height: 490,
    shape: "pill",
    contentWidth: 164,
    narrowWidth: 164,
    titleWidth: 140,
    cardWidth: 164,
    topButtonWidth: 78,
    pageButtonWidth: 64,
    pageIndicatorWidth: 70,
    qrSize: 164
  },
  {
    key: "pill_212_520",
    width: 212,
    height: 520,
    shape: "pill",
    contentWidth: 180,
    narrowWidth: 176,
    titleWidth: 156,
    cardWidth: 188,
    topButtonWidth: 80,
    pageButtonWidth: 74,
    pageIndicatorWidth: 92,
    qrSize: 180
  },
  {
    key: "portrait_280_456",
    width: 280,
    height: 456,
    shape: "rounded-portrait",
    contentWidth: 224,
    narrowWidth: 204,
    titleWidth: 180,
    cardWidth: 236,
    topButtonWidth: 84,
    pageButtonWidth: 78,
    pageIndicatorWidth: 96,
    qrSize: 190
  },
  {
    key: "portrait_336_480",
    width: 336,
    height: 480,
    shape: "rounded-portrait",
    contentWidth: 240,
    narrowWidth: 204,
    titleWidth: 190,
    cardWidth: 240,
    topButtonWidth: 84,
    pageButtonWidth: 78,
    pageIndicatorWidth: 96,
    qrSize: 196
  },
  {
    key: "square_390_450",
    width: 390,
    height: 450,
    shape: "rounded-square",
    contentWidth: 270,
    narrowWidth: 214,
    titleWidth: 196,
    cardWidth: 270,
    topButtonWidth: 88,
    pageButtonWidth: 82,
    pageIndicatorWidth: 100,
    qrSize: 204
  },
  {
    key: "square_432_514",
    width: 432,
    height: 514,
    shape: "rounded-square",
    contentWidth: 292,
    narrowWidth: 224,
    titleWidth: 210,
    cardWidth: 292,
    topButtonWidth: 88,
    pageButtonWidth: 84,
    pageIndicatorWidth: 104,
    qrSize: 216
  },
  {
    key: "round_466_466",
    width: 466,
    height: 466,
    shape: "round",
    contentWidth: 286,
    narrowWidth: 224,
    titleWidth: 210,
    cardWidth: 254,
    topButtonWidth: 88,
    pageButtonWidth: 84,
    pageIndicatorWidth: 104,
    qrSize: 204
  }
]

function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value))
}

function nearestProfile(width, height, screenShape) {
  const w = width || 212
  const h = height || 520
  if (screenShape === "round") {
    return KNOWN_PROFILES[6]
  }
  let best = KNOWN_PROFILES[1]
  let bestScore = Infinity
  for (let i = 0; i < KNOWN_PROFILES.length; i += 1) {
    const profile = KNOWN_PROFILES[i]
    const score = Math.abs(profile.width - w) + Math.abs(profile.height - h)
    if (score < bestScore) {
      best = profile
      bestScore = score
    }
  }
  return best
}

export function createScreenLayout(width, height, screenShape) {
  const profile = nearestProfile(width, height, screenShape)
  const screenWidth = width || profile.width
  const screenHeight = height || profile.height
  const contentWidth = clamp(profile.contentWidth, 156, screenWidth - 28)
  const cardWidth = clamp(profile.cardWidth, 156, screenWidth - 24)
  const narrowWidth = clamp(profile.narrowWidth, 156, screenWidth - 24)
  const topButtonWidth = profile.topButtonWidth
  const titleWidth = profile.titleWidth
  const queryWidth = clamp(screenWidth - 36, 156, cardWidth + 56)
  const maxPaginationWidth = clamp(cardWidth, 156, screenWidth - 24)
  const pageIndicatorWidth = clamp(profile.pageIndicatorWidth, 56, Math.floor(maxPaginationWidth * 0.38))
  const pageButtonWidth = Math.max(50, Math.floor((maxPaginationWidth - pageIndicatorWidth) / 2))
  const paginationWidth = pageButtonWidth * 2 + pageIndicatorWidth
  const isPill = profile.shape === "pill"
  const keyboardTopbarWidth = isPill
    ? 192
    : clamp(screenWidth - (profile.shape === "round" ? 46 : 32), 224, screenWidth - 24)
  const keyboardTopbarLeft = Math.floor((screenWidth - keyboardTopbarWidth) / 2)
  const keyboardButtonWidth = isPill ? 48 : clamp(Math.floor(keyboardTopbarWidth / 5), 56, 70)
  const keyboardNumberButtonWidth = keyboardButtonWidth
  const keyboardGroupLeft = isPill ? 9 : 0
  const keyboardNumberLeft = isPill ? 70 : Math.floor((keyboardTopbarWidth - keyboardNumberButtonWidth) / 2)
  const keyboardDeleteLeft = isPill ? 135 : keyboardTopbarWidth - keyboardButtonWidth
  const keyboardSearchLeft = isPill ? 3 : 0
  const keyboardSearchWidth = isPill ? 186 : keyboardTopbarWidth
  const keyboardPreviewLeft = isPill ? 15 : 16
  const keyboardPreviewWidth = isPill ? 144 : Math.max(132, keyboardTopbarWidth - 72)
  const keyboardPreviewTextWidth = keyboardPreviewWidth + (isPill ? 82 : 150)
  const keyboardMoreLeft = isPill ? 120 : keyboardTopbarWidth - 58
  const keyboardRoundScrollInset = profile.shape === "round" ? 42 : 0
  const keyboardKeyPadding = isPill ? Math.floor((screenWidth - 192) / 2) : keyboardRoundScrollInset
  const keyboardKeyPaddingRight = profile.shape === "round" ? 118 : keyboardKeyPadding

  return {
    key: profile.key,
    shape: profile.shape,
    screenWidth,
    screenHeight,
    contentWidth,
    contentLeft: Math.floor((screenWidth - contentWidth) / 2),
    cardWidth,
    cardLeft: Math.floor((screenWidth - cardWidth) / 2),
    narrowWidth,
    narrowLeft: Math.floor((screenWidth - narrowWidth) / 2),
    topButtonWidth,
    topButtonLeft: Math.floor((screenWidth - topButtonWidth) / 2),
    titleWidth,
    titleLeft: Math.floor((screenWidth - titleWidth) / 2),
    queryWidth,
    queryLeft: Math.floor((screenWidth - queryWidth) / 2),
    keyboardTopbarWidth,
    keyboardTopbarLeft,
    keyboardSearchLeft,
    keyboardSearchWidth,
    keyboardPreviewLeft,
    keyboardPreviewWidth,
    keyboardPreviewTextWidth,
    keyboardMoreLeft,
    keyboardGroupLeft,
    keyboardGroupWidth: keyboardButtonWidth,
    keyboardNumberLeft,
    keyboardNumberWidth: keyboardNumberButtonWidth,
    keyboardDeleteLeft,
    keyboardDeleteWidth: keyboardButtonWidth,
    keyboardKeyPaddingLeft: keyboardKeyPadding,
    keyboardKeyPaddingRight,
    keyboardInitialScrollLeft: keyboardRoundScrollInset,
    pageButtonWidth,
    pageIndicatorWidth,
    paginationWidth,
    paginationLeft: Math.floor((screenWidth - paginationWidth) / 2),
    qrSize: profile.qrSize,
    qrLeft: Math.floor((screenWidth - profile.qrSize) / 2),
    qrTop: Math.floor((screenHeight - profile.qrSize) / 2),
    headerHeight: profile.shape === "pill" ? 124 : 118,
    resultsListTopPadding: profile.shape === "pill" ? 132 : 126,
    bottomSafe: profile.shape === "round" ? 30 : 10,
    guideListHeight: profile.shape === "round" ? Math.max(260, screenHeight - 150) : Math.max(260, screenHeight - 110),
    aboutInfoTop: profile.shape === "round" ? 256 : (profile.shape === "pill" ? 270 : 264)
  }
}
