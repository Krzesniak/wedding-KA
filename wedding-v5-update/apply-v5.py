from pathlib import Path
import re, shutil, sys
r=Path.cwd(); hp=r/'src/app/app.component.html'; sp=r/'src/app/app.component.scss'; tp=r/'src/app/app.component.ts'
if not all(p.exists() for p in (hp,sp,tp,r/'public/images')): sys.exit('Uruchom skrypt w katalogu glownym projektu.')
a=Path(__file__).parent/'assets'; shutil.copy2(a/'together-2018.jpg',r/'public/images/together-2018.jpg')
h=hp.read_text(encoding='utf-8')
# Tinder: add Ania as observer on left, safely around existing phone.
if 'class="swipe-ania"' not in h:
 marker='<div class="phone" aria-label="Animowana karta profilu">'
 ania='''<aside class="swipe-ania" data-reveal><div class="swipe-ania__portrait"><img src="/images/ania.jpg" alt="Portret Ani"></div><p>Ania wykonuje<br><strong>ruch w prawo</strong></p><span aria-hidden="true">→</span></aside>\n      '''
 if marker not in h: sys.exit('Nie znaleziono telefonu Tinder.')
 h=h.replace(marker,ania+marker,1)
# Relationship date: replace simple section with photo composition.
newdate='''<section class="together-date" data-reveal>
      <figure class="together-date__photo"><img src="/images/together-2018.jpg" alt="Wspólne zdjęcie z 2018 roku" loading="lazy"></figure>
      <div class="together-date__copy"><span>Od tego dnia</span><strong>Razem od 15 lipca 2018</strong><p>Właśnie wtedy oficjalnie zostali parą.</p><i aria-hidden="true">♥</i></div>
    </section>'''
h,n=re.subn(r'<section class="together-date"[^>]*>.*?</section>',newdate,h,count=1,flags=re.S)
if not n:
 marker='    <section class="date-night">'
 if marker not in h: sys.exit('Nie znaleziono miejsca na date zwiazku.')
 h=h.replace(marker,'    '+newdate+'\n\n'+marker,1)
hp.write_text(h,encoding='utf-8')
# Add animation for Ania Tinder if absent.
t=tp.read_text(encoding='utf-8')
if "'.swipe-ania'" not in t:
 old="""        .from('.phone', { y: 80, opacity: 0, rotation: -4, duration: .9 })"""
 new="""        .from('.swipe-ania', { x: -90, opacity: 0, duration: .9, ease: 'power3.out' })
        .from('.phone', { y: 80, opacity: 0, rotation: -4, duration: .9 }, '-=.45')"""
 if old not in t: sys.exit('Nie znaleziono animacji telefonu.')
 t=t.replace(old,new,1)
