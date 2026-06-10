# -*- coding: utf-8 -*-
"""
build_treatment_template.py  ·  lsb-treatment-builder 강제 렌더 모듈
=====================================================================
SKILL.md 4.2-a(typeset)·Phase 5(겹침 게이트)·§6(폰트 하한)이 "산문 규칙"으로만
존재해 매 세션 지켜지지 않던 문제를, **실제 코드로 강제**하기 위한 재사용 모듈.

텍스트가 주인공인 페이지(전략 비트·컨셉 카피·키비주얼 카피·클로징)는 반드시
이 모듈의 typeset()/draw_block()을 거치고, 빌드 직전 assert_no_overlap()로
텍스트-패널/이미지 겹침을 검사한다. 미달이면 빌드 보류.

§8(에디토리얼 레이아웃 시스템, _2606041330): 4K 기본 캔버스 + 이미지 합성
아키타입(cover_split / two_col / fullbleed_kv / cut_board) + 팔레트 토큰 + 이미지
존재 게이트. "텍스트만 그라데이션 위에 중앙정렬"되던 평면 출력을 막고, 코덱스
리디자인급(좌측정렬 위계·2단·크림 카드·풀블리드·썸네일 그리드)을 기본값으로.

규칙 출처: REFERENCE/text-setting.md (4축) · REFERENCE/editorial-layout.md (레이아웃)
         · SKILL.md Phase 4·5 · §6.
의존성: Pillow.  폰트: 제목 Black Han Sans, 본문 Noto Sans KR (경로 주입).
"""

import re, os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

# ─────────────────────────────────────────────────────────────────────────
# 0. 폰트 하한 (Q6 — 광고주/텍스트-주인공 페이지에만. 제작 8블록 페이지는 예외)
#    1920×1080 논리 기준 px. page_type="production"이면 하한 면제(None).
# ─────────────────────────────────────────────────────────────────────────
FONT_FLOORS = {
    "client":    {"kicker": 24, "headline": 64, "subhead": 40, "body": 40, "caption": 24},
    "text_hero": {"kicker": 24, "headline": 72, "subhead": 44, "body": 42, "caption": 24},
    "production": None,   # 8블록 풀필드 — 의도적 소폰트, 하한 면제
}

def floor_for(page_type, role):
    table = FONT_FLOORS.get(page_type)
    if not table:
        return 0
    return table.get(role, 0)

def assert_font_floor(page_type, role, size):
    fl = floor_for(page_type, role)
    if size < fl:
        raise ValueError(
            "FONT-FLOOR 위반: %s/%s = %dpx < 하한 %dpx (page_type=%s)"
            % (page_type, role, size, fl, page_type))
    return True

# ─────────────────────────────────────────────────────────────────────────
# 1. 의미 단위 줄바꿈 (text-setting 축1) — 글자 단위 금지
# ─────────────────────────────────────────────────────────────────────────
_CONTRAST = re.compile(r"(아니라|아닌)\s+")

def split_clauses(text):
    t = text.strip()
    if "//" in t:
        return [p.strip() for p in t.split("//") if p.strip()]
    chunks = [c.strip() for c in re.split(r"(?<=[,，])\s+", t) if c.strip()]
    if len(chunks) >= 2:
        return chunks
    m = _CONTRAST.search(t)
    if m:
        a, b = t[:m.end()].strip(), t[m.end():].strip()
        if a and b:
            return [a, b]
    return [t]

# ─────────────────────────────────────────────────────────────────────────
# 2. 포인트 컬러 1강조 (축2) — *강조구* 마크업. 블록당 1개만.
# ─────────────────────────────────────────────────────────────────────────
_EMPH = re.compile(r"\*([^*]+)\*")

def parse_spans(line, base_color, point_color, emphasis_budget):
    spans, idx = [], 0
    for m in _EMPH.finditer(line):
        if m.start() > idx:
            spans.append({"text": line[idx:m.start()], "color": base_color})
        if emphasis_budget[0] > 0:
            spans.append({"text": m.group(1), "color": point_color, "emph": True})
            emphasis_budget[0] -= 1
        else:
            spans.append({"text": m.group(1), "color": base_color, "warn_extra_emph": True})
        idx = m.end()
    if idx < len(line):
        spans.append({"text": line[idx:], "color": base_color})
    return spans or [{"text": line, "color": base_color}]

