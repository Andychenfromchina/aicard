#!/usr/bin/env python3
# build_poster.py — AI名片海报一键构建(与原版逐像素同构)
# 用法: 改下方 CONFIG → python3 build_poster.py → 得 poster.jpg
# 依赖: pip install qrcode pillow ;渲染用本机 Chrome(macOS/Windows 自带中文字体,Linux 需装 Noto Sans CJK)
import base64
import io
import os
import shutil
import subprocess
import sys
import tempfile

# ==================== CONFIG:改这里 ====================
CONFIG = {
    "PHOTO": "photo.jpg",                 # 方形头像照片路径(建议≥560×560)
    "QR_URL": "https://ddd.baiyihuodong.com/chen",  # 二维码指向的链接
    "NAME": "陈永俊",
    "SUBTITLE": "AI实战首席导师 · AI获客实战派",
    "ROLE": "百商智校 · 董事长",
    "SLOGAN_L1": "30天帮你的企业把",
    "SLOGAN_L2": "AI获客成本降低50%",
    "STAT1_N": "1,000+", "STAT1_L": "上线智能体",
    "STAT2_N": "3,000+", "STAT2_L": "服务企业",
    "STAT3_N": "5,000+", "STAT3_L": "AI员工",
    "WECHAT": "zhizhedachen6",
    "CTA_TEXT": "百商AI一键制作你的AI名片",
    "OUT": "poster.jpg",
}
# =======================================================

TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "poster-template.html")


def find_chrome():
    for p in (
        os.environ.get("CHROME"),
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        shutil.which("google-chrome"), shutil.which("chromium"),
        shutil.which("chromium-browser"), shutil.which("chrome"),
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    ):
        if p and os.path.exists(p):
            return p
    sys.exit("找不到 Chrome:装 Chrome 或设环境变量 CHROME=可执行文件路径")


def make_qr_b64(url):
    # ⚠️铁律:二维码必须用库生成,任何"手绘/AI画"的二维码矩阵都是扫不出的假码
    import qrcode
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=12, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#0a0f1c", back_color="white").convert("RGB")
    buf = io.BytesIO()
    img.save(buf, "PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def photo_b64(path):
    from PIL import Image
    img = Image.open(path).convert("RGB")
    w, h = img.size
    side = min(w, h)  # 居中方形裁剪
    img = img.crop(((w - side) // 2, (h - side) // 2, (w + side) // 2, (h + side) // 2))
    img = img.resize((560, 560), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=86, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def main():
    html = open(TEMPLATE, encoding="utf-8").read()
    html = html.replace("__PHOTO__", photo_b64(CONFIG["PHOTO"]))
    html = html.replace("__QR__", make_qr_b64(CONFIG["QR_URL"]))
    for k, v in CONFIG.items():
        if k in ("PHOTO", "QR_URL", "OUT"):
            continue
        html = html.replace(f"__{k}__", v)
    if "__" in html.replace("__proto__", ""):
        i = html.find("__")
        sys.exit(f"仍有未填占位符,请检查 CONFIG:...{html[i:i+30]}...")

    with tempfile.TemporaryDirectory() as td:
        page = os.path.join(td, "poster.html")
        png = os.path.join(td, "poster.png")
        open(page, "w", encoding="utf-8").write(html)
        subprocess.run([
            find_chrome(), "--headless", "--disable-gpu", "--hide-scrollbars",
            "--force-device-scale-factor=1", "--window-size=750,1250",
            f"--screenshot={png}", "file://" + page,
        ], check=True, capture_output=True)
        from PIL import Image
        Image.open(png).convert("RGB").save(CONFIG["OUT"], quality=86, optimize=True)
    print(f"✅ {CONFIG['OUT']} ({os.path.getsize(CONFIG['OUT'])} bytes) · 750×1250")
    print("提醒:部署后 URL 记得带版本号 ?v=N,改图必须换号,否则微信缓存旧图")


if __name__ == "__main__":
    main()
