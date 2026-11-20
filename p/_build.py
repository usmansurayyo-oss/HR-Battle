# -*- coding: utf-8 -*-
"""Страницы параграфов учебного пособия: цели, интерактивный глоссарий,
интерактивный тест и связь с практическим занятием.

    python3 p/_build.py      (данные — p/_data.json)

Результат: p/<N>/index.html, p/index.html и QR-коды p/qr/p-<NN>.svg|.png
"""
import html
import json
import os
import sys

import segno

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "pz"))
from _build import CSS, THUMB_JS  # noqa: E402  (общий стиль с практическими занятиями)
from _data import BOOK, AUTHOR, LESSONS  # noqa: E402

BASE_URL = "https://usmansurayyo-oss.github.io/HR-Battle/p/"
DATA = json.load(open(os.path.join(HERE, "_data.json"), encoding="utf-8"))
VIDEO = {L["n"]: L["video"] for L in LESSONS}
PZ_TITLE = {L["n"]: L["title"] for L in LESSONS}

EXTRA_CSS = """
.term{border-bottom:1px solid var(--line);padding:8px 0}
.term:last-child{border-bottom:0}
.term summary{cursor:pointer;font-weight:600}
.term p{margin:6px 0 0;color:var(--mute)}
.term.plain{font-weight:600}
.q{margin:0 0 16px}
.q b{display:block;margin-bottom:6px}
.q label{display:block;padding:8px 10px;border:1px solid var(--line);border-radius:10px;margin:6px 0;cursor:pointer}
.q label.right{border-color:var(--accent);background:var(--accent-soft)}
.q label.wrong{border-color:var(--warn);background:var(--warn-soft)}
button.btn{border:0;font:inherit;cursor:pointer}
#score{font-weight:700;margin-top:10px}
"""

TEST_JS = """<script>
document.getElementById('check').addEventListener('click', function () {
  var qs = document.querySelectorAll('.q'), ok = 0, answered = 0;
  qs.forEach(function (q) {
    var right = +q.dataset.a, picked = q.querySelector('input:checked');
    q.querySelectorAll('label').forEach(function (l, i) {
      l.classList.remove('right', 'wrong');
      if (i === right) l.classList.add('right');
    });
    if (picked) {
      answered++;
      var v = +picked.value;
      if (v === right) ok++; else picked.parentNode.classList.add('wrong');
    }
  });
  var s = document.getElementById('score');
  s.textContent = 'Результат: ' + ok + ' из ' + qs.length +
    (answered < qs.length ? ' (отвечено ' + answered + ')' : '') +
    (ok === qs.length ? ' — отлично!' : ok >= 3 ? ' — хорошо, повторите ошибки.' : ' — перечитайте параграф.');
});
document.getElementById('reset').addEventListener('click', function () {
  document.querySelectorAll('.q input').forEach(function (i) { i.checked = false; });
  document.querySelectorAll('.q label').forEach(function (l) { l.classList.remove('right', 'wrong'); });
  document.getElementById('score').textContent = '';
});
</script>"""


def page(title, body, scripts=""):
    return f"""<!doctype html>
<html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<style>{CSS}{EXTRA_CSS}</style></head>
<body><main>
{body}
<footer>{html.escape(AUTHOR)} «{html.escape(BOOK)}». Учебное пособие. Ташкент, 2026.</footer>
</main>
{scripts}
</body></html>
"""


def ul(items):
    return "<ul>" + "".join(f"<li>{html.escape(i)}</li>" for i in items) + "</ul>"


