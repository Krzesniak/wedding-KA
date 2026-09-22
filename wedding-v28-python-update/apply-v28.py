from pathlib import Path
import re
import sys

root = Path.cwd()
ts_path = root / 'src/app/app.component.ts'
scss_path = root / 'src/app/app.component.scss'

missing = [str(p) for p in (ts_path, scss_path) if not p.exists()]
if missing:
    print('ERROR: Uruchom skrypt w glownym katalogu projektu wedding-story.')
    print('Brakuje:', ', '.join(missing))
    sys.exit(1)

ts = ts_path.read_text(encoding='utf-8')

# Remove timing constants introduced by V27. V28 uses two separate timelines.
ts = re.sub(
    r"\s*const mobileRoad = window\.matchMedia\('\(max-width: 760px\)'\)\.matches;\s*"
    r"const roadEnterDuration = mobileRoad \? 6\.2 : 2\.25;\s*"
    r"const roadPauseDuration = mobileRoad \? 2\.8 : 1\.4;\s*"
    r"const roadExitDuration = mobileRoad \? 6\.0 : 2\.1;\s*",
    '\n',
    ts,
    count=1,
    flags=re.S,
)

# Replace the current road timeline. Desktop timing and behavior stay identical.
road_pattern = re.compile(
    r"\s*gsap\.timeline\(\{ repeat: -1, repeatDelay: 1\.1, scrollTrigger: \{ trigger: '\.road-scene'.*?"
    r"\.to\('\.road-scene__copy', \{ opacity: 0, duration: \.45 \}, '-=1\.25'\);",
    re.S,
)

replacement = r'''
      const roadMedia = gsap.matchMedia();

      roadMedia.add('(min-width: 761px)', () => {
        gsap.timeline({ repeat: -1, repeatDelay: 1.1, scrollTrigger: { trigger: '.road-scene', start: 'top 75%', end: 'bottom 25%', toggleActions: 'restart pause restart pause' } })
          .fromTo('.road-scene__car', { xPercent: 135, rotation: 1.5 }, { xPercent: 0, rotation: 0, duration: 2.25, ease: 'power2.out' })
          .fromTo('.road-scene__copy', { opacity: 0, y: 28 }, { opacity: 1, y: 0, duration: .8 }, '-=.55')
          .to('.road-scene__car', { xPercent: -135, duration: 2.1, ease: 'power2.in', delay: 1.4 })
          .to('.road-scene__copy', { opacity: 0, duration: .45 }, '-=1.25');
      });

      roadMedia.add('(max-width: 760px)', () => {
        gsap.timeline({ repeat: -1, repeatDelay: 1.4, scrollTrigger: { trigger: '.road-scene', start: 'top 75%', end: 'bottom 25%', toggleActions: 'restart pause restart pause' } })
          .set('.road-scene__copy', { opacity: 1, y: 0 })
          .fromTo('.road-scene__car',
            { xPercent: 145, rotation: 0 },
            { xPercent: 0, rotation: 0, duration: 6.2, ease: 'power2.out' }
          )
          .to('.road-scene__car', { xPercent: 0, duration: 3.6, ease: 'none' })
          .to('.road-scene__car', { xPercent: -145, duration: 6.0, ease: 'power2.in' })
          .to('.road-scene__copy', { opacity: 0, duration: .45 }, '-=1.1');
      });'''

ts, count = road_pattern.subn(replacement, ts, count=1)
if count != 1:
    print('ERROR: Nie znaleziono aktualnej animacji road-scene. Najpierw zastosuj V27.')
    sys.exit(1)

ts_path.write_text(ts, encoding='utf-8')

# Keep mobile car centered at the pause point. No desktop changes.
scss = scss_path.read_text(encoding='utf-8')
scss = re.sub(r'\n/\* v28 mobile centered car pause \*/.*\Z', '', scss, flags=re.S)
scss += r'''

/* v28 mobile centered car pause */
@media screen and (max-width:760px){
  .road-scene__car{
    left:50%!important;
    right:auto!important;
    transform:translateX(-50%);
    transform-origin:center bottom!important;
  }
  .road-scene__car img{
    object-position:center bottom!important;
  }
}
'''
scss_path.write_text(scss, encoding='utf-8')

print('OK: zastosowano V28.')
print('Mobile: auto wjezdza na srodek, stoi 3.6 s i dopiero odjezdza w lewo.')
print('Desktop: bez zmian.')
print('Uruchom teraz: npm run build && npm start')
