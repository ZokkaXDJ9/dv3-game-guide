"""Fill Dragon ability descriptions from local English translation tables."""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--tables", type=Path, required=True, help="Decoded 1.0.18 static table directory")
parser.add_argument("--lang", type=Path, required=True, help="English lang_en.lua from the local research corpus")
args = parser.parse_args()

def rows(name):
    raw = json.loads((args.tables / f"{name}.dat.json").read_text(encoding="utf-8"))["tables"][0]["rows"]
    return [dict(zip(raw[0], row)) for row in raw[1:]]

def lua_unescape(text):
    return re.sub(r"\\([\\'\"nrt])", lambda m: {"n": "\n", "r": "\r", "t": "\t"}.get(m.group(1), m.group(1)), text)

translations = {}
for path in (args.lang, args.lang.with_name("lang_en_patch.lua")):
    raw = path.read_text(encoding="utf-8")
    for key, value in re.findall(r"\['((?:\\.|[^'])*)'\]\s*=\s*'((?:\\.|[^'])*)'", raw):
        translations[lua_unescape(key)] = lua_unescape(value)

ability_by_id = {a["id"]: a for a in rows("table_ability")}
dragon_ability = {d["id"]: d.get("ability", "") for d in rows("table_dragon")}
catalog_path = ROOT / "data" / "catalog-data.js"
text = catalog_path.read_text(encoding="utf-8")
prefix = "window.GAME_CATALOG"
if not text.startswith(prefix):
    raise ValueError("catalog-data.js does not start with window.GAME_CATALOG")
payload = text[len(prefix):].strip()
if payload.startswith("="):
    payload = payload[1:].strip()
catalog = json.loads(payload.strip().rstrip(";"))
resolved = 0
for dragon in catalog["dragons"]:
    ability = ability_by_id.get(dragon_ability.get(dragon["id"], ""))
    if not ability:
        continue
    description = translations.get(ability.get("t_desc", ""))
    if not description:
        continue
    description = re.sub(r"\{@#;[^}]+\}", "", description)
    description = description.replace("{@}", "")
    dragon["ability"]["description"] = description
    resolved += 1
catalog_path.write_text(prefix + " = " + json.dumps(catalog, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
print(f"Added English ability descriptions for {resolved} Dragons")
