from pathlib import Path
import re, shutil, sys
r=Path.cwd(); hp=r/'src/app/app.component.html'; sp=r/'src/app/app.component.scss'; images=r/'public/images'
if not all(p.exists() for p in (hp,sp,images)):
    sys.exit('ERROR: Uruchom skrypt w katalogu glownym projektu po zastosowaniu V14.')
shutil.copy2(Path(__file__).parent/'assets/money-background.jpg',images/'money-background.jpg')
h=hp.read_text(encoding='utf-8')
# Money card gets the supplied banknote background while preserving falling notes.
money_pattern=r'(<article class="future-card future-card--money"[^>]*>)(.*?)(</article>)'
m=re.search(money_pattern,h,flags=re.S)
if not m: sys.exit('ERROR: Nie znaleziono karty future-card--money. Najpierw zastosuj V14.')
body=m.group(2)
if 'money-background.jpg' not in body:
    body='''\n          <img class="money-background" src="/images/money-background.jpg" alt="Tło z banknotami" loading="lazy">'''+body
h=h[:m.start()]+m.group(1)+body+m.group(3)+h[m.end():]
# Requested final sentence.
h=h.replace('Żyjcie długo, szczęśliwie<br>i zdecydowanie bez kredytu.','Żyjcie długo, szczęśliwie<br>i zawsze blisko siebie')
# Add final wedding closing slide after future.
closing='''

    <section class="closing-scene">
      <div class="closing-scene__glow" aria-hidden="true"></div>
      <div class="closing-scene__flowers" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i></div>
      <div class="closing-scene__rings" aria-hidden="true"><span></span><span></span></div>
      <div class="closing-scene__copy" data-reveal><p>Z całego serca</p><h2>Życzą</h2><strong>Kinga i Piotrek</strong><small>26 września 2026</small></div>
    </section>'''
if 'class="closing-scene"' in h:
    h=re.sub(r'\s*<section class="closing-scene">.*?</section>',closing,h,count=1,flags=re.S)
else:
    fm=re.search(r'<section class="future">.*?</section>',h,flags=re.S)
    if not fm: sys.exit('ERROR: Nie znaleziono sekcji future.')
    h=h[:fm.end()]+closing+h[fm.end():]
hp.write_text(h,encoding='utf-8')

s=sp.read_text(encoding='utf-8'); s=re.sub(r'\n/\* v15 final future and closing \*/.*\Z','',s,flags=re.S)
s+='''

/* v15 final future and closing */
/* Family crop keeps all three faces comfortably in view. */
.future-card--family>img{object-fit:cover;object-position:center 34%;transform:scale(.94);background:#c9b092}.future-card--family{background:#c9b092}
/* Supplied banknotes as the base, with the existing animated notes still falling above. */
.future-card--money>.money-background{position:absolute;z-index:0;inset:0;width:100%;height:100%;object-fit:cover;object-position:center;filter:saturate(.78) sepia(.08) brightness(.66)}.future-card--money::after{z-index:1;background:linear-gradient(transparent 30%,rgba(8,5,3,.91) 84%)}.future-card--money .money-vault{z-index:2!important}.future-card--money>div:last-child{z-index:4}
.future__ending{max-width:20ch;font-size:clamp(2.2rem,5.5vw,4.6rem)!important}
.closing-scene{position:relative;min-height:100dvh;display:grid;place-items:center;overflow:hidden;isolation:isolate;text-align:center;background:radial-gradient(circle at 50% 43%,#3d2718,#130c08 55%,#070403);color:#fff0dc}.closing-scene__glow{position:absolute;z-index:-2;width:min(90vw,48rem);aspect-ratio:1;border-radius:50%;background:radial-gradient(circle,rgba(223,174,95,.28),transparent 68%);filter:blur(24px);animation:closingGlow 3.8s ease-in-out infinite}.closing-scene__copy{position:relative;z-index:3;padding:2rem}.closing-scene__copy p{margin:0;color:#dcb36f;font-size:.72rem;font-weight:700;letter-spacing:.24em;text-transform:uppercase}.closing-scene__copy h2{margin:.7rem 0 0;font-size:clamp(3rem,8vw,6rem)}.closing-scene__copy strong{display:block;color:#f7dec0;font:italic clamp(3.8rem,11vw,9rem)/.98 Georgia}.closing-scene__copy small{display:block;margin-top:2rem;color:#a9937f;font-size:.68rem;letter-spacing:.2em;text-transform:uppercase}.closing-scene__rings{position:absolute;z-index:1;top:12%;left:50%;display:flex;transform:translateX(-50%);opacity:.42}.closing-scene__rings span{width:5rem;aspect-ratio:1;border:.45rem solid #d8aa57;border-radius:50%;box-shadow:inset 0 .18rem .22rem #fff2c2,0 0 1.2rem #d5a75c55}.closing-scene__rings span+span{margin-left:-1.2rem;border-color:#e4ded2}.closing-scene__flowers{position:absolute;z-index:1;inset:0;pointer-events:none}.closing-scene__flowers i{position:absolute;width:1rem;height:1.6rem;border-radius:90% 10% 70% 20%;background:#d4a45a;animation:closingPetal 7s linear infinite}.closing-scene__flowers i:nth-child(1){left:7%;animation-delay:-1s}.closing-scene__flowers i:nth-child(2){left:24%;animation-delay:-5s;background:#8d493b}.closing-scene__flowers i:nth-child(3){left:42%;animation-delay:-2.5s}.closing-scene__flowers i:nth-child(4){left:61%;animation-delay:-6s;background:#a75c45}.closing-scene__flowers i:nth-child(5){left:78%;animation-delay:-3.5s}.closing-scene__flowers i:nth-child(6){left:93%;animation-delay:-.4s;background:#8d493b}@keyframes closingGlow{50%{transform:scale(1.08);opacity:.72}}@keyframes closingPetal{from{top:-8%;transform:rotate(0);opacity:0}12%{opacity:.85}to{top:108%;transform:translateX(5rem) rotate(620deg);opacity:.15}}
@media(max-width:680px){.future-card--family>img{object-position:center 30%;transform:scale(.97)}.closing-scene__rings{top:14%}.closing-scene__copy strong{font-size:clamp(3.4rem,15vw,5.5rem)}}@media(prefers-reduced-motion:reduce){.closing-scene__glow,.closing-scene__flowers i{animation:none!important}}
'''
sp.write_text(s,encoding='utf-8')
print('OK: zastosowano V15. Uruchom npm run build.')
