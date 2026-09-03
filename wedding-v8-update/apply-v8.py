from pathlib import Path
import re, shutil, sys
from PIL import Image, ImageEnhance, ImageFilter

root=Path.cwd()
html_path=root/'src/app/app.component.html'
scss_path=root/'src/app/app.component.scss'
ts_path=root/'src/app/app.component.ts'
images=root/'public/images'
if not all(p.exists() for p in (html_path,scss_path,ts_path,images)):
    sys.exit('ERROR: Uruchom skrypt w katalogu glownym projektu.')

assets=Path(__file__).resolve().parent/'assets'
# Prepare underwater photo for browser use.
sea=Image.open(assets/'ania-sea.png').convert('RGB')
sea=sea.resize((1260,1060),Image.Resampling.LANCZOS)
sea=ImageEnhance.Contrast(sea).enhance(1.05)
sea=ImageEnhance.Color(sea).enhance(1.08)
sea=ImageEnhance.Sharpness(sea).enhance(1.18)
sea.save(images/'ania-sea.jpg',quality=93,optimize=True)

# Clean the existing V7 young photo by removing the narrow left/right UI zones.
young_path=images/'together-young-2018.jpg'
if young_path.exists():
    young=Image.open(young_path).convert('RGB')
    w,h=young.size
    young=young.crop((int(w*.105),int(h*.025),int(w*.895),int(h*.975)))
    young=young.resize((1100,1320),Image.Resampling.LANCZOS)
    young=young.filter(ImageFilter.UnsharpMask(radius=1.2,percent=105,threshold=3))
    young=ImageEnhance.Contrast(young).enhance(1.035)
    young=ImageEnhance.Color(young).enhance(1.035)
    young.save(images/'together-young-2018-clean.jpg',quality=94,optimize=True)
else:
    sys.exit('ERROR: Brakuje public/images/together-young-2018.jpg. Najpierw zastosuj V7.')

html=html_path.read_text(encoding='utf-8')
html=html.replace('/images/together-young-2018.jpg','/images/together-young-2018-clean.jpg')
# Enrich date decorations while remaining idempotent.
hearts='''<div class="date-hearts" aria-hidden="true">
        <span>♥</span><span>♥</span><span>♥</span><span>♥</span><span>♥</span><span>♥</span>
        <span>♥</span><span>♥</span><span>♥</span><span>♥</span><span>♥</span><span>♥</span>
      </div>
      <div class="date-confetti" aria-hidden="true">
        <i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i>
      </div>'''
html,n=re.subn(r'<div class="date-hearts".*?</div>',hearts,html,count=1,flags=re.S)
if not n: sys.exit('ERROR: Nie znaleziono serduszek slajdu z data.')
# Add lead line above existing memories kicker.
if 'I tak płynął im czas...' not in html:
    html=html.replace('<header class="memories-scene__header" data-reveal>','<header class="memories-scene__header" data-reveal>\n        <p class="memories-scene__lead">I tak płynął im czas...</p>',1)
# Replace right placeholder with sea photo.
travel='''<article class="memory-card memory-card--travel" data-reveal>
        <img src="/images/ania-sea.jpg" alt="Podwodne zdjęcie z podróży" loading="lazy">
        <div><span>Wspólne podróże</span><h3>Razem odkrywali świat, także ten ukryty pod powierzchnią.</h3></div>
      </article>'''
html,n=re.subn(r'<article class="memory-card memory-card--travel[^>]*>.*?</article>',travel,html,count=1,flags=re.S)
if not n: sys.exit('ERROR: Nie znaleziono prawego kafla wspolnych podrozy.')
html_path.write_text(html,encoding='utf-8')

# GSAP: animate both hearts and confetti, replacing previous date-hearts animation.
ts=ts_path.read_text(encoding='utf-8')
ts=re.sub(r"\n\s*gsap\.from\('\.date-hearts span'.*?\n\s*\}\);",'',ts,count=1,flags=re.S)
anim="""
      gsap.timeline({ scrollTrigger: { trigger: '.together-date', start: 'top 72%', once: true } })
        .from('.date-hearts span', { y: 100, opacity: 0, scale: .25, rotation: -30, duration: 1, stagger: .08, ease: 'back.out(1.8)' })
        .from('.date-confetti i', { y: -90, opacity: 0, rotation: -180, duration: 1.25, stagger: .055, ease: 'power2.out' }, '-=.75');

"""
marker="      gsap.timeline({ scrollTrigger: { trigger: '.date-scene'"
if marker not in ts: sys.exit('ERROR: Nie znaleziono animacji daty slubu.')
ts=ts.replace(marker,anim+marker,1)
ts_path.write_text(ts,encoding='utf-8')