tp.write_text(t,encoding='utf-8')
# CSS overrides. Remove older v5 on rerun.
s=sp.read_text(encoding='utf-8'); s=re.sub(r'\n/\* v5 framing and story fixes \*/.*\Z','',s,flags=re.S)
s+='''

/* v5 framing and story fixes */
/* Obrączki: hide contaminated lower fringe behind clean dark mask, keep ring bodies above it. */
.rings-photo{top:5%;overflow:visible;isolation:isolate;filter:drop-shadow(0 .9rem 1rem rgba(0,0,0,.65))}
.rings-photo::after{content:"";position:absolute;z-index:2;left:8%;right:8%;bottom:3%;height:12%;background:linear-gradient(180deg,transparent,#090603 76%);filter:blur(2px);pointer-events:none}
.rings-photo img{position:relative;z-index:1;clip-path:inset(0 0 5% 0)}
.rings-photo__shine{z-index:3;opacity:.32;inset:-8%;background:linear-gradient(105deg,transparent 43%,rgba(255,237,185,.38) 49%,transparent 55%);filter:blur(11px)}
.intro__glow{opacity:.35!important;width:min(76vw,34rem);background:radial-gradient(circle,rgba(207,155,76,.25),transparent 67%);filter:blur(35px)}
.intro__copy{position:relative;z-index:6;margin-top:16rem;text-shadow:0 3px 18px #000,0 1px 3px #000}
.intro__copy .kicker{color:#e4b55f}.intro__copy h1{color:#fff3df}.intro__copy>p:last-child{color:#f0e3d2}
/* Great Wall: move portrait right; keep copy in a protected left column. */
.wall__karol{object-position:72% 28%}
.wall-scene__copy{max-width:min(46vw,39rem);padding:1.2rem;border-radius:1rem;background:linear-gradient(90deg,rgba(8,6,4,.55),rgba(8,6,4,.08));backdrop-filter:blur(1px)}
.wall-scene__copy h2{font-size:clamp(2.4rem,5.5vw,5.4rem)}
/* Tinder participant on left. */
.swipe-scene{grid-template-columns:minmax(0,1fr) auto;column-gap:clamp(1rem,4vw,5rem)}
.swipe-scene__copy{grid-column:1/-1}
.swipe-ania{align-self:center;justify-self:end;display:grid;grid-template-columns:auto auto;align-items:center;gap:.8rem;text-align:right;color:#eadde0}
.swipe-ania__portrait{width:clamp(8rem,20vw,15rem);aspect-ratio:3/4;overflow:hidden;border-radius:8rem 8rem 1rem 1rem;border:2px solid rgba(255,255,255,.38);box-shadow:0 1.4rem 3rem #0008}
.swipe-ania__portrait img{width:100%;height:100%;object-fit:cover;object-position:center 20%}
.swipe-ania p{margin:0;line-height:1.5}.swipe-ania strong{color:#ef718b}.swipe-ania>span{grid-column:1/-1;color:#ef718b;font-size:3rem;animation:swipeHint 1.25s ease-in-out infinite}
@keyframes swipeHint{50%{transform:translateX(15px)}}
/* Relationship anniversary composition. */
.together-date{min-height:92dvh;padding:clamp(2rem,6vw,6rem);display:grid;grid-template-columns:minmax(0,1.25fr) minmax(18rem,.75fr);align-items:center;gap:clamp(2rem,6vw,6rem);background:linear-gradient(135deg,#eee3d4,#cbb99e);color:#1b1510}
.together-date__photo{margin:0;height:min(74dvh,50rem);overflow:hidden;border-radius:1rem 1rem 12rem 12rem;box-shadow:0 2rem 4rem rgba(51,34,20,.3)}
.together-date__photo img{width:100%;height:100%;object-fit:cover;object-position:center 45%}
.together-date__copy{display:grid;justify-items:start}.together-date__copy span{color:#8b6332;font-size:.72rem;font-weight:700;letter-spacing:.2em;text-transform:uppercase}.together-date__copy strong{margin:1rem 0;font:clamp(2.7rem,6vw,5.7rem)/1.02 Georgia;font-weight:400}.together-date__copy p{font-size:clamp(1rem,2vw,1.3rem);color:#66594c;line-height:1.6}.together-date__copy i{color:#c34d65;font-size:2.5rem}
@media(max-width:760px){.rings-photo{top:8%}.intro__copy{margin-top:14rem}.wall__karol{object-position:64% 35%}.wall-scene__copy{max-width:92%;background:linear-gradient(90deg,rgba(8,6,4,.72),rgba(8,6,4,.18))}.wall-scene__copy h2{font-size:2.2rem}.swipe-scene{grid-template-columns:1fr}.swipe-scene__copy{grid-column:auto}.swipe-ania{justify-self:center;grid-template-columns:auto auto;text-align:left}.swipe-ania__portrait{width:8.5rem}.swipe-ania>span{grid-column:auto;font-size:2.3rem}.together-date{grid-template-columns:1fr;min-height:auto}.together-date__photo{height:62dvh}.together-date__copy{justify-items:center;text-align:center}}
'''
sp.write_text(s,encoding='utf-8')
print('OK: zastosowano V5. Uruchom npm run build.')
