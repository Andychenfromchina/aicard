# AI名片「保存海报 + 分享链接」按钮组件 · 快速部署手册

> 来源:https://ddd.baiyihuodong.com/chen 联系区组件(2026-07-06 线上版逐字提取)。
> 纯原生 HTML/CSS/JS,零依赖、零外部请求;类名带 `bsc-` 前缀,不会污染宿主页面样式。
> 适配:手机浏览器 / 微信内置浏览器 / 桌面浏览器。

---

## 一、组件做什么

| 按钮 | 点击行为 |
|---|---|
| 🖼 **保存AI名片图片**(金) | 弹出全屏遮罩层展示海报图,提示「长按图片·保存到手机相册」(微信/手机长按图片即可存);点 ✕ 或空白处关闭 |
| 🔗 **分享AI名片链接**(青) | 三级策略:**微信内**→弹「点击右上角···转发给朋友」引导层(微信不允许网页直接拉起转发,这是行业标准做法);**普通手机浏览器**→拉起系统原生分享面板;**都不支持**→复制链接+toast 提示去粘贴 |

## 二、部署三步

1. **替换 3 个占位**(在下方代码里搜索):
   - `__POSTER_URL__` → 你的海报图完整地址(建议带版本号,如 `https://xx.com/poster.jpg?v=1`;改图必须换版本号,否则微信缓存旧图)
   - `__SHARE_URL__` → 要分享出去的页面链接
   - `__SHARE_TITLE__` → 系统分享面板里显示的标题
2. **整块粘贴到页面 `</body>` 之前**。⚠️ 铁律:遮罩层 HTML 必须出现在绑定它的 `<script>` **之前**(本代码块内部顺序已排好,整块粘贴即安全;若拆开集成,切记先 HTML 后 JS,否则 `querySelector` 拿到 null 会抛错连累页面其他脚本)
3. 把「按钮对」那段 HTML 挪到你页面想显示按钮的位置(其余遮罩/toast 留在 body 尾部即可)

## 三、完整代码(整块可拷)

