from pathlib import Path
import shutil

root = Path.cwd()
required = [
    root / 'src/app/app.component.html',
    root / 'src/app/app.component.scss',
    root / 'src/app/app.component.ts',
    root / 'src/index.html',
    root / 'public/images',
]
missing = [str(path) for path in required if not path.exists()]
if missing:
    raise SystemExit('Uruchom skrypt w katalogu głównym projektu. Brakuje: ' + ', '.join(missing))

package_dir = Path(__file__).resolve().parent
images = root / 'public/images'
for name in ['wedding-rings.png', 'karol-great-wall.jpg', 'karol-restaurant.jpg']:
    shutil.copy2(package_dir / 'assets' / name, images / name)

html_path = root / 'src/app/app.component.html'
html = html_path.read_text(encoding='utf-8')
html = html.replace('28 września 2026', '26 września 2026')
html = html.replace('28.09.2026', '26.09.2026')

old_rings = '''      <div class="bands" aria-hidden="true">
        <i class="band band--gold"></i><i class="band band--silver"></i>
      </div>'''
new_rings = '''      <div class="rings-photo" aria-hidden="true">
        <img src="/images/wedding-rings.png" alt="">
        <span class="rings-photo__shine"></span>
      </div>'''
if old_rings not in html:
    raise SystemExit('Nie znaleziono sekcji obrączek w app.component.html. Projekt różni się od przekazanej wersji.')
html = html.replace(old_rings, new_rings)

html = html.replace(
    'src="/images/karol.jpg" alt="Portret Karola podczas podróży"',
    'src="/images/karol-great-wall.jpg" alt="Karol na Wielkim Murze Chińskim"'
)
html = html.replace(
    'No dobrze, na zdjęciu jest Sfinks. W naszej historii na chwilę trafia jednak na Wielki Mur.',
    'Tym razem bez filmowych sztuczek. Karol naprawdę dotarł na Wielki Mur Chiński.'
)

anchor = '''        <article data-reveal><span>🤍</span><h3>Miłości na każdy dzień</h3><p>Spokojnej, mocnej i zawsze gotowej na kolejną wspólną przygodę.</p></article>'''
extra = '''
        <article data-reveal><span>🏠</span><h3>Domu pełnego ciepła</h3><p>Miejsca, do którego zawsze chce się wracać, niezależnie od pogody i korków.</p></article>
        <article data-reveal><span>☕</span><h3>Spokojnych poranków</h3><p>Z dobrą kawą, wolnym weekendem i bez pytania: „Co dzisiaj jemy?”.</p></article>
        <article data-reveal><span>🌍</span><h3>Wspólnych odkryć</h3><p>Od Wielkiego Muru po małe miejsca, które staną się tylko Wasze.</p></article>
        <article data-reveal><span>💪</span><h3>Siły na trudniejsze dni</h3><p>Bo we dwoje każdy problem jest mniejszy, a każda radość dwa razy większa.</p></article>
        <article data-reveal><span>🎉</span><h3>Mnóstwa dobrych ludzi</h3><p>Takich, którzy będą świętować sukcesy i przyniosą pizzę w kryzysie.</p></article>
        <article data-reveal><span>✨</span><h3>Spełnionych marzeń</h3><p>Tych wielkich, tych całkiem małych i tych jeszcze niewypowiedzianych.</p></article>'''
if 'Domu pełnego ciepła' not in html:
    if anchor not in html:
        raise SystemExit('Nie znaleziono ostatniego kafelka życzeń.')
    html = html.replace(anchor, anchor + extra)

# Restaurant memory between date-night and kiss scene.
restaurant_section = '''
    <section class="restaurant-scene">
      <div class="restaurant-scene__copy">
        <p class="kicker" data-reveal>Wspólna codzienność</p>
        <h2 data-reveal>Najlepsze historie mają też dobry smak.</h2>
        <p data-reveal>Podróże, kolacje i wszystkie małe chwile, które z czasem stają się najważniejsze.</p>
      </div>
      <figure class="restaurant-scene__photo" data-reveal>
        <img src="/images/karol-restaurant.jpg" alt="Karol podczas kolacji w restauracji" loading="lazy">
      </figure>
    </section>

'''
if 'class="restaurant-scene"' not in html:
    marker = '    <section class="kiss-scene chapter--center">'
    if marker not in html:
        raise SystemExit('Nie znaleziono sceny buziaka.')
    html = html.replace(marker, restaurant_section + marker)

