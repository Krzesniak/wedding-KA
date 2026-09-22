from pathlib import Path
import re
import shutil
import sys

root = Path.cwd()
html_path = root / 'src/app/app.component.html'
scss_path = root / 'src/app/app.component.scss'
images_dir = root / 'public/images'

missing = [str(p) for p in (html_path, scss_path, images_dir) if not p.exists()]
if missing:
    print('ERROR: Uruchom skrypt w glownym katalogu projektu wedding-story.')
    print('Brakuje:', ', '.join(missing))
    sys.exit(1)

assets = Path(__file__).resolve().parent / 'assets'
shutil.copy2(assets / 'family-v25.jpg', images_dir / 'family-v25.jpg')

html = html_path.read_text(encoding='utf-8')

# Replace the family picture with the new portrait while keeping the existing copy.
html, count = re.subn(
    r'(<article class="future-card future-card--family"[^>]*>\s*)'
    r'<img[^>]*>'
    r'(\s*<div>)',
    r'\1<img src="/images/family-v25.jpg" alt="Troje dzieci razem" loading="lazy">\2',
    html,
    count=1,
    flags=re.S,
)
if count != 1:
    print('ERROR: Nie znaleziono karty future-card--family.')
    sys.exit(1)

html_path.write_text(html, encoding='utf-8')

scss = scss_path.read_text(encoding='utf-8')
scss = re.sub(r'\n/\* v25 complete car and family photo fit \*/.*\Z', '', scss, flags=re.S)
scss += r'''

/* v25 complete car and family photo fit */
/* The car is anchored by its wheels to the road instead of positioned from the top. */
.road-scene__car{
  top:auto!important;
  bottom:24%!important;
  left:50%!important;
  width:min(68vw,66rem)!important;
  max-width:68vw!important;
  transform:translateX(-50%);
  overflow:visible!important;
}
.road-scene__car img{
  display:block!important;
  width:100%!important;
  height:auto!important;
  max-height:none!important;
  object-fit:contain!important;
  object-position:center bottom!important;
  clip-path:none!important;
  border-radius:0!important;
  transform:none!important;
}
.road-scene__road{
  inset:70% 0 0!important;
}

/* Preserve the portrait proportions and show the complete family photo. */
.future-card--family{
  isolation:isolate;
  background:#9b806d;
}
.future-card--family::before{
  content:"";
  position:absolute;
  z-index:0;
  inset:-1.5rem;
  background:url('/images/family-v25.jpg') center/cover no-repeat;
  filter:blur(22px) brightness(.58) saturate(.82);
  transform:scale(1.1);
}
.future-card--family>img{
  position:absolute!important;
  z-index:1!important;
  inset:0!important;
  display:block!important;
  width:100%!important;
  height:100%!important;
  object-fit:contain!important;
  object-position:center!important;
  transform:none!important;
  filter:none!important;
  background:transparent!important;
}
.future-card--family::after{
  z-index:2!important;
  background:linear-gradient(180deg,rgba(8,5,3,.02) 35%,rgba(8,5,3,.9) 91%)!important;
}
.future-card--family>div:last-child{
  z-index:3!important;
}

@media(max-width:760px){
  .road-scene__car{
    bottom:25%!important;
    width:78vw!important;
    max-width:78vw!important;
  }
  .road-scene__road{
    inset:71% 0 0!important;
  }
  .future-card--family>img{
    object-fit:contain!important;
    object-position:center!important;
  }
}

@media(max-width:390px){
  .road-scene__car{
    bottom:26%!important;
    width:82vw!important;
    max-width:82vw!important;
  }
}
'''
scss_path.write_text(scss, encoding='utf-8')

print('OK: zastosowano V25.')
print('Samochod jest zakotwiczony kolami przy drodze i widoczny w calosci.')
print('Zdjecie dzieci zachowuje proporcje i jest wyswietlane bez rozciagania.')
print('Uruchom teraz: npm run build && npm start')
