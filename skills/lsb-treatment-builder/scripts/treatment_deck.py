# -*- coding: utf-8 -*-
"""
treatment_deck.py - LSB cinematic treatment-deck builder (merged _2606140000)
=============================================================================
Reverse-engineered from 35 real studio decks in the reference folder (Yangban Kim,
Woori Bank, Air Force, KT, LG, KG, Ministry of Health, Shinsegae, Baemin, KT-Y, etc.).
Single source of truth for the rules: REFERENCE/treatment-deck-system.md.

Three hard laws (do not break - the director's repeated complaints):
  1. IMAGE RATIO: keep every image's ORIGINAL aspect ratio. `place_image(mode="auto")`
     letterboxes when the source ratio differs from the cell (>8%); only crops when they
     already match. Reference photos = always contain. Storyboard cells = set the cell to
     the cut's own ratio so "cover" never actually crops. Never squeeze a portrait into a
     landscape cell.
  2. POINT COLOR: derive ONE accent from the brand's primary color (theme_from_brand);
     never hardcode. Apply it to text / thin lines / one keyword only - never as a filled
     box behind text.
  3. NO TEXT BOX: text sits directly on the dark (or light) page, or on a full-bleed image
     via a gradient scrim. No filled cream/tinted card behind copy. Ever.

Archetypes: cover_film, cover_type, section_divider, concept_headline, narration_still,
            mood_board, scene_hero, scene_cluster, storyboard_grid, option_ab, closing
            (+ save_pdf). Canvas 16:9 4K (3840x2160 = logical 1920x1080 x SCALE2).
Deps: Pillow. Fonts: display(Black Han Sans), body(Noto Sans KR), serif(Noto Serif CJK).
"""
import os
from PIL import Image, ImageDraw, ImageFont

SCALE = 2
PW, PH = 1920, 1080
MARGIN = 110
PAGE_AR = PW / PH

# Default dark-cinematic theme. Overwritten per brand via theme_from_brand(). No cream surface.
THEME = {
    "bg": "#0E0B09", "panel": "#16110D", "ink": "#F3ECE3", "muted": "#9C8E80",
    "point": "#FFC72C", "accent2": "#DA291C", "line": "#3A2A1E",
    "wordmark": "LSB PRODUCTION", "domain": "lsbproduction.com",
}

# Tone presets pick the BASE (dark vs light) and default ink. The POINT color still comes
# from the brand. See REFERENCE/treatment-deck-system.md section "Tone profiles".
TONE_PRESETS = {
    "cinematic":       {"bg": "#0E0B09", "ink": "#F3ECE3"},  # premium / emotional / film (default)
    "editorial_light": {"bg": "#FFFFFF", "ink": "#1A1A1A"},  # strategy / clean / airy
    "service":         {"bg": "#FFFFFF", "ink": "#161616"},  # friendly / consumer service
    "luxury":          {"bg": "#1A2030", "ink": "#EDE8DE"},  # fashion / premium
    "public":          {"bg": "#FFFFFF", "ink": "#1F1F1F"},  # gov / public-interest / documentary
    "brand_immersive": {"bg": "#000000", "ink": "#F2F2F2"},  # brand-world (e.g. telecom)
}

def _rgb(h):
    if isinstance(h, (tuple, list)): return tuple(h)
    h = h.lstrip("#"); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
def _hex(t): return "#%02X%02X%02X" % tuple(t)
def _mix(a, b, t): a, b = _rgb(a), _rgb(b); return tuple(int(a[i]*(1-t)+b[i]*t) for i in range(3))
def _lum(h):
    r, g, b = _rgb(h); return (0.299*r + 0.587*g + 0.114*b) / 255
def S(v): return int(round(v*SCALE))

def theme_from_brand(brand_hex=None, tone="cinematic", accent2=None, genre_accent=None):
    """Build a theme from the brand's primary color (LAW 2). `tone` sets the base/ink.
       Point = brand color, lifted for contrast against the base; falls back to genre color,
       then to the tone default. Point is used for text/lines only, never filled boxes."""
    pre = TONE_PRESETS.get(tone, TONE_PRESETS["cinematic"])
    th = dict(THEME); th.update(pre)
    is_dark = _lum(th["bg"]) < 0.5
    point = brand_hex or genre_accent
    if point:
        if is_dark and _lum(point) < 0.20:  point = _hex(_mix(point, "#FFFFFF", 0.40))  # lift on dark
        if (not is_dark) and _lum(point) > 0.80: point = _hex(_mix(point, "#000000", 0.40))  # deepen on light
        th["point"] = point
    th["accent2"] = accent2 or th["point"]
    th["panel"] = _hex(_mix(th["bg"], th["ink"], 0.06))   # non-text placeholder face (base-tinted)
    th["line"]  = _hex(_mix(th["bg"], th["ink"], 0.20))
    th["muted"] = _hex(_mix(th["ink"], th["bg"], 0.42))
    return th

