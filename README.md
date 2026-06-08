# Chemistry Toolbox

<p align="center">
  小米 Vela 手表端化学方程式查询工具
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.5.0-1f8f68" alt="Version">
  <img src="https://img.shields.io/badge/platform-Xiaomi%20Vela-1f8f68" alt="Xiaomi Vela">
  <img src="https://img.shields.io/badge/device-watch-2d6cdf" alt="Watch">
  <img src="https://img.shields.io/badge/status-active-1e9b6c" alt="Active">
</p>

## 简介

`Chemistry Toolbox` 是一个面向小米 Vela 可穿戴设备的小屏化学工具箱。当前核心能力是输入两个关键分子式，查询同时包含这两个分子式的化学方程式，并在手环/手表屏幕上以分页、可滚动列表展示结果。

项目最初来源于输入法演示工程，现已重构为化学方程式检索应用，并持续围绕化学输入、离线数据库和小屏阅读体验迭代。

## 当前功能

- 双分子式查询：首页提供两个输入框，按“搜索”后查询同时包含二者的方程式。
- 化学式专用键盘：保留元素、数字、括号、常见基团、电荷输入能力，并优化蜂窝式主键盘布局。
- 小屏结果页：支持上下滑动、分页按钮、动态卡片高度、下标/上标显示和胶囊屏分页栏轻微横向拖动。
- 多屏适配：支持胶囊屏、竖向圆角矩形、方形圆角矩形和圆形屏，非胶囊屏结果卡片与说明卡片按屏幕宽度放大。
- 离线方程式库：内置手工整理数据和从 PDF 导入的紧凑反应索引。
- 编辑辅助：编辑页支持“回车”保存和红色“删除”一键清空当前输入。
- 赞助页：内置赞助码页面。
- 关于页：展示版本、开发者、项目地址和反馈邮箱。
- 使用说明页：提供输入、键盘、搜索结果和注意事项说明。
- 版本同步：统一从 `src/common/appInfo.js` 管理版本，构建前自动同步到清单和 npm 元数据。

## 界面

- 首页：两个分子式输入框、搜索按钮、赞助/关于/使用说明入口。
- 结果页：顶部返回、查询结果标题、查询式；下方为可滚动卡片列表和分页按钮，翻页后自动回到当前页首张卡片。
- 说明页：返回按钮置顶，卡片按文本行数自适应高度，列表仅上下滑动，并为胶囊屏保留底部安全滑动余量。
- 关于页：应用图标、版本号、开发者、项目地址、反馈邮箱。

## 项目结构

```text
src/
├─ common/
│  ├─ appInfo.js              # 应用名、版本号、开发者和项目地址
│  ├─ logo.png                # 应用图标
│  └─ sponsor-code.png        # 赞助码图片
├─ components/
│  └─ InputMethod/            # 键盘图标资源
├─ data/
│  ├─ reactions.js            # 手工整理的高质量反应数据
│  └─ generatedReactionText.js # PDF 导入生成的紧凑反应索引
├─ pages/
│  ├─ index/                  # 首页、编辑页、化学键盘
│  ├─ results/                # 查询结果页
│  ├─ sponsor/                # 赞助页
│  ├─ about/                  # 关于页
│  └─ guide/                  # 使用说明页
├─ services/
│  ├─ chemSearch.js           # 双分子式检索逻辑
│  ├─ deviceLayout.js         # 设备屏幕信息读取与布局应用
│  ├─ formulaFormat.js        # 分子式上下标和方程式显示格式化
│  └─ screenProfile.js        # 不同屏幕形状和分辨率的布局参数
└─ manifest.json              # Vela 应用配置

scripts/
├─ check_format.mjs           # 分子式显示格式回归检查
├─ check_layout.mjs           # 多屏布局边界检查
├─ check_search.mjs           # 搜索结果回归检查
├─ import_reactions.py        # 从高中化学方程式 PDF 导入数据
└─ sync_version.js            # 构建前同步版本号
```

## 数据来源与导入

项目当前使用两类反应数据：

- 手工整理数据：质量较高，可包含类型、条件、现象等说明。
- PDF 导入数据：覆盖面更大，用于扩充可搜索方程式数量。

导入脚本默认读取：

```text
C:\Users\Administrator\Downloads\最全高中化学方程式分类汇总.pdf
```

重新导入：

```bash
python scripts/import_reactions.py
```

导入后会更新：

```text
src/data/generatedReactionText.js
```

## 版本管理

版本号统一维护在：

```text
src/common/appInfo.js
```

当前版本：

```js
export const APP_VERSION = "1.5.0"
export const APP_VERSION_CODE = 10500
```

执行 `npm run start`、`npm run build`、`npm run release` 前会自动运行 `scripts/sync_version.js`，同步到：

- `src/manifest.json`
- `package.json`
- `package-lock.json`

## 本地开发

### 安装依赖

```bash
npm install
```

### 启动开发

```bash
npm run start
```

### 构建 Debug 包

```bash
npm run build
```

### 构建 Release 包

```bash
npm run release
```

构建产物输出到 `dist/`。正式包示例：

```text
dist/com.chemistry.toolbox.miband.release.1.5.0.rpk
```

### 回归检查

```bash
npm run check
```

## 注意事项

- `sign/` 目录包含签名文件，已加入 `.gitignore`，不要提交私钥。
- 项目为离线检索应用，不依赖网络请求。
- PDF 导入数据经过清洗和去重，但仍可能存在资料源或抽取误差。
- 资源来源于网络，侵权必删。

## 项目地址

仓库地址：

[pcai7296/Chemistry-Toolbox](https://github.com/pcai7296/Chemistry-Toolbox)

仓库不一定始终公开。

## 反馈

如有建议和反馈，请联系：

- `18938087296@163.com`
- `1992976096@qq.com`
