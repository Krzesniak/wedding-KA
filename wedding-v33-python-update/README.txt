V33 Python update

Przeznaczenie:
Naprawa blokowania mobilnego scrolla po otwarciu listu z zyczeniami.

1. Skopiuj folder wedding-v33-python-update do glownego katalogu projektu.
2. Uruchom:

python wedding-v33-python-update/apply-v33.py
npm run build
npm start

V33:
- usuwa ograniczenie wysokosci sekcji z listami,
- wymusza jedna kolumne listow na mobile,
- pozwala sekcji rosnac po otwarciu listu,
- tymczasowo wylacza scroll-snap, gdy jakikolwiek list jest otwarty,
- po toggle wywoluje ScrollTrigger.refresh(),
- przewija otwarty list do najblizszej widocznej pozycji.