scss=scss_path.read_text(encoding='utf-8')
scss=re.sub(r'\n/\* v8 celebration and memories \*/.*\Z','',scss,flags=re.S)
scss+='''

/* v8 celebration and memories */
.together-date__photo{overflow:hidden;background:#211a15}
.together-date__photo img{width:100%;height:100%;object-fit:contain;object-position:center;background:#211a15;filter:saturate(1.04) contrast(1.025)}
.date-hearts{z-index:1}.date-hearts span{filter:drop-shadow(0 .25rem .3rem rgba(94,39,48,.13))}
.date-hearts span:nth-child(7){left:3%;top:42%;font-size:1.15rem;animation-delay:.25s}.date-hearts span:nth-child(8){left:36%;bottom:7%;font-size:2.5rem;animation-delay:.9s}.date-hearts span:nth-child(9){left:58%;top:5%;font-size:1.7rem;animation-delay:1.4s}.date-hearts span:nth-child(10){right:3%;top:48%;font-size:1.15rem;animation-delay:1.9s}.date-hearts span:nth-child(11){right:29%;bottom:5%;font-size:2.1rem;animation-delay:2.4s}.date-hearts span:nth-child(12){left:48%;top:48%;font-size:1rem;animation-delay:2.9s}
.date-confetti{position:absolute;z-index:1;inset:0;pointer-events:none;overflow:hidden}.date-confetti i{position:absolute;width:.55rem;height:1rem;border-radius:.15rem;background:#d8a64d;animation:confettiFall 5.6s linear infinite}.date-confetti i:nth-child(3n){background:#c94968}.date-confetti i:nth-child(3n+1){background:#f1d59e}.date-confetti i:nth-child(1){left:5%;top:8%;animation-delay:-1s}.date-confetti i:nth-child(2){left:14%;top:60%;animation-delay:-3s}.date-confetti i:nth-child(3){left:25%;top:18%;animation-delay:-4.5s}.date-confetti i:nth-child(4){left:35%;top:78%;animation-delay:-2s}.date-confetti i:nth-child(5){left:44%;top:9%;animation-delay:-5s}.date-confetti i:nth-child(6){left:54%;top:70%;animation-delay:-.5s}.date-confetti i:nth-child(7){left:63%;top:20%;animation-delay:-3.4s}.date-confetti i:nth-child(8){left:72%;top:82%;animation-delay:-1.7s}.date-confetti i:nth-child(9){left:81%;top:11%;animation-delay:-4s}.date-confetti i:nth-child(10){left:90%;top:58%;animation-delay:-2.7s}.date-confetti i:nth-child(11){left:96%;top:24%;animation-delay:-5.2s}.date-confetti i:nth-child(12){left:48%;top:35%;animation-delay:-1.3s}@keyframes confettiFall{0%{transform:translateY(-5rem) rotate(0deg);opacity:0}12%{opacity:.78}88%{opacity:.65}100%{transform:translateY(18rem) rotate(540deg);opacity:0}}
.together-date__photo,.together-date__copy{z-index:3}
.memories-scene__lead{margin:0 0 .65rem;color:#8f6334;font:italic clamp(1.2rem,2vw,1.8rem) Georgia;letter-spacing:.03em}.memory-card--cats>img{object-position:center 54%}.memory-card--travel>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center}.memory-card--travel::after{background:linear-gradient(transparent 42%,rgba(4,18,25,.9))}.memory-card--travel span{color:#f1c66f}
@media(max-width:760px){.together-date__photo img{height:auto;max-height:none}.memory-card--cats>img{object-position:center 50%}.memory-card--travel>img{object-position:center}}
@media(prefers-reduced-motion:reduce){.date-hearts span,.date-confetti i{animation:none!important}}
'''
scss_path.write_text(scss,encoding='utf-8')
print('OK: zastosowano V8. Uruchom npm run build.')
