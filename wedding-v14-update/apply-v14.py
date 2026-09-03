from pathlib import Path
import re, shutil, sys
r=Path.cwd(); hp=r/'src/app/app.component.html'; sp=r/'src/app/app.component.scss'; images=r/'public/images'
if not all(p.exists() for p in (hp,sp,images)):
    sys.exit('ERROR: Uruchom skrypt w katalogu glownym projektu.')
shutil.copy2(Path(__file__).parent/'assets/family.jpg',images/'family.jpg')
h=hp.read_text(encoding='utf-8')
# 12th wish, compatible with already converted details letters.
if 'Własnych małych tradycji' not in h:
    letter='''
        <details class="wish-letter" data-reveal>
          <summary><span class="wish-letter__seal">🕯️</span><span class="wish-letter__title">Własnych małych tradycji</span><span class="wish-letter__hint">Otwórz list</span></summary>
          <div class="wish-letter__paper"><p>Takich, które po latach nadal będą przypominać, że najpiękniejsza historia powstaje z codziennych chwil.</p><span class="wish-letter__signature">Dla Was ♥</span></div>
        </details>'''
    grid=re.search(r'(<div class="wish-grid">)(.*?)(</div>\s*</section>)',h,flags=re.S)
    if not grid: sys.exit('ERROR: Nie znaleziono wish-grid.')
    h=h[:grid.end(2)]+letter+h[grid.end(2):]
# Remove signature names block only, preserve quote.
h=re.sub(r'\s*<p class="signature__names"[^>]*>.*?</p>','',h,count=1,flags=re.S)
# Replace final future section with three equal windows.
future='''<section class="future">
      <header class="future__header" data-reveal><p class="kicker">A na koniec życzymy Wam także…</p><h2>pełnego pakietu szczęścia</h2></header>
      <div class="future-grid">
        <article class="future-card future-card--family" data-reveal>
          <img src="/images/family.jpg" alt="Troje dzieci razem" loading="lazy">
          <div><span>01</span><h3>Zdrowa, wesoła rodzina</h3><p>Pełna energii, wspólnych przygód i codziennych powodów do śmiechu.</p></div>
        </article>
        <article class="future-card future-card--home" data-reveal>
          <img src="https://images.unsplash.com/photo-1558230844-d88915e549d0?auto=format&fit=crop&w=1400&q=85" alt="Willa w ciepłym świetle" loading="lazy">
          <div><span>02</span><h3>Piękny dom</h3><p>Wasze własne miejsce, do którego zawsze chce się wracać.</p></div>
        </article>
        <article class="future-card future-card--money" data-reveal>
          <div class="money-vault" aria-hidden="true"><b>💰</b><i>100</i><i>50</i><i>200</i><i>100</i><i>50</i><i>200</i><i>100</i><i>50</i><i>200</i><i>100</i><i>50</i><i>200</i></div>
          <div><span>03</span><h3>Kupa pieniążków</h3><p>Na marzenia, podróże i wszystkie nieplanowane okazje.</p></div>
        </article>
      </div>
      <p class="future__ending" data-reveal>Żyjcie długo, szczęśliwie<br>i zdecydowanie bez kredytu.</p>
      <div class="confetti" aria-hidden="true">✦ · ♥ · ✦ · ♥ · ✦</div><p class="final-date">26 września 2026</p>
    </section>'''
h,n=re.subn(r'<section class="future">.*?</section>',future,h,count=1,flags=re.S)
if not n: sys.exit('ERROR: Nie znaleziono sekcji future.')
hp.write_text(h,encoding='utf-8')