# ─────────────────────────────────────────────────────────────────────────
# 3. typeset — 4축 통합. 한 카피 블록 → 렌더 플랜(줄별 size·color·align)
# ─────────────────────────────────────────────────────────────────────────
ROLE_SCALE = {"conclusion": 1.0, "intro": 0.62, "sub": 0.38}
CENTER_TONES = {"cinematic", "cover", "eod", "emotional", "slogan"}
LEFT_TONES   = {"service", "info", "logic", "editorial"}

def typeset(text, base_size, theme, tone="", warnings=None):
    if warnings is None:
        warnings = []
    lines_raw = split_clauses(text)
    budget = [1]
    emph_idx = next((i for i, l in enumerate(lines_raw) if _EMPH.search(l)), len(lines_raw) - 1)
    out_lines = []
    for i, raw in enumerate(lines_raw):
        if i == emph_idx:
            role = "conclusion"
        elif raw.startswith("(") or i > emph_idx:
            role = "sub"
        else:
            role = "intro"
        size = max(1, round(base_size * ROLE_SCALE[role]))
        spans = parse_spans(raw, theme["text"], theme["point"], budget)
        if role == "sub":
            for s in spans:
                if not s.get("emph"):
                    s["color"] = theme.get("muted", theme["text"])
        if any(s.get("warn_extra_emph") for s in spans):
            warnings.append("1블록 2강조+ 감지 → 추가 강조는 기본색으로 강등: %r" % raw)
        out_lines.append({"spans": spans, "size": size, "role": role})
    if tone in LEFT_TONES:
        align = "left"
    elif tone in CENTER_TONES:
        align = "center"
    else:
        align = "center" if len(out_lines) <= 2 else "left"
    for l in out_lines:
        l["align"] = align
    if budget[0] == 1 and len(lines_raw) > 1:
        warnings.append("강조 마크업(*..*) 없음 → 마지막 줄을 결론으로 추정. planner가 *강조* 부여 권장.")
    return {"lines": out_lines, "align": align, "warnings": warnings}

# ─────────────────────────────────────────────────────────────────────────
# 4. 폭 측정 · 헤드라인 자동 축소 (Phase 5 — 패널 비침범)
# ─────────────────────────────────────────────────────────────────────────
def _line_width(spans, font):
    return sum(font.getlength(s["text"]) for s in spans)

def fit_headline(text, font_path, max_w, theme, sizes=None, tone=""):
    if sizes is None:
        sizes = [120, 108, 96, 84, 76, 68, 60, 54, 48, 42]
    for size in sizes:
        plan = typeset(text, size, theme, tone=tone)
        widest = max(_line_width(l["spans"], ImageFont.truetype(font_path, l["size"]))
                     for l in plan["lines"])
        if widest <= max_w:
            return size, plan
    return sizes[-1], typeset(text, sizes[-1], theme, tone=tone)

# ─────────────────────────────────────────────────────────────────────────
# 5. 블록 렌더 (PIL) — 줄 폭 초과 시 size만 축소(글자 단위 재분할 금지)
# ─────────────────────────────────────────────────────────────────────────
def draw_block(draw, plan, x, y, box_w, disp_font_path, leading=1.18):
    rects, cy = [], y
    for line in plan["lines"]:
        size = line["size"]
        f = ImageFont.truetype(disp_font_path, size)
        while _line_width(line["spans"], f) > box_w and size > 12:
            size -= 2
            f = ImageFont.truetype(disp_font_path, size)
        lw = _line_width(line["spans"], f)
        if plan["align"] == "center":
            sx = x + max(0, (box_w - lw) / 2)
        else:
            sx = x
        ascent, descent = f.getmetrics()
        lh = (ascent + descent)
        px = sx
        for s in line["spans"]:
            draw.text((px, cy), s["text"], font=f, fill=s["color"])
            px += f.getlength(s["text"])
        rects.append((sx, cy, sx + lw, cy + lh))
        cy += round(lh * leading)
    return cy, rects

