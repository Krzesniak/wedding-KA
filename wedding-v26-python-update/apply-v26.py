from pathlib import Path
import re
import sys

root = Path.cwd()
scss_path = root / 'src/app/app.component.scss'

if not scss_path.exists():
    print('ERROR: Uruchom skrypt w glownym katalogu projektu wedding-story.')
    sys.exit(1)

scss = scss_path.read_text(encoding='utf-8')
scss = re.sub(r'\n/\* v26 car road position \*/.*\Z', '', scss, flags=re.S)
scss += r'''

/* v26 car road position */
/* Place the complete car lower, with the tyres visually resting on the road. */
.road-scene__car{
  top:auto!important;
  bottom:12%!important;
  left:50%!important;
  width:min(61vw,62rem)!important;
  max-width:61vw!important;
  transform:translateX(-50%);
  transform-origin:center bottom!important;
  overflow:visible!important;
}
.road-scene__car img{
  display:block!important;
  width:100%!important;
  height:auto!important;
  max-height:none!important;
  object-fit:contain!important;
  object-position:center bottom!important;
  clip-path:none!important;
  border-radius:0!important;
  transform:none!important;
}
.road-scene__copy{
  top:8%!important;
  left:4%!important;
  right:4%!important;
  width:auto!important;
  max-width:none!important;
  padding:0 1rem!important;
  text-align:center!important;
}
.road-scene__copy h2{
  max-width:15ch!important;
  margin:.7rem auto 0!important;
  font-size:clamp(2.8rem,6.8vw,6.2rem)!important;
  line-height:.96!important;
}
.road-scene__road{
  inset:69% 0 0!important;
}

@media(max-width:760px){
  .road-scene__car{
    bottom:15%!important;
    width:76vw!important;
    max-width:76vw!important;
  }
  .road-scene__copy{
    top:7%!important;
    left:.75rem!important;
    right:.75rem!important;
  }
  .road-scene__copy h2{
    max-width:13ch!important;
    font-size:clamp(2.2rem,10vw,3.6rem)!important;
  }
  .road-scene__road{
    inset:70% 0 0!important;
  }
}

@media(max-width:390px){
  .road-scene__car{
    bottom:17%!important;
    width:80vw!important;
    max-width:80vw!important;
  }
  .road-scene__copy h2{
    font-size:clamp(2rem,9.4vw,3rem)!important;
  }
}
'''
scss_path.write_text(scss, encoding='utf-8')

print('OK: zastosowano V26.')
print('Auto zostalo obnizone, lekko zmniejszone i oddzielone od napisu.')
print('Uruchom teraz: npm run build && npm start')
