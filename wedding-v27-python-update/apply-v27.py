from pathlib import Path
import re
import sys

root = Path.cwd()
scss_path = root / 'src/app/app.component.scss'
ts_path = root / 'src/app/app.component.ts'

missing = [str(p) for p in (scss_path, ts_path) if not p.exists()]
if missing:
    print('ERROR: Uruchom skrypt w glownym katalogu projektu wedding-story.')
    print('Brakuje:', ', '.join(missing))
    sys.exit(1)

# Mobile-only visual sizing. Desktop rules remain untouched.
scss = scss_path.read_text(encoding='utf-8')
scss = re.sub(r'\n/\* v27 mobile car size and speed \*/.*\Z', '', scss, flags=re.S)
scss += r'''

/* v27 mobile car size and speed */
@media screen and (max-width:760px){
  .road-scene__car{
    top:auto!important;
    bottom:13%!important;
    left:50%!important;
    width:112vw!important;
    max-width:112vw!important;
    transform:translateX(-50%);
    transform-origin:center bottom!important;
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
    inset:69% 0 0!important;
  }
}
@media screen and (max-width:390px){
  .road-scene__car{
    bottom:14%!important;
    width:118vw!important;
    max-width:118vw!important;
  }
}
'''
scss_path.write_text(scss, encoding='utf-8')

# Make only the mobile GSAP journey slower. Desktop keeps the original timings.
ts = ts_path.read_text(encoding='utf-8')

# Add the mobile timing flag once, just before the road timeline.
road_marker = "      gsap.timeline({ repeat: -1, repeatDelay: 1.1, scrollTrigger: { trigger: '.road-scene'"
flag = "      const mobileRoad = window.matchMedia('(max-width: 760px)').matches;\n      const roadEnterDuration = mobileRoad ? 6.2 : 2.25;\n      const roadPauseDuration = mobileRoad ? 2.8 : 1.4;\n      const roadExitDuration = mobileRoad ? 6.0 : 2.1;\n\n"
if 'const mobileRoad =' not in ts:
    if road_marker not in ts:
        print('ERROR: Nie znaleziono osi czasu road-scene w app.component.ts.')
        sys.exit(1)
    ts = ts.replace(road_marker, flag + road_marker, 1)

# Normalize duration values so rerunning the updater is safe.
ts = re.sub(
    r"\.fromTo\('\.road-scene__car', \{ xPercent: 135, rotation: 1\.5 \}, \{ xPercent: 0, rotation: 0, duration: (?:2\.25|roadEnterDuration),",
    ".fromTo('.road-scene__car', { xPercent: 135, rotation: 1.5 }, { xPercent: 0, rotation: 0, duration: roadEnterDuration,",
    ts,
    count=1,
)
ts = re.sub(
    r"\.to\('\.road-scene__car', \{ xPercent: -135, duration: (?:2\.1|roadExitDuration), ease: 'power2\.in', delay: (?:1\.4|roadPauseDuration) \}\)",
    ".to('.road-scene__car', { xPercent: -135, duration: roadExitDuration, ease: 'power2.in', delay: roadPauseDuration })",
    ts,
    count=1,
)

if 'duration: roadEnterDuration' not in ts or 'duration: roadExitDuration' not in ts:
    print('ERROR: Nie udalo sie zmienic czasu animacji samochodu.')
    sys.exit(1)

ts_path.write_text(ts, encoding='utf-8')

print('OK: zastosowano V27.')
print('Mobile: samochod jest wiekszy i jedzie znacznie wolniej.')
print('Desktop: rozmiar i predkosc pozostaly bez zmian.')
print('Uruchom teraz: npm run build && npm start')
