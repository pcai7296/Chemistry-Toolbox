import { createScreenLayout } from "./screenProfile.js"

export function applyResponsiveLayout(page, device, fallbackShape) {
  const initialShape = fallbackShape || page.screenShape || "pill"
  page.applyScreenLayout(createScreenLayout(page.screenWidth, page.screenHeight, initialShape))

  if (!device || !device.getInfo) {
    return
  }

  device.getInfo({
    success: (data) => {
      if (!data) {
        return
      }
      page.applyScreenLayout(createScreenLayout(
        data.screenWidth || page.screenWidth,
        data.screenHeight || page.screenHeight,
        data.screenShape || initialShape
      ))
    }
  })
}
