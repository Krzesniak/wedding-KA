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

# ---------------- SCSS ----------------
scss = scss_path.read_text(encoding='utf-8')
scss = re.sub(r'\n/\* v33 mobile wishes scroll fix \*/.*\Z', '', scss, flags=re.S)
scss += r'''

/* v33 mobile wishes scroll fix */
@media screen and (max-width:760px){
  /* The wishes section is intentionally a normal, long document section. */
  main > section.wishes,
  main > section.wishes.mobile-long-slide{
    position:relative!important;
    display:block!important;
    width:100%!important;
    min-width:0!important;
    max-width:100vw!important;
    height:auto!important;
    min-height:100svh!important;
    max-height:none!important;
    margin:0!important;
    padding:4rem .85rem!important;
    overflow:visible!important;
    overscroll-behavior:auto!important;
    scroll-snap-align:none!important;
    scroll-snap-stop:normal!important;
    contain:none!important;
  }

  .wishes header{
    width:min(100%,31rem)!important;
    margin:0 auto 2rem!important;
    text-align:center!important;
  }

  .wishes .wish-grid{
    position:relative!important;
    display:grid!important;
    grid-template-columns:minmax(0,1fr)!important;
    align-items:start!important;
    width:min(100%,31rem)!important;
    max-width:31rem!important;
    height:auto!important;
    min-height:0!important;
    max-height:none!important;
    margin:0 auto!important;
    gap:1rem!important;
    overflow:visible!important;
    contain:none!important;
  }

  .wishes .wish-letter{
    position:relative!important;
    display:block!important;
    width:100%!important;
    min-width:0!important;
    height:auto!important;
    min-height:0!important;
    max-height:none!important;
    margin:0!important;
    overflow:visible!important;
    contain:none!important;
  }

  .wishes .wish-letter summary{
    box-sizing:border-box!important;
    width:100%!important;
    height:12.5rem!important;
    min-height:12.5rem!important;
    max-height:none!important;
  }

  .wishes .wish-letter[open] summary{
    height:3.1rem!important;
    min-height:3.1rem!important;
  }

  .wishes .wish-letter__paper{
    box-sizing:border-box!important;
    position:relative!important;
    display:block!important;
    width:calc(100% - 1.3rem)!important;
    height:auto!important;
    min-height:0!important;
    max-height:none!important;
    margin:-.35rem .65rem 0!important;
    overflow:visible!important;
  }

  /* Disable snap while the user is interacting with the list of letters. */
  html.wishes-open,
  html.wishes-open body{
    scroll-snap-type:none!important;
  }

  html.wishes-open main{
    scroll-snap-type:none!important;
  }

  /* Never leave letter content hidden because a reveal animation was interrupted. */
  .wishes [data-reveal],
  .wishes .wish-letter,
  .wishes .wish-letter__paper{
    visibility:visible!important;
  }
}

@supports not (height:100svh){
  @media screen and (max-width:760px){
    main > section.wishes,
    main > section.wishes.mobile-long-slide{
      min-height:100vh!important;
    }
  }
}
'''
scss_path.write_text(scss, encoding='utf-8')

# ---------------- TYPESCRIPT ----------------
ts = ts_path.read_text(encoding='utf-8')

# Install one delegated toggle handler. It refreshes ScrollTrigger only after layout settles.
handler = r'''
    const wishesSection = root.querySelector<HTMLElement>('.wishes');
    if (wishesSection && !wishesSection.dataset['toggleBound']) {
      wishesSection.dataset['toggleBound'] = 'true';

      wishesSection.addEventListener('toggle', (event) => {
        const letter = event.target;
        if (!(letter instanceof HTMLDetailsElement) || !letter.classList.contains('wish-letter')) {
          return;
        }

        const anyOpen = !!wishesSection.querySelector<HTMLDetailsElement>('.wish-letter[open]');
        document.documentElement.classList.toggle('wishes-open', anyOpen);

        window.requestAnimationFrame(() => {
          window.requestAnimationFrame(() => {
            ScrollTrigger.refresh();
            letter.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
          });
        });
      }, true);
    }

'''

# Remove previous V33 handler if rerun.
ts = re.sub(
    r"\s*const wishesSection = root\.querySelector<HTMLElement>\('\.wishes'\);.*?\n\s*}\n\n(?=\s*ScrollTrigger\.refresh\(\);)",
    '\n',
    ts,
    count=1,
    flags=re.S,
)

marker = '    ScrollTrigger.refresh();'
if marker not in ts:
    print('ERROR: Nie znaleziono ScrollTrigger.refresh().')
    sys.exit(1)

ts = ts.replace(marker, handler + marker, 1)
ts_path.write_text(ts, encoding='utf-8')

print('OK: zastosowano V33 mobile wishes scroll fix.')
print('Na mobile sekcja z listami przewija sie naturalnie i nie blokuje strony.')
print('Po otwarciu lub zamknieciu listu pozycje GSAP sa przeliczane.')
print('Uruchom teraz: npm run build && npm start')
