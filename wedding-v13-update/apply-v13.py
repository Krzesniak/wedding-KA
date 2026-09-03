from pathlib import Path
import re, shutil, sys
r=Path.cwd(); hp=r/'src/app/app.component.html'; sp=r/'src/app/app.component.scss'; tp=r/'src/app/app.component.ts'; audio=r/'public/audio'
if not all(p.exists() for p in (hp,sp,tp,r/'public')): sys.exit('ERROR: Uruchom skrypt w katalogu glownym projektu.')
audio.mkdir(parents=True,exist_ok=True); shutil.copy2(Path(__file__).parent/'assets/Biedronka.m4a',audio/'Biedronka.m4a')
h=hp.read_text(encoding='utf-8')
# Add audio slide immediately after wishes.
voice='''

    <section class="voice-scene">
      <div class="voice-scene__flowers" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
      <div class="voice-card" data-reveal>
        <div class="voice-card__seal" aria-hidden="true">♥</div>
        <p class="kicker">Głos prosto z serca</p>
        <h2>Jeszcze kilka słów dla Was…</h2>
        <p class="voice-card__lead">Kliknij i posłuchaj wiadomości przygotowanej specjalnie na tę okazję.</p>
        <audio class="wedding-audio" controls preload="metadata">
          <source src="/audio/Biedronka.m4a" type="audio/mp4">
          Twoja przeglądarka nie obsługuje odtwarzania audio.
        </audio>
        <div class="voice-wave" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
        <small>Wiadomość głosowa · 00:30</small>
      </div>
    </section>'''
if 'class="voice-scene"' in h:
 h=re.sub(r'\s*<section class="voice-scene">.*?</section>',voice,h,count=1,flags=re.S)
else:
 wishes=re.search(r'<section class="wishes">.*?</section>',h,flags=re.S)
 if not wishes: sys.exit('ERROR: Nie znaleziono sekcji wishes.')
 h=h[:wishes.end()]+voice+h[wishes.end():]
hp.write_text(h,encoding='utf-8')
# Add audio event handling: wave animates only during playback.
t=tp.read_text(encoding='utf-8')
if "wedding-audio" not in t:
 marker='    ScrollTrigger.refresh();'
 code="""    const audio = root.querySelector<HTMLAudioElement>('.wedding-audio');
    const wave = root.querySelector<HTMLElement>('.voice-wave');
    audio?.addEventListener('play', () => wave?.classList.add('is-playing'));
    audio?.addEventListener('pause', () => wave?.classList.remove('is-playing'));
    audio?.addEventListener('ended', () => wave?.classList.remove('is-playing'));

"""
 if marker not in t: sys.exit('ERROR: Nie znaleziono ScrollTrigger.refresh().')
 t=t.replace(marker,code+marker,1)
