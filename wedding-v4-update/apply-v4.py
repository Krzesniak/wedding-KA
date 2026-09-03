from pathlib import Path
import re, shutil, sys
root=Path.cwd(); hp=root/'src/app/app.component.html'; sp=root/'src/app/app.component.scss'; tp=root/'src/app/app.component.ts'; ip=root/'src/index.html'
if not all(p.exists() for p in (hp,sp,tp,ip,root/'public/images')): sys.exit('Uruchom skrypt w katalogu glownym projektu.')
assets=Path(__file__).parent/'assets'
for n in ('wedding-rings-clean.png','karol-2018.jpg','couple-anime-hug.png'): shutil.copy2(assets/n,root/'public/images'/n)
h=hp.read_text(encoding='utf-8').replace('28 września 2026','26 września 2026').replace('28.09.2026','26.09.2026')
# Rings, compatible with V1-V3
rings='''\n      <div class="rings-photo" aria-hidden="true"><img src="/images/wedding-rings-clean.png" alt=""><span class="rings-photo__shine"></span></div>'''
h,n=re.subn(r'\s*<div class="(?:bands|rings-photo)" aria-hidden="true">.*?</div>',rings,h,count=1,flags=re.S)
if not n: sys.exit('Nie znaleziono sekcji obraczek.')
# Story copy
h=h.replace('Gdzieś bardzo, bardzo daleko…','Był 2018 rok…')
h=h.replace('Karol był już prawie<br>na końcu świata.','Dwie różne drogi<br>miały za chwilę się spotkać.')
h=h.replace('No dobrze, na zdjęciu jest Sfinks. W naszej historii na chwilę trafia jednak na Wielki Mur.','Karol poznawał świat, nie wiedząc jeszcze, że najważniejsza podróż zacznie się całkiem niedługo.')
h=h.replace('Tym razem bez filmowych sztuczek. Karol naprawdę dotarł na Wielki Mur Chiński.','Karol poznawał świat, nie wiedząc jeszcze, że najważniejsza podróż zacznie się całkiem niedługo.')
# Match profile
h,n=re.subn(r'(<div class="profile-card">\s*)<img[^>]+>(\s*<div class="profile-card__caption">).*?(</div>)',r'\1<img src="/images/karol-2018.jpg" alt="Starsze zdjęcie Karola">\2<strong>Karol</strong><span>To wygląda obiecująco ✨</span>\3',h,count=1,flags=re.S)
if not n: sys.exit('Nie znaleziono karty Match.')
# Relationship date after match scene
if 'Razem od 15 lipca 2018' not in h:
 marker='    <section class="date-night">'
 date='''    <section class="together-date" data-reveal><span>Od tego dnia</span><strong>Razem od 15 lipca 2018</strong><i>♥</i></section>\n\n'''
 if marker not in h: sys.exit('Nie znaleziono miejsca na date zwiazku.')
 h=h.replace(marker,date+marker,1)
