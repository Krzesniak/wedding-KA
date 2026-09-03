from pathlib import Path
import re, shutil, sys
root=Path.cwd()
html_path=root/'src/app/app.component.html'
scss_path=root/'src/app/app.component.scss'
ts_path=root/'src/app/app.component.ts'
images=root/'public/images'
if not all(path.exists() for path in (html_path,scss_path,ts_path,images)):
    sys.exit('ERROR: Uruchom skrypt w katalogu glownym projektu.')
assets=Path(__file__).resolve().parent/'assets'
shutil.copy2(assets/'engagement-ring.jpg',images/'engagement-ring.jpg')

html=html_path.read_text(encoding='utf-8')
# Remove complete restaurant/crab slide, regardless of earlier V2/V8 formatting.
html,count=re.subn(r'\s*<section class="restaurant-scene">.*?</section>\s*','\n',html,count=1,flags=re.S)
# New proposal slide after memories, before closeness scene.
proposal='''
    <section class="proposal-scene">
      <div class="proposal-scene__photo" data-reveal>
        <img src="/images/engagement-ring.jpg" alt="Dłoń z pierścionkiem zaręczynowym" loading="lazy">
        <span class="ring-spark ring-spark--one" aria-hidden="true">✦</span>
        <span class="ring-spark ring-spark--two" aria-hidden="true">✦</span>
        <span class="ring-spark ring-spark--three" aria-hidden="true">✧</span>
        <i class="ring-glint" aria-hidden="true"></i>
      </div>
      <div class="proposal-scene__copy">
        <p class="kicker" data-reveal>Kolejny wielki krok</p>
        <h2 data-reveal>Aż w końcu przyszedł czas na wyczekiwane „TAK”!!!</h2>
        <p data-reveal>Jedno pytanie, jeden pierścionek i odpowiedź, która rozpoczęła następny rozdział.</p>
      </div>
    </section>

'''
# Ensure idempotence by replacing existing proposal or inserting it.
if 'class="proposal-scene"' in html:
    html=re.sub(r'\s*<section class="proposal-scene">.*?</section>\s*','\n'+proposal,html,count=1,flags=re.S)
else:
    marker=re.search(r'\s*<section class="kiss-scene',html)
    if not marker:
        marker=re.search(r'\s*<section class="date-scene',html)
    if not marker:
        sys.exit('ERROR: Nie znaleziono miejsca na slajd zareczyn.')
    html=html[:marker.start()]+'\n'+proposal+html[marker.start():]
html_path.write_text(html,encoding='utf-8')

# GSAP sparkle sequence, safe on rerun.
ts=ts_path.read_text(encoding='utf-8')
ts=re.sub(r"\n\s*gsap\.timeline\(\{ scrollTrigger: \{ trigger: '\.proposal-scene'.*?;\n",'\n',ts,count=1,flags=re.S)
animation="""
      gsap.timeline({ scrollTrigger: { trigger: '.proposal-scene', start: 'top 68%', once: true } })
        .from('.proposal-scene__photo', { opacity: 0, scale: .93, y: 45, duration: 1.15, ease: 'power3.out' })
        .from('.ring-spark', { opacity: 0, scale: 0, rotation: -90, duration: .6, stagger: .14, ease: 'back.out(2.4)' }, '-=.45')
        .fromTo('.ring-glint', { xPercent: -180, opacity: 0 }, { xPercent: 220, opacity: .95, duration: 1.25, ease: 'power2.inOut' }, '-=.5')
        .to('.ring-spark', { scale: 1.25, opacity: .45, duration: .85, yoyo: true, repeat: -1, stagger: .16, ease: 'sine.inOut' });

"""
marker="      gsap.timeline({ scrollTrigger: { trigger: '.kiss-scene'"
if marker not in ts:
    marker="      gsap.timeline({ scrollTrigger: { trigger: '.date-scene'"
if marker not in ts:
    sys.exit('ERROR: Nie znaleziono miejsca na animacje zareczyn.')
ts=ts.replace(marker,animation+marker,1)
ts_path.write_text(ts,encoding='utf-8')

scss=scss_path.read_text(encoding='utf-8')
scss=re.sub(r'\n/\* v9 cats and proposal \*/.*\Z','',scss,flags=re.S)
scss+='''

/* v9 cats and proposal */
/* Keep the cat and face visible by moving the caption into a compact top panel. */
.memory-card--cats>img{object-position:center 47%;filter:brightness(.92)}
.memory-card--cats::after{background:linear-gradient(180deg,rgba(4,4,3,.72),transparent 38%,rgba(4,4,3,.08))}
.memory-card--cats>div:last-child{top:0;bottom:auto;max-width:78%;padding:1.35rem 1.5rem;background:linear-gradient(135deg,rgba(10,8,6,.78),rgba(10,8,6,.12));border-radius:0 0 1.1rem 0}
.memory-card--cats h3{font-size:clamp(1.5rem,2.7vw,2.5rem);max-width:16ch}
/* New engagement slide. */
.proposal-scene{position:relative;min-height:100dvh;padding:clamp(3rem,7vw,7rem) clamp(1.25rem,5vw,5rem);display:grid;grid-template-columns:minmax(0,1.1fr) minmax(22rem,.9fr);align-items:center;gap:clamp(2rem,6vw,6rem);overflow:hidden;background:radial-gradient(circle at 30% 48%,#542b22,#160c0b 52%,#080505);color:#fff0df}
.proposal-scene__photo{position:relative;height:min(78dvh,52rem);overflow:hidden;border-radius:1.4rem 1.4rem 12rem 12rem;box-shadow:0 2rem 5rem rgba(0,0,0,.58);isolation:isolate}
.proposal-scene__photo::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 62%,rgba(16,7,7,.34));pointer-events:none}
.proposal-scene__photo img{width:100%;height:100%;object-fit:cover;object-position:center 43%;filter:saturate(1.03) contrast(1.03)}
.proposal-scene__copy{position:relative;z-index:2}.proposal-scene__copy h2{margin:.8rem 0 1.6rem;max-width:12ch}.proposal-scene__copy>p:last-child{max-width:34rem;color:#cfbdb3;line-height:1.75}
.ring-spark{position:absolute;z-index:4;color:#fff2bc;text-shadow:0 0 .7rem #fff,0 0 1.5rem #ffcf68;pointer-events:none}.ring-spark--one{left:43%;top:34%;font-size:3rem}.ring-spark--two{left:50%;top:29%;font-size:1.7rem}.ring-spark--three{left:37%;top:39%;font-size:1.35rem}
.ring-glint{position:absolute;z-index:3;inset:-25%;background:linear-gradient(110deg,transparent 43%,rgba(255,247,208,.65) 49%,transparent 55%);transform:translateX(-180%) rotate(8deg);mix-blend-mode:screen;filter:blur(8px);pointer-events:none}
@media(max-width:760px){.memory-card--cats>img{object-position:center 45%}.memory-card--cats>div:last-child{max-width:92%;padding:1rem 1.15rem}.proposal-scene{grid-template-columns:1fr;padding-block:4rem}.proposal-scene__photo{height:64dvh;order:1}.proposal-scene__copy{order:2;text-align:center}.proposal-scene__copy h2,.proposal-scene__copy>p:last-child{margin-left:auto;margin-right:auto}.ring-spark--one{left:42%;top:35%}.ring-spark--two{left:51%;top:30%}.ring-spark--three{left:35%;top:40%}}
@media(prefers-reduced-motion:reduce){.ring-spark{animation:none!important}}
'''
scss_path.write_text(scss,encoding='utf-8')
print('OK: zastosowano V9. Uruchom npm run build.')