# ─────────────────────────────────────────────────────────────────────────
# 6. 겹침 게이트 (Phase 5 필수)
# ─────────────────────────────────────────────────────────────────────────
def _overlap(a, b, pad=0):
    ax0, ay0, ax1, ay1 = a; bx0, by0, bx1, by1 = b
    return not (ax1 <= bx0 + pad or bx1 <= ax0 + pad or
                ay1 <= by0 + pad or by1 <= ay0 + pad)

def find_overlaps(text_rects, blocker_rects, pad=2):
    hits = []
    for i, tr in enumerate(text_rects):
        for j, br in enumerate(blocker_rects):
            if _overlap(tr, br, pad):
                hits.append((i, j))
    return hits

def assert_no_overlap(text_rects, blocker_rects, label=""):
    hits = find_overlaps(text_rects, blocker_rects)
    if hits:
        raise ValueError("OVERLAP 위반%s: 텍스트가 패널/이미지와 겹침 %r"
                         % ((" ["+label+"]") if label else "", hits))
    return True

# ─────────────────────────────────────────────────────────────────────────
# 7. 카피/라벨 존재 체크 (Q2)
# ─────────────────────────────────────────────────────────────────────────
def check_copy_present(slide, page_type):
    missing = []
    if page_type in ("client", "text_hero"):
        if not (slide.get("headline") or slide.get("copy")):
            missing.append("headline/copy 비어 있음 (텍스트-주인공 페이지)")
    return missing

# ═════════════════════════════════════════════════════════════════════════
# 8. 에디토리얼 레이아웃 시스템 (4K 기본 · 이미지 합성)   _2606041330
#    좌표·폰트는 '논리(1920×1080)'로 쓰고 출력은 ×SCALE(=3840×2160).
#    REFERENCE/editorial-layout.md 의 아키타입을 코드화.
# ═════════════════════════════════════════════════════════════════════════
SCALE = 2
PW, PH = 1920, 1080            # 논리 좌표
MARGIN, GUTTER, RADIUS = 96, 48, 28

# 기본 웜 에디토리얼 테마(허쉬 리디자인 계열). 브랜드별로 덮어쓴다.
THEME_EDITORIAL = {
    "bg": "#2A0A12", "surface": "#FBF7EF", "surface_ink": "#2A0A12",
    "ink": "#F5EEE7", "muted": "#C8B6A8", "point": "#C9882F", "line": "#5A2E1A",
    # typeset 호환 키
    "text": "#F5EEE7",
}
def theme_for_typeset(theme, on_surface=False):
    """typeset()/draw_block은 text/point/muted 키를 본다. 서피스(크림) 위면 잉크색 전환."""
    if on_surface:
        return {"text": theme["surface_ink"], "point": theme["point"],
                "muted": _mix(theme["surface_ink"], theme["surface"], 0.45)}
    return {"text": theme.get("ink", theme.get("text")), "point": theme["point"],
            "muted": theme.get("muted")}

def _rgb(h):
    if isinstance(h, (tuple, list)): return tuple(h)
    h = h.lstrip("#"); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
def _mix(a, b, t):
    a, b = _rgb(a), _rgb(b); return tuple(int(a[i]*(1-t)+b[i]*t) for i in range(3))
def S(v): return int(round(v*SCALE))
def Ft(path, size): return ImageFont.truetype(path, int(size*SCALE))

def new_canvas(theme=None, bg=None):
    theme = theme or THEME_EDITORIAL
    im = Image.new("RGB", (PW*SCALE, PH*SCALE), _rgb(bg or theme["bg"]))
    return im, ImageDraw.Draw(im)

def rounded_img(im, src, box, theme, radius=RADIUS, label=""):
    """box=(x0,y0,x1,y1) 논리좌표. src 이미지 cover-fit + 라운드. 없으면 surface 플레이스홀더."""
    x0, y0, x1, y1 = [S(v) for v in box]; w, h = x1-x0, y1-y0
    if w <= 0 or h <= 0: return (box, False)
    has = bool(src) and os.path.exists(src)
    if has:
        im2 = Image.open(src).convert("RGB")
        sr = max(w/im2.width, h/im2.height)
        im2 = im2.resize((max(1, int(im2.width*sr)), max(1, int(im2.height*sr))))
        ox = (im2.width-w)//2; oy = (im2.height-h)//2
        im2 = im2.crop((ox, oy, ox+w, oy+h))
    else:
        im2 = Image.new("RGB", (w, h), _rgb(theme["surface"]))
        d2 = ImageDraw.Draw(im2)
        d2.line([(0, 0), (w, h)], fill=_mix(theme["surface"], theme["surface_ink"], .12), width=S(2))
        if label:
            f = Ft(_BODYF[0] or "", 22)
            d2.text((w//2, h//2), label, font=f, fill=_rgb(theme["muted"]), anchor="mm")
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w-1, h-1], S(radius), fill=255)
    im.paste(im2, (x0, y0), mask)
    return ((x0, y0, x1, y1), has)

