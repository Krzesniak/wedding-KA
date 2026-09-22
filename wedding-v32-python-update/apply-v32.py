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

# Remove the V31 CSS block that moved scrolling into <main>.
scss = scss_path.read_text(encoding='utf-8')
scss, removed = re.subn(
    r'\n/\* v31 mobile slide presentation \*/.*?(?=\n/\* v3[2-9]|\n/\* v[4-9][0-9]|\Z)',
    '',
    scss,
    count=1,
    flags=re.S,
)

# Remove a previous V32 block when rerunning.
scss = re.sub(r'\n/\* v32 mobile scroll recovery \*/.*\Z', '', scss, flags=re.S)

scss += r'''

/* v32 mobile scroll recovery */
@media screen and (max-width:760px){
  /* Window/document is the scroll container again, matching every GSAP ScrollTrigger. */
  html{
    height:auto!important;
    min-height:100%!important;
    overflow-x:hidden!important;
    overflow-y:auto!important;
    scroll-snap-type:y proximity;
    scroll-behavior:smooth;
    overscroll-behavior-y:auto;
  }

  body{
    height:auto!important;
    min-height:100%!important;
    overflow-x:hidden!important;
    overflow-y:visible!important;
  }

  app-root,
  :host{
    display:block!important;
    width:100%!important;
    height:auto!important;
    min-height:100%!important;
    overflow:visible!important;
  }

  main{
    display:block!important;
    width:100%!important;
    height:auto!important;
    min-height:100%!important;
    overflow:visible!important;
  }

  main > section{
    box-sizing:border-box!important;
    width:100%!important;
    max-width:100vw!important;
    min-width:0!important;
    min-height:100svh!important;
    height:auto!important;
    max-height:none!important;
    margin:0!important;
    scroll-snap-align:start;
    scroll-snap-stop:normal;
    overflow-x:hidden!important;
  }

  /* Long slides can be taller than one viewport and scroll naturally with the page. */
  main > section.mobile-long-slide{
    min-height:100svh!important;
    height:auto!important;
    max-height:none!important;
    overflow-x:hidden!important;
    overflow-y:visible!important;
    scroll-snap-align:start;
  }

  /* Never hide a slide merely because IntersectionObserver has not marked it active. */
  main > section:not(.is-active-slide) [data-reveal]{
    animation-play-state:running!important;
  }
}

@supports not (height:100svh){
  @media screen and (max-width:760px){
    main > section,
    main > section.mobile-long-slide{
      min-height:100vh!important;
    }
  }
}
'''
scss_path.write_text(scss, encoding='utf-8')

# Remove the V31 IntersectionObserver. It is no longer needed and could leave stale classes.
ts = ts_path.read_text(encoding='utf-8')
observer_pattern = re.compile(
    r"\s*if \(window\.matchMedia\('\(max-width: 760px\)'\)\.matches\) \{\s*"
    r"const slides = Array\.from\(root\.querySelectorAll<HTMLElement>\(':scope > section'\)\);.*?"
    r"slides\.forEach\(\(slide\) => slideObserver\.observe\(slide\)\);\s*\}",
    re.S,
)
ts, observer_removed = observer_pattern.subn('\n', ts, count=1)

# Refresh after fonts/images and after the browser restores its scroll position.
refresh_code = r'''
    window.setTimeout(() => ScrollTrigger.refresh(), 150);
    window.addEventListener('load', () => ScrollTrigger.refresh(), { once: true });
'''
if "window.setTimeout(() => ScrollTrigger.refresh(), 150);" not in ts:
    marker = '    ScrollTrigger.refresh();'
    if marker not in ts:
        print('ERROR: Nie znaleziono ScrollTrigger.refresh().')
        sys.exit(1)
    ts = ts.replace(marker, marker + refresh_code, 1)

ts_path.write_text(ts, encoding='utf-8')

print('OK: zastosowano V32 mobile scroll recovery.')
print('Usunieto blok V31 CSS:', bool(removed))
print('Usunieto obserwator V31:', bool(observer_removed))
print('Przewijanie wrocilo do okna, wiec ScrollTrigger ponownie widzi slajdy.')
print('Uruchom: npm run build && npm start')