def sec_html(s, prev, nxt):
    o = s["outcomes"]
    terms = ""
    for g in s["glossary"]:
        if g["d"]:
            terms += (f'<details class="term"><summary>{html.escape(g["t"][:1].upper() + g["t"][1:])}</summary>'
                      f'<p>{html.escape(g["d"])}</p></details>')
        else:
            terms += f'<div class="term plain">{html.escape(g["t"][:1].upper() + g["t"][1:])}</div>'
    qs = ""
    for k, q in enumerate(s["test"]):
        opts = "".join(
            f'<label><input type="radio" name="q{k}" value="{i}"> {"абвг"[i]}) {html.escape(t)}</label>'
            for i, t in enumerate(q["opts"]))
        qs += f'<div class="q" data-a="{q["a"]}"><b>{k + 1}. {html.escape(q["q"])}</b>{opts}</div>'
    pz = s["pz"]
    vid, vtitle = VIDEO[pz]
    nav = '<div class="nav">'
    nav += f'<a href="../{prev}/">← § {prev}</a>' if prev else "<span></span>"
    nav += '<a href="../">Все параграфы</a>'
    nav += f'<a href="../{nxt}/">§ {nxt} →</a>' if nxt else "<span></span>"
    nav += "</div>"
    body = f"""
<p class="book">{html.escape(BOOK)}</p>
<span class="num">§ {s['n']}</span>
<h1>{html.escape(s['title'])}</h1>

<section class="card idea"><h2>🎯 Что вы освоите</h2>
<p style="margin:0 0 4px"><b>Узнаете:</b></p>{ul(o['know'])}
<p style="margin:8px 0 4px"><b>Поймёте:</b></p>{ul(o['und'])}
<p style="margin:8px 0 4px"><b>Приобретёте навыки:</b></p>{ul(o['skill'])}
</section>

<section class="card"><h2>📖 Интерактивный глоссарий</h2>
<p class="goal" style="margin-bottom:8px">Нажмите на термин, чтобы увидеть определение.</p>
{terms}
</section>

<section class="card"><h2>✅ Проверьте себя</h2>
{qs}
<button class="btn" id="check">Проверить</button>
<button class="btn" id="reset" style="background:var(--line);color:var(--text);margin-left:6px">Сначала</button>
<p id="score"></p>
</section>

<section class="card"><h2>▶ Видео и практика</h2>
<a class="video" href="https://www.youtube.com/watch?v={vid}" data-vid="{vid}">
<img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt="" loading="lazy"><span class="play">▶</span></a>
<p class="vbad" hidden>Это видео сейчас недоступно на YouTube.</p>
<div class="vlinks"><p>Практическое занятие {pz}: <a href="../../pz/{pz}/">{html.escape(PZ_TITLE[pz])}</a> — видео и пошаговый разбор решения.</p></div>
</section>
{nav}
"""
    return page(f"§ {s['n']}. {s['title']}", body, TEST_JS + THUMB_JS)


def index_html():
    items = "".join(f'<a href="{s["n"]}/"><b>§ {s["n"]}</b>{html.escape(s["title"])}</a>' for s in DATA)
    body = f"""
<p class="book">{html.escape(AUTHOR)}</p>
<h1>{html.escape(BOOK)}</h1>
<p class="goal">Материалы к параграфам: цели, интерактивный глоссарий, тест для самопроверки, видео и практика.</p>
<section class="card list">{items}</section>
<p class="goal"><a href="../pz/">Практические занятия →</a></p>
"""
    return page(f"{BOOK} — параграфы", body)


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def qr(url, name):
    q = segno.make(url, error="m", micro=False)
    out = os.path.join(HERE, "qr")
    os.makedirs(out, exist_ok=True)
    q.save(os.path.join(out, f"{name}.svg"), scale=10, border=2)
    q.save(os.path.join(out, f"{name}.png"), scale=30, border=2)


def main():
    ns = [s["n"] for s in DATA]
    for i, s in enumerate(DATA):
        prev = ns[i - 1] if i else None
        nxt = ns[i + 1] if i + 1 < len(ns) else None
        write(os.path.join(HERE, str(s["n"]), "index.html"), sec_html(s, prev, nxt))
        qr(f"{BASE_URL}{s['n']}/", f"p-{s['n']:02d}")
    write(os.path.join(HERE, "index.html"), index_html())
    print(f"OK: {len(DATA)} страниц")


if __name__ == "__main__":
    main()