_BODYF = [None]; _TITLEF = [None]
def set_fonts(title_path, body_path): _TITLEF[0] = title_path; _BODYF[0] = body_path

def eyebrow(draw, text, x, y, theme, num=None, size=22):
    """번호(있으면 굵게) + 레터스페이스 라벨. 좌측정렬 키커."""
    bf = _BODYF[0]; tf = _TITLEF[0] or _BODYF[0]
    cx = S(x)
    if num:
        nf = Ft(tf, size*1.5); draw.text((cx, S(y)-S(size*0.4)), num, font=nf, fill=_rgb(theme["point"]))
        cx += int(draw.textlength(num, font=nf)) + S(14)
    lab = " ".join(list(text)) if len(text) <= 28 else text
    f = Ft(bf, size); draw.text((cx, S(y)), lab, font=f, fill=_rgb(theme["point"]))

def footer(draw, theme, left="", right="", size=15):
    bf = _BODYF[0]; f = Ft(bf, size); col = _mix(theme["ink"], theme["bg"], .45)
    if left:  draw.text((S(MARGIN), S(PH-44)), left, font=f, fill=col)
    if right: draw.text((S(PW-MARGIN), S(PH-44)), right, font=f, fill=col, anchor="ra")

def _para(draw, text, x, y, max_w, theme, size=20, leading=1.5, color=None, muted=False):
    bf = _BODYF[0]; f = Ft(bf, size); col = _rgb(color or (theme["muted"] if muted else theme["ink"]))
    cx, cy = S(x), S(y); mw = S(max_w); out_bottom = cy
    for para in str(text).split("\n"):
        cur = ""
        for word in para.split(" "):
            t = (cur+" "+word).strip()
            if draw.textlength(t, font=f) <= mw: cur = t
            else:
                draw.text((cx, cy), cur, font=f, fill=col); a, d = f.getmetrics(); cy += int((a+d)*leading); cur = word
        draw.text((cx, cy), cur, font=f, fill=col); a, d = f.getmetrics(); cy += int((a+d)*leading)
    return cy/ SCALE

# ── 아키타입 A: 표지 분할 (텍스트 좌 / 히어로 이미지 우) ──
def cover_split(im, draw, theme, title, sub="", tags=None, hero=None, eyebrow_txt="TREATMENT"):
    tf = _TITLEF[0]
    img_x0 = PW*0.54
    rounded_img(im, hero, (img_x0, MARGIN, PW-MARGIN, PH-MARGIN), theme, label="HERO IMAGE")
    eyebrow(draw, eyebrow_txt, MARGIN, MARGIN+8, theme, size=22)
    col_w = img_x0 - MARGIN - GUTTER
    size, plan = fit_headline(title, tf, S(col_w), theme_for_typeset(theme), tone="editorial",
                              sizes=[S(v) for v in (132,118,104,92,82,72,64,56)])
    by, _ = draw_block(draw, plan, S(MARGIN), S(PH*0.30), S(col_w), tf, leading=1.06)
    if sub:
        by = _para(draw, sub, MARGIN, by/SCALE+18, col_w, theme, size=24, muted=True)
    if tags:
        f = Ft(_BODYF[0], 18); ty = S(PH-MARGIN-30); tx = S(MARGIN)
        for t in tags:
            tw = draw.textlength(t, font=f); pad = S(16)
            draw.rounded_rectangle([tx, ty, tx+tw+pad*2, ty+S(36)], S(18),
                                   outline=_rgb(theme["point"]), width=S(2))
            draw.text((tx+pad, ty+S(8)), t, font=f, fill=_rgb(theme["ink"])); tx += int(tw)+pad*2+S(14)
    footer(draw, theme, left="LSB PRODUCTION", right="AD TREATMENT")
    return im