# Replace kiss scene with approach then crossfade to shared anime embrace.
hug='''\n    <section class="kiss-scene chapter--center">\n      <div class="hug-stage">\n        <div class="anime-character anime-character--ania"><img src="/images/ania-anime.png" alt="Stylizowana postać Ani"></div>\n        <div class="anime-character anime-character--karol"><img src="/images/karol-anime.png" alt="Stylizowana postać Karola"></div>\n        <div class="anime-hug-final"><img src="/images/couple-anime-hug.png" alt="Stylizowana para w objęciu"></div>\n        <div class="floating-hearts" aria-hidden="true"><span>♥</span><span>♥</span><span>♥</span><span>♥</span><i>✦</i><i>✦</i></div>\n      </div>\n      <p class="kicker" data-reveal>A później…</p><h2 data-reveal>już zawsze bliżej siebie.</h2><p data-reveal>Od pierwszego spotkania do wspólnej historii, która trwa do dziś.</p>\n    </section>\n\n    '''
h,n=re.subn(r'\s*<section class="kiss-scene chapter--center">.*?</section>\s*(?=<section class="date-scene">)',hug,h,count=1,flags=re.S)
if not n: sys.exit('Nie znaleziono sceny bliskosci.')
hp.write_text(h,encoding='utf-8'); ip.write_text(ip.read_text(encoding='utf-8').replace('28.09.2026','26.09.2026'),encoding='utf-8')
# TS: remove previous kiss timeline and insert robust hug animation
t=tp.read_text(encoding='utf-8')
t=re.sub(r"\n\s*gsap\.timeline\(\{ scrollTrigger: \{ trigger: '\.kiss-scene'.*?;\n",'\n',t,flags=re.S)
anim="""\n      gsap.timeline({ scrollTrigger: { trigger: '.kiss-scene', start: 'top 68%', once: true } })\n        .from('.anime-character--ania', { xPercent: -170, opacity: 0, duration: 1.25, ease: 'power3.out' })\n        .from('.anime-character--karol', { xPercent: 170, opacity: 0, duration: 1.25, ease: 'power3.out' }, '<')\n        .to('.anime-character--ania', { xPercent: 42, rotation: 2, duration: 1.1, ease: 'power2.inOut' })\n        .to('.anime-character--karol', { xPercent: -42, rotation: -2, duration: 1.1, ease: 'power2.inOut' }, '<')\n        .to('.anime-character', { opacity: 0, scale: .92, duration: .45 })\n        .fromTo('.anime-hug-final', { opacity: 0, scale: .82 }, { opacity: 1, scale: 1, duration: .8, ease: 'back.out(1.45)' }, '-=.25')\n        .from('.floating-hearts > *', { y: 45, scale: 0, opacity: 0, rotation: -25, duration: .75, stagger: .12, ease: 'back.out(2)' }, '-=.38')\n        .to('.floating-hearts span', { y: -18, duration: 1.3, yoyo: true, repeat: -1, stagger: .16, ease: 'sine.inOut' });\n\n"""
marker="      gsap.timeline({ scrollTrigger: { trigger: '.date-scene'"
if marker not in t: sys.exit('Nie znaleziono osi czasu animacji daty.')
tp.write_text(t.replace(marker,anim+marker,1),encoding='utf-8')
# CSS append idempotently
s=sp.read_text(encoding='utf-8'); s=re.sub(r'\n/\* v4 story corrections \*/.*\Z','',s,flags=re.S)
s+='''\n\n/* v4 story corrections */\n.rings-photo img{mix-blend-mode:normal}.profile-card img{object-position:center 28%}.together-date{min-height:55dvh;padding:4rem 1.5rem;display:grid;place-content:center;justify-items:center;text-align:center;background:#0b0807}.together-date span{color:var(--gold);font-size:.72rem;letter-spacing:.2em;text-transform:uppercase}.together-date strong{margin:.8rem 0;font:clamp(2.5rem,8vw,5.5rem)/1.05 Georgia;font-weight:400}.together-date i{color:#e75b74;font-size:2rem}.hug-stage{grid-column:1/-1;position:relative;width:min(96vw,64rem);height:clamp(22rem,67vw,42rem);margin-bottom:1.5rem}.anime-character,.anime-hug-final{position:absolute;inset:0;display:flex;align-items:flex-end}.anime-character img{width:clamp(15rem,45vw,31rem)}.anime-character--ania{justify-content:flex-start}.anime-character--karol{justify-content:flex-end}.anime-character--karol img{transform:scaleX(-1)}.anime-hug-final{z-index:2;justify-content:center;opacity:0}.anime-hug-final img{max-width:90%;max-height:100%;filter:drop-shadow(0 1.3rem 1.5rem #000b)}.floating-hearts{position:absolute;z-index:4;left:50%;top:8%;width:min(70%,28rem);height:45%;transform:translateX(-50%);color:#ec617d;pointer-events:none}.floating-hearts span,.floating-hearts i{position:absolute}.floating-hearts span:nth-child(1){left:8%;top:38%;font-size:2.2rem}.floating-hearts span:nth-child(2){left:31%;top:4%;font-size:1.5rem}.floating-hearts span:nth-child(3){right:25%;top:13%;font-size:2.8rem}.floating-hearts span:nth-child(4){right:5%;top:45%;font-size:1.7rem}.floating-hearts i:nth-of-type(1){left:18%;top:3%;color:#f4c36f;font-size:1.4rem}.floating-hearts i:nth-of-type(2){right:15%;top:2%;color:#f4c36f;font-size:1.8rem}@media(max-width:600px){.hug-stage{width:108vw;height:25rem}.anime-character img{width:17rem}.anime-hug-final img{max-width:96%}}\n'''
sp.write_text(s,encoding='utf-8')
print('OK: zastosowano V4. Uruchom npm run build.')