def brand_theme(point, accent2=None, bg="#0E0B09", ink="#F3ECE3"):
    """Back-compat shim. Prefer theme_from_brand()."""
    t = dict(THEME); t.update(bg=bg, point=point, accent2=accent2 or point, ink=ink)
    t["panel"] = _hex(_mix(bg, ink, 0.06)); t["line"] = _hex(_mix(bg, ink, 0.20)); t["muted"] = _hex(_mix(ink, bg, 0.42))
    return t

_F = {}; _FONTS = {"display": None, "body": None, "serif": None}
def set_fonts(display, body, serif=None):
    _FONTS["display"], _FONTS["body"], _FONTS["serif"] = display, body, serif or body
def Ft(kind, size):
    p = _FONTS.get(kind) or _FONTS["body"]; k = (p, int(size*SCALE))
    if k not in _F: _F[k] = ImageFont.truetype(p, int(size*SCALE))
    return _F[k]
def new_canvas(theme=None):
    th = theme or THEME; im = Image.new("RGB", (PW*SCALE, PH*SCALE), _rgb(th["bg"]))
    return im, ImageDraw.Draw(im)

# ===== IMAGE PLACEMENT (LAW 1) =====
def place_image(im, src, box, theme, mode="auto", radius=0, dim=0.0, label="", tol=0.08):
    """mode: 'auto' (cover only if source ratio within tol of cell, else contain/letterbox),
       'contain' (always preserve ratio, letterbox on base color),
       'cover' (fill; use only for full-bleed KV where some crop is acceptable).
       radius/shadow default 0 (clean rect like the reference decks)."""
    x0, y0, x1, y1 = [S(v) for v in box]; w, h = x1-x0, y1-y0
    if w <= 0 or h <= 0: return False
    has = bool(src) and os.path.exists(src)
    if has:
        s = Image.open(src).convert("RGB")
        cell_ar, img_ar = w/h, s.width/s.height; m = mode
        if m == "fit":  m = "contain"     # alias (THE IMAGE LAW wording uses fit/fill)
        if m == "fill": m = "cover"       # alias
        if m == "auto": m = "cover" if abs(cell_ar-img_ar)/cell_ar <= tol else "contain"
        if m == "contain":
            r = min(w/s.width, h/s.height); nw, nh = max(1, int(s.width*r)), max(1, int(s.height*r))
            s = s.resize((nw, nh)); cell = Image.new("RGB", (w, h), _rgb(theme["bg"]))
            cell.paste(s, ((w-nw)//2, (h-nh)//2))
        else:
            r = max(w/s.width, h/s.height); s = s.resize((max(1, int(s.width*r)), max(1, int(s.height*r))))
            ox, oy = (s.width-w)//2, (s.height-h)//2; cell = s.crop((ox, oy, ox+w, oy+h))
        if dim > 0: cell = Image.blend(cell, Image.new("RGB", (w, h), _rgb(theme["bg"])), dim)
    else:
        cell = Image.new("RGB", (w, h), _rgb(theme["panel"])); d2 = ImageDraw.Draw(cell)
        d2.line([(0, 0), (w, h)], fill=_mix(theme["panel"], theme["ink"], .10), width=S(2))
        if label: d2.text((w//2, h//2), label, font=Ft("body", 18), fill=_rgb(theme["muted"]), anchor="mm")
    if radius > 0:
        mask = Image.new("L", (w, h), 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, w-1, h-1], S(radius), fill=255)
        im.paste(cell, (x0, y0), mask)
    else: im.paste(cell, (x0, y0))
    return has

def _scrim(im, theme, top_frac=0.5, strength=205):
    g = Image.new("L", (PW*SCALE, PH*SCALE), 0); gd = ImageDraw.Draw(g); y0 = int(PH*SCALE*top_frac)
    for yy in range(y0, PH*SCALE):
        gd.line([(0, yy), (PW*SCALE, yy)], fill=min(strength, int(strength*(yy-y0)/(PH*SCALE-y0))))
    im.paste(Image.new("RGB", im.size, _rgb(theme["bg"])), (0, 0), g)

def _vtext(im, theme, text, x_logical, col=None):
    f = Ft("body", 12); tmp = Image.new("RGBA", (S(420), S(18)), (0, 0, 0, 0))
    ImageDraw.Draw(tmp).text((0, 0), text, font=f, fill=(col or _mix(theme["ink"], theme["bg"], .58))+(255,))
    tmp = tmp.rotate(90, expand=True); im.paste(tmp, (S(x_logical), S(PH//2)-tmp.height//2), tmp)

def furniture(draw, theme, page=None, foot_left=None):
    """Edge furniture: left vertical = domain, right vertical = copyright, footer = wordmark + page."""
    im = draw._image
    _vtext(im, theme, theme.get("domain", ""), 30)
    _vtext(im, theme, "(c) 2026 LSB PRODUCTION. ALL RIGHTS RESERVED.", PW-44)
    f = Ft("body", 13); col = _mix(theme["ink"], theme["bg"], .5)
    draw.text((S(MARGIN), S(PH-40)), foot_left or theme.get("wordmark", "LSB PRODUCTION"), font=f, fill=col)
    if page is not None:
        draw.text((S(PW-MARGIN), S(PH-40)), str(page), font=f, fill=col, anchor="ra")

def eyebrow(draw, theme, text, x=MARGIN, y=58, point=True):
    draw.text((S(x), S(y)), " ".join(list(text)) if len(text) <= 30 else text,
              font=Ft("body", 14), fill=_rgb(theme["point"] if point else theme["muted"]))

def center_title(draw, theme, text, y, accent=None, size=30, font="display"):
    f = Ft(font, size)
    if accent and accent in text:
        i = text.index(accent); parts = [(text[:i], theme["ink"]), (accent, theme["point"]), (text[i+len(accent):], theme["ink"])]
    else: parts = [(text, theme["ink"])]
    total = sum(draw.textlength(t, font=f) for t, _ in parts); x = S(PW//2)-total/2
    for t, col in parts: draw.text((x, S(y)), t, font=f, fill=_rgb(col)); x += draw.textlength(t, font=f)

def _wrap(draw, text, font, max_w):
    out, cur = [], ""
    for ch in str(text):
        if draw.textlength(cur+ch, font=font) <= max_w: cur += ch
        else: out.append(cur); cur = ch
    if cur: out.append(cur)
    return out

# ===== ARCHETYPES =====
def cover_film(im, draw, theme, hero, title_ko, title_en="", date="", eyebrow_txt="AD TREATMENT"):
    place_image(im, hero, (0, 0, PW, PH), theme, mode="cover", label="KEY VISUAL")
    _scrim(im, theme, 0.42, 200)
    if eyebrow_txt: eyebrow(draw, theme, eyebrow_txt)
    center_title(draw, theme, title_ko, PH-205, size=64)
    if title_en: draw.text((S(PW//2), S(PH-120)), title_en, font=Ft("serif", 28), fill=_rgb(theme["muted"]), anchor="mm")
    if date: draw.text((S(PW//2), S(PH-82)), date, font=Ft("body", 15), fill=_mix(theme["ink"], theme["bg"], .4), anchor="mm")
    furniture(draw, theme); return im

def cover_type(im, draw, theme, word, sub="", info=None):
    im.paste(Image.new("RGB", im.size, _rgb(theme["accent2"])), (0, 0))
    layer = Image.new("RGBA", (S(PW), S(PH)), (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
    wf = Ft("display", 230); ld.text((S(110), S(PH//2)), word, font=wf, fill=_rgb(theme["ink"])+(255,), anchor="lm")
    layer = layer.rotate(-8, center=(S(PW//2), S(PH//2)), resample=Image.BICUBIC); im.paste(layer, (0, 0), layer)
    if sub: draw.text((S(MARGIN), S(PH-150)), sub, font=Ft("serif", 30), fill=_rgb(theme["ink"]))
    furniture(draw, theme); return im

def section_divider(im, draw, theme, label, big_letter=None, on_brand=True):
    if on_brand: im.paste(Image.new("RGB", im.size, _rgb(theme["accent2"])), (0, 0))
    if big_letter:
        draw.text((S(PW//2), S(PH//2)-S(20)), big_letter, font=Ft("display", 300), fill=_rgb(theme["ink"]), anchor="mm")
        draw.text((S(PW//2), S(PH//2)+S(150)), label, font=Ft("serif", 28), fill=_rgb(theme["ink"]), anchor="mm")
    else:
        draw.text((S(PW//2), S(PH//2)), label, font=Ft("display", 60), fill=_rgb(theme["ink"]), anchor="mm")
        w = draw.textlength(label, font=Ft("display", 60))
        draw.line([(S(PW//2)-w/2, S(PH//2)+S(52)), (S(PW//2)+w/2, S(PH//2)+S(52))], fill=_rgb(theme["ink"]), width=S(2))
    furniture(draw, theme); return im

def concept_headline(im, draw, theme, head, eyebrow_txt="Concept.", sub="", on_brand=True):
    if on_brand: im.paste(Image.new("RGB", im.size, _rgb(theme["accent2"])), (0, 0))
    draw.text((S(MARGIN), S(PH*0.30)), eyebrow_txt, font=Ft("serif", 36), fill=_rgb(theme["ink"]))
    f = Ft("display", 110)
    for i, ln in enumerate(str(head).split("//")):
        draw.text((S(MARGIN), S(PH*0.30)+S(60)+i*S(120)), ln.strip(), font=f, fill=_rgb(theme["ink"]))
    if sub: draw.text((S(MARGIN), S(PH-150)), sub, font=Ft("body", 24), fill=_mix(theme["ink"], theme["bg"], .25))
    furniture(draw, theme); return im

def narration_still(im, draw, theme, hero, sec_no, sec_title, paras):
    place_image(im, hero, (0, 0, PW, PH), theme, mode="cover", dim=0.58, label="CONCEPT")
    draw.text((S(MARGIN), S(58)), "%s  %s" % (sec_no, sec_title), font=Ft("body", 18), fill=_rgb(theme["point"]))
    f = Ft("serif", 27); lh = int(f.size*1.7); mw = S(PW-2*MARGIN-S(120)); lines = []
    for p in paras: lines += _wrap(draw, p, f, mw)+[""]
    cy = S(PH//2)-len(lines)*lh//2
    for ln in lines: draw.text((S(PW//2), cy), ln, font=f, fill=_rgb(theme["ink"]), anchor="ma"); cy += lh
    furniture(draw, theme); return im

def mood_board(im, draw, theme, title, images, captions=None, takeaway="", cols=3):
    eyebrow(draw, theme, title, point=True)
    n = len(images); rows = (n+cols-1)//cols; gap = 22; top = 130; bot = 150
    gw = (PW-2*MARGIN-(cols-1)*gap)/cols; gh = (PH-top-bot-(rows-1)*gap)/rows
    for i, src in enumerate(images):
        r, c = divmod(i, cols); x0 = MARGIN+c*(gw+gap); y0 = top+r*(gh+gap)
        place_image(im, src, (x0, y0, x0+gw, y0+gh), theme, mode="contain", label="ref")  # references keep original ratio
        if captions and i < len(captions) and captions[i]:
            draw.text((S(x0), S(y0+gh)+S(6)), captions[i][:36], font=Ft("body", 13), fill=_rgb(theme["muted"]))
    if takeaway: draw.text((S(PW//2), S(PH-86)), ">>  "+takeaway, font=Ft("serif", 26), fill=_rgb(theme["ink"]), anchor="mm")
    furniture(draw, theme); return im

def scene_hero(im, draw, theme, page, title, desc, hero, accent=None, bottom=None):
    center_title(draw, theme, title, 96, accent=accent, size=30)
    if desc: draw.text((S(PW//2), S(142)), desc, font=Ft("body", 17), fill=_rgb(theme["muted"]), anchor="mm")
    place_image(im, hero, (MARGIN+90, 200, PW-MARGIN-90, PH-170), theme, mode="contain", label="scene")  # single hero = letterbox
    if bottom: draw.text((S(PW//2), S(PH-92)), bottom, font=Ft("serif", 24), fill=_mix(theme["ink"], theme["bg"], .22), anchor="mm")
    furniture(draw, theme, page=page); return im

def scene_cluster(im, draw, theme, page, title, desc, hero, supports, accent=None):
    center_title(draw, theme, title, 96, accent=accent, size=30)
    if desc: draw.text((S(MARGIN), S(160)), desc, font=Ft("body", 16), fill=_rgb(theme["muted"]))
    place_image(im, hero, (MARGIN, 205, PW*0.66, PH-150), theme, mode="auto", label="main")
    sx = PW*0.66+22; nn = max(1, len(supports)); sh = (PH-150-205-(nn-1)*18)/nn
    for i, s in enumerate(supports):
        y0 = 205+i*(sh+18); place_image(im, s, (sx, y0, PW-MARGIN, y0+sh), theme, mode="auto", label="sub")
    furniture(draw, theme, page=page); return im

def storyboard_grid(im, draw, theme, sec_no, sec_title, seq, cuts, cols=4, vertical=False):
    """cuts=[{img,no,tc,cap,ref(bool)}]. vertical=True -> 9:16 cells. Cells are set to the cut
       ratio so 'auto' never crops. Set vertical to match the campaign's aspect ratio.
       The grid is CENTERED horizontally (each row by its own item count) and vertically
       balanced in the available band — never left-pinned with dead space on the right."""
    draw.text((S(MARGIN), S(54)), "%s  %s" % (sec_no, sec_title), font=Ft("body", 22), fill=_rgb(theme["ink"]))
    if seq: draw.text((S(MARGIN), S(92)), seq, font=Ft("body", 15), fill=_rgb(theme["muted"]))
    n = len(cuts); rows = (n+cols-1)//cols; gap = 18; cap_h = 66
    head_y, foot_y = 140, PH-72; avail = foot_y-head_y
    gw = (PW-2*MARGIN-(cols-1)*gap)/cols; gh = gw*(16/9) if vertical else gw*(9/16)
    if rows*(gh+cap_h)+(rows-1)*gap > avail:                       # height clamp -> gw shrinks
        gh = (avail-rows*cap_h-(rows-1)*gap)/rows; gw = gh*(9/16) if vertical else gh*(16/9)
    block_h = rows*(gh+cap_h)+(rows-1)*gap
    top = head_y + max(0, (avail-block_h)/2)                       # vertical centering
    for i, cut in enumerate(cuts):
        r, c = divmod(i, cols)
        in_row = min(cols, n-r*cols)                               # items in THIS row
        row_w = in_row*gw+(in_row-1)*gap
        x_off = (PW-row_w)/2                                       # horizontal centering (per row)
        x0 = x_off+c*(gw+gap); y0 = top+r*(gh+cap_h+gap)
        place_image(im, cut.get("img"), (x0, y0, x0+gw, y0+gh), theme, mode="auto", label="cut")
        bw = S(50) if len(str(cut.get("no", i+1))) <= 2 else S(64)
        draw.rectangle([S(x0), S(y0), S(x0)+bw, S(y0)+S(30)], fill=_rgb(theme["point"]))
        draw.text((S(x0)+S(8), S(y0)+S(3)), "#"+str(cut.get("no", i+1)), font=Ft("display", 18), fill=_rgb(theme["bg"]))
        if cut.get("ref"):
            draw.rectangle([S(x0+gw)-S(58), S(y0), S(x0+gw), S(y0)+S(26)], fill=_rgb(theme["accent2"]))
            draw.text((S(x0+gw)-S(50), S(y0)+S(4)), "REF", font=Ft("body", 14), fill=_rgb(theme["ink"]))
        ty = S(y0+gh)+S(9)
        if cut.get("tc"): draw.text((S(x0), ty), cut["tc"], font=Ft("serif", 16), fill=_rgb(theme["muted"]))
        if cut.get("cap"):
            for j, ln in enumerate(_wrap(draw, cut["cap"], Ft("body", 16), S(gw))[:2]):
                draw.text((S(x0), ty+S(22)+j*S(21)), ln, font=Ft("body", 16), fill=_mix(theme["ink"], theme["bg"], .15))
    furniture(draw, theme); return im

def cut_board(im, draw, theme, page, eyebrow_txt, cuts, accent=None):
    """Detailed cut board — up to 2 cuts per page. Each cut:
       {img, no, name, scene, vo}. Each card's WIDTH is derived from the image's own aspect
       ratio at a fixed height (so the image fills the card with NO crop — original ratio law),
       the cards are centered as a group, and the number chip + caption block (scene name in
       point color, 장면 / V.O at a readable type scale) pin to each card's left edge.
       Fixes the prior 'tiny captions, top-heavy, image/chip misaligned' pages."""
    eyebrow(draw, theme, eyebrow_txt or "CUT BOARD", point=True)
    cuts = cuts[:2]; n = max(1, len(cuts)); colgap = 96
    img_h = PH*0.54; max_w = (PW-2*MARGIN-(n-1)*colgap)/n
    # derive each card's width from its image ratio (fallback to vertical 9:16)
    cards = []
    for cut in cuts:
        src = cut.get("img"); ar = 9/16
        if src and os.path.exists(src):
            try:
                from PIL import Image as _I
                w, h = _I.open(src).size; ar = w/h
            except Exception: pass
        cw = min(max_w, img_h*ar); cards.append((cut, cw))
    group_w = sum(cw for _, cw in cards)+(n-1)*colgap
    head_y, foot_y = 132, PH-70
    cap_block_h = 156
    top = head_y + max(0, ((foot_y-head_y)-(img_h+34+cap_block_h))/2)   # vertical balance
    x = (PW-group_w)/2                                                  # center the card group
    point = _rgb(theme["point"]); ink = _rgb(theme["ink"]); muted = _rgb(theme["muted"])
    for cut, cw in cards:
        place_image(im, cut.get("img"), (x, top, x+cw, top+img_h), theme, mode="cover", label="cut")
        no = str(cut.get("no", 1)); bw = S(50) if len(no) <= 2 else S(64)
        draw.rectangle([S(x), S(top), S(x)+bw, S(top)+S(30)], fill=point)
        draw.text((S(x)+S(8), S(top)+S(3)), "#"+no, font=Ft("display", 18), fill=_rgb(theme["bg"]))
        cy = top+img_h+34
        if cut.get("name"):
            draw.text((S(x), S(cy)), cut["name"], font=Ft("display", 30), fill=point); cy += 48
        if cut.get("scene"):
            for ln in _wrap(draw, "장면 · "+cut["scene"], Ft("body", 20), S(cw))[:3]:
                draw.text((S(x), S(cy)), ln, font=Ft("body", 20), fill=ink); cy += 31
        if cut.get("vo"):
            cy += 4
            for ln in _wrap(draw, "V.O · "+cut["vo"], Ft("body", 20), S(cw))[:2]:
                draw.text((S(x), S(cy)), ln, font=Ft("body", 20), fill=muted); cy += 31
        x += cw+colgap
    furniture(draw, theme, page=page); return im

def option_ab(im, draw, theme, title, a_img, b_img, a_label="A", b_label="B (rec)", a_cap="", b_cap=""):
    center_title(draw, theme, title, 70, size=30)
    half = (PW-2*MARGIN-60)/2
    for k, (src, lab, cap) in enumerate([(a_img, a_label, a_cap), (b_img, b_label, b_cap)]):
        x0 = MARGIN+k*(half+60)
        place_image(im, src, (x0, 180, x0+half, PH-200), theme, mode="contain", label=lab)
        draw.text((S(x0), S(PH-180)), lab, font=Ft("display", 26), fill=_rgb(theme["point"] if "rec" in lab.lower() else theme["ink"]))
        if cap: draw.text((S(x0), S(PH-138)), cap, font=Ft("body", 16), fill=_rgb(theme["muted"]))
    furniture(draw, theme); return im

def closing(im, draw, theme, word="E.O.D", sub="", on_brand=True):
    if on_brand: im.paste(Image.new("RGB", im.size, _rgb(theme["accent2"])), (0, 0))
    center_title(draw, theme, word, PH//2-60, size=104)
    if sub: draw.text((S(PW//2), S(PH//2)+S(64)), sub, font=Ft("serif", 28), fill=_mix(theme["ink"], theme["bg"], .15), anchor="mm")
    furniture(draw, theme); return im

# ===== GATES & SAVE =====
def assert_images_present(placed_flags, page_kind=""):
    if not any(placed_flags):
        raise RuntimeError("IMAGE MANDATE: 0 real images on '%s' page - halt build (do not fill with vectors/cream)." % page_kind)

def save_pdf(pages, out_path, dpi=150):
    pages = [p.convert("RGB") for p in pages]
    pages[0].save(out_path, "PDF", save_all=True, append_images=pages[1:], resolution=dpi)
    return out_path
