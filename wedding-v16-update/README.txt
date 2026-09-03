Wymagany projekt po V15.

Skopiuj folder wedding-v16-update do katalogu glownego projektu i uruchom:

python wedding-v16-update/apply-v16.py
npm run build
npm start

V16:
- ustawia zdjęcie dzieci bez rozciągania i bez obcinania,
- używa rozmytej kopii zdjęcia jako tła wolnej przestrzeni,
- zapisuje przesłane zdjęcie willi lokalnie jako public/images/villa.jpg,
- usuwa zależność karty domu od zewnętrznego URL.
