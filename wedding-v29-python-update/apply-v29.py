from pathlib import Path
import re
import sys

root = Path.cwd()
ts_path = root / 'src/app/app.component.ts'

if not ts_path.exists():
    print('ERROR: Uruchom skrypt w glownym katalogu projektu wedding-story.')
    print('Brakuje:', ts_path)
    sys.exit(1)

ts = ts_path.read_text(encoding='utf-8')

# Change only the mobile road timeline created by V28.
mobile_pattern = re.compile(
    r"(roadMedia\.add\('\(max-width: 760px\)', \(\) => \{\s*"
    r"gsap\.timeline\(\{ repeat: -1, repeatDelay: )1\.4(, scrollTrigger:.*?"
    r"\.fromTo\('\.road-scene__car',\s*"
    r"\{ xPercent: 145, rotation: 0 \},\s*"
    r"\{ xPercent: 0, rotation: 0, duration: )6\.2(, ease: 'power2\.out' \}\s*"
    r"\)\s*"
    r"\.to\('\.road-scene__car', \{ xPercent: 0, duration: )3\.6(, ease: 'none' \}\)\s*"
    r"\.to\('\.road-scene__car', \{ xPercent: -145, duration: )6\.0(, ease: 'power2\.in' \}\))",
    re.S,
)

match = mobile_pattern.search(ts)
if not match:
    # Allow safe rerun if V29 values are already present.
    already = (
        "repeatDelay: 0.5" in ts
        and "duration: 3.0, ease: 'power2.out'" in ts
        and "xPercent: 0, duration: 2.0" in ts
        and "xPercent: -145, duration: 3.0" in ts
    )
    if already:
        print('OK: parametry V29 sa juz ustawione. Brak dodatkowych zmian.')
        sys.exit(0)
    print('ERROR: Nie znaleziono mobilnej animacji z V28.')
    print('Najpierw zastosuj wedding-v28-python-update.')
    sys.exit(1)

ts = mobile_pattern.sub(
    lambda m: (
        m.group(1) + '0.5' + m.group(2) + '3.0' +
        m.group(3) + '2.0' + m.group(4) + '3.0' + m.group(5)
    ),
    ts,
    count=1,
)

ts_path.write_text(ts, encoding='utf-8')

print('OK: zastosowano V29.')
print('Mobile: wjazd 3.0 s, postoj 2.0 s, wyjazd 3.0 s, przerwa 0.5 s.')
print('Desktop: bez zmian.')
print('Uruchom teraz: npm run build && npm start')
