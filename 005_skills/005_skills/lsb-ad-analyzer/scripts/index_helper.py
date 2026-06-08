# -*- coding: utf-8 -*-
"""
LSB 데이터셋 카테고리 인덱스 헬퍼. (lsb-ad-analyzer_2606021505 — 전축 영문 통일 + 크로스플랫폼)

변경점:
- 모든 축의 인덱스 언어를 'en'으로 통일. (한국어/영어 혼용 분리룰 폐지)
 값 vocabulary는 lsb-treatment-builder/REFERENCE/keyword-vocabulary.md(영문 토큰 + KO 별칭) 참조.
- 경로 결합을 os.path.join으로 (Windows \\ / macOS / 양쪽 호환).
- dataset-dir는 '연결된 LSB_Ad_Datas 폴더의 절대경로'를 넘긴다. 하드코딩 금지.

사용법:
 # entry 하나 인덱스에 추가(또는 갱신)
 python3 index_helper.py update --entry "<DATASET>/entries/ADV-2026-001.json" --dataset-dir "<DATASET>"
 # 전체 재인덱싱
 python3 index_helper.py rebuild --dataset-dir "<DATASET>"
 # 다축 키워드 검색(영문 토큰)
 python3 index_helper.py search --dataset-dir "<DATASET>" --industry finance --target-demo mz --tone punchy_humor
 # 삭제 시 인덱스에서 제거
 python3 index_helper.py remove --entry-id ADV-2026-001 --dataset-dir "<DATASET>"

 <DATASET> = 사용자가 연결한 LSB_Ad_Datas 폴더의 절대경로
 (mac 예: /Users/<id>/Desktop/LSB_Ad_Datas, Win 예: C:\\Users\\<id>\\Desktop\\LSB_Ad_Datas)

각 인덱스 파일 구조:
 {
 "_meta": {"axis": "industry", "language": "en", "updated": "2026-06-02"},
 "finance": ["ADV-2026-001"],
 "automotive": ["ADV-2026-002", "ADV-2026-003"]
 }
"""

import json
import os
import sys
import argparse
import glob
from datetime import date

# search_keywords의 10개 축 (전부 영문 토큰으로 인덱싱)
AXES = [
 "industry",
 "product_category",
 "target_demo",
 "media_format",
 "tone",
 "pacing",
 "technique",
 "vfx_keywords",
 "copy_strategy_keywords",
 "concept_derivation_pattern",
]


def _idx_path(dataset_dir, axis):
 return os.path.join(dataset_dir, "index", "by_%s.json" % axis)


def _master_path(dataset_dir):
 return os.path.join(dataset_dir, "index", "master.json")


def _load_idx(dataset_dir, axis):
 path = _idx_path(dataset_dir, axis)
 if os.path.exists(path):
 with open(path, encoding="utf-8") as f:
 return json.load(f)
 return {
 "_meta": {
 "axis": axis,
 "language": "en",
 "updated": str(date.today),
 "entry_count": 0,
 }
 }


def _save_idx(dataset_dir, axis, idx):
 os.makedirs(os.path.join(dataset_dir, "index"), exist_ok=True)
 idx.setdefault("_meta", {})["axis"] = axis
 idx["_meta"]["language"] = "en"
 idx["_meta"]["updated"] = str(date.today)
 all_ids = set
 for k, v in idx.items:
 if k == "_meta":
 continue
 for eid in v:
 all_ids.add(eid)
 idx["_meta"]["entry_count"] = len(all_ids)
 with open(_idx_path(dataset_dir, axis), "w", encoding="utf-8") as f:
 json.dump(idx, f, ensure_ascii=False, indent=2, sort_keys=False)


def update_entry(entry_path, dataset_dir):
 """entry 하나를 모든 축 인덱스에 추가."""
 with open(entry_path, encoding="utf-8") as f:
 entry = json.load(f)
 eid = entry["id"]
 sk = entry.get("search_keywords", {})

 if not sk:
 print("WARN: %s에 search_keywords 없음. STEP 5.5 출력 누락." % eid)
 return

 for axis in AXES:
 values = sk.get(axis, [])
 if not values:
 continue
 if isinstance(values, str):
 values = [values]
 idx = _load_idx(dataset_dir, axis)
 for v in values:
 v = str(v).strip
 if not v:
 continue
 idx.setdefault(v, [])
 if eid not in idx[v]:
 idx[v].append(eid)
 _save_idx(dataset_dir, axis, idx)

 master_path = _master_path(dataset_dir)
 if os.path.exists(master_path):
 with open(master_path, encoding="utf-8") as f:
 master = json.load(f)
 else:
 master = {}
 sr = entry.get("source_ref", {})
 master[eid] = {
 "path": os.path.join("entries", "%s.json" % eid).replace("\\", "/"),
 "category_primary": entry.get("category_primary"),
 "brand": sr.get("brand"),
 "title": sr.get("title_or_campaign"),
 "year": sr.get("year"),
 "search_keywords": sk,
 "confidence": entry.get("inferred_creative_thinking", {}).get("confidence", "inferred"),
 }
 os.makedirs(os.path.join(dataset_dir, "index"), exist_ok=True)
 with open(master_path, "w", encoding="utf-8") as f:
 json.dump(master, f, ensure_ascii=False, indent=2)

 print("OK: %s 인덱스 갱신 (%d 축)." % (eid, len([a for a in AXES if sk.get(a)])))


