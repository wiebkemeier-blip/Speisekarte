"""Erzeugt die Gäste-Webseite der Speisekarte aus menu_data.py."""
import html, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from menu_data import DE, EN

E = html.escape


def dishes(items, d):
    out = []
    for name, pre, desc, price, four, supp, gold in items:
        tags = f'<span class="tag">{E(d["tag4"])}</span>' if four else ""
        supp_html = f'<span class="supp">{E(supp)}</span>' if supp else ""
        pre_html = f'<p class="pre">{E(pre)}</p>' if pre else ""
        out.append(f'''
      <li class="dish{' gold' if gold else ''}">
        <div class="dtext">{pre_html}<h3>{E(name)}</h3><p class="desc">{E(desc)}</p></div>
        <div class="dside"><span class="price">{E(price)}</span>{tags}{supp_html}</div>
      </li>''')
    return '<ul class="dishes">' + "".join(out) + "</ul>"


def stamp(d):
    rows = "".join(f'<div class="st-row"><span>{E(n)} <i>{E(q)}</i></span><b>{E(p)}</b></div>' for n, q, p in d["extras"])
    return f'<aside class="stamp" aria-label="{E(d["extra_label"])}"><div class="st-in"><div class="st-title">{E(d["extra_label"])}</div>{rows}</div></aside>'


def price_table(d):
    head = "".join(f"<th scope='col'><span class='lg'>{E(c)}</span><span class='sh' aria-hidden='true'>{E(s)}</span></th>" for c, s in zip(d["menu_cols"], d["menu_cols_short"]))
    body = "".join("<tr><th scope='row'>" + E(r[0]) + "</th>" + "".join(f"<td>{E(v)}</td>" for v in r[1:]) + "</tr>" for r in d["menu_rows"])
    return f'''
      <table class="menutab"><thead><tr><td></td>{head}</tr></thead><tbody>{body}</tbody></table>
      <p class="note gold-note">{E(d["gold_note"])}</p>
      <p class="note">{E(d["veg"])}</p>'''


def drinks(d):
    out = []
    for sub, items in d["drinks"]:
        out.append(f'<h4 class="sub">{E(sub)}</h4><ul class="drinks">')
        for name, desc, price, af in items:
            tag = f' <span class="supp">{E(d["alc_free"])}</span>' if af else ""
            out.append(f'<li><div class="dtext"><h3 class="dname">{E(name)}{tag}</h3><p class="desc">{E(desc)}</p></div><span class="price">{E(price)}</span></li>')
        out.append("</ul>")
    return "".join(out)


def champ(d):
    rows = "".join(f'<li><span class="vint">{E(v)}</span><h3 class="dname">{E(n)}</h3><span class="price">{E(p)}</span></li>' for n, v, p in d["champ"])
    return f'<h4 class="sub">Bonnaire <span class="place">Cramant</span></h4><p class="cols">{E(d["champ_cols"])}</p><ul class="champ">{rows}</ul>'


def lang_block(d, hidden):
    h = " hidden" if hidden else ""
    return f'''
  <div class="lang" lang="{d["lang"]}" data-lang="{d["lang"]}"{h}>
    <section class="sec sec-menu">
      <h2>{E(d["ch1"])}</h2>
      <div class="menu-body">
        <div class="stamp-col">{stamp(d)}</div>
        <div class="menu-main">{dishes(d["menu"], d)}{price_table(d)}</div>
      </div>
    </section>
    <div class="cols2">
      <section class="sec">
        <h2>{E(d["ch2"])}</h2>
        {dishes(d["classics"], d)}
      </section>
      <section class="sec">
        <h2>{E(d["ch3"])}</h2>
        <p class="note">{E(d["special_note"])}</p>
        {dishes(d["special"], d)}
      </section>
      <section class="sec">
        <h2>{E(d["drinks_title"])}</h2>
        {drinks(d)}
      </section>
      <section class="sec">
        <h2>{E(d["champ_title"])}</h2>
        {champ(d)}
      </section>
    </div>
    <p class="vat">{E(d["price_note"])}</p>
  </div>'''


