"""Convert the maintained FAQ answer workbook into the browser question bank."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "content" / "faq-answer-workbook.md"
OUTPUT = ROOT / "question-bank.js"


def slug(value):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", value.lower())).strip("-")


def finish_question(category, title, body):
    body = "\n".join(body).strip()
    body = re.split(r"\n\*\*Steps or recommendation:\*\*", body, maxsplit=1)[0].strip()
    body = re.sub(r"\n?\n---\s*$", "", body).strip()
    dynamic = "DYNAMIC / TBD" in body
    is_tbd = bool(re.search(r"\*\*Answer draft: (?:DYNAMIC / )?TBD\*\*", body))
    prompt_notes = ""
    if is_tbd:
        body = re.sub(r"\*\*Answer draft: (?:DYNAMIC / )?TBD\*\*", "", body, count=1).strip()
        prompt_notes = body
        answer = ""
    else:
        answer = body
    category["questions"].append({
        "id": f"{category['id']}-{slug(title)}",
        "text": title,
        "answer": answer,
        "promptNotes": prompt_notes,
        "dynamic": dynamic or category["changing"],
    })


lines = SOURCE.read_text(encoding="utf-8").splitlines()
categories = []
category = None
question = None
body = []
for line in lines:
    if line.startswith("## "):
        if category and question:
            finish_question(category, question, body)
            question = None
            body = []
        title = line[3:].strip()
        if title.startswith(("Current /", "Current ")):
            category = {"id": "current-info", "title": title, "changing": True, "questions": []}
        else:
            category = {"id": slug(title), "title": title, "changing": False, "questions": []}
        categories.append(category)
    elif line.startswith("### ") and category:
        if question:
            finish_question(category, question, body)
        question = line[4:].strip()
        body = []
    elif question:
        body.append(line)

if category and question:
    finish_question(category, question, body)

payload = "window.GUIDE_QUESTIONS = " + json.dumps(categories, ensure_ascii=False, separators=(",", ":")) + ";\n"
OUTPUT.write_text(payload, encoding="utf-8")
count = sum(len(c["questions"]) for c in categories)
answered = sum(bool(q["answer"]) for c in categories for q in c["questions"])
print(f"Wrote {count} questions in {len(categories)} topics ({answered} with imported answer drafts)")