def rebuild_all(dataset_dir):
 """entries/의 모든 entry로 인덱스 처음부터 재구축."""
 for axis in AXES:
 path = _idx_path(dataset_dir, axis)
 if os.path.exists(path):
 os.remove(path)
 mp = _master_path(dataset_dir)
 if os.path.exists(mp):
 os.remove(mp)

 entries = sorted(glob.glob(os.path.join(dataset_dir, "entries", "ADV-*.json")))
 print("%d개 entry 재인덱싱 중..." % len(entries))
 for ep in entries:
 update_entry(ep, dataset_dir)


def remove_entry(entry_id, dataset_dir):
 """entry ID를 모든 인덱스에서 제거."""
 for axis in AXES:
 idx = _load_idx(dataset_dir, axis)
 for k, v in idx.items:
 if k == "_meta":
 continue
 if entry_id in v:
 v.remove(entry_id)
 empty = [k for k, v in idx.items if k != "_meta" and not v]
 for k in empty:
 del idx[k]
 _save_idx(dataset_dir, axis, idx)

 master_path = _master_path(dataset_dir)
 if os.path.exists(master_path):
 with open(master_path, encoding="utf-8") as f:
 master = json.load(f)
 master.pop(entry_id, None)
 with open(master_path, "w", encoding="utf-8") as f:
 json.dump(master, f, ensure_ascii=False, indent=2)
 print("OK: %s 인덱스에서 제거." % entry_id)


def search(dataset_dir, **kwargs):
 """다축 키워드(영문 토큰)로 entry 검색. 매칭 score 높은 순.

 Returns: [(entry_id, score, hits),...] — score = 매칭 축 수
 참고: planner는 이 함수를 import하지 않아도 된다. index/by_<axis>.json을
 직접 json.load 해서 같은 매칭을 할 수 있다(인덱스는 평범한 JSON).
 """
 matches = {}
 for axis, values in kwargs.items:
 if axis not in AXES:
 continue
 if isinstance(values, str):
 values = [values]
 idx = _load_idx(dataset_dir, axis)
 for v in values:
 for eid in idx.get(v, []):
 matches.setdefault(eid, {"score": 0, "hits": {}})
 matches[eid]["score"] += 1
 matches[eid]["hits"].setdefault(axis, []).append(v)
 out = [(eid, m["score"], m["hits"]) for eid, m in matches.items]
 out.sort(key=lambda x: -x[1])
 return out


def main:
 p = argparse.ArgumentParser
 sub = p.add_subparsers(dest="cmd", required=True)

 p_up = sub.add_parser("update")
 p_up.add_argument("--entry", required=True)
 p_up.add_argument("--dataset-dir", required=True)

 p_rb = sub.add_parser("rebuild")
 p_rb.add_argument("--dataset-dir", required=True)

 p_rm = sub.add_parser("remove")
 p_rm.add_argument("--entry-id", required=True)
 p_rm.add_argument("--dataset-dir", required=True)

 p_se = sub.add_parser("search")
 p_se.add_argument("--dataset-dir", required=True)
 for axis in AXES:
 p_se.add_argument("--%s" % axis.replace("_", "-"), action="append", default=[])

 args = p.parse_args

 if args.cmd == "update":
 update_entry(args.entry, args.dataset_dir)
 elif args.cmd == "rebuild":
 rebuild_all(args.dataset_dir)
 elif args.cmd == "remove":
 remove_entry(args.entry_id, args.dataset_dir)
 elif args.cmd == "search":
 kwargs = {}
 for axis in AXES:
 v = getattr(args, axis)
 if v:
 kwargs[axis] = v
 results = search(args.dataset_dir, **kwargs)
 print("매칭 entry %d개:" % len(results))
 for eid, score, hits in results[:20]:
 print(" [%d] %s hits=%s" % (score, eid, hits))


if __name__ == "__main__":
 main
