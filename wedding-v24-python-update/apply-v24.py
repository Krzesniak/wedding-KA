from pathlib import Path
import re
import shutil
import sys

root = Path.cwd()
html_path = root / 'src/app/app.component.html'
scss_path = root / 'src/app/app.component.scss'
images_dir = root / 'public/images'
video_dir = root / 'public/video'

missing = [str(p) for p in (html_path, scss_path, images_dir) if not p.exists()]
if missing:
    print('ERROR: Uruchom skrypt w glownym katalogu projektu wedding-story.')
    print('Brakuje:', ', '.join(missing))
    sys.exit(1)

assets = Path(__file__).resolve().parent / 'assets'
video_dir.mkdir(parents=True, exist_ok=True)
shutil.copy2(assets / 'blogoslawienstwo.mp4', video_dir / 'blogoslawienstwo.mp4')
shutil.copy2(assets / 'car-full-tight.png', images_dir / 'car-full-tight.png')

html = html_path.read_text(encoding='utf-8')

# Use a tightly cropped transparent car, so the wheels sit visibly on the road.
html, car_count = re.subn(
    r'src="/images/(?:car-couple\.jpg|car-full(?:-tight)?\.png)"\s+alt="[^"]*"',
    'src="/images/car-full-tight.png" alt="Samochód z parą"',
    html,
    count=1,
)
if car_count != 1:
    print('ERROR: Nie znaleziono zdjęcia samochodu. Najpierw zastosuj V23.')
    sys.exit(1)

video_section = '''

    <section class="blessing-scene">
      <div class="blessing-scene__ornament" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
      <header class="blessing-scene__copy" data-reveal>
        <p class="kicker">Na wspólną drogę</p>
        <h2>Błogosławieństwa Bożego!</h2>
      </header>
      <div class="blessing-video" data-reveal>
        <video controls preload="metadata" playsinline>
          <source src="/video/blogoslawienstwo.mp4" type="video/mp4">
          Twoja przeglądarka nie obsługuje odtwarzania filmu.
        </video>
        <span class="blessing-video__frame" aria-hidden="true"></span>
      </div>
    </section>'''

# Replace on rerun, otherwise insert directly after the full package section.
if 'class="blessing-scene"' in html:
    html = re.sub(
        r'\s*<section class="blessing-scene">.*?</section>',
        video_section,
        html,
        count=1,
        flags=re.S,
    )
else:
    future = re.search(r'<section class="future">.*?</section>', html, flags=re.S)
    if not future:
        print('ERROR: Nie znaleziono slajdu pelnego pakietu szczescia.')
        sys.exit(1)
    html = html[:future.end()] + video_section + html[future.end():]

html_path.write_text(html, encoding='utf-8')

scss = scss_path.read_text(encoding='utf-8')
scss = re.sub(r'\n/\* v24 car road alignment and blessing video \*/.*\Z', '', scss, flags=re.S)
scss += r'''

/* v24 car road alignment and blessing video */
.road-scene__car{
  top:39%;
  width:min(82vw,72rem);
  max-width:82vw;
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
.road-scene__road{
  inset:70% 0 0;
}

.blessing-scene{
  position:relative;
  min-height:100dvh;
  padding:clamp(4rem,7vw,7rem) clamp(1.25rem,5vw,5rem);
  display:grid;
  grid-template-columns:minmax(18rem,.7fr) minmax(0,1.3fr);
  align-items:center;
  gap:clamp(2rem,6vw,6rem);
  overflow:hidden;
  isolation:isolate;
  background:radial-gradient(circle at 70% 45%,#efe0c5,#b88753 48%,#3a2115 88%);
  color:#fff6e6;
}
.blessing-scene::before{
  content:"";
  position:absolute;
  z-index:-2;
  inset:0;
  background:linear-gradient(115deg,rgba(31,17,11,.84),rgba(31,17,11,.2) 58%,rgba(255,240,208,.08));
}
.blessing-scene__copy{
  position:relative;
  z-index:2;
  text-align:center;
}
.blessing-scene__copy h2{
  max-width:12ch;
  margin:.8rem auto 0;
  font-size:clamp(3rem,7vw,6.5rem);
  text-shadow:0 .3rem 1.4rem rgba(42,19,9,.45);
}
.blessing-video{
  position:relative;
  width:100%;
  max-width:64rem;
  margin:auto;
  padding:.7rem;
  border:1px solid rgba(255,228,178,.58);
  border-radius:1.5rem;
  background:rgba(255,247,232,.13);
  box-shadow:0 2rem 5rem rgba(37,17,8,.42);
  backdrop-filter:blur(10px);
}
.blessing-video video{
  display:block;
  width:100%;
  max-height:76dvh;
  border-radius:1rem;
  background:#120b08;
}
.blessing-video__frame{
  position:absolute;
  inset:-.7rem;
  z-index:-1;
  border:1px solid rgba(255,225,168,.32);
  border-radius:2rem;
}
.blessing-scene__ornament{
  position:absolute;
  inset:0;
  pointer-events:none;
}
.blessing-scene__ornament i{
  position:absolute;
  width:1rem;
  height:1.55rem;
  border-radius:90% 10% 70% 20%;
  background:#e0b66d;
  animation:blessingPetal 7s linear infinite;
}
.blessing-scene__ornament i:nth-child(1){left:8%;animation-delay:-1s}
.blessing-scene__ornament i:nth-child(2){left:35%;animation-delay:-5s;background:#fff0c7}
.blessing-scene__ornament i:nth-child(3){left:69%;animation-delay:-2.5s}
.blessing-scene__ornament i:nth-child(4){left:91%;animation-delay:-6s;background:#fff0c7}
@keyframes blessingPetal{
  from{top:-8%;transform:rotate(0);opacity:0}
  12%{opacity:.8}
  to{top:108%;transform:translateX(4rem) rotate(620deg);opacity:.1}
}

@media(max-width:760px){
  .road-scene__car{
    top:42%!important;
    width:86vw!important;
    max-width:86vw!important;
  }
  .road-scene__road{
    inset:69% 0 0!important;
  }
  .blessing-scene{
    min-height:auto;
    padding:4rem 1rem;
    grid-template-columns:1fr;
    gap:1.5rem;
  }
  .blessing-scene__copy{
    order:1;
  }
  .blessing-scene__copy h2{
    font-size:clamp(2.5rem,11vw,4rem);
  }
  .blessing-video{
    order:2;
    width:min(100%,32rem);
  }
  .blessing-video video{
    max-height:74svh;
  }
}
@media(prefers-reduced-motion:reduce){
  .blessing-scene__ornament i{animation:none!important}
}
'''
scss_path.write_text(scss, encoding='utf-8')

print('OK: zastosowano V24.')
print('Dodano film: public/video/blogoslawienstwo.mp4')
print('Dodano samochod: public/images/car-full-tight.png')
print('Uruchom teraz: npm run build && npm start')
