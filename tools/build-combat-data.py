"""Build stage enemy matchups and versioned Raid boss clues from local tables."""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--tables", type=Path, required=True, help="Decoded DV3 1.0.18 static table directory")
parser.add_argument("--lang", type=Path, required=True, help="English lang_en.lua from the local research corpus")
args = parser.parse_args()

def rows(name):
    raw = json.loads((args.tables / f"{name}.dat.json").read_text(encoding="utf-8"))["tables"][0]["rows"]
    return [dict(zip(raw[0], row)) for row in raw[1:]]

def lua_unescape(value):
    return re.sub(r"\\([\\'\"nrt])", lambda m: {"n": "\n", "r": "\r", "t": "\t"}.get(m.group(1), m.group(1)), value)

translations = {}
for path in (args.lang, args.lang.with_name("lang_en_patch.lua")):
    text = path.read_text(encoding="utf-8")
    for key, value in re.findall(r"\['((?:\\.|[^'])*)'\]\s*=\s*'((?:\\.|[^'])*)'", text):
        translations[key] = lua_unescape(value)
        translations[lua_unescape(key)] = lua_unescape(value)

catalog_text = (ROOT / "data" / "catalog-data.js").read_text(encoding="utf-8")
catalog_payload = catalog_text.split("=", 1)[1].strip().rstrip(";")
catalog = json.loads(catalog_payload)
dragons_by_id = {d["id"]: d for d in catalog["dragons"]}
elements_by_id = {e["id"]: e["element"] for e in rows("table_element") if e["element"] not in {"none", "special"}}

matchup_rows = rows("table_element_matchup")
element_names = [key for key in matchup_rows[0] if key != "attack_element"]
matchups = {row["attack_element"]: {name: int(row.get(name) or 0) for name in element_names} for row in matchup_rows}

def element_ids(row, fields):
    result = []
    for key in fields:
        value = row.get(key, "")
        if value in elements_by_id and elements_by_id[value] not in result:
            result.append(elements_by_id[value])
    return result

expedition_enemies = {}
for row in rows("table_expedition_enemy"):
    expedition_enemies[row["enemy_id"]] = {"dragonId": row.get("unit_id", ""), "elements": element_ids(row, ["r_ele1", "r_ele2", "r_ele3"])}

dungeon_enemies = {}
for row in rows("table_dungeon_enemy"):
    dungeon_enemies[row["enemy_id"]] = {"dragonId": row.get("did", ""), "elements": element_ids(row, ["r_ele1", "r_ele2", "r_ele3"])}

raid_bosses = []
for row in rows("table_raid_boss"):
    if row.get("season") != "1" or row.get("chroma") != "FALSE":
        continue
    dragon = dragons_by_id.get(row.get("did", ""), {})
    hint = translations.get(row.get("t_hint", ""), "")
    if not hint:
        continue
    phases = []
    for i in range(1, 5):
        phase_hint = translations.get(row.get(f"t_phase_{i}", ""), "")
        phase_skills = translations.get(row.get(f"r_phase_skills_{i}", ""), "")
        phases.append({"number": i, "threshold": row.get(f"phase_{i}", ""), "hint": phase_hint, "skills": phase_skills})
    raid_bosses.append({
        "id": row["id"], "dragonId": row["did"], "name": dragon.get("name", "Raid boss"),
        "elements": dragon.get("elements", []), "hint": hint, "phases": phases,
        "stats": {key.upper(): int(row[key]) for key in ["hp", "atk", "def", "mag", "mr", "spd"] if str(row.get(key, "")).isdigit()},
        "recommendedPower": row.get("std_power", ""), "timeLimitSeconds": row.get("max_time", "")
    })

payload = {"version": "1.0.18", "matchups": matchups, "expeditionEnemies": expedition_enemies, "dungeonEnemies": dungeon_enemies, "raidBosses": raid_bosses}
(ROOT / "data" / "combat-data.js").write_text("window.COMBAT_DATA = " + json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
print(f"Wrote matchup chart, {len(expedition_enemies)} Expedition enemies, {len(dungeon_enemies)} Dungeon enemies, and {len(raid_bosses)} translated Raid bosses")