tp.write_text(t,encoding='utf-8')
# Style overrides.
s=sp.read_text(encoding='utf-8'); s=re.sub(r'\n/\* v13 celebration timing, equal letters and voice \*/.*\Z','',s,flags=re.S)
s+='''

/* v13 celebration timing, equal letters and voice */
/* Keep the newlyweds title lower and visible longer. */
.newlyweds-scene__copy{position:absolute;left:0;right:0;bottom:7%;padding:2rem 1.5rem 2.5rem;background:linear-gradient(transparent,rgba(18,9,5,.72));animation:newlywedsHold 7s ease-in-out infinite}.newlyweds-scene__copy h2{font-size:clamp(3.1rem,9vw,7.7rem)}@keyframes newlywedsHold{0%,8%{opacity:0;transform:translateY(28px)}18%,82%{opacity:1;transform:none}94%,100%{opacity:0;transform:translateY(12px)}}
/* Equal-sized letters and a much smaller open hint. */
.wish-grid{align-items:stretch}.wish-letter{height:100%;display:grid;grid-template-rows:auto 1fr}.wish-letter summary{height:15.5rem;min-height:15.5rem}.wish-letter__title{min-height:3.35em;display:grid;place-items:center}.wish-letter__hint{margin-top:.65rem;font-size:.5rem!important;letter-spacing:.12em;opacity:.72}.wish-letter[open] .wish-letter__hint::after{font-size:.5rem}.wish-letter__paper{min-height:10rem;height:100%}
/* Wedding voice-message slide. */
.voice-scene{position:relative;min-height:100dvh;padding:clamp(3rem,7vw,7rem) 1.25rem;display:grid;place-items:center;overflow:hidden;background:radial-gradient(circle at 50% 35%,#f7ebd6,#d5b58a 58%,#896044);color:#2d1f17;isolation:isolate}.voice-scene::before{content:"";position:absolute;z-index:-2;inset:0;background:repeating-linear-gradient(115deg,transparent 0 24px,rgba(255,255,255,.08) 25px 26px)}.voice-card{position:relative;width:min(92vw,48rem);padding:clamp(2.4rem,6vw,5rem);text-align:center;border:1px solid rgba(110,69,37,.34);border-radius:1rem;background:rgba(255,248,234,.94);box-shadow:0 2rem 5rem rgba(74,42,23,.3)}.voice-card::before,.voice-card::after{content:"❦";position:absolute;color:#a45d49;font:3rem Georgia}.voice-card::before{left:1.4rem;top:1rem}.voice-card::after{right:1.4rem;bottom:1rem;transform:rotate(180deg)}.voice-card__seal{display:grid;place-items:center;width:4.3rem;aspect-ratio:1;margin:-4.8rem auto 1.5rem;border-radius:50%;background:#8f4137;color:#fff1dd;font-size:1.7rem;box-shadow:0 .7rem 1.3rem rgba(69,30,25,.3)}.voice-card h2{max-width:13ch;margin:.8rem auto 1.2rem;font-size:clamp(2.8rem,7vw,5.2rem)}.voice-card__lead{max-width:34rem;margin:0 auto 1.7rem;color:#6f5a4a;line-height:1.7}.wedding-audio{display:block;width:min(100%,34rem);margin:0 auto;accent-color:#8f4137}.voice-card small{display:block;margin-top:1rem;color:#95775f;font-size:.68rem;letter-spacing:.14em;text-transform:uppercase}.voice-wave{height:3.4rem;margin:1.25rem auto 0;display:flex;align-items:center;justify-content:center;gap:.38rem}.voice-wave i{display:block;width:.32rem;height:.65rem;border-radius:99px;background:#a95b49;transform-origin:center}.voice-wave.is-playing i{animation:voiceBar .8s ease-in-out infinite alternate}.voice-wave.is-playing i:nth-child(2n){animation-delay:-.25s}.voice-wave.is-playing i:nth-child(3n){animation-delay:-.5s}@keyframes voiceBar{from{height:.55rem;opacity:.55}to{height:2.7rem;opacity:1}}.voice-scene__flowers i{position:absolute;width:9rem;height:9rem;border:1rem solid rgba(151,83,55,.2);border-radius:50% 0 50% 50%;transform:rotate(35deg)}.voice-scene__flowers i:nth-child(1){left:-3rem;top:8%}.voice-scene__flowers i:nth-child(2){right:-3rem;top:16%;transform:rotate(215deg)}.voice-scene__flowers i:nth-child(3){left:8%;bottom:-4rem;transform:scale(.7) rotate(75deg)}.voice-scene__flowers i:nth-child(4){right:9%;bottom:-4rem;transform:scale(.7) rotate(255deg)}
@media(max-width:650px){.newlyweds-scene__copy{bottom:3%}.wish-letter summary{height:14rem;min-height:14rem}.wish-letter__paper{min-height:0}.voice-card{padding:3.2rem 1.3rem 2rem}.voice-card__seal{margin-top:-5.2rem}}
@media(prefers-reduced-motion:reduce){.newlyweds-scene__copy,.voice-wave i{animation:none!important}.newlyweds-scene__copy{opacity:1!important;transform:none!important}}
'''
sp.write_text(s,encoding='utf-8')
print('OK: zastosowano V13. Uruchom npm run build.')
