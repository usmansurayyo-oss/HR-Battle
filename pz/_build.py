# -*- coding: utf-8 -*-
"""Собирает страницы практических занятий и QR-коды.

    pip install segno
    python3 pz/_build.py

Результат:
  pz/index.html          — список всех занятий
  pz/<N>/index.html      — страница занятия N (видео + разбор)
  pz/qr/pz-<N>.svg|.png  — QR-код на страницу занятия N (для вёрстки книги)
  pz/qr/pz-all.svg|.png  — QR-код на список занятий
"""
import html
import os
import sys

import segno

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _data import AUTHOR, BOOK, LESSONS  # noqa: E402

BASE_URL = "https://usmansurayyo-oss.github.io/HR-Battle/pz/"

CSS = """
:root{--bg:#f6f7f9;--card:#fff;--text:#1b2230;--mute:#5b6576;--line:#e2e6ec;--accent:#0b7a5c;--accent-soft:#e3f4ee;--warn:#9a4b00;--warn-soft:#fff3e3;--code:#eef1f5}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#11161f;--card:#19202c;--text:#e8edf5;--mute:#9aa6b8;--line:#2a3443;--accent:#5fd3ad;--accent-soft:#16332b;--warn:#ffb866;--warn-soft:#33260f;--code:#232c3a}}
:root[data-theme="dark"]{--bg:#11161f;--card:#19202c;--text:#e8edf5;--mute:#9aa6b8;--line:#2a3443;--accent:#5fd3ad;--accent-soft:#16332b;--warn:#ffb866;--warn-soft:#33260f;--code:#232c3a}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font:17px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif}
main{max-width:760px;margin:0 auto;padding:20px 16px 60px}
a{color:var(--accent)}
.book{font-size:13px;color:var(--mute);text-transform:uppercase;letter-spacing:.06em;margin:0 0 6px}
h1{font-size:1.55rem;line-height:1.25;margin:4px 0 10px}
h2{font-size:1.15rem;margin:0 0 10px}
.num{display:inline-block;background:var(--accent);color:var(--card);border-radius:8px;padding:2px 10px;font-weight:700;font-size:14px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px;margin:14px 0}
.goal{color:var(--mute);margin:0}
.video{position:relative;padding-top:56.25%;border-radius:10px;overflow:hidden;background:#000}
.video iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.vlinks{margin:10px 0 0;font-size:15px}
.vlinks p{margin:6px 0}
.idea{background:var(--accent-soft);border-color:transparent}
ol.steps{padding-left:22px;margin:0}
ol.steps li{margin:8px 0}
ul{padding-left:20px;margin:0}
li{margin:5px 0}
.warn{background:var(--warn-soft);border-color:transparent}
.warn h2{color:var(--warn)}
code{background:var(--code);border-radius:5px;padding:1px 5px;font-size:.92em;word-break:break-word}
.nav{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;margin-top:22px;font-size:15px}
.list a{display:block;text-decoration:none;color:var(--text);padding:12px 0;border-bottom:1px solid var(--line)}
.list a:last-child{border-bottom:0}
.list b{color:var(--accent);margin-right:8px}
footer{color:var(--mute);font-size:13px;margin-top:26px}
"""


def page(title, body):
    return f"""<!doctype html>
<html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<style>{CSS}</style></head>
<body><main>
{body}
<footer>{html.escape(AUTHOR)} «{html.escape(BOOK)}». Учебное пособие. Ташкент, 2026.<br>
Видео размещены на YouTube их авторами; ссылки даны в учебных целях.</footer>
</main></body></html>
"""


def yt(vid):
    return f"https://www.youtube.com/watch?v={vid}"


def lesson_html(L, prev, nxt):
    vid, vtitle = L["video"]
    evid, etitle = L["extra"]
    steps = "".join(f"<li>{s}</li>" for s in L["steps"])
    mistakes = "".join(f"<li>{m}</li>" for m in L["mistakes"])
    qs = "".join(f"<li>{html.escape(q)}</li>" for q in L["questions"])
    nav = '<div class="nav">'
    nav += f'<a href="../{prev}/">← Занятие {prev}</a>' if prev else "<span></span>"
    nav += '<a href="../">Все занятия</a>'
    nav += f'<a href="../{nxt}/">Занятие {nxt} →</a>' if nxt else "<span></span>"
    nav += "</div>"
    body = f"""
<p class="book">{html.escape(BOOK)} · Приложение Б</p>
<span class="num">Практическое занятие {L['n']}</span>
<h1>{html.escape(L['title'])}</h1>
<p class="goal"><b>Цель:</b> {html.escape(L['goal'])} <b>Теория:</b> {html.escape(L['theory'])} пособия.</p>

<section class="card">
<h2>▶ Видео к занятию</h2>
<div class="video"><iframe src="https://www.youtube-nocookie.com/embed/{vid}" title="{html.escape(vtitle)}" loading="lazy"
 allow="accelerometer; encrypted-media; gyroscope; picture-in-picture; fullscreen" allowfullscreen></iframe></div>
<div class="vlinks">
<p><a href="{yt(vid)}">{html.escape(vtitle)}</a> — открыть в YouTube</p>
<p>Дополнительно: <a href="{yt(evid)}">{html.escape(etitle)}</a></p>
</div>
</section>

<section class="card idea"><h2>💡 Главная идея</h2><p style="margin:0">{L['idea']}</p></section>

<section class="card"><h2>🧮 Разбор решения по шагам</h2><ol class="steps">{steps}</ol></section>

<section class="card"><h2>📊 Как сделать в Excel</h2><p style="margin:0">{L['excel']}</p></section>

<section class="card warn"><h2>⚠️ Типичные ошибки</h2><ul>{mistakes}</ul></section>

<section class="card"><h2>❓ Контрольные вопросы</h2><ol>{qs}</ol></section>
{nav}
"""
    return page(f"Занятие {L['n']}. {L['title']}", body)


def index_html():
    items = "".join(
        f'<a href="{L["n"]}/"><b>{L["n"]}</b>{html.escape(L["title"])}</a>' for L in LESSONS
    )
    body = f"""
<p class="book">{html.escape(AUTHOR)}</p>
<h1>{html.escape(BOOK)}</h1>
<p class="goal">Практические занятия: видео и разбор решений. Каждое занятие в пособии
(Приложение Б) отмечено QR-кодом, который ведёт на его страницу.</p>
<section class="card list">{items}</section>
"""
    return page(f"{BOOK} — практические занятия", body)


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def qr(url, name):
    q = segno.make(url, error="m", micro=False)
    out = os.path.join(HERE, "qr")
    os.makedirs(out, exist_ok=True)
    q.save(os.path.join(out, f"{name}.svg"), scale=10, border=2)
    q.save(os.path.join(out, f"{name}.png"), scale=30, border=2)  # ~1000 px, 600 dpi при 4 см


def main():
    ns = [L["n"] for L in LESSONS]
    for i, L in enumerate(LESSONS):
        prev = ns[i - 1] if i else None
        nxt = ns[i + 1] if i + 1 < len(ns) else None
        write(os.path.join(HERE, str(L["n"]), "index.html"), lesson_html(L, prev, nxt))
        qr(f"{BASE_URL}{L['n']}/", f"pz-{L['n']:02d}")
    write(os.path.join(HERE, "index.html"), index_html())
    qr(BASE_URL, "pz-all")
    print(f"OK: {len(LESSONS)} страниц, QR в {os.path.join(HERE, 'qr')}")


if __name__ == "__main__":
    main()
