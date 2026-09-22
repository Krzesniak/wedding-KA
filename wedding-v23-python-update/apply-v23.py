from pathlib import Path
import re
import shutil
import sys

root = Path.cwd()
html_path = root / 'src/app/app.component.html'
scss_path = root / 'src/app/app.component.scss'
images_dir = root / 'public/images'

required = [html_path, scss_path, images_dir]
missing = [str(path) for path in required if not path.exists()]
if missing:
    print('ERROR: Uruchom skrypt w glownym katalogu projektu wedding-story.')
    print('Brakuje:', ', '.join(missing))
    sys.exit(1)

assets = Path(__file__).resolve().parent / 'assets'
shutil.copy2(assets / 'car-full.png', images_dir / 'car-full.png')
shutil.copy2(assets / 'proposal-full.jpg', images_dir / 'proposal-full.jpg')

html = html_path.read_text(encoding='utf-8')

# 1. Replace the old car image with the complete transparent car image.
html, car_count = re.subn(
    r'src="/images/(?:car-couple|car-full)\.(?:jpg|png)"\s+alt="[^"]*"',
    'src="/images/car-full.png" alt="Samochód z parą"',
    html,
    count=1,
)
if car_count != 1:
    print('ERROR: Nie znaleziono obrazu samochodu w app.component.html.')
    sys.exit(1)

# 2. Normalize the proposal visuals. Supports both the old layout and rerunning V23.
proposal_visuals = '''      <div class="proposal-scene__visuals">
        <figure class="proposal-scene__person" data-reveal>
          <img src="/images/proposal-full.jpg" alt="Portret z pierścionkiem zaręczynowym" loading="lazy">
        </figure>
        <div class="proposal-scene__photo" data-reveal>
          <img src="/images/engagement-ring.jpg" alt="Dłoń z pierścionkiem zaręczynowym" loading="lazy">
          <span class="ring-spark ring-spark--one" aria-hidden="true">✦</span><span class="ring-spark ring-spark--two" aria-hidden="true">✦</span><span class="ring-spark ring-spark--three" aria-hidden="true">✧</span><i class="ring-glint" aria-hidden="true"></i>
        </div>
      </div>'''

if 'class="proposal-scene__visuals"' in html:
    pattern = re.compile(
        r'\s*<div class="proposal-scene__visuals">.*?</div>\s*</div>',
        re.S,
    )
    match = pattern.search(html)
    if not match:
        print('ERROR: Nie udalo sie odczytac istniejacej galerii zareczynowej.')
        sys.exit(1)
    html = html[:match.start()] + '\n' + proposal_visuals + html[match.end():]
else:
    old_photo = re.compile(
        r'\s*<div class="proposal-scene__photo" data-reveal>\s*'
        r'<img src="/images/engagement-ring\.jpg".*?'
        r'</div>',
        re.S,
    )
    html, proposal_count = old_photo.subn('\n' + proposal_visuals, html, count=1)
    if proposal_count != 1:
        print('ERROR: Nie znaleziono sekcji zdjęcia pierścionka.')
        sys.exit(1)

html_path.write_text(html, encoding='utf-8')

scss = scss_path.read_text(encoding='utf-8')
scss = re.sub(r'\n/\* v23 proposal gallery and complete car \*/.*\Z', '', scss, flags=re.S)
scss += r'''

/* v23 proposal gallery and complete car */
.proposal-scene{
  grid-template-columns:minmax(0,1.25fr) minmax(20rem,.75fr);
}
.proposal-scene__visuals{
  position:relative;
  display:grid;
  grid-template-columns:minmax(0,1fr) minmax(13rem,.52fr);
  align-items:end;
  gap:1rem;
  min-width:0;
}
.proposal-scene__person{
  position:relative;
  min-width:0;
  height:min(78dvh,52rem);
  margin:0;
  overflow:hidden;
  border-radius:1.4rem 1.4rem 9rem 9rem;
  background:#25140f;
  box-shadow:0 2rem 5rem rgba(0,0,0,.5);
}
.proposal-scene__person img{
  display:block;
  width:100%;
  height:100%;
  object-fit:cover;
  object-position:center 55%;
}
.proposal-scene__visuals .proposal-scene__photo{
  height:min(58dvh,38rem);
  margin:0 0 1.4rem -3.5rem;
  border:4px solid rgba(255,242,218,.82);
  border-radius:1.2rem 1.2rem 7rem 7rem;
  z-index:3;
}
.proposal-scene__copy{
  text-align:center;
  align-items:center;
}
.proposal-scene__copy h2,
.proposal-scene__copy>p:last-child{
  margin-left:auto;
  margin-right:auto;
}
.road-scene__car{
  width:min(80vw,70rem);
  filter:drop-shadow(0 1.5rem 1rem rgba(0,0,0,.48));
}
.road-scene__car img{
  display:block;
  width:100%;
  height:auto;
  object-fit:contain;
  clip-path:none;
  border-radius:0;
  transform:none!important;
}
@media(max-width:760px){
  .proposal-scene{
    display:flex!important;
    flex-direction:column!important;
    padding:3.5rem 1rem!important;
    gap:1.5rem!important;
  }
  .proposal-scene__visuals{
    order:1;
    width:min(100%,28rem);
    margin:0 auto;
    grid-template-columns:1fr;
    gap:.85rem;
  }
  .proposal-scene__person{
    width:100%;
    height:auto;
    aspect-ratio:2/3;
    border-radius:1rem 1rem 5rem 5rem;
  }
  .proposal-scene__person img{
    object-position:center center;
  }
  .proposal-scene__visuals .proposal-scene__photo{
    width:58%!important;
    height:auto!important;
    aspect-ratio:3/4!important;
    margin:-8.5rem .75rem 0 auto!important;
    border-width:3px;
    border-radius:.9rem .9rem 3rem 3rem;
  }
  .proposal-scene__copy{
    order:2;
  }
  .road-scene__car{
    top:45%!important;
    width:88vw!important;
    max-width:88vw!important;
  }
  .road-scene__car img{
    transform:none!important;
  }
}
'''
scss_path.write_text(scss, encoding='utf-8')

print('OK: zastosowano V23 Python update.')
print('Dodano:')
print('  public/images/car-full.png')
print('  public/images/proposal-full.jpg')
print('Zmieniono:')
print('  src/app/app.component.html')
print('  src/app/app.component.scss')
print('Uruchom teraz: npm run build && npm start')
