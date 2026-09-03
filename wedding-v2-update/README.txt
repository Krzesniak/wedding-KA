WEDDING STORY V2 - instrukcja

1. Rozpakuj ten pakiet w dowolnym miejscu.
2. Otworz Git Bash w glownym katalogu projektu wedding-story.
3. Uruchom:

   python /sciezka/do/wedding-v2-update/apply-update.py

Alternatywnie skopiuj folder wedding-v2-update do katalogu projektu i uruchom:

   python wedding-v2-update/apply-update.py

4. Sprawdz zmiany:

   git diff
   npm run build
   npm start

5. Jesli wszystko dziala:

   git add .
   git commit -m "Wedding story v2: rings, photos, wishes and date"
   git push

Skrypt wykonuje tylko kontrolowane zamiany. Jesli pliki projektu roznia sie od przekazanej wersji, zatrzyma sie z komunikatem zamiast uszkodzic kod.
