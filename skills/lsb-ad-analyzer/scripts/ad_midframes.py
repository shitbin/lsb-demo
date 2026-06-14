# -*- coding: utf-8 -*-
"""컷별 '중간 프레임'을 데이터셋에 보존 + 라벨드 컨택트시트 생성.

목적: 다른 세션(=다른 Claude)이 텍스트 라벨만으로는 이해 못 하는
      '한 프레임 안의 분할/멀티패널/필름스트립 레이아웃'을 실제 이미지로 보고 참고하게 한다.

입력은 이미 추출해 둔 frames/allframes/ (원본 해상도 전 프레임)와 확정된 컷 경계다.
allframes에서 각 컷의 '가운데 프레임'을 골라 복사하므로 추가 디코딩/행걸림이 없다.

usage:
  python ad_midframes.py --allframes <frames/allframes> --fps <FPS> \
      --cuts "0:1.3,1.3:3.0,3.0:5.2,..."  --out <DATASET>/entries/ADV-YYYY-NNN_frames \
      [--id ADV-YYYY-NNN] [--cols 4]
  # --cuts 가 없으면 allframes 개수를 N등분(균등) 폴백.
"""
import argparse, os, glob, shutil, json, math
from PIL import Image, ImageDraw, ImageFont

FONT = "/sessions/blissful-exciting-carson/.fonts/NotoSansKR.ttf"

def list_frames(d):
    return sorted(glob.glob(os.path.join(d, "*.png")) + glob.glob(os.path.join(d, "*.jpg")))

def parse_cuts(s, fps, nframes):
    cuts = []
    if s:
        for i, seg in enumerate([x for x in s.split(",") if x.strip()]):
            a, b = seg.split(":"); cuts.append((i + 1, float(a), float(b)))
    else:
        dur = nframes / fps; n = max(6, int(dur // 2)); step = dur / n
        cuts = [(i + 1, i * step, (i + 1) * step) for i in range(n)]
    return cuts

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--allframes", required=True)
    ap.add_argument("--fps", type=float, required=True)
    ap.add_argument("--cuts", default="")
    ap.add_argument("--out", required=True)
    ap.add_argument("--id", default="ADV")
    ap.add_argument("--cols", type=int, default=4)
    a = ap.parse_args()

    frames = list_frames(a.allframes)
    if not frames:
        raise SystemExit("no frames in %s" % a.allframes)
    n = len(frames)
    os.makedirs(a.out, exist_ok=True)
    cuts = parse_cuts(a.cuts, a.fps, n)

    mids = []
    for idx, s, e in cuts:
        mid_t = (s + e) / 2.0
        fi = min(n - 1, max(0, int(round(mid_t * a.fps))))   # 중간 시점 → 프레임 인덱스
        src = frames[fi]
        dst = os.path.join(a.out, "cut%02d_mid.png" % idx)
        shutil.copyfile(src, dst)
        mids.append((idx, s, e, mid_t, os.path.basename(dst)))

    # 라벨드 컨택트시트 (분할 레이아웃을 한눈에)
    cols = a.cols; tw = 460
    im0 = Image.open(os.path.join(a.out, mids[0][4])); th = int(tw * im0.height / im0.width)
    pad = 12; lab = 30; rows = math.ceil(len(mids) / cols)
    sheet = Image.new("RGB", (cols * (tw + pad) + pad, rows * (th + lab + pad) + pad), (24, 26, 30))
    d = ImageDraw.Draw(sheet)
    try: f = ImageFont.truetype(FONT, 22)
    except Exception: f = ImageFont.load_default()
    for k, (idx, s, e, mid_t, name) in enumerate(mids):
        r = k // cols; c = k % cols; x = pad + c * (tw + pad); y = pad + r * (th + lab + pad)
        im = Image.open(os.path.join(a.out, name)).convert("RGB").resize((tw, th)); sheet.paste(im, (x, y + lab))
        d.text((x + 4, y + 4), "cut%02d  %.2f-%.2fs" % (idx, s, e), font=f, fill=(120, 210, 255))
    cs = os.path.join(a.out, "contact_sheet.png"); sheet.save(cs)

    json.dump({"id": a.id, "fps": a.fps, "frame_count": n, "cut_count": len(mids),
               "contact_sheet": "contact_sheet.png",
               "cuts": [{"index": i, "start": round(s, 3), "end": round(e, 3),
                         "mid_sec": round(m, 3), "mid_frame": nm} for i, s, e, m, nm in mids]},
              open(os.path.join(a.out, "frames_index.json"), "w"), ensure_ascii=False, indent=2)
    print("OK mids=%d -> %s" % (len(mids), a.out))
    print("contact_sheet:", cs)

if __name__ == "__main__":
    main()
