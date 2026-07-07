# AI 名片 · 百商智校

暗黑科技风 AI 名片 H5，单文件零依赖（原生 HTML/CSS/JS，无外部请求）。含罗盘仪表盘（SVG）、Tab 状态机、海报弹层长按保存、微信分享三级策略、移动优先响应式。

## 在线名片

| 人物 | 正式版（微信分享用这个） | GitHub 预览 |
|---|---|---|
| 陈永俊 · 董事长 | https://ddd.baiyihuodong.com/chen | https://andychenfromchina.github.io/aicard/ |
| 许新风 · 合伙人 | https://ddd.baiyihuodong.com/aic/xuxinfeng | https://andychenfromchina.github.io/aicard/aic/xuxinfeng.html |
| 刘国歌 · 合伙人 | https://ddd.baiyihuodong.com/aic/liuguoge | https://andychenfromchina.github.io/aicard/aic/liuguoge.html |

> GitHub 版为代码镜像/预览：资产走相对路径、og 指 GitHub，但「分享 AI 名片链接」按钮仍指向 ddd 正式版。

## 目录

```
index.html                    陈永俊名片（GitHub 预览版）
aic/<slug>.html               合伙人名片
*-poster.jpg / *-share.jpg    海报(750×1250) / 微信分享缩略图(512²)
poster-template.html          ★ 海报参数化模板(占位符 + 锁死设计规格)
build_poster.py               ★ 单人海报一键构建(改 CONFIG → 出图)
build_posters_batch.py        ★ 多人海报批量构建(参考;照片自备)
AI名片按钮组件-部署手册.md      保存海报 / 分享链接 按钮组件复用手册
```

## 海报生成（别照截图让 AI 重画，必走样）

海报不在网页代码里、是预渲染 JPG。复刻用参数化模板：

1. `pip install qrcode pillow`
2. 改 `build_poster.py` 顶部 `CONFIG`：照片路径 / 二维码链接 / 姓名 / 头衔 / 三个数据 / 微信号 / CTA 文案
3. `python3 build_poster.py` → 得 `poster.jpg`（750×1250，与原版逐像素同构）

**铁律**：模板设计规格（金渐变 `#d9a13a→#ffb800→#ffd966` / 头像彩环 / 三色数据 / 圆角）不要改；CJK 字体栈不要删（Linux 渲染需装 Noto Sans CJK）；二维码必须用 qrcode 库生成（手绘 / AI 画的必是扫不出的假码）。

## 复刻一张新名片

把 [复刻AI名片-提示词.md](复刻AI名片-提示词.md) 整段复制给任意 AI 编程助手（Claude Code / Cursor 等），填好 7 项信息即自动生成同款新名片。

## 按钮组件复用

「保存 AI 名片图片 / 分享 AI 名片链接」两颗按钮是零依赖组件（类名 `bsc-` 前缀，不污染宿主页），可整块粘到任意页面。见 [AI名片按钮组件-部署手册.md](AI名片按钮组件-部署手册.md)。

## 微信分享卡片描述

微信把纯 URL 自动链接成卡片时：标题 ← `<title>`，灰色描述 ← `<meta name="description">`，缩略图 ← `og:image`。当前描述统一为 slogan「AI名片，让所有AI大模型认识你！」。改后测试记得用带 `?v=N` 的新 URL 绕开微信缓存。
