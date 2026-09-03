from pathlib import Path
import re,shutil,sys
r=Path.cwd(); hp=r/'src/app/app.component.html'; sp=r/'src/app/app.component.scss'; tp=r/'src/app/app.component.ts'; images=r/'public/images'
if not all(p.exists() for p in (hp,sp,tp,images)): sys.exit('ERROR: Uruchom skrypt w katalogu glownym projektu.')
shutil.copy2(Path(__file__).parent/'assets/altar-clean.jpg',images/'altar-clean.jpg')
h=hp.read_text(encoding='utf-8')
# Ensure wedding date text is exact.
h=h.replace('28.09.2026','26.09.2026').replace('28 września 2026','26 września 2026')
# Extract date scene and relocate immediately after road scene.
m=re.search(r'\s*(<section class="date-scene">.*?</section>)',h,flags=re.S)
if not m: sys.exit('ERROR: Nie znaleziono slajdu date-scene.')
date=m.group(1); h=h[:m.start()]+h[m.end():]
road=re.search(r'<section class="road-scene">.*?</section>',h,flags=re.S)
if not road: sys.exit('ERROR: Nie znaleziono slajdu road-scene. Najpierw zastosuj V10.')
pos=road.end(); h=h[:pos]+'\n\n    '+date.strip()+h[pos:]
# Insert/replace altar scene after date scene.
altar='''

    <section class="altar-scene">
      <div class="altar-scene__photo" data-reveal><img src="/images/altar-clean.jpg" alt="Pamiątkowa scena przy ołtarzu" loading="lazy"><span class="altar-scene__light" aria-hidden="true"></span></div>
      <div class="altar-scene__copy" data-reveal><p class="kicker">I właśnie tutaj...</p><h2>rozpoczyna się ich następny rozdział.</h2><p>26 września 2026</p></div>
    </section>'''
if 'class="altar-scene"' in h:
 h=re.sub(r'\s*<section class="altar-scene">.*?</section>',altar,h,count=1,flags=re.S)
else:
 dm=re.search(r'<section class="date-scene">.*?</section>',h,flags=re.S)
 h=h[:dm.end()]+altar+h[dm.end():]
hp.write_text(h,encoding='utf-8')

t=tp.read_text(encoding='utf-8')
# Proposal image stays; remove any timeline that animates photo opacity/visibility.
t=re.sub(r"\n\s*gsap\.timeline\(\{ scrollTrigger: \{ trigger: '\.proposal-scene'.*?;\n",'\n',t,count=1,flags=re.S)
# Replace road timeline with right-to-left travel and persistent, centered copy.
t=re.sub(r"\n\s*gsap\.timeline\(\{ repeat: -1, repeatDelay: 1\.1, scrollTrigger: \{ trigger: '\.road-scene'.*?;\n",'\n',t,count=1,flags=re.S)
road_anim="""
      gsap.timeline({ repeat: -1, repeatDelay: 1.1, scrollTrigger: { trigger: '.road-scene', start: 'top 75%', end: 'bottom 25%', toggleActions: 'restart pause restart pause' } })
        .fromTo('.road-scene__car', { xPercent: 135, rotation: 1.5 }, { xPercent: 0, rotation: 0, duration: 2.25, ease: 'power2.out' })
        .fromTo('.road-scene__copy', { opacity: 0, y: 28 }, { opacity: 1, y: 0, duration: .8 }, '-=.55')
        .to('.road-scene__car', { xPercent: -135, duration: 2.1, ease: 'power2.in', delay: 1.4 })
        .to('.road-scene__copy', { opacity: 0, duration: .45 }, '-=1.25');

"""
marker="      gsap.timeline({ scrollTrigger: { trigger: '.kiss-scene'"
if marker not in t: marker="      gsap.timeline({ scrollTrigger: { trigger: '.date-scene'"
if marker not in t: sys.exit('ERROR: Nie znaleziono miejsca na poprawiona animacje auta.')
t=t.replace(marker,road_anim+marker,1)
tp.write_text(t,encoding='utf-8')

s=sp.read_text(encoding='utf-8'); s=re.sub(r'\n/\* v11 persistent proposal and altar \*/.*\Z','',s,flags=re.S)
s+='''

/* v11 persistent proposal and altar */
.proposal-scene__photo,.proposal-scene__photo[data-reveal]{opacity:1!important;visibility:visible!important;transform:none!important;display:block!important;align-self:center}.proposal-scene__photo img{opacity:1!important;visibility:visible!important;display:block!important}.proposal-scene__copy{display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center}.proposal-scene__copy h2,.proposal-scene__copy>p:last-child{margin-left:auto;margin-right:auto}.proposal-scene__copy h2{max-width:12ch}.proposal-scene__copy>p:last-child{text-align:center}
/* Drive toward the left, matching the direction of the car composition. */
.road-scene__car img{transform:scaleX(-1)}.road-scene__road span{animation-name:roadMotionLeft}@keyframes roadMotionLeft{from{transform:translateX(-55vw)}to{transform:translateX(65vw)}}.road-scene__dust{left:auto;right:9%}
/* Altar scene follows the wedding-date chapter. */
.altar-scene{position:relative;min-height:105dvh;padding:clamp(3rem,7vw,7rem) clamp(1.25rem,5vw,5rem);display:grid;grid-template-columns:minmax(0,1.1fr) minmax(22rem,.9fr);align-items:center;gap:clamp(2rem,6vw,6rem);overflow:hidden;background:#eee7de;color:#1c1713}
.altar-scene__photo{position:relative;height:min(84dvh,56rem);overflow:hidden;border-radius:14rem 14rem 1.2rem 1.2rem;background:#d8d2cb;box-shadow:0 2rem 4rem rgba(57,44,34,.25)}.altar-scene__photo img{width:100%;height:100%;object-fit:cover;object-position:center 48%;filter:contrast(1.025) saturate(.92)}.altar-scene__light{position:absolute;inset:-20%;background:linear-gradient(110deg,transparent 42%,rgba(255,255,240,.28) 49%,transparent 57%);animation:altarLight 5s ease-in-out infinite;mix-blend-mode:screen}@keyframes altarLight{0%,28%{transform:translateX(-120%)}70%,100%{transform:translateX(120%)}}.altar-scene__copy h2{margin:.8rem 0 1.4rem;max-width:12ch}.altar-scene__copy>p:last-child{color:#8a673d;font-weight:700;letter-spacing:.18em;text-transform:uppercase}
@media(max-width:760px){.proposal-scene__copy{padding-top:1rem}.road-scene__car img{transform:scaleX(-1)}.altar-scene{grid-template-columns:1fr;padding-block:4rem}.altar-scene__photo{height:72dvh}.altar-scene__copy{text-align:center}.altar-scene__copy h2{margin-left:auto;margin-right:auto}}
@media(prefers-reduced-motion:reduce){.altar-scene__light{animation:none!important}}
'''
sp.write_text(s,encoding='utf-8')
print('OK: zastosowano V11. Uruchom npm run build.')
