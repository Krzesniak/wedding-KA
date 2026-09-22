from pathlib import Path
import re
import sys

root = Path.cwd()
html_path = root / 'src/app/app.component.html'
scss_path = root / 'src/app/app.component.scss'
ts_path = root / 'src/app/app.component.ts'

missing = [str(p) for p in (html_path, scss_path, ts_path) if not p.exists()]
if missing:
    print('ERROR: Uruchom skrypt w glownym katalogu projektu wedding-story.')
    print('Brakuje:', ', '.join(missing))
    sys.exit(1)

# -------------------- HTML --------------------
html = html_path.read_text(encoding='utf-8')

# Mark sections that may need internal scrolling on mobile.
long_classes = [
    'memories-scene',
    'wishes',
    'voice-scene',
    'future',
    'blessing-scene',
]
for class_name in long_classes:
    html = re.sub(
        rf'<section class="{re.escape(class_name)}(?![^\"]*mobile-long-slide)([^"]*)">',
        rf'<section class="{class_name}\1 mobile-long-slide">',
        html,
        count=1,
    )

html_path.write_text(html, encoding='utf-8')

# -------------------- TYPESCRIPT --------------------
ts = ts_path.read_text(encoding='utf-8')

# Remove V27 timing constants if they remain.
ts = re.sub(
    r"\s*const mobileRoad = window\.matchMedia\('\(max-width: 760px\)'\)\.matches;\s*"
    r"const roadEnterDuration = mobileRoad \? .*?;\s*"
    r"const roadPauseDuration = mobileRoad \? .*?;\s*"
    r"const roadExitDuration = mobileRoad \? .*?;\s*",
    '\n',
    ts,
    count=1,
    flags=re.S,
)

# Replace an existing roadMedia implementation, or the older single road timeline.
road_media_pattern = re.compile(
    r"\s*const roadMedia = gsap\.matchMedia\(\);.*?"
    r"roadMedia\.add\('\(max-width: 760px\)', \(\) => \{.*?\n\s*\}\);",
    re.S,
)

single_road_pattern = re.compile(
    r"\s*gsap\.timeline\(\{ repeat: -1, repeatDelay: .*?scrollTrigger: \{ trigger: '\.road-scene'.*?"
    r"\.to\('\.road-scene__copy', \{ opacity: 0, duration: \.45 \}, '-=1\.25'\);",
    re.S,
)

road_code = r'''
      const roadMedia = gsap.matchMedia();

      // Desktop remains unchanged.
      roadMedia.add('(min-width: 761px)', () => {
        gsap.timeline({ repeat: -1, repeatDelay: 1.1, scrollTrigger: { trigger: '.road-scene', start: 'top 75%', end: 'bottom 25%', toggleActions: 'restart pause restart reset' } })
          .fromTo('.road-scene__car', { xPercent: 135, rotation: 1.5 }, { xPercent: 0, rotation: 0, duration: 2.25, ease: 'power2.out' })
          .fromTo('.road-scene__copy', { opacity: 0, y: 28 }, { opacity: 1, y: 0, duration: .8 }, '-=.55')
          .to('.road-scene__car', { xPercent: -135, duration: 2.1, ease: 'power2.in', delay: 1.4 })
          .to('.road-scene__copy', { opacity: 0, duration: .45 }, '-=1.25');
      });

      // Mobile uses pixel movement. x: 0 is the exact visual center because CSS
      // centers the wrapper independently through the translate property.
      roadMedia.add('(max-width: 760px)', () => {
        const travelDistance = () => Math.max(window.innerWidth * 1.45, 620);

        gsap.timeline({ repeat: -1, repeatDelay: .5, scrollTrigger: { trigger: '.road-scene', start: 'top 63%', end: 'bottom 37%', toggleActions: 'restart pause restart reset' } })
          .set('.road-scene__copy', { opacity: 1, y: 0 })
          .fromTo('.road-scene__car',
            { x: () => travelDistance(), rotation: 0 },
            { x: 0, rotation: 0, duration: 3, ease: 'power2.out' }
          )
          .to('.road-scene__car', { x: 0, duration: 2, ease: 'none' })
          .to('.road-scene__car', { x: () => -travelDistance(), duration: 3, ease: 'power2.in' })
          .to('.road-scene__copy', { opacity: 0, duration: .35 }, '-=.8');
      });'''

