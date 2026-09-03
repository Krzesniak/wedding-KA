from pathlib import Path
import re,shutil,sys
r=Path.cwd(); hp=r/'src/app/app.component.html'; sp=r/'src/app/app.component.scss'; tp=r/'src/app/app.component.ts'
if not all(p.exists() for p in (hp,sp,tp,r/'public/images')): sys.exit('ERROR: Uruchom skrypt w katalogu glownym projektu.')
a=Path(__file__).parent/'assets'; shutil.copy2(a/'together-young-2018.jpg',r/'public/images/together-young-2018.jpg')
h=hp.read_text(encoding='utf-8')
# Tinder headline copy.
h=h.replace('W tym samym czasie','W tym samym czasie - lutym 2018 roku')
# Prevent duplication if rerun.
h=h.replace('W tym samym czasie - lutym 2018 roku - lutym 2018 roku','W tym samym czasie - lutym 2018 roku')
# Exact relationship section, supports all previous variants.
section='''<section class="together-date" data-reveal>
      <div class="date-hearts" aria-hidden="true"><span>♥</span><span>♥</span><span>♥</span><span>♥</span><span>♥</span><span>♥</span></div>
      <figure class="together-date__photo"><img src="/images/together-young-2018.jpg" alt="Wspólne zdjęcie z 2018 roku" loading="lazy"></figure>
      <div class="together-date__copy"><span>I stało się...</span><strong>15 lipca 2018 roku zostali oficjalnie parą!</strong><i aria-hidden="true">♥</i></div>
    </section>'''
h,n=re.subn(r'<section class="together-date"[^>]*>.*?</section>',section,h,count=1,flags=re.S)
if not n:
 marker='    <section class="memories-scene">'
 if marker not in h: marker='    <section class="date-night">'
 if marker not in h: sys.exit('ERROR: Nie znaleziono miejsca na slajd daty.')
 h=h.replace(marker,'    '+section+'\n\n'+marker,1)
hp.write_text(h,encoding='utf-8')

# Add a light heart entrance animation only once.
t=tp.read_text(encoding='utf-8')
if "'.date-hearts span'" not in t:
 anim="""\n      gsap.from('.date-hearts span', {\n        y: 90, opacity: 0, scale: .35, rotation: -25, duration: 1.1, stagger: .16, ease: 'back.out(1.8)',\n        scrollTrigger: { trigger: '.together-date', start: 'top 72%', once: true }\n      });\n\n"""
 marker="      gsap.timeline({ scrollTrigger: { trigger: '.date-scene'"
 if marker not in t: sys.exit('ERROR: Nie znaleziono animacji daty slubu.')
 t=t.replace(marker,anim+marker,1)
tp.write_text(t,encoding='utf-8')

s=sp.read_text(encoding='utf-8'); s=re.sub(r'\n/\* v7 date and Tinder layout \*/.*\Z','',s,flags=re.S)
s+='''

/* v7 date and Tinder layout */
/* Tinder is a two-column composition on desktop: copy left, phone right. */
.swipe-scene{grid-template-columns:minmax(0,1fr) minmax(20rem,28rem);grid-template-rows:auto 1fr;column-gap:clamp(2rem,7vw,8rem);align-items:center}
.swipe-scene__copy{grid-column:1;grid-row:1/3;align-self:center;max-width:46rem}.swipe-scene__copy .kicker{font-size:.78rem}.swipe-scene__copy h2{margin-top:1rem}
.phone{grid-column:2;grid-row:1/3;justify-self:end;align-self:center}
/* Relationship date with complete uncropped 2018 photo. */
.together-date{position:relative;isolation:isolate;overflow:hidden;grid-template-columns:minmax(20rem,.8fr) minmax(25rem,1.2fr);background:linear-gradient(135deg,#eadfce,#d3c1a7)}
.together-date__photo{position:relative;z-index:2;height:min(78dvh,50rem);border-radius:1rem 1rem 10rem 10rem;background:#201914}
.together-date__photo img{width:100%;height:100%;object-fit:contain;object-position:center;background:#201914}
.together-date__copy{position:relative;z-index:3;align-content:center}.together-date__copy span{font-size:.78rem}.together-date__copy strong{max-width:13ch;font-size:clamp(3rem,5.8vw,6rem)}
.date-hearts{position:absolute;z-index:1;inset:0;pointer-events:none;color:rgba(191,66,92,.42)}.date-hearts span{position:absolute;animation:heartFloat 4.2s ease-in-out infinite}.date-hearts span:nth-child(1){left:7%;bottom:8%;font-size:2.2rem}.date-hearts span:nth-child(2){left:43%;top:10%;font-size:1.4rem;animation-delay:.5s}.date-hearts span:nth-child(3){right:8%;top:16%;font-size:2.8rem;animation-delay:1.1s}.date-hearts span:nth-child(4){right:15%;bottom:9%;font-size:1.8rem;animation-delay:1.6s}.date-hearts span:nth-child(5){left:51%;bottom:21%;font-size:1.25rem;animation-delay:2.1s}.date-hearts span:nth-child(6){left:29%;top:7%;font-size:1.8rem;animation-delay:2.7s}@keyframes heartFloat{0%,100%{transform:translateY(0) rotate(-4deg)}50%{transform:translateY(-22px) rotate(5deg)}}
@media(max-width:760px){.swipe-scene{grid-template-columns:1fr;grid-template-rows:auto auto;row-gap:2rem}.swipe-scene__copy{grid-column:1;grid-row:1;text-align:left}.phone{grid-column:1;grid-row:2;justify-self:center}.together-date{grid-template-columns:1fr;padding-block:4rem}.together-date__photo{height:auto;min-height:0;max-height:none;border-radius:1rem 1rem 7rem 7rem}.together-date__photo img{height:auto;max-height:none}.together-date__copy{justify-items:center;text-align:center}.together-date__copy strong{max-width:15ch;font-size:clamp(2.5rem,12vw,4.3rem)}}
'''
sp.write_text(s,encoding='utf-8')
print('OK: zastosowano V7. Uruchom npm run build.')
