from pathlib import Path
import re, shutil, sys

root = Path.cwd()
html_path = root / 'src/app/app.component.html'
scss_path = root / 'src/app/app.component.scss'
images = root / 'public/images'

if not all(path.exists() for path in (html_path, scss_path, images)):
    sys.exit('ERROR: Uruchom skrypt w katalogu glownym projektu po zastosowaniu V15.')

if not (images / 'family.jpg').exists():
    sys.exit('ERROR: Brakuje public/images/family.jpg. Najpierw zastosuj V14.')

shutil.copy2(Path(__file__).resolve().parent / 'assets' / 'villa.jpg', images / 'villa.jpg')

html = html_path.read_text(encoding='utf-8')

# Replace any previous home image, including the remote Unsplash URL.
home_pattern = re.compile(
    r'(<article class="future-card future-card--home"[^>]*>\s*)'
    r'<img[^>]*>'
    r'(\s*<div>)',
    re.S
)
replacement = (
    r'\1<img src="/images/villa.jpg" alt="Willa z ogrodem i basenem" loading="lazy">\2'
)
html, count = home_pattern.subn(replacement, html, count=1)
if count != 1:
    sys.exit('ERROR: Nie znaleziono karty future-card--home. Najpierw zastosuj V14 i V15.')

html_path.write_text(html, encoding='utf-8')

scss = scss_path.read_text(encoding='utf-8')
scss = re.sub(r'\n/\* v16 family crop and local villa \*/.*\Z', '', scss, flags=re.S)
scss += r'''

/* v16 family crop and local villa */
/* Do not stretch or crop the children photo. The blurred layer fills the 3:2 card behind it. */
.future-card--family{isolation:isolate;background:#8f785f}
.future-card--family::before{content:"";position:absolute;z-index:-1;inset:-1.5rem;background:url('/images/family.jpg') center/cover no-repeat;filter:blur(18px) brightness(.67) saturate(.82);transform:scale(1.08)}
.future-card--family>img{position:absolute;z-index:0;inset:0;width:100%;height:100%;object-fit:contain!important;object-position:center!important;transform:none!important;background:transparent!important;filter:none}
.future-card--family::after{z-index:1;background:linear-gradient(180deg,rgba(8,5,3,.04) 30%,rgba(8,5,3,.9) 88%)}
.future-card--family>div:last-child{z-index:3}
/* Local villa supplied by the user. Keep the full facade and pool in the frame. */
.future-card--home{background:#302a22}
.future-card--home>img{object-fit:cover;object-position:center center;transform:none;filter:saturate(1.03) contrast(1.025)}
.future-card--home::after{background:linear-gradient(180deg,rgba(8,5,3,.02) 36%,rgba(8,5,3,.9) 88%)}
@media(max-width:680px){.future-card--family>img{object-fit:contain!important}.future-card--home>img{object-position:center}}
'''
scss_path.write_text(scss, encoding='utf-8')

print('OK: zastosowano V16. Uruchom npm run build.')
