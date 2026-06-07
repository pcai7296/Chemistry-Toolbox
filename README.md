# Chemistry Toolbox

<p align="center">
  面向小米 Vela 手表设备的化学方程式查询工具
</p>

<p align="center">
  <img src="https://img.shields.io/badge/platform-Xiaomi%20Vela-1f8f68" alt="Xiaomi Vela">
  <img src="https://img.shields.io/badge/device-watch-2d6cdf" alt="Watch">
  <img src="https://img.shields.io/badge/status-active-1f8f68" alt="Active">
</p>

## 项目简介

`Chemistry Toolbox` 是一个运行在小米 Vela 可穿戴设备上的化学工具应用，当前聚焦于：

- 使用两个分子式作为查询条件
- 检索同时包含这两个分子式的化学方程式
- 在手表小屏上展示可翻页、可滚动的结果列表
- 提供面向化学式输入优化过的专用键盘

这个项目最初来源于一个输入法演示工程，现已重构为真正的化学工具箱方向。

## 当前功能

- 双输入框搜索：输入两个分子式后进入结果页查询
- 化学式专用键盘：保留元素、数字、括号、电荷等核心输入能力
- 方程式结果页：支持分页、上下滚动、底部翻页按钮
- 化学式格式化显示：结果页会把原子数显示为下标
- 本地离线反应库：内置常见方程式，不依赖联网
- PDF 导入库：支持将整理好的方程式资料批量导入项目数据

## 界面说明

### 首页

- 两个可编辑的分子式输入框
- 点击搜索后跳转到结果页

### 结果页

- 显示同时命中两个分子式的方程式
- 支持上下滑动浏览当前页结果
- 支持底部 `上一页 / 下一页` 按钮切换分页

## 项目结构

```text
src/
├─ components/
│  └─ InputMethod/          # 迁移并改造后的输入法组件资源
├─ data/
│  ├─ reactions.js          # 手工整理 + 导入库合并后的反应数据入口
│  └─ generatedReactions.js # 由导入脚本生成的批量反应数据
├─ pages/
│  ├─ index/                # 首页与化学式输入
│  └─ results/              # 查询结果页
├─ services/
│  └─ chemSearch.js         # 双分子式检索逻辑
└─ manifest.json            # Vela 应用配置

scripts/
└─ import_reactions.py      # 从资料文本中抽取方程式并生成数据文件
```

## 数据来源与导入

项目当前同时使用两类反应数据：

- 手工整理的数据：字段更完整，适合展示反应类型、条件、现象
- 批量导入的数据：覆盖面更大，用于扩充可检索方程式数量

导入脚本：

```bash
python scripts/import_reactions.py
```

脚本会根据本地资料文本重新生成：

- `src/data/generatedReactions.js`

## 本地开发

### 环境要求

- Node.js
- `aiot-toolkit`
- 小米 Vela Quick App 开发环境

### 安装依赖

```bash
npm install
```

### 启动开发

```bash
npm run start
```

### 构建

```bash
npm run build
```

### 发布包

```bash
npm run release
```

构建产物会输出到 `dist/`。

## 技术要点

- 基于 Xiaomi Vela Quick App `.ux` 页面体系
- 使用 `system.storage` 保存查询参数和输入内容
- 使用独立结果页避免首页首次加载过重
- 对导入方程式做去重与清洗，降低 OCR / 换行带来的错误

## 后续计划

- 扩充高质量反应库并补全条件、现象、分类
- 增强带电离子与复杂化学式检索
- 优化结果卡片布局，适配圆形/胶囊屏边界
- 增加物质详情页，而不只停留在方程式列表

## 仓库说明

这是一个持续迭代中的个人项目，当前重点是：

1. 先把手表端查询链路做稳定
2. 再提高化学数据质量
3. 最后继续完善交互和显示效果

如果你也在做 Vela 手表应用，这个项目也可以作为：

- 双输入框检索页示例
- 小屏结果列表分页示例
- 可定制输入键盘改造示例