# ── 아키타입 B: 2단 (논증 좌 / 크림 PROOF 카드 또는 이미지 우) ──
def two_col(im, draw, theme, headline, body="", eyebrow_num=None, eyebrow_txt="STRATEGY",
            proof_title="PROOF", proof_points=None, side_img=None):
    tf = _TITLEF[0]
    eyebrow(draw, eyebrow_txt, MARGIN, MARGIN+12, theme, num=eyebrow_num, size=22)
    col_w = PW*0.52 - MARGIN - GUTTER/2
    size, plan = fit_headline(headline, tf, S(col_w), theme_for_typeset(theme), tone="editorial",
                              sizes=[S(v) for v in (104,92,82,72,64,56,50)])
    by, hrects = draw_block(draw, plan, S(MARGIN), S(MARGIN+96), S(col_w), tf, leading=1.08)
    text_rects = list(hrects)
    if body:
        _para(draw, body, MARGIN, by/SCALE+24, col_w, theme, size=22, muted=True)
    rx0 = PW*0.54
    if side_img:
        box, _ = rounded_img(im, side_img, (rx0, MARGIN+40, PW-MARGIN, PH-MARGIN-40), theme, label="IMAGE")
        blocker = [box]
    else:
        card = [S(rx0), S(MARGIN+40), S(PW-MARGIN), S(PH-MARGIN-40)]
        draw.rounded_rectangle(card, S(RADIUS), fill=_rgb(theme["surface"]))
        blocker = [tuple(card)]
        f0 = Ft(_BODYF[0], 18)
        draw.text((card[0]+S(36), card[1]+S(32)), " ".join(list(proof_title)),
                  font=f0, fill=_rgb(theme["point"]))
        cy = card[1]+S(86)
        for p in (proof_points or []):
            draw.ellipse([card[0]+S(36), cy+S(10), card[0]+S(48), cy+S(22)], fill=_rgb(theme["point"]))
            fp = Ft(_BODYF[0], 23)
            _para(draw, p, (card[0])/SCALE+64, cy/SCALE, (card[2]-card[0])/SCALE-96, theme,
                  size=23, color=theme["surface_ink"])
            cy += S(64)
    footer(draw, theme, left="LSB PRODUCTION", right="AD TREATMENT")
    assert_no_overlap(text_rects, blocker, label="two_col")
    return im

# ── 아키타입 C: 풀블리드 키비주얼 + 하단 스크림 텍스트 ──
def fullbleed_kv(im, draw, theme, hero, lines=None, eyebrow_txt=None):
    rounded_img(im, hero, (0, 0, PW, PH), theme, radius=0, label="KEY VISUAL")
    # 하단 스크림
    grad = Image.new("L", (S(PW), S(PH)), 0)
    gd = ImageDraw.Draw(grad)
    for yy in range(S(int(PH*0.5)), S(PH)):
        a = int(210*(yy-S(PH*0.5))/(S(PH*0.5)))
        gd.line([(0, yy), (S(PW), yy)], fill=min(210, max(0, a)))
    black = Image.new("RGB", (S(PW), S(PH)), _rgb(theme["bg"]))
    im.paste(black, (0, 0), grad)
    if eyebrow_txt: eyebrow(draw, eyebrow_txt, MARGIN, MARGIN, theme, size=22)
    if lines:
        tf = _TITLEF[0]; cy = PH-MARGIN-len(lines)*70
        for ln in lines:
            f = Ft(tf, 64); draw.text((S(MARGIN), S(cy)), ln, font=f, fill=_rgb(theme["ink"])); cy += 70
    footer(draw, theme, right="AD TREATMENT")
    return im