if road_media_pattern.search(ts):
    ts = road_media_pattern.sub('\n' + road_code, ts, count=1)
elif single_road_pattern.search(ts):
    ts = single_road_pattern.sub('\n' + road_code, ts, count=1)
elif 'const travelDistance' not in ts:
    print('ERROR: Nie znaleziono aktualnej animacji road-scene.')
    print('Upewnij sie, ze projekt zawiera poprawki V28/V29.')
    sys.exit(1)

# Animations restart when the slide is re-entered and reset after leaving.
ts = ts.replace("toggleActions: 'restart pause restart pause'", "toggleActions: 'restart pause restart reset'")

# Install a mobile slide observer once. It prevents animations on a barely visible next slide.
observer_marker = '    ScrollTrigger.refresh();'
observer_code = r'''    if (window.matchMedia('(max-width: 760px)').matches) {
      const slides = Array.from(root.querySelectorAll<HTMLElement>(':scope > section'));
      const slideObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          const slide = entry.target as HTMLElement;
          slide.classList.toggle('is-active-slide', entry.isIntersecting && entry.intersectionRatio >= 0.82);
        });
      }, { threshold: [0, 0.82, 1] });

      slides.forEach((slide) => slideObserver.observe(slide));
    }

'''
if 'is-active-slide' not in ts:
    if observer_marker not in ts:
        print('ERROR: Nie znaleziono ScrollTrigger.refresh().')
        sys.exit(1)
    ts = ts.replace(observer_marker, observer_code + observer_marker, 1)

ts_path.write_text(ts, encoding='utf-8')

# -------------------- SCSS --------------------
scss = scss_path.read_text(encoding='utf-8')
scss = re.sub(r'\n/\* v31 mobile slide presentation \*/.*\Z', '', scss, flags=re.S)
scss += r'''

/* v31 mobile slide presentation */
@media screen and (max-width:760px){
  html, body{
    height:100%;
    overflow:hidden!important;
  }

  :host{
    display:block;
    height:100svh;
    overflow:hidden;
  }

  main{
    width:100%;
    height:100svh;
    overflow-x:hidden!important;
    overflow-y:auto!important;
    scroll-snap-type:y mandatory;
    scroll-behavior:smooth;
    overscroll-behavior-y:contain;
    -webkit-overflow-scrolling:touch;
  }

  main > section{
    box-sizing:border-box!important;
    width:100%!important;
    min-width:0!important;
    min-height:100svh!important;
    max-width:100vw!important;
    margin:0!important;
    scroll-snap-align:start;
    scroll-snap-stop:always;
    overflow-x:hidden!important;
  }

  /* Long slides stay one snap page, but their content can scroll internally. */
  main > section.mobile-long-slide{
    height:100svh!important;
    max-height:100svh!important;
    min-height:100svh!important;
    overflow-x:hidden!important;
    overflow-y:auto!important;
    overscroll-behavior-y:contain;
    scrollbar-width:thin;
  }

  /* Keep inactive slides from visually starting before they own the viewport. */
  main > section:not(.is-active-slide) [data-reveal]{
    animation-play-state:paused;
  }

  /* Exact mobile car centering: CSS owns base centering, GSAP owns x travel. */
  .road-scene__car{
    left:50%!important;
    right:auto!important;
    translate:-50% 0!important;
    transform:none;
    will-change:transform;
  }

  .road-scene__car img{
    object-position:center bottom!important;
  }
}

@supports not (height:100svh){
  @media screen and (max-width:760px){
    :host, main, main > section, main > section.mobile-long-slide{
      height:100vh;
      min-height:100vh!important;
      max-height:100vh!important;
    }
  }
}
'''
scss_path.write_text(scss, encoding='utf-8')

print('OK: zastosowano V31.')
print('Mobile: samochod staje w rzeczywistym srodku ekranu.')
print('Mobile: jeden slajd zajmuje caly ekran i przyciaga sie po puszczeniu.')
print('Dlugie slajdy przewijaja sie wewnetrznie.')
print('Animacje resetuja sie po opuszczeniu i startuja ponownie po powrocie.')
print('Uruchom teraz: npm run build && npm start')