CSS = """
:root{
  --paper:#FFFFFF; --ink:#161615; --muted:#5E5E58; --gold:#8D7535; --gold-ui:#B8A068;
  --pink:#DE19AD; --pill:#ECEAE5; --line:#161615;
  --sans:"Jost","Futura","Century Gothic",system-ui,sans-serif;
  color-scheme: light;
}
/* Layout: eine ruhige Spalte wie die gedruckte Karte; ab Tablet zwei Spalten für Klassiker, Extrawurst und Getränke */
html{background:var(--paper)}
body{background:var(--paper);color:var(--ink);font-family:var(--sans);font-weight:400;font-size:16px;line-height:1.5}
.wrap{max-width:860px;margin:0 auto;padding-inline:20px;padding-block:28px 56px}
header{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:16px 24px;margin-bottom:36px}
header img{width:min(260px,62vw);height:auto;display:block}
.switch{display:inline-flex;border:1px solid #D9D6CE;border-radius:999px;padding:3px}
.switch button{font:500 12px/1 var(--sans);letter-spacing:.16em;text-transform:uppercase;border:0;background:none;color:var(--muted);padding:9px 14px;border-radius:999px;cursor:pointer}
.switch button[aria-pressed="true"]{background:var(--ink);color:var(--paper)}
.switch button:focus-visible{outline:2px solid var(--gold-ui);outline-offset:2px}
.sec{position:relative;margin-bottom:44px;min-width:0}
h2{font-weight:500;font-size:clamp(18px,3.4vw,22px);letter-spacing:.16em;text-transform:uppercase;margin:0 0 4px;padding-bottom:10px;border-bottom:2px solid var(--line);text-wrap:balance}
ul{list-style:none;margin:0;padding:0}
.dish{display:flex;gap:16px;justify-content:space-between;padding:14px 0 12px}
.dtext{min-width:0;flex:1}
.dish h3,.dname{margin:0;font-weight:500;font-size:15px;letter-spacing:.06em;text-transform:uppercase}
.dname{text-transform:none;letter-spacing:.01em;font-size:16px}
.pre{margin:0 0 2px;color:var(--muted);font-size:14px}
.desc{margin:3px 0 0;color:var(--muted);font-size:15px;line-height:1.45;max-width:58ch}
.dside{display:flex;flex-direction:column;align-items:flex-end;gap:6px;flex:none;text-align:right}
.price{font-weight:500;font-size:16px;font-variant-numeric:tabular-nums;white-space:nowrap}
.tag{font-size:11px;letter-spacing:.08em;text-transform:uppercase;background:var(--pill);color:#4A4A45;padding:3px 8px;border-radius:4px;white-space:nowrap}
.supp{font-size:12px;color:var(--muted);border:1px solid #C9C6BE;border-radius:4px;padding:2px 7px;white-space:nowrap;letter-spacing:.02em;font-weight:400;text-transform:none;vertical-align:2px}
.dish.gold h3,.dish.gold .desc,.dish.gold .price{color:var(--gold)}
.stamp{display:inline-block;margin:18px 0 8px 4px;transform:rotate(-6deg);border:2px solid var(--pink);border-radius:6px;padding:3px;color:var(--pink);background:var(--paper)}
.st-in{border:1px solid var(--pink);border-radius:3px;padding:10px 14px 8px;min-width:190px}
.st-title{font-weight:500;font-size:12px;letter-spacing:.18em;text-transform:uppercase;text-align:center;padding-bottom:6px;margin-bottom:6px;border-bottom:1px solid var(--pink)}
.st-row{display:flex;justify-content:space-between;gap:14px;font-size:14px;line-height:1.7}
.st-row i{font-style:normal;opacity:.8}
.st-row b{font-weight:500}
.sec-menu .dishes{clear:none}
.menutab{border-collapse:collapse;margin-top:26px;padding-top:0;border-top:1px solid var(--line);width:100%;font-variant-numeric:tabular-nums}
.menutab thead th{font-weight:500;font-size:11px;letter-spacing:.16em;line-height:1.35;text-transform:uppercase;color:var(--gold);text-align:right;vertical-align:bottom;padding:14px 0 6px 14px}
.menutab thead th:last-child{max-width:12em}
.menutab .sh{display:none}
.menutab tbody th{text-align:left;font-weight:400;padding:6px 0}
.menutab td{text-align:right;font-weight:500;padding:6px 0}
.note{margin:10px 0 0;color:var(--muted);font-size:14px;max-width:62ch}
.gold-note{color:var(--gold);margin-top:16px}
.sub{margin:18px 0 4px;font-weight:500;font-size:12px;letter-spacing:.2em;text-transform:uppercase;color:var(--gold)}
.place{color:var(--muted);letter-spacing:.04em;text-transform:none;font-weight:400;font-size:14px;margin-left:6px}
.cols{margin:0 0 6px;color:var(--muted);font-size:13px}
.drinks li,.champ li{display:flex;gap:14px;justify-content:space-between;align-items:baseline;padding:7px 0}
.champ .vint{color:var(--gold);font-weight:500;width:28px;flex:none}
.champ .dname{flex:1;min-width:0}
.vat{color:var(--muted);font-size:13px;margin-top:8px}
@media (min-width:760px){
  .cols2{display:grid;grid-template-columns:1fr 1fr;gap:0 48px;align-items:start}
}
@media (min-width:760px){
  .menu-body{display:grid;grid-template-columns:200px minmax(0,1fr);gap:0 28px;align-items:start}
  .stamp{margin:22px 0 0 -6px}
  .st-in{min-width:0}
}
@media (max-width:520px){
  .menutab thead th{letter-spacing:.08em;padding-left:10px}
  .menutab .lg{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
  .menutab .sh{display:inline}
  .dish{gap:12px}
}
"""

LOGO_ALT = "Kettner's Kamota"


def page():
    return f'''<title>Kettner's Kamota Speisekarte</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Jost:wght@400;500&display=swap">
<style>{CSS}</style>
<div class="wrap">
  <header>
    <img src="logo.png" alt="{LOGO_ALT}" width="466" height="100">
    <div class="switch" role="group" aria-label="Sprache / Language">
      <button id="b-de" type="button" data-lang="de" aria-pressed="true">Deutsch</button>
      <button id="b-en" type="button" data-lang="en" aria-pressed="false">English</button>
    </div>
  </header>
  <main>{lang_block(DE, False)}{lang_block(EN, True)}
  </main>
</div>
<script>
(function(){{
  function show(l){{
    document.querySelectorAll('.lang').forEach(function(s){{ s.hidden = s.dataset.lang !== l; }});
    document.querySelectorAll('.switch button').forEach(function(b){{ b.setAttribute('aria-pressed', String(b.dataset.lang === l)); }});
    document.documentElement.lang = l;
  }}
  document.querySelectorAll('.switch button').forEach(function(b){{ b.addEventListener('click', function(){{ show(b.dataset.lang); }}); }});
  if (location.hash === '#en') show('en');
}})();
</script>
'''


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web", "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w").write(page())
    print("ok", out)