s=sp.read_text(encoding='utf-8'); s=re.sub(r'\n/\* v14 twelve letters and future windows \*/.*\Z','',s,flags=re.S)
s+='''

/* v14 twelve letters and future windows */
/* When open, summary becomes only a compact close control. */
.wish-letter[open] summary{min-height:3.1rem!important;height:3.1rem!important;padding:.55rem 1rem;background:#d9b889}.wish-letter[open] .wish-letter__seal,.wish-letter[open] .wish-letter__title{display:none}.wish-letter[open] .wish-letter__hint{margin:0!important;font-size:0!important;opacity:1}.wish-letter[open] .wish-letter__hint::after{content:"Zamknij list";font-size:.56rem!important;letter-spacing:.14em;color:#69452d}
.signature__names{display:none!important}
.future{min-height:125dvh;padding:clamp(5rem,8vw,8rem) clamp(1.25rem,4vw,4rem);display:block;background:radial-gradient(circle at 50% 15%,#4a301d,#0d0906 55%);text-align:center}.future__header{display:grid;justify-items:center;margin-bottom:3rem}.future__header h2{margin:.8rem 0 0;max-width:14ch}.future-grid{width:min(100%,94rem);margin:0 auto;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1.25rem}.future-card{position:relative;min-height:66dvh;overflow:hidden;border:1px solid rgba(220,177,105,.52);border-radius:1.4rem;background:#17100b;text-align:left;box-shadow:0 1.5rem 3.5rem #0007}.future-card>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center}.future-card::after{content:"";position:absolute;inset:0;background:linear-gradient(transparent 38%,rgba(8,5,3,.94) 83%)}.future-card>div:last-child{position:absolute;z-index:3;left:0;right:0;bottom:0;padding:2rem}.future-card>div:last-child>span{color:#deb267;font-size:.68rem;font-weight:700;letter-spacing:.18em}.future-card h3{margin:.55rem 0 .7rem;color:#fff0da;font:clamp(1.9rem,3.5vw,3.3rem)/1.04 Georgia}.future-card p{margin:0;color:#cdbfaf;line-height:1.55}.future-card--family>img{object-position:center 42%}.future-card--home>img{object-position:center}.future-card--money{background:radial-gradient(circle at 50% 35%,#745026,#17100b 72%)}.future-card--money::after{background:linear-gradient(transparent 42%,rgba(8,5,3,.96) 84%)}.money-vault{position:absolute!important;z-index:1!important;inset:0!important;padding:0!important;overflow:hidden}.money-vault b{position:absolute;left:50%;top:38%;transform:translate(-50%,-50%);font-size:clamp(6rem,12vw,11rem);filter:drop-shadow(0 1rem 1rem #0008)}.money-vault i{position:absolute;top:-15%;display:grid;place-items:center;width:4.5rem;height:2.2rem;border:2px solid #315f35;background:#8fca82;color:#204527;font:700 .8rem monospace;box-shadow:0 .25rem .3rem #0004;animation:cashFall 4.6s linear infinite}.money-vault i:nth-of-type(1){left:5%;animation-delay:-.3s}.money-vault i:nth-of-type(2){left:18%;animation-delay:-2.5s}.money-vault i:nth-of-type(3){left:31%;animation-delay:-1.1s}.money-vault i:nth-of-type(4){left:44%;animation-delay:-3.6s}.money-vault i:nth-of-type(5){left:57%;animation-delay:-.8s}.money-vault i:nth-of-type(6){left:70%;animation-delay:-2.9s}.money-vault i:nth-of-type(7){left:83%;animation-delay:-1.8s}.money-vault i:nth-of-type(8){left:92%;animation-delay:-4.3s}.money-vault i:nth-of-type(9){left:12%;animation-delay:-4s}.money-vault i:nth-of-type(10){left:38%;animation-delay:-2s}.money-vault i:nth-of-type(11){left:64%;animation-delay:-3.2s}.money-vault i:nth-of-type(12){left:78%;animation-delay:-.1s}@keyframes cashFall{0%{transform:translate3d(0,-5rem,0) rotate(-18deg);opacity:0}10%{opacity:1}100%{transform:translate3d(2rem,52rem,0) rotate(430deg);opacity:.25}}.future__ending{margin:4rem auto 1rem!important}.future .confetti,.future .final-date{position:static}
@media(max-width:1000px){.future-grid{grid-template-columns:1fr 1fr}.future-card--money{grid-column:1/-1;min-height:55dvh}}@media(max-width:680px){.future-grid{grid-template-columns:1fr}.future-card--money{grid-column:auto}.future-card{min-height:66dvh}.future{padding-inline:1rem}}
@media(prefers-reduced-motion:reduce){.money-vault i{animation:none!important}}
'''
sp.write_text(s,encoding='utf-8')
print('OK: zastosowano V14. Uruchom npm run build.')
