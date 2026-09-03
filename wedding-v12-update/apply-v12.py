from pathlib import Path
import re, shutil, sys
r=Path.cwd(); hp=r/'src/app/app.component.html'; sp=r/'src/app/app.component.scss'; tp=r/'src/app/app.component.ts'; images=r/'public/images'
if not all(p.exists() for p in (hp,sp,tp,images)):
    sys.exit('ERROR: Uruchom skrypt w katalogu glownym projektu.')
shutil.copy2(Path(__file__).parent/'assets/newlyweds.jpg', images/'newlyweds.jpg')

h=hp.read_text(encoding='utf-8')
celebration='''
    <section class="newlyweds-scene">
      <img src="/images/newlyweds.jpg" alt="Pamiątkowy portret pary" loading="lazy">
      <div class="newlyweds-scene__shade"></div>
      <div class="newlyweds-scene__petals" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
      <div class="newlyweds-scene__copy" data-reveal><p>26 września 2026</p><h2>Niech żyje para młoda!</h2></div>
    </section>

'''
# Replace on rerun, otherwise insert directly before wishes.
if 'class="newlyweds-scene"' in h:
    h=re.sub(r'\s*<section class="newlyweds-scene">.*?</section>\s*','\n'+celebration,h,count=1,flags=re.S)
else:
    marker=re.search(r'\s*<section class="wishes">',h)
    if not marker: sys.exit('ERROR: Nie znaleziono sekcji wishes.')
    h=h[:marker.start()]+'\n'+celebration+h[marker.start():]

# Add the requested wish only once.
requested='''
        <article data-reveal><span>🔍</span><h3>Żeby Karol zawsze szybko się znajdywał</h3><p>Zwłaszcza gdy z ust Ani padnie: „Gdzie jest Karol?”.</p></article>'''
if 'Gdzie jest Karol?' not in h:
    grid_end=h.find('</div>', h.find('class="wish-grid"'))
    if grid_end<0: sys.exit('ERROR: Nie znaleziono konca wish-grid.')
    h=h[:grid_end]+requested+'\n      '+h[grid_end:]

# Convert each wish article into an accessible clickable mini-letter.
section_match=re.search(r'(<div class="wish-grid">)(.*?)(</div>\s*</section>)',h,flags=re.S)
if not section_match: sys.exit('ERROR: Nie znaleziono wish-grid.')
body=section_match.group(2)
article_re=re.compile(r'<article data-reveal>\s*<span>(.*?)</span>\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>\s*</article>',re.S)
def convert(m):
    icon,title,text=[x.strip() for x in m.groups()]
    return f'''<details class="wish-letter" data-reveal>
          <summary><span class="wish-letter__seal">{icon}</span><span class="wish-letter__title">{title}</span><span class="wish-letter__hint">Otwórz list</span></summary>
          <div class="wish-letter__paper"><p>{text}</p><span class="wish-letter__signature">Dla Was ♥</span></div>
        </details>'''
body,count=article_re.subn(convert,body)
if count==0 and 'class="wish-letter"' not in body:
    sys.exit('ERROR: Nie znaleziono kafelkow zyczen do konwersji.')
h=h[:section_match.start(2)]+body+h[section_match.end(2):]
hp.write_text(h,encoding='utf-8')

# Add subtle entrance animation for the new slide without controlling its persistent visibility.
t=tp.read_text(encoding='utf-8')
if "'.newlyweds-scene__copy'" not in t:
    anim="""
      gsap.from('.newlyweds-scene__copy', {
        opacity: 0, y: 45, scale: .94, duration: 1.15, ease: 'power3.out',
        scrollTrigger: { trigger: '.newlyweds-scene', start: 'top 72%', toggleActions: 'restart pause restart pause' }
      });

"""
    marker="      gsap.timeline({ scrollTrigger: { trigger: '.date-scene'"
    if marker not in t: marker="      gsap.utils.toArray<HTMLElement>('[data-reveal]')"
    if marker not in t: sys.exit('ERROR: Nie znaleziono miejsca na animacje nowego slajdu.')
    t=t.replace(marker,anim+marker,1)
tp.write_text(t,encoding='utf-8')