```html
<!-- ============ ① 按钮对:放到页面需要的位置 ============ -->
<div class="bsc-row">
  <button class="bsc-btn bsc-gold" id="bscPosterBtn" type="button">
    <span aria-hidden="true">🖼</span>保存AI名片图片
  </button>
  <button class="bsc-btn bsc-cyan" id="bscShareBtn" type="button">
    <span aria-hidden="true">🔗</span>分享AI名片链接
  </button>
</div>

<!-- ============ ② 遮罩层 + toast:放 </body> 前、且必须在 ③脚本 之前 ============ -->
<div class="bsc-poster-mask" id="bscPosterMask" hidden role="dialog" aria-modal="true" aria-label="AI名片海报,长按图片保存">
  <button class="bsc-poster-close" id="bscPosterClose" type="button" aria-label="关闭">✕</button>
  <div class="bsc-poster-box">
    <img src="__POSTER_URL__" alt="AI名片海报">
    <div class="bsc-poster-tip">长按图片 · 保存到手机相册</div>
  </div>
</div>
<div class="bsc-wxguide" id="bscWxGuide" hidden>
  <div class="bsc-wxguide-arrow" aria-hidden="true">⬆</div>
  <div class="bsc-wxguide-text">点击右上角「···」<br>转发给朋友或分享到朋友圈</div>
</div>
<div class="bsc-toast" id="bscToast" role="status" aria-live="polite"></div>

<style>
/* ============ 按钮(金/青,微信内金色渐变+发光阴影) ============ */
.bsc-row{display:flex;gap:10px;margin:16px 0}
.bsc-btn{flex:1;display:inline-flex;align-items:center;justify-content:center;gap:6px;min-height:46px;
  border-radius:12px;border:1px solid transparent;font-size:.96rem;font-weight:700;cursor:pointer;
  white-space:nowrap;user-select:none;-webkit-tap-highlight-color:transparent;
  transition:transform .15s cubic-bezier(.34,1.56,.5,1),box-shadow .25s}
.bsc-btn:active{transform:scale(.96)}
.bsc-gold{background:linear-gradient(135deg,#d9a13a,#ffb800 55%,#ffd966);color:#1a1204;
  box-shadow:0 6px 18px rgba(255,184,0,.3)}
.bsc-gold:hover{box-shadow:0 10px 26px rgba(255,184,0,.45);transform:translateY(-1px)}
.bsc-cyan{background:linear-gradient(135deg,#00f0ff 0%,#00b8c7 100%);color:#050810;
  box-shadow:0 6px 18px rgba(0,240,255,.25)}
.bsc-cyan:hover{box-shadow:0 10px 26px rgba(0,240,255,.4);transform:translateY(-1px)}

/* ============ 海报弹层 ============ */
.bsc-poster-mask{position:fixed;inset:0;z-index:120;background:rgba(3,6,14,.9);
  -webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);
  display:flex;flex-direction:column;align-items:center;justify-content:center}
.bsc-poster-mask[hidden],.bsc-wxguide[hidden]{display:none}
/* -webkit-touch-callout:default 保证 iOS 微信里长按能呼出"保存图片" */
.bsc-poster-box img{max-width:82vw;max-height:72vh;border-radius:18px;display:block;
  box-shadow:0 24px 70px rgba(0,0,0,.7);-webkit-touch-callout:default}
.bsc-poster-tip{text-align:center;font-size:.84rem;color:#ffd966;margin-top:14px;letter-spacing:.08em}
.bsc-poster-close{position:absolute;top:calc(16px + env(safe-area-inset-top));right:16px;width:44px;height:44px;
  border-radius:50%;border:1px solid rgba(255,255,255,.25);background:rgba(255,255,255,.08);
  color:#fff;font-size:1.05rem;cursor:pointer}

/* ============ 微信右上角分享引导层 ============ */
.bsc-wxguide{position:fixed;inset:0;z-index:120;background:rgba(3,6,14,.84);text-align:right;padding:20px 26px}
.bsc-wxguide-arrow{font-size:2.5rem;color:#ffd966;line-height:1;
  animation:bscNudge 1s ease-in-out infinite alternate}
@keyframes bscNudge{from{transform:translateY(0)}to{transform:translateY(-10px)}}
.bsc-wxguide-text{font-size:1.02rem;color:#fff;line-height:1.8;margin-top:8px;font-weight:600}

/* ============ toast 反馈 ============ */
.bsc-toast{position:fixed;left:50%;bottom:calc(84px + env(safe-area-inset-bottom));z-index:130;
  transform:translate(-50%,24px);background:rgba(14,21,38,.92);border:1px solid rgba(255,184,0,.5);
  color:#f0f4ff;padding:.7em 1.3em;border-radius:999px;font-size:.84rem;opacity:0;pointer-events:none;
  transition:opacity .3s,transform .3s cubic-bezier(.34,1.56,.5,1);
  box-shadow:0 10px 30px rgba(0,0,0,.5);max-width:86vw;text-align:center}
.bsc-toast.show{opacity:1;transform:translate(-50%,0)}
</style>

<!-- ============ ③ 脚本:必须在遮罩层 HTML 之后 ============ -->
<script>
(function () {
  'use strict';
  /* ====== 改这三个 ====== */
  var SHARE_URL = '__SHARE_URL__';
  var SHARE_TITLE = '__SHARE_TITLE__';
  /* POSTER_URL 直接写在上面 <img src> 里 */

  var $ = function (s) { return document.querySelector(s); };

  /* toast 即时反馈 */
  var toastTimer;
  function toast(msg) {
    var el = $('#bscToast'); el.textContent = msg; el.classList.add('show');
    clearTimeout(toastTimer); toastTimer = setTimeout(function () { el.classList.remove('show'); }, 2200);
  }

  /* 剪贴板:clipboard API → execCommand 双降级,失败绝不报成功 */
  function copy(text, okMsg) {
    function fallback() {
      var ta = document.createElement('textarea');
      ta.value = text; ta.setAttribute('readonly', '');
      ta.style.cssText = 'position:fixed;opacity:0';
      document.body.appendChild(ta);
      ta.select(); ta.setSelectionRange(0, text.length);
      var ok = false;
      try { ok = document.execCommand('copy'); } catch (e) {}
      ta.remove();
      toast(ok ? okMsg : '复制失败,请手动记下:' + text);
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function () { toast(okMsg); }, fallback);
    } else { fallback(); }
  }

  /* 点击+键盘(Enter/空格)双绑定,无障碍 */
  function bindTap(el, fn) {
    el.addEventListener('click', fn);
    el.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); fn(); }
    });
  }

  /* ---------- 保存海报:弹层 + 长按保存 ---------- */
  var posterMask = $('#bscPosterMask'), wxGuide = $('#bscWxGuide');
  bindTap($('#bscPosterBtn'), function () { posterMask.hidden = false; });
  $('#bscPosterClose').addEventListener('click', function () { posterMask.hidden = true; });
  posterMask.addEventListener('click', function (e) { if (e.target === posterMask) posterMask.hidden = true; });
  wxGuide.addEventListener('click', function () { wxGuide.hidden = true; });

  /* ---------- 分享链接:微信引导 → 系统分享 → 复制兜底 ---------- */
  bindTap($('#bscShareBtn'), function () {
    if (/MicroMessenger/i.test(navigator.userAgent)) { wxGuide.hidden = false; return; }
    if (navigator.share) {
      navigator.share({ title: SHARE_TITLE, text: SHARE_TITLE, url: SHARE_URL })
        .catch(function (e) { if (!e || e.name !== 'AbortError') copy(SHARE_URL, '链接已复制,去微信粘贴发给好友 ✅'); });
      return;
    }
    copy(SHARE_URL, '链接已复制,去微信粘贴发给好友 ✅');
  });
})();
</script>
```

