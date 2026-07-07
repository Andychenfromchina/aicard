import base64, io, re, sys
import qrcode

SLOGAN = "AI名片，让所有AI大模型认识你！"
COMMON = dict(SLOGAN_L1="30天帮你的企业把", SLOGAN_L2="AI获客成本降低50%",
    STAT1_N="1,000+", STAT1_L="上线智能体", STAT2_N="3,000+", STAT2_L="服务企业",
    STAT3_N="5,000+", STAT3_L="AI员工", CTA_TEXT=SLOGAN)

PEOPLE = {
  "chen":     dict(PHOTO="poster_photo.jpg",    QR="https://ddd.baiyihuodong.com/chen",
                   NAME="陈永俊", SUBTITLE="AI实战首席导师 · AI获客实战派", ROLE="百商智校 · 董事长", WECHAT="zhizhedachen6"),
  "xuxinfeng":dict(PHOTO="xuxinfeng-photo.jpg", QR="https://ddd.baiyihuodong.com/aic/xuxinfeng",
                   NAME="许新风", SUBTITLE="AI全域获客导师", ROLE="百商智校 · 合伙人", WECHAT="13676281949"),
  "liuguoge": dict(PHOTO="liuguoge-photo.jpg",  QR="https://ddd.baiyihuodong.com/aic/liuguoge",
                   NAME="刘国歌", SUBTITLE="AI全域获客导师", ROLE="百商智校 · 合伙人", WECHAT="jiajia1892481"),
}

def qr_b64(url):
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=12, border=2)
    q.add_data(url); q.make(fit=True)
    im = q.make_image(fill_color="#0a0f1c", back_color="white").convert("RGB")
    b = io.BytesIO(); im.save(b, "PNG")
    return "data:image/png;base64," + base64.b64encode(b.getvalue()).decode()

def build(slug):
    p = PEOPLE[slug]
    t = open("poster-template.html", encoding="utf-8").read()
    t = t.replace("__PHOTO__", "data:image/jpeg;base64," + base64.b64encode(open(p["PHOTO"],"rb").read()).decode())
    t = t.replace("__QR__", qr_b64(p["QR"]))
    cfg = dict(COMMON); cfg.update(NAME=p["NAME"], SUBTITLE=p["SUBTITLE"], ROLE=p["ROLE"], WECHAT=p["WECHAT"])
    for k, v in cfg.items():
        t = t.replace(f"__{k}__", v)
    assert not re.findall(r'__[A-Z_]+__', t), f"leftover in {slug}: {set(re.findall(r'__[A-Z_]+__', t))}"
    out = f"_poster_{slug}.html"
    open(out, "w", encoding="utf-8").write(t)
    return out

for slug in sys.argv[1:] or PEOPLE:
    print(build(slug))