s=sp.read_text(encoding='utf-8'); s=re.sub(r'\n/\* v12 newlyweds and autumn letters \*/.*\Z','',s,flags=re.S)
s+='''

/* v12 newlyweds and autumn letters */
.newlyweds-scene{position:relative;min-height:100dvh;display:grid;place-items:center;overflow:hidden;isolation:isolate;background:#1a110c;color:#fff5e7}
.newlyweds-scene>img{position:absolute;z-index:-3;inset:0;width:100%;height:100%;object-fit:cover;object-position:center 42%;filter:saturate(.96) contrast(1.04)}
.newlyweds-scene__shade{position:absolute;z-index:-2;inset:0;background:linear-gradient(180deg,rgba(20,10,5,.1),rgba(20,10,5,.28) 55%,rgba(20,10,5,.72))}
.newlyweds-scene__copy{text-align:center;padding:2rem;text-shadow:0 .25rem 1.4rem #170b05}.newlyweds-scene__copy p{margin:0;color:#f1c878;font-size:.75rem;font-weight:700;letter-spacing:.22em;text-transform:uppercase}.newlyweds-scene__copy h2{max-width:12ch;margin:1rem auto 0;font-size:clamp(3.8rem,11vw,9rem)}
.newlyweds-scene__petals{position:absolute;z-index:2;inset:0;pointer-events:none}.newlyweds-scene__petals i{position:absolute;top:-8%;width:.8rem;height:1.25rem;border-radius:80% 10% 70% 20%;background:#c86d39;animation:petalFall 7s linear infinite}.newlyweds-scene__petals i:nth-child(2n){background:#e0a34f}.newlyweds-scene__petals i:nth-child(3n){background:#934b31}.newlyweds-scene__petals i:nth-child(1){left:7%;animation-delay:-1s}.newlyweds-scene__petals i:nth-child(2){left:19%;animation-delay:-5s}.newlyweds-scene__petals i:nth-child(3){left:34%;animation-delay:-3s}.newlyweds-scene__petals i:nth-child(4){left:48%;animation-delay:-6s}.newlyweds-scene__petals i:nth-child(5){left:62%;animation-delay:-2s}.newlyweds-scene__petals i:nth-child(6){left:74%;animation-delay:-4s}.newlyweds-scene__petals i:nth-child(7){left:87%;animation-delay:-.5s}.newlyweds-scene__petals i:nth-child(8){left:95%;animation-delay:-5.5s}@keyframes petalFall{0%{transform:translate3d(0,-10vh,0) rotate(0);opacity:0}12%{opacity:.9}55%{transform:translate3d(4rem,55vh,0) rotate(280deg)}100%{transform:translate3d(-2rem,112vh,0) rotate(620deg);opacity:.15}}
.wishes{position:relative;background:radial-gradient(circle at 50% 0,#f5ead8,#dbc4a3 76%);overflow:hidden}.wishes::before,.wishes::after{content:"❦";position:absolute;color:rgba(126,69,37,.18);font:clamp(10rem,22vw,23rem) Georgia}.wishes::before{left:-3rem;top:8rem;transform:rotate(-24deg)}.wishes::after{right:-3rem;bottom:1rem;transform:rotate(156deg)}.wishes header,.wish-grid{position:relative;z-index:2}
.wish-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1.25rem;align-items:start}.wish-letter{background:transparent}.wish-letter summary{position:relative;min-height:15rem;padding:2.2rem 1.6rem 1.5rem;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;list-style:none;cursor:pointer;border:1px solid #b99367;border-radius:.45rem;background:linear-gradient(145deg,#f7ead3,#e1c39b);box-shadow:0 1rem 2rem rgba(76,47,25,.15);transition:transform .25s ease,box-shadow .25s ease}.wish-letter summary::-webkit-details-marker{display:none}.wish-letter summary::before,.wish-letter summary::after{content:"";position:absolute;top:0;width:50%;height:48%;border-bottom:1px solid rgba(127,83,46,.3)}.wish-letter summary::before{left:0;transform:skewY(28deg);transform-origin:left top}.wish-letter summary::after{right:0;transform:skewY(-28deg);transform-origin:right top}.wish-letter summary:hover{transform:translateY(-5px) rotate(-.35deg);box-shadow:0 1.4rem 2.4rem rgba(76,47,25,.23)}.wish-letter__seal{position:relative;z-index:2;display:grid;place-items:center;width:3.5rem;aspect-ratio:1;margin-bottom:1rem;border-radius:50%;background:#8e3f32;color:#fff6e8;box-shadow:0 .35rem .7rem rgba(73,31,25,.28);font-size:1.35rem}.wish-letter__title{position:relative;z-index:2;font:1.45rem/1.15 Georgia;color:#2f2016}.wish-letter__hint{position:relative;z-index:2;margin-top:1rem;color:#8a5d38;font-size:.66rem;font-weight:700;letter-spacing:.16em;text-transform:uppercase}.wish-letter__paper{margin:-.35rem .65rem 0;padding:1.6rem 1.4rem 1.35rem;border:1px solid #c9a978;border-top:0;border-radius:0 0 .45rem .45rem;background:#fff8e9;color:#49372a;box-shadow:0 1rem 1.5rem rgba(76,47,25,.12);animation:letterOpen .38s ease-out}.wish-letter__paper p{margin:0!important;color:#49372a!important}.wish-letter__signature{display:block;margin-top:1.2rem;color:#9a5a42;font:italic 1rem Georgia;text-align:right}@keyframes letterOpen{from{opacity:0;transform:translateY(-1.2rem) scaleY(.75)}to{opacity:1;transform:none}}.wish-letter[open] summary{border-radius:.45rem .45rem 0 0}.wish-letter[open] .wish-letter__hint{font-size:0}.wish-letter[open] .wish-letter__hint::after{content:"Zamknij list";font-size:.66rem}
@media(max-width:1050px){.wish-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:650px){.newlyweds-scene>img{object-position:center}.wish-grid{grid-template-columns:1fr}.wish-letter summary{min-height:13rem}}
@media(prefers-reduced-motion:reduce){.newlyweds-scene__petals i{animation:none!important}.wish-letter__paper{animation:none}}
'''
sp.write_text(s,encoding='utf-8')
print('OK: zastosowano V12. Uruchom npm run build.')
