from pathlib import Path
import re, shutil, sys
r=Path.cwd(); hp=r/'src/app/app.component.html'; sp=r/'src/app/app.component.scss'; tp=r/'src/app/app.component.ts'
if not all(p.exists() for p in (hp,sp,tp,r/'public/images')):
    sys.exit('ERROR: Uruchom skrypt w katalogu glownym projektu.')
assets=Path(__file__).parent/'assets'
shutil.copy2(assets/'cats-memory.jpg',r/'public/images/cats-memory.jpg')
shutil.copy2(assets/'together-visible.png',r/'public/images/together-visible.png')

h=hp.read_text(encoding='utf-8')
# Remove the V5 Ania block placed outside the phone.
h=re.sub(r'\s*<aside class="swipe-ania".*?</aside>\s*','\n      ',h,count=1,flags=re.S)
# Keep the concise Tinder copy if an earlier edit changed it.
h=h.replace('Ania wykonuje<br><strong>ruch w prawo</strong>','')
# Replace relationship-date photo with a source where both faces are in the frame.
h=re.sub(r'(<figure class="together-date__photo">\s*<img src=")[^"]+("[^>]*>)',r'\1/images/together-visible.png\2',h,count=1,flags=re.S)
# Ensure exact official wording.
h=h.replace('Właśnie wtedy oficjalnie zostali parą.','15 lipca 2018 oficjalnie zostali parą.')
# Remove old date-night slide and insert memories slide with cats and travel placeholder.
memories='''
    <section class="memories-scene">
      <header class="memories-scene__header" data-reveal>
        <p class="kicker">Ich wspólna codzienność</p>
        <h2>Małe chwile.<br>Wielkie wspomnienia.</h2>
      </header>
      <article class="memory-card memory-card--cats" data-reveal>
        <img src="/images/cats-memory.jpg" alt="Domowe wspomnienie z kotami" loading="lazy">
        <div><span>Domowe historie</span><h3>Najlepszy odpoczynek ma czasem cztery łapy.</h3></div>
      </article>
      <article class="memory-card memory-card--travel memory-card--placeholder" data-reveal>
        <div class="memory-card__placeholder" aria-hidden="true">✦</div>
        <div><span>Wspólne podróże</span><h3>Tu pojawi się zdjęcie Ani z podróży.</h3><p>Plik docelowy: <code>public/images/ania-travel.jpg</code></p></div>
      </article>
    </section>

'''
pattern=r'\s*<section class="date-night">.*?</section>\s*(?=<section class="(?:restaurant-scene|kiss-scene))'
h,n=re.subn(pattern,'\n'+memories,h,count=1,flags=re.S)
if not n and 'class="memories-scene"' not in h:
    # Varying project: inject before restaurant/kiss.
    marker=re.search(r'\s*<section class="(?:restaurant-scene|kiss-scene)',h)
    if not marker: sys.exit('ERROR: Nie znaleziono slajdu randki ani kolejnej sceny.')
    h=h[:marker.start()]+'\n'+memories+h[marker.start():]
hp.write_text(h,encoding='utf-8')

# Remove animation step for the V5 Ania block.
t=tp.read_text(encoding='utf-8')
t=re.sub(r"\s*\.from\('\.swipe-ania'.*?\)\n",'\n',t,count=1)
tp.write_text(t,encoding='utf-8')

s=sp.read_text(encoding='utf-8')
s=re.sub(r'\n/\* v6 layout and memories \*/.*\Z','',s,flags=re.S)
s+='''

/* v6 layout and memories */
/* Great Wall copy moved right, away from the face. */
.wall-scene__copy{left:auto;right:clamp(1.25rem,5vw,5rem);top:14%;max-width:min(43vw,37rem);text-align:right;background:linear-gradient(270deg,rgba(8,6,4,.68),rgba(8,6,4,.12));padding:1.35rem 1.5rem}
.wall-scene__copy>p:last-child{margin-left:auto}
/* Return Tinder to the earlier simple composition, without Ania next to the phone. */
.swipe-scene{grid-template-columns:1fr;column-gap:0}.swipe-scene__copy{grid-column:auto}.phone{justify-self:center}
/* Relationship photo: show both faces, do not crop the top. */
.together-date__photo{background:#1c1713}.together-date__photo img{width:100%;height:100%;object-fit:contain;object-position:center;background:#1c1713}
/* New two-card memories section. */
.memories-scene{position:relative;min-height:110dvh;padding:clamp(4rem,8vw,8rem) clamp(1.25rem,5vw,5rem);display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:clamp(1rem,3vw,2.5rem);align-items:stretch;background:#eee3d3;color:#1d1712}
.memories-scene__header{grid-column:1/-1;text-align:center;margin-bottom:1rem}.memories-scene__header h2{margin:.8rem 0 1rem}
.memory-card{position:relative;min-height:70dvh;overflow:hidden;border-radius:1.5rem;background:#17120f;color:#fff;box-shadow:0 2rem 4rem rgba(48,32,19,.25)}
.memory-card>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center}
.memory-card::after{content:"";position:absolute;inset:0;background:linear-gradient(transparent 48%,rgba(5,4,3,.92))}
.memory-card>div:last-child{position:absolute;z-index:2;left:0;right:0;bottom:0;padding:clamp(1.4rem,4vw,2.5rem)}
.memory-card span{color:#e6b968;font-size:.68rem;font-weight:700;letter-spacing:.18em;text-transform:uppercase}.memory-card h3{margin:.65rem 0 0;font:clamp(1.8rem,4vw,3.3rem)/1.08 Georgia;font-weight:400}.memory-card p{color:#bfb5ab}.memory-card code{color:#efd09b}
.memory-card--cats>img{object-position:center 48%}
.memory-card--placeholder{background:radial-gradient(circle at 50% 32%,#705038,#17120f 70%)}.memory-card__placeholder{position:absolute!important;inset:0!important;display:grid;place-items:center;padding:0!important;color:#e6b968;font-size:7rem}
@media(max-width:760px){.wall-scene__copy{left:1rem;right:1rem;top:auto;bottom:5%;max-width:none;text-align:left;background:linear-gradient(90deg,rgba(8,6,4,.78),rgba(8,6,4,.22))}.wall-scene__copy>p:last-child{margin-left:0}.wall__karol{object-position:55% 18%}.memories-scene{grid-template-columns:1fr}.memory-card{min-height:68dvh}.together-date__photo{height:auto;min-height:55dvh}.together-date__photo img{height:auto;max-height:72dvh}}
'''
sp.write_text(s,encoding='utf-8')
print('OK: zastosowano V6. Uruchom npm run build.')
