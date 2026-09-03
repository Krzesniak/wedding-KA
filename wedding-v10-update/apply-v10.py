from pathlib import Path
import re,shutil,sys
r=Path.cwd(); hp=r/'src/app/app.component.html'; sp=r/'src/app/app.component.scss'; tp=r/'src/app/app.component.ts'; images=r/'public/images'
if not all(p.exists() for p in (hp,sp,tp,images)): sys.exit('ERROR: Uruchom skrypt w katalogu glownym projektu.')
shutil.copy2(Path(__file__).parent/'assets/car-couple.jpg',images/'car-couple.jpg')
if not (images/'engagement-ring.jpg').exists():
    sys.exit('ERROR: Brakuje public/images/engagement-ring.jpg. Najpierw zastosuj V9, bo V10 korzysta z przeslanego zdjecia pierscionka z V9.')
h=hp.read_text(encoding='utf-8')
# Normalize proposal photo and ensure it cannot disappear behind text.
proposal_pattern=r'<section class="proposal-scene">.*?</section>'
proposal='''<section class="proposal-scene">
      <div class="proposal-scene__photo" data-reveal>
        <img src="/images/engagement-ring.jpg" alt="Dłoń z pierścionkiem zaręczynowym" loading="lazy">
        <span class="ring-spark ring-spark--one" aria-hidden="true">✦</span><span class="ring-spark ring-spark--two" aria-hidden="true">✦</span><span class="ring-spark ring-spark--three" aria-hidden="true">✧</span><i class="ring-glint" aria-hidden="true"></i>
      </div>
      <div class="proposal-scene__copy"><p class="kicker" data-reveal>Kolejny wielki krok</p><h2 data-reveal>Aż w końcu przyszedł czas na wyczekiwane „TAK”!!!</h2><p data-reveal>Jedno pytanie, jeden pierścionek i odpowiedź, która rozpoczęła następny rozdział.</p></div>
    </section>'''
h,n=re.subn(proposal_pattern,proposal,h,count=1,flags=re.S)
if not n: sys.exit('ERROR: Nie znaleziono slajdu z pierscionkiem. Najpierw zastosuj V9.')
# Insert/replace car slide directly after proposal.
car='''

    <section class="road-scene">
      <div class="road-scene__sky" aria-hidden="true"><i></i><i></i><i></i></div>
      <div class="road-scene__car"><img src="/images/car-couple.jpg" alt="Wspólne zdjęcie w samochodzie" loading="lazy"></div>
      <div class="road-scene__dust" aria-hidden="true"><i></i><i></i><i></i></div>
      <div class="road-scene__copy"><p class="kicker">Kierunek: wspólna przyszłość</p><h2>W drodze do nowego etapu!</h2></div>
      <div class="road-scene__road" aria-hidden="true"><span></span><span></span><span></span></div>
    </section>'''
if 'class="road-scene"' in h:
    h=re.sub(r'\s*<section class="road-scene">.*?</section>',car,h,count=1,flags=re.S)
else:
    pos=h.find('</section>',h.find('class="proposal-scene"'))
    if pos<0: sys.exit('ERROR: Nie znaleziono konca slajdu zareczyn.')
    pos+=len('</section>'); h=h[:pos]+car+h[pos:]
hp.write_text(h,encoding='utf-8')

t=tp.read_text(encoding='utf-8')
# All viewport animations should restart whenever the slide re-enters the viewport.
t=t.replace("once: true", "toggleActions: 'restart pause restart pause'")
# Normalize proposal timeline where available: loop its decorative part while visible.
t=re.sub(r"\n\s*gsap\.timeline\(\{ scrollTrigger: \{ trigger: '\.road-scene'.*?;\n",'\n',t,count=1,flags=re.S)
road="""
      gsap.timeline({ repeat: -1, repeatDelay: 1.1, scrollTrigger: { trigger: '.road-scene', start: 'top 75%', end: 'bottom 25%', toggleActions: 'restart pause restart pause' } })
        .fromTo('.road-scene__car', { xPercent: -135, rotation: -1.5 }, { xPercent: 0, rotation: 0, duration: 2.25, ease: 'power2.out' })
        .fromTo('.road-scene__copy', { opacity: 0, y: 32 }, { opacity: 1, y: 0, duration: .8 }, '-=.6')
        .to('.road-scene__car', { xPercent: 135, duration: 2.1, ease: 'power2.in', delay: 1.4 })
        .to('.road-scene__copy', { opacity: 0, duration: .45 }, '-=1.25');

"""
marker="      gsap.timeline({ scrollTrigger: { trigger: '.kiss-scene'"
if marker not in t: marker="      gsap.timeline({ scrollTrigger: { trigger: '.date-scene'"
if marker not in t: sys.exit('ERROR: Nie znaleziono miejsca na animacje auta.')
t=t.replace(marker,road+marker,1)
tp.write_text(t,encoding='utf-8')

