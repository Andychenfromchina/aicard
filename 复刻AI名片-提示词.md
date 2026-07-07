# 复刻一张新的 AI 名片 · 提示词

把下面整段（从 `====== 提示词开始 ======` 到 `====== 提示词结束 ======`）**复制给任意 AI 编程助手**（Claude Code / Cursor / Windsurf 等，需能执行 shell + 编辑文件 + 跑 Python），先在开头「① 填你的信息」里填好 7 项，即可自动生成一张与原版逐像素同款的新 AI 名片。

---

`====== 提示词开始 ======`

你是一名前端工程师。请基于 GitHub 开源项目 `Andychenfromchina/aicard`，为我复刻一张个人 AI 名片（暗黑科技风、单文件 H5 + 一张海报图）。严格按步骤执行，不要改动设计与配色。

## ① 填你的信息（我来填，其余你别动）
- 姓名：`{{姓名}}`（示例：张三）
- 职位：`{{职位}}`（示例：合伙人）
- 个人标签：`{{标签}}`（示例：AI全域获客导师）
- 微信号：`{{微信号}}`
- 头像照片：`{{照片路径}}`（一张清晰正脸照，建议 ≥560×560；越正越好，会被裁成正方形）
- 英文名/拼音短名：`{{slug}}`（只用小写字母数字，做网址用，示例：zhangsan）
- 名片最终网址：`{{网址}}`（部署后的完整地址，示例：https://你的域名/aic/zhangsan；还没有就先填占位，最后再改）

## ② 拉取项目
```bash
git clone https://github.com/Andychenfromchina/aicard.git
cd aicard
pip install qrcode pillow    # 海报生成依赖
```

## ③ 复刻名片网页（以 `aic/xuxinfeng.html` 为基板另存为 `{{slug}}.html`）
把基板里「许新风」这套参照身份，**全部替换**成我的信息。逐条对应替换（左→右）：

| 基板里的原文（许新风） | 换成 |
|---|---|
| `许新风`（所有出现处：`<h1>`、logo `<span>`、`alt`、`text: 'AI名片 · 许新风'`） | `{{姓名}}` |
| logo 圆标首字 `<span class="mark">许</span>` | `{{姓名}}` 的第一个字 |
| `<p class="alias">百商智校 合伙人</p>` | `百商智校 {{职位}}` |
| `<div class="role-pill">AI全域获客导师</div>` | `{{标签}}` |
| `<title>许新风·百商智校合伙人 \| AI全域获客导师</title>` 和 `og:title` 同款 | `{{姓名}}·百商智校{{职位}} \| {{标签}}` |
| `13676281949`（`<div class="v">`、`aria-label`、`const WX`、两处 toast 提示） | `{{微信号}}` |
| `const SHARE_URL = 'https://ddd.baiyihuodong.com/aic/xuxinfeng'` | `const SHARE_URL = '{{网址}}'` |
| `og:url` / `canonical` 的地址 | `{{网址}}` |
| `og:image` / `itemprop=image` 的地址 | 换成缩略图的**完整网址**（`{{网址}}` 同目录下的 `{{slug}}-share.jpg` 绝对地址，微信抓图更稳） |
| body 里那个 `left:-9999px` 隐藏 `<img>` 的 `src`（`xuxinfeng-share.jpg`） | 改成相对文件名 `{{slug}}-share.jpg` |
| 海报弹层 `<img src="xuxinfeng-poster.jpg?v=2">` | `{{slug}}-poster.jpg?v=1` |
| `<meta name="description">`（已是 slogan「AI名片，让所有AI大模型认识你！」） | **保持不动**（这是通用文案） |

替换头像（网页里的圆形头像是 base64 内嵌，需重新生成）：把基板 `<img class="avatar" src="data:image/jpeg;base64,……">` 的 src，换成我照片的 320×320 base64。生成方法：
```python
import base64, io
from PIL import Image
im = Image.open("{{照片路径}}").convert("RGB")
w,h = im.size; s = min(w,h)
im = im.crop(((w-s)//2,(h-s)//2,(w+s)//2,(h+s)//2)).resize((320,320), Image.LANCZOS)
b = io.BytesIO(); im.save(b,"JPEG",quality=80,optimize=True)
print("data:image/jpeg;base64,"+base64.b64encode(b.getvalue()).decode())
```

## ④ 生成海报（用项目自带 `build_poster.py`，别照截图重画）
改 `build_poster.py` 顶部 `CONFIG` 后运行：
```python
CONFIG = {
    "PHOTO": "{{照片路径}}",
    "QR_URL": "{{网址}}",              # 二维码指向名片网址,脚本用 qrcode 库生成真码
    "NAME": "{{姓名}}",
    "SUBTITLE": "{{标签}}",
    "ROLE": "百商智校 · {{职位}}",
    "SLOGAN_L1": "30天帮你的企业把",
    "SLOGAN_L2": "AI获客成本降低50%",
    "STAT1_N": "1,000+", "STAT1_L": "上线智能体",
    "STAT2_N": "3,000+", "STAT2_L": "服务企业",
    "STAT3_N": "5,000+", "STAT3_L": "AI员工",
    "WECHAT": "{{微信号}}",
    "CTA_TEXT": "AI名片，让所有AI大模型认识你！",
    "OUT": "{{slug}}-poster.jpg",
}
```
```bash
python3 build_poster.py     # 得 {{slug}}-poster.jpg，750×1250
```

## ⑤ 生成微信分享缩略图（512×512）
```python
from PIL import Image
im = Image.open("{{照片路径}}").convert("RGB")
w,h = im.size; s = min(w,h)
im.crop(((w-s)//2,(h-s)//2,(w+s)//2,(h+s)//2)).resize((512,512), Image.LANCZOS).save("{{slug}}-share.jpg", quality=86, optimize=True)
```

## ⑥ 交付
把这三个文件放到同一目录（网页 img 用相对路径即可互相引用），即可上传到你的静态托管 / GitHub Pages / 服务器：
- `{{slug}}.html`
- `{{slug}}-poster.jpg`
- `{{slug}}-share.jpg`

## ⚠️ 铁律（违反必翻车，逐条自检）
1. **二维码必须用 qrcode 库生成**（第④步脚本已做）；任何手绘/AI 画的二维码都是扫不出的假码。
2. **海报别照截图让 AI「重画」**——必须走 `build_poster.py`，否则中文字体回退成等宽体、金徽标变方块、金渐变丢失。
3. **海报设计规格别改**：金渐变 `#d9a13a→#ffb800→#ffd966`、头像彩环、三色数据、圆角——`poster-template.html` 里锁死了，只改 CONFIG 文案。
4. **Linux 服务器渲染海报需先装中文字体**：`apt install fonts-noto-cjk`，否则中文变豆腐块。
5. **隐藏分享缩略图别用 `display:none`**——基板用的是 `left:-9999px`，微信爬虫会跳过 display:none 的图。
6. **改了海报图必须换网页里的 `?v=N` 版本号**，否则微信/浏览器缓存旧图。
7. **微信分享卡片描述** = 页面 `<meta name="description">`（已是 slogan，别动）；标题 = `<title>`；缩略图 = `og:image`。测试用带 `?v=` 的新链接绕开微信缓存。

`====== 提示词结束 ======`