html_path.write_text(html, encoding='utf-8')

index_path = root / 'src/index.html'
index = index_path.read_text(encoding='utf-8').replace('28.09.2026', '26.09.2026')
index_path.write_text(index, encoding='utf-8')

ts_path = root / 'src/app/app.component.ts'
ts = ts_path.read_text(encoding='utf-8')
old_timeline = '''        .from('.band--gold', { x: -160, rotation: -80, opacity: 0, duration: 1.65, ease: 'power3.out' }, '-=.6')
        .from('.band--silver', { x: 160, rotation: 80, opacity: 0, duration: 1.65, ease: 'power3.out' }, '<')
        .to('.bands', { scale: 1.06, duration: .7, yoyo: true, repeat: 1 })'''
new_timeline = '''        .from('.rings-photo', { y: 55, scale: .62, rotation: -7, opacity: 0, duration: 1.9, ease: 'power3.out' }, '-=.6')
        .to('.rings-photo', { scale: 1.055, duration: .75, yoyo: true, repeat: 1 })
        .fromTo('.rings-photo__shine', { xPercent: -170, opacity: 0 }, { xPercent: 190, opacity: .9, duration: 1.15, ease: 'power2.inOut' }, '-=1.15')'''
if old_timeline not in ts:
    raise SystemExit('Nie znaleziono starej animacji obrączek w app.component.ts.')
ts = ts.replace(old_timeline, new_timeline)
ts_path.write_text(ts, encoding='utf-8')

scss_path = root / 'src/app/app.component.scss'
scss = scss_path.read_text(encoding='utf-8')
scss += '''

/* Wedding story v2 */
.rings-photo{position:absolute;top:10%;display:grid;place-items:center;width:min(94vw,44rem);opacity:1;filter:drop-shadow(0 1.5rem 1.6rem #000c);overflow:hidden}
.rings-photo img{display:block;width:100%;height:auto;object-fit:contain;mix-blend-mode:screen}
.rings-photo__shine{position:absolute;inset:-20%;background:linear-gradient(105deg,transparent 38%,rgba(255,248,217,.8) 48%,transparent 58%);transform:translateX(-170%) rotate(10deg);mix-blend-mode:screen;filter:blur(6px);pointer-events:none}
.wall-scene__sky,.wall-scene__mountains,.wall-scene__wall{display:none}
.wall-scene{background:linear-gradient(90deg,#302215,#8e6848)}
.wall__karol{inset:0;width:100%;height:100%;max-width:none;object-fit:cover;object-position:center 36%;clip-path:none;filter:brightness(.82) saturate(.9)}
.wall-scene::after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(90deg,rgba(12,8,5,.82) 0 42%,rgba(12,8,5,.16) 72%)}
.wall-scene__copy{z-index:1;text-shadow:0 2px 20px #000}
.date-night__photo img,.signature__photo img,.future__picture>img{object-position:center 24%}
.restaurant-scene{position:relative;min-height:100dvh;padding:max(3rem,env(safe-area-inset-top)) clamp(1.25rem,5vw,5rem);display:grid;gap:2.5rem;align-items:center;background:#15100c}
.restaurant-scene__copy p:last-child{max-width:38rem;color:#c7b9aa;line-height:1.75}
.restaurant-scene__photo{margin:0;height:68dvh;overflow:hidden;border-radius:1.2rem 1.2rem 12rem 12rem;box-shadow:0 2rem 4rem #0008}
.restaurant-scene__photo img{width:100%;height:100%;object-fit:cover;object-position:center 24%}
.wish-grid{grid-template-columns:1fr}
@media(min-width:700px){.wish-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.restaurant-scene{grid-template-columns:1fr 1fr}.restaurant-scene__photo{height:78dvh}}
@media(min-width:1200px){.wish-grid{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media(max-width:600px){.rings-photo{top:14%;width:100vw}.intro__copy{margin-top:14rem}.wall-scene::after{background:linear-gradient(180deg,rgba(12,8,5,.78),rgba(12,8,5,.08) 56%,rgba(12,8,5,.38))}.wall-scene__copy{top:8%}.date-night__photo img,.signature__photo img,.future__picture>img{object-position:center 22%}}
'''
scss_path.write_text(scss, encoding='utf-8')

print('Aktualizacja v2 zastosowana.')
print('Dodano: realistyczne obrączki, Wielki Mur, restaurację, 10 życzeń, poprawione kadry i datę 26.09.2026.')
