"""Build the static stage reference from decoded DV3 1.0.18 tables."""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--tables", type=Path, required=True, help="Directory containing decoded table_*.dat.json files")
parser.add_argument("--lang", type=Path, required=True, help="English lang_en.lua from the local research corpus")
args = parser.parse_args()
TABLES = args.tables
LANG = args.lang

def read_table(name):
    payload = json.loads((TABLES / f"{name}.dat.json").read_text(encoding="utf-8"))
    rows = payload["tables"][0]["rows"]
    return [dict(zip(rows[0], row)) for row in rows[1:]]

def unescape_lua(value):
    return re.sub(r"\\([\\'\"nrt])", lambda m: {"n": "\n", "r": "\r", "t": "\t"}.get(m.group(1), m.group(1)), value)

translations = {}
for file in [LANG, LANG.with_name("lang_en_patch.lua")]:
    text = file.read_text(encoding="utf-8")
    for key, value in re.findall(r"\['((?:\\.|[^'])*)'\]\s*=\s*'((?:\\.|[^'])*)'", text):
        translations[unescape_lua(key)] = unescape_lua(value)

def translated(value, fallback):
    return translations.get(value, fallback)

zones = read_table("table_expedition_zone")
zone_names = {z["id"]: translated(z["t_name"], f"Expedition {z['idx']}") for z in zones}
expedition = []
for row in read_table("table_expedition_zone_stage"):
    enemies = []
    for i in range(1, 4):
        if row.get(f"enemy_id_{i}"):
            raw = row.get(f"r_name_{i}", "")
            enemies.append({"id": row[f"enemy_id_{i}"], "name": translated(raw, f"Enemy {i}"), "level": row.get(f"r_lv_{i}", "")})
    expedition.append({"id": row["id"], "zoneId": row["epd_id"], "zone": zone_names.get(row["epd_id"], "Expedition"), "stage": row["stage"], "name": translated(row.get("r_stage_name", ""), f"Stage {row['stage']}"), "stamina": row.get("stamina", ""), "power": row.get("std_power", ""), "enemies": enemies, "firstReward": row.get("first_clear_reward", "")})

dungeon_zones = read_table("table_dungeon_zone")
dungeon_names = {d["dungeon_id"]: translated(d.get("r_zone", ""), f"Dungeon {d.get('r_zone', '')}") for d in dungeon_zones}
dungeon_meta = {d["dungeon_id"]: d for d in dungeon_zones}
dungeon_groups = {}
for row in read_table("table_dungeon_zone_stage"):
    key = (row["dungeon_id"], row["stage"])
    item = dungeon_groups.setdefault(key, {"id": f"{row['dungeon_id']}-{row['stage']}", "zoneId": row["dungeon_id"], "zone": dungeon_names.get(row["dungeon_id"], "Dungeon"), "stage": row["stage"], "levelName": translated(dungeon_meta[row["dungeon_id"]].get("t_level_name", ""), ""), "power": dungeon_meta[row["dungeon_id"]].get("std_power", ""), "stamina": dungeon_meta[row["dungeon_id"]].get("stamina", ""), "enemies": []})
    item["enemies"].append({"id": row.get("enemy_id", ""), "name": translated(row.get("r_name", ""), "Enemy"), "level": row.get("r_lv", "")})
dungeons = sorted(dungeon_groups.values(), key=lambda x: (x["zone"], int(x["stage"])))

out = {"version": "1.0.18", "expeditions": expedition, "dungeons": dungeons}
(ROOT / "data" / "stage-data.js").write_text("window.STAGE_DATA = " + json.dumps(out, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
print(f"Wrote {len(expedition)} Expedition stages and {len(dungeons)} Dungeon stage groups")
