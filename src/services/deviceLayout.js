import device from "@system.device"
import { createScreenLayout } from "./screenProfile.js"

export function applyResponsiveLayout(page, fallbackShape) {
  const initialShape = fallbackShape || page.screenShape || "pill"
  page.applyScreenLayout(createScreenLayout(page.screenWidth, page.screenHeight, initialShape))

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
