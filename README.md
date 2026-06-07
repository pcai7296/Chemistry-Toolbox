## Chemistry Toolbox

Xiaomi Vela wearable quick app project scaffolded from the neighboring projects in this workspace.

## Built-in Keyboard Migration

This project now includes the custom keyboard component migrated from `com.bandbbs.ebook-n67`.

- Component path: `src/components/InputMethod/`
- Main file: `src/components/InputMethod/InputMethod.ux`
- Dictionary assets: `src/components/InputMethod/assets/dic.js` and `dicUtil.js`

### How It Is Wired

The index page demonstrates a minimal integration:

- Import component:
  - `<import name="input-method" src="../../components/InputMethod/InputMethod.ux"></import>`
- Render component:
  - `<input-method ... @complete="onInput" @delete="onDelete" @visibilityChange="onVisibilityChange" />`
- Toggle show/hide by binding:
  - `hide="{{hideKeyboard}}"` (set `hideKeyboard = false` to show keyboard)

### Events

- `@complete`: emitted with `{ detail: { content } }` for confirmed input text
- `@delete`: emitted when keyboard delete is triggered
- `@visibilityChange`: emitted when keyboard visibility changes

### Required Manifest Features

Added in `src/manifest.json`:

- `system.vibrator` (key click vibration)
- `system.device` (screen width adaptation on rect/pill devices)

Without these, keyboard behavior may be degraded or partially unavailable.

### Quick Reuse In Other Pages

1. Copy `src/components/InputMethod/` directory.
2. Add `system.vibrator` and `system.device` to `features`.
3. Import `InputMethod.ux` in your page.
4. Provide these page fields/methods:
   - state: `hideKeyboard`, input text value
   - methods: `toggleKeyboard`, `onInput`, `onDelete`, `onVisibilityChange`

### Development

```bash
npm install
npm run start
```

### Build

```bash
npm run build
npm run release
```

The generated package is written to `dist/`.
