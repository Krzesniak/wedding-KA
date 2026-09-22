V32 naprawia puste slajdy po V31.

Przyczyna:
V31 ustawila element main jako osobny kontener przewijania, ale istniejace animacje GSAP obserwowaly okno. Elementy pozostawaly niewidoczne.

Instalacja:
1. Skopiuj folder wedding-v32-python-update do glownego katalogu projektu.
2. Uruchom:

python wedding-v32-python-update/apply-v32.py
npm run build
npm start

V32:
- przywraca przewijanie dokumentu,
- zachowuje lagodne scroll-snap proximity,
- usuwa mobilny IntersectionObserver z V31,
- ponownie przelicza ScrollTrigger po zaladowaniu strony,
- nie zmienia animacji samochodu z V31/V29.