## 四、避坑清单(全部踩过)

1. **遮罩 HTML 必须在脚本之前**——放脚本后面,绑定时元素不存在,一个 TypeError 连累整页 JS
2. **海报图改版必须换 `?v=N` 版本号**——微信/浏览器缓存旧图,「明明部署了还是旧版」九成是这个
3. **微信内不能用 `<a download>` 下载、不能直接拉起转发**——所以保存走"长按图片"、分享走"右上角引导层",别试图绕过
4. **iOS 长按保存依赖 `-webkit-touch-callout:default`**——别在海报 img 上全局禁用 callout
5. **隐藏图片别用 `display:none`**(本组件不涉及,但同页放微信分享缩略图时:用 `left:-9999px`,display:none 会被微信爬虫跳过)
6. **`execCommand('copy')` 失败不抛异常**——必须检查返回值,否则会弹假成功 toast
7. **z-index**:遮罩 120 / toast 130,若宿主页有更高层级浮窗自行上调
8. 海报图建议 **750 宽、<300KB**,弹层里 `max-height:72vh` 保证一屏放得下、提示文案不被顶出屏

## 五、二维码生成(海报里要放码时)

**严禁让 AI 直接"画"二维码**(手绘矩阵必是假码、扫不出),必须用库生成:

```python
import qrcode
qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=12, border=2)
qr.add_data('https://你的链接')
qr.make(fit=True)
qr.make_image(fill_color="#0a0f1c", back_color="white").save('qr.png')
```

## 六、海报本体也要复刻?用参数化模板,别照截图重画

⚠️ **海报不在网页代码里**——它是一张预渲染的 JPG。只复制按钮组件代码拿不到海报;让 AI 照截图"重画"必然走样(字体回退成等宽体、徽标变方块、金渐变丢失)。正确做法:

1. 取仓库里两个文件:[`poster-template.html`](poster-template.html)(参数化模板,设计规格已锁死并注释) + [`build_poster.py`](build_poster.py)(一键构建)
2. 改 `build_poster.py` 顶部 CONFIG:照片路径 / 二维码链接 / 姓名 / 头衔 / 三个数据 / 微信号 / CTA 文案
3. `pip install qrcode pillow` 后运行 `python3 build_poster.py` → 得 `poster.jpg`(750×1250,与原版逐像素同构)

**三条铁律**:
- 模板里的设计规格(金渐变色值/头像彩环/三色数据/圆角)**不要改**,改了就和原版不一致
- CJK 字体栈不要删(Linux 服务器渲染需先装 Noto Sans CJK,否则中文变豆腐块/等宽体)
- 二维码由脚本用 qrcode 库生成,**严禁手绘/AI画码**(必是假码)

---
*线上参考:https://ddd.baiyihuodong.com/chen(点「保存AI名片图片」「分享AI名片链接」体验实际交互)*
