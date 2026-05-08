# My Open Bypass List Merge — 开源代理规则合并工具

[![GitHub stars](https://img.shields.io/github/stars/muse433/my-open-bypass-list-merge?style=social)](https://github.com/muse433/my-open-bypass-list-merge)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/muse433/my-open-bypass-list-merge/merge.yml?label=Daily%20Merge)](https://github.com/muse433/my-open-bypass-list-merge/actions/workflows/merge.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 痛点：你也在用小火箭管理多个规则链接？

如果你是 Shadowrocket（小火箭）、Clash Meta 或 Surge 用户，你一定遇到过这些问题：

- ❌ **维护多个规则链接的痛苦** — Reddit 一个、Twitter 一个、AI 服务一个、流媒体一个...每次更新配置都要逐个添加
- ❌ **规则文件膨胀** — 单个规则文件越加越多，配置越来越乱
- ❌ **规则冲突与重复** — 不同来源的规则相互覆盖，不知道哪个生效
- ❌ **更新不及时** — 手动更新总忘记，某个链接失效了也不知道

> **一句话解决**：把所有规则的远程链接合并为一个，每天自动更新，小火箭只要维护这一个链接。

---

## ✨ 功能特点

| 特性 | 说明 |
|------|------|
| 🚀 **一键管理** | 6 个主流规则列表合并为 1 个链接 |
| 🔄 **每日自动更新** | GitHub Action 每天 UTC 00:00 自动拉取最新规则 |
| 🧹 **自动去重** | 智能去重，同一条规则不会出现两次 |
| 📝 **自动清理** | 去除所有注释和空行，轻量化输出 |
| 🔌 **即插即用** | 配置一次，后续无需任何操作 |
| 🧩 **完全开源** | MIT 协议，欢迎 Fork/PR/Star |
| 🔒 **无账号依赖** | 无需注册，不需要任何 API Key |

---

## 📦 目前合并的规则源

| 分类 | 原始来源 | 说明 |
|------|---------|------|
| 🌐 **Reddit 直连** | blackmatrix7/ios_rule_script | Reddit 代理规则 |
| 🐦 **Twitter/X 直连** | blackmatrix7/ios_rule_script | Twitter/X 代理规则 |
| 📺 **流媒体代理** | ACL4SSR | 视频/流媒体走代理 |
| 🤖 **Gemini 直连** | blackmatrix7/ios_rule_script | Google Gemini 直连 |
| 🧠 **AI 服务** | ACL4SSR | 通用 AI 服务直连 |
| 🔮 **OpenAI 直连** | ACL4SSR | ChatGPT/OpenAI 直连 |

> 💡 这些规则让 Reddit、Twitter、各种 AI 服务走直连（不走代理），流媒体走代理。你可以按需增减。

---

## 📥 快速使用

### Shadowrocket（小火箭）

```
https://raw.githubusercontent.com/muse433/my-open-bypass-list-merge/main/merged.list
```

**配置步骤：**
1. 打开 Shadowrocket
2. 进入「配置」
3. 点击「远程文件」→ 「添加配置」
4. 粘贴上面的链接
5. 保存 → 应用

### Clash Meta / Clash Verge

在 `rules` 段添加：
```yaml
- RULE-SET,https://raw.githubusercontent.com/muse433/my-open-bypass-list-merge/main/merged.list,DIRECT
```

### Surge

在 `Rule` 段添加：
```
RULE-SET,https://raw.githubusercontent.com/muse433/my-open-bypass-list-merge/main/merged.list,DIRECT
```

---

## 🔧 工作原理

```
每天 UTC 00:00（北京时间 08:00）
        ↓
GitHub Action 自动触发
        ↓
从 6 个源分别拉取最新规则
        ↓
逐行解析 + 去注释 + 去空行 + 去重
        ↓
输出合并后的 merged.list
        ↓
推送回仓库 → raw 链接自动更新
```

**你的 Shadowrocket 只要引用这个 raw 链接，就会自动获取最新的合并规则。**

---

## 🤝 贡献指南

### 想加新的规则源？

1. Fork 本仓库
2. 编辑 `merge.py`，在 `URLS` 列表追加新 URL
3. 提交 PR

**举个🌰：**
```python
URLS = [
    # ... 现有源
    "https://raw.githubusercontent.com/xxx/xxx/master/rule.list",  # 你的新源
]
```

### 想优化合并逻辑？

欢迎任何改进：
- 更聪明的去重策略
- 规则冲突检测
- 支持更多代理客户端格式
- 性能优化

直接提交 PR 或开 Issue 讨论。

---

## 🏗️ 项目结构

```
my-open-bypass-list-merge/
├── merge.py                  # 核心合并脚本
├── merged.list               # 每日自动生成的合并文件
├── .github/workflows/
│   └── merge.yml            # GitHub Action 配置
├── README.md                 # 本文件
└── LICENSE                   # MIT 协议
```

---

## 📊 数据分析（给高级用户）

合并文件的格式完全兼容 Shadowrocket 和 Clash 的规则语法：

```
# 域名直连
DOMAIN-SUFFIX,reddit.com,DIRECT
DOMAIN-SUFFIX,twitter.com,DIRECT

# IP 段规则
IP-CIDR,0.0.0.0/8,DIRECT

# 正则匹配
URL-REGEX,^https?://.../DIRECT
```

> 每条规则都是独立完整的，不会因合并顺序产生覆盖冲突。

---

## 📜 许可证

MIT License — 你可以自由使用、修改、分发。

---

## ⭐ 支持项目

如果这个项目帮到了你，请给我们点个 ⭐ Star！

- **Star 仓库** → [muse433/my-open-bypass-list-merge](https://github.com/muse433/my-open-bypass-list-merge)
- **提 Issue** → 遇到问题或建议
- **提交 PR** → 想加新源或改进代码
- **分享** → 去 V2EX、即刻、Telegram 群告诉更多朋友

---

> **关键词：** Shadowrocket 规则合并 · 小火箭规则列表 · Clash 规则聚合 · 代理规则管理 · Bypass list merge · 科学上网规则 · 代理自动化 · GitHub Action 自动更新 · 开源代理工具 · Reddit 直连规则 · Twitter 直连 · OpenAI 直连 · AI 服务直连 · ACL4SSR · blackmatrix7
