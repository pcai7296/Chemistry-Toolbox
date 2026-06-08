const fs = require("fs")
const path = require("path")

const root = path.resolve(__dirname, "..")
const appInfoPath = path.join(root, "src", "common", "appInfo.js")
const source = fs.readFileSync(appInfoPath, "utf8")

function readConst(name) {
  const stringMatch = source.match(new RegExp(`export const ${name} = "([^"]+)"`))
  if (stringMatch) {
    return stringMatch[1]
  }
  const numberMatch = source.match(new RegExp(`export const ${name} = ([0-9]+)`))
  if (numberMatch) {
    return Number(numberMatch[1])
  }
  throw new Error(`Missing ${name} in appInfo.js`)
}

const version = readConst("APP_VERSION")
const versionCode = readConst("APP_VERSION_CODE")

function updateJson(relativePath, updater) {
  const filePath = path.join(root, relativePath)
  const json = JSON.parse(fs.readFileSync(filePath, "utf8"))
  updater(json)
  fs.writeFileSync(filePath, `${JSON.stringify(json, null, 2)}\n`)
}

updateJson("src/manifest.json", (manifest) => {
  manifest.versionName = version
  manifest.versionCode = versionCode
})

updateJson("package.json", (pkg) => {
  pkg.version = version
})

updateJson("package-lock.json", (lock) => {
  lock.version = version
  if (lock.packages && lock.packages[""]) {
    lock.packages[""].version = version
  }
})

console.log(`Synced app version ${version} (${versionCode})`)
