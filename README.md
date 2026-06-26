# Chemistry Toolbox

<p align="center">
  小米 Vela 手表端化学方程式查询与周期表工具
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.8.0-1f8f68" alt="Version">
  <img src="https://img.shields.io/badge/platform-Xiaomi%20Vela-1f8f68" alt="Xiaomi Vela">
  <img src="https://img.shields.io/badge/device-Xiaomi%20Band%2010-2d6cdf" alt="Xiaomi Band 10">
  <img src="https://img.shields.io/badge/status-active-1e9b6c" alt="Active">
</p>

## 简介

`Chemistry Toolbox` 是一个面向小米 Vela 可穿戴设备的小屏化学工具箱。当前主要能力包括：

- 输入两个关键分子式，查询同时包含二者的化学方程式。
- 使用离线周期表图片浏览元素，并通过屏幕中央准星查看元素详情。
- 在手环/手表窄屏上展示反应类型、条件、现象等可用信息。

项目最初来源于输入法演示工程，现已重构为离线化学工具应用，并持续围绕小屏输入、离线数据库、手环端性能和阅读体验迭代。

## 当前功能

- 首页入口：首页保留搜索、周期表、赞助、关于和使用说明入口。
- 方程式搜索：搜索页提供两个输入框，按“搜索”后查询同时包含二者的方程式。
- 化学式专用键盘：支持元素、数字、括号、常见基团、电荷输入。
- 离线反应库：内置 20 条手工精选反应和 1522 条导入反应。
- 构建期索引：导入脚本生成倒排索引，手环端搜索时避免扫描大文本。
- 结果卡片：精选结果优先，导入结果按源顺序展示；类型、条件、现象有信息才显示。
- 长文本显示：长反应物、长生成物、现象和条件会拆行显示，避免省略号截断。
- 周期表：使用整张透明背景周期表图片，拖动图片到固定准星下，点击“查看”打开元素详情。
- 元素详情：显示基础信息、周期/族/分区、电子构型、常见价态、电负性、半径、电离能、物态和发现信息等可用字段。
- 多屏适配：支持胶囊屏、竖向圆角矩形、方形圆角矩形和圆形屏布局参数。
- 关于页：展示版本、开发者、项目地址和反馈邮箱。
- 使用说明页：随当前首页、搜索和周期表交互更新。

## 界面

- 首页：周期表、搜索、赞助、关于、使用说明入口。
- 搜索页：两个分子式输入框、搜索按钮和化学式输入法。
- 结果页：顶部返回、查询结果标题、查询式；下方为可滚动卡片列表和分页按钮。
- 周期表页：固定返回、标题、准星和查看按钮；底层周期表图片可拖动。
- 元素详情：在周期表上方弹出信息卡，长字段按行展开。
- 说明页：卡片式使用说明，适配手环窄屏滚动阅读。

## 项目结构

```text
src/
├─ common/
│  ├─ appInfo.js                  # 应用名、版本号、开发者和项目地址
│  ├─ logo.png                    # 应用图标
│  ├─ periodic-table.png          # 透明背景周期表图片
│  └─ sponsor-code.png            # 赞助码图片
├─ components/
│  └─ InputMethod/                # 键盘图标资源
├─ data/
│  ├─ reactions.js                # 手工精选反应数据
│  ├─ generatedReactionIndex.js   # 构建期生成的方程式数组和倒排索引
│  ├─ generatedReactionText.js    # 导入数据的兼容文本输出
│  ├─ periodicElements.js         # 元素详情源数据
│  └─ periodicElementsCompact.js  # 运行时使用的紧凑元素数据
├─ pages/
│  ├─ index/                      # 首页和化学键盘
│  ├─ search/                     # 方程式搜索页
│  ├─ periodic/                   # 周期表页
│  ├─ results/                    # 查询结果页
│  ├─ sponsor/                    # 赞助页
│  ├─ about/                      # 关于页
│  └─ guide/                      # 使用说明页
├─ services/
│  ├─ chemSearch.js               # 双分子式检索逻辑
│  ├─ deviceLayout.js             # 设备屏幕信息读取与布局应用
│  ├─ formulaFormat.js            # 分子式上下标和方程式显示格式化
│  └─ screenProfile.js            # 不同屏幕形状和分辨率的布局参数
└─ manifest.json                  # Vela 应用配置

scripts/
├─ build_reaction_database.py     # 反应库清洗和扩容脚本
├─ check_format.mjs               # 分子式显示格式回归检查
├─ check_layout.mjs               # 多屏布局边界检查
├─ check_search.mjs               # 搜索和索引回归检查
├─ import_reactions.py            # 导入并生成反应库索引
└─ sync_version.js                # 构建前同步版本号
```

## 数据来源与导入

项目当前使用两类反应数据：

- 手工精选数据：质量较高，可包含类型、条件、现象等说明。
- 导入数据：覆盖面更大，用于扩充可搜索方程式数量。

导入脚本会生成构建期索引：

```text
src/data/generatedReactionIndex.js
```

重新导入：

```bash
python scripts/import_reactions.py
```

导入后建议运行：

```bash
npm run check
npm run build
```

## 版本管理

版本号统一维护在：

```text
src/common/appInfo.js
```

当前版本：

```js
export const APP_VERSION = "1.8.0"
export const APP_VERSION_CODE = 10800
```

执行 `npm run start`、`npm run build`、`npm run release` 前会自动运行 `scripts/sync_version.js`，同步到：

- `src/manifest.json`
- `package.json`
- `package-lock.json`

## 本地开发

安装依赖：

```bash
npm install
```

启动开发：

```bash
npm run start
```

构建 Debug 包：

```bash
npm run build
```

构建 Release 包：

```bash
npm run release
```

构建产物输出到 `dist/`。Debug 包示例：

```text
dist/com.chemistry.toolbox.miband.debug.1.8.0.rpk
```

回归检查：

```bash
npm run check
```

## 注意事项

- `sign/` 目录包含签名文件，不要提交私钥。
- 项目为离线检索应用，不依赖网络请求。
- 导入数据经过清洗和去重，但仍可能存在资料源或抽取误差。
- 周期表交互优先保证性能和对齐稳定，因此使用“拖动图片到准星后查看”的方式。
- Vela 文本组件在长字符串上可能出现截断，结果页和元素详情页应优先使用拆行后的多个文本节点。
- 资源来源于网络，侵权必删。

## 项目地址

[pcai7296/Chemistry-Toolbox](https://github.com/pcai7296/Chemistry-Toolbox)

## 反馈

如有建议和反馈，请联系：

- `18938087296@163.com`
- `1992976096@qq.com`