# ── 아키타입 D: 컷보드 (썸네일 그리드) ──
def cut_board(im, draw, theme, title, thumbs, labels=None, cols=4, eyebrow_txt="CUT BOARD"):
    tf = _TITLEF[0]
    eyebrow(draw, eyebrow_txt, MARGIN, MARGIN, theme, size=22)
    f = Ft(tf, 56); draw.text((S(MARGIN), S(MARGIN+34)), title, font=f, fill=_rgb(theme["ink"]))
    top = MARGIN+130; n = len(thumbs); rows = (n+cols-1)//cols
    gw = (PW-2*MARGIN-(cols-1)*GUTTER)/cols; gh = gw*9/16
    avail_h = PH-MARGIN-top
    if rows*(gh+44)+ (rows-1)*GUTTER > avail_h:        # 넘치면 행 높이 축소
        gh = (avail_h-(rows)*44-(rows-1)*GUTTER)/rows; gw = gh*16/9
    lf = Ft(_BODYF[0], 17)
    for i, src in enumerate(thumbs):
        r, c = i//cols, i % cols
        x0 = MARGIN + c*(gw+GUTTER); y0 = top + r*(gh+44+GUTTER)
        rounded_img(im, src, (x0, y0, x0+gw, y0+gh), theme, radius=16, label="cut%02d" % (i+1))
        lab = (labels[i] if labels and i < len(labels) else "CUT %02d" % (i+1))
        draw.text((S(x0)+S(4), S(y0+gh)+S(10)), lab, font=lf, fill=_rgb(theme["muted"]))
    footer(draw, theme, left="LSB PRODUCTION", right="AD TREATMENT")
    return im

# ── 이미지 존재 게이트 (Phase 5 — cover/KV/board에 이미지 0장이면 보류) ──
def assert_images_present(page_kind, placed_flags, label=""):
    """page_kind in {cover,key_visual,cut_board,scene}. placed_flags=[bool,...] (rounded_img 반환의 has).
    이미지가 들어가야 할 페이지인데 실제 합성 0장이면 ValueError."""
    if page_kind in ("cover", "key_visual", "cut_board", "scene"):
        if not any(placed_flags):
            raise ValueError("IMAGE-MANDATE 위반%s: %s 페이지에 합성된 실제 이미지 0장 (플레이스홀더만)"
                             % ((" ["+label+"]") if label else "", page_kind))
    return True

def save_pdf(pages, out_path, dpi=150):
    pages = [p.convert("RGB") for p in pages]
    pages[0].save(out_path, "PDF", save_all=True, append_images=pages[1:], resolution=dpi)
    return out_path

# 자기 테스트 (python build_treatment_template.py) — 4K 아키타입 렌더
if __name__ == "__main__":
    import glob
    th = {"text": "#F4F7FB", "point": "#2EE6C8", "muted": "#9AA6B8"}
    p = typeset("무라벨은 '부족'이 아니라 // '*더 순수함*'으로", 84, th, tone="slogan")
    for l in p["lines"]:
        print(l["role"], l["size"], "".join(s["text"] for s in l["spans"]),
              "| point:", [s["text"] for s in l["spans"] if s.get("emph")])
    print("align:", p["align"], "| warnings:", p["warnings"])
    # 레이아웃 스모크 테스트(폰트 있으면)
    tf = "/sessions/blissful-exciting-carson/.fonts/NotoSansKR.ttf"
    if os.path.exists(tf):
        set_fonts(tf, tf)
        T2 = THEME_EDITORIAL; out = []
        im, d = new_canvas(T2); cover_split(im, d, T2, "폰 뒤에, *초콜릿* 한 조각.",
            sub="미니덕트 X 허쉬 맥세이프 카드지갑 스탠드", tags=["#choco","#magsafe","#No.8"], hero=None); out.append(im)
        im, d = new_canvas(T2); two_col(im, d, T2, "은유가 아니라 // *제품의 물리적 진실*",
            body="허쉬 초콜릿 바의 양각과 공식 라이선스, 형 시향지까지 제품 자체가 카피의 근거.",
            eyebrow_num="05.", eyebrow_txt="STRATEGY",
            proof_points=["4×3 초콜릿 바 양각 실루엣","공식 라이선스 콜라보 No.8","무라벨 금지·실제 패키지 고정"]); out.append(im)
        im, d = new_canvas(T2); cut_board(im, d, T2, "30초 트리트먼트 컷보드", [None]*12); out.append(im)
        save_pdf(out, "/tmp/lt_smoke.pdf")
        for i, im in enumerate(out): im.save("/tmp/lt_%d.png" % i)
        print("smoke OK -> /tmp/lt_*.png  size:", out[0].size)