s=sp.read_text(encoding='utf-8'); s=re.sub(r'\n/\* v10 proposal, road and looping \*/.*\Z','',s,flags=re.S)
s+='''

/* v10 proposal, road and looping */
.proposal-scene__photo{display:block!important;visibility:visible!important;opacity:1;z-index:2;background:#120b09}.proposal-scene__photo img{display:block!important;visibility:visible!important;opacity:1!important;width:100%;height:100%;object-fit:cover;object-position:center 42%}.proposal-scene__copy{z-index:3}.ring-spark{animation:ringPulse 1.45s ease-in-out infinite}.ring-spark--two{animation-delay:.35s}.ring-spark--three{animation-delay:.7s}.ring-glint{animation:ringSweep 3.4s ease-in-out infinite}@keyframes ringPulse{0%,100%{transform:scale(.7) rotate(-8deg);opacity:.3}50%{transform:scale(1.25) rotate(8deg);opacity:1}}@keyframes ringSweep{0%,25%{transform:translateX(-180%) rotate(8deg);opacity:0}45%{opacity:.85}70%,100%{transform:translateX(220%) rotate(8deg);opacity:0}}
.road-scene{position:relative;min-height:100dvh;display:grid;place-items:center;overflow:hidden;isolation:isolate;background:linear-gradient(#8bb8d2 0 55%,#d4b37d 55% 68%,#302b29 68%);color:#fff7e9}.road-scene__sky{position:absolute;inset:0 0 32%;z-index:-3;background:linear-gradient(#79aecb,#d9cfb5)}.road-scene__sky i{position:absolute;width:9rem;height:2rem;border-radius:50%;background:#fff8;filter:blur(8px);animation:cloudDrive 9s linear infinite}.road-scene__sky i:nth-child(1){top:15%;left:8%}.road-scene__sky i:nth-child(2){top:28%;left:45%;animation-delay:-4s}.road-scene__sky i:nth-child(3){top:10%;right:5%;animation-delay:-7s}@keyframes cloudDrive{from{transform:translateX(-25vw)}to{transform:translateX(115vw)}}.road-scene__car{position:absolute;z-index:2;left:50%;top:37%;width:min(90vw,62rem);transform:translateX(-50%);filter:drop-shadow(0 1.8rem 1.2rem rgba(0,0,0,.48))}.road-scene__car img{display:block;width:100%;border-radius:1.4rem;clip-path:polygon(0 3%,100% 3%,100% 94%,0 94%)}.road-scene__copy{position:absolute;z-index:4;top:12%;text-align:center;text-shadow:0 .2rem 1rem #20323c}.road-scene__copy h2{margin:.7rem 0;font-size:clamp(3rem,8vw,7rem)}.road-scene__road{position:absolute;z-index:-1;inset:68% 0 0;background:#302b29;border-top:.35rem solid #e8d3a4}.road-scene__road span{position:absolute;top:52%;width:12rem;height:.55rem;background:#f1e2b9;animation:roadMotion 1.1s linear infinite}.road-scene__road span:nth-child(1){left:4%}.road-scene__road span:nth-child(2){left:42%}.road-scene__road span:nth-child(3){right:2%}@keyframes roadMotion{from{transform:translateX(45vw)}to{transform:translateX(-65vw)}}.road-scene__dust{position:absolute;z-index:1;left:9%;top:65%}.road-scene__dust i{position:absolute;width:1rem;height:1rem;border-radius:50%;background:#d5b78088;animation:dust 1.5s ease-out infinite}.road-scene__dust i:nth-child(2){animation-delay:.4s}.road-scene__dust i:nth-child(3){animation-delay:.8s}@keyframes dust{from{transform:translate(0,0) scale(.4);opacity:.8}to{transform:translate(-6rem,-2rem) scale(2);opacity:0}}
@media(max-width:760px){.proposal-scene__photo img{object-position:center 40%}.road-scene__car{top:42%;width:110vw}.road-scene__copy{top:10%;padding:0 1rem}.road-scene__copy h2{font-size:clamp(2.8rem,14vw,4.8rem)}}@media(prefers-reduced-motion:reduce){.ring-spark,.ring-glint,.road-scene__sky i,.road-scene__road span,.road-scene__dust i{animation:none!important}}
'''
sp.write_text(s,encoding='utf-8')
print('OK: zastosowano V10. Uruchom npm run build.')
