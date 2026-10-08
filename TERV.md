# megkerulhetetlen.hu — könyv-aloldalak (landingek) TERV

Állapot: **ÉPÍTVE 2026-10-08, előnézet él a GitHub Pages-en; DNS-átállás és hiányzó anyagok várnak.** Forrás-brief: Notion „Landingek” oldal
(https://novastudio.notion.site/Landingek-3f0c32f2c061804db64ceaf712d80e95), nyers export: `anyagok/notion-landingek-export.json`.

## 1. Mi ez

Kalti „Megkerülhetetlen” könyvébe QR-kódok kerülnek; minden QR egy aloldalra visz a **megkerulhetetlen.hu** fődomain alatt.
A Notion-adatbázis 17 aloldalt sorol fel, 3 sablonba sorolva, a könyv 3 fejezetéhez (Storytelling, Rendszerek, Stratégia) kötve.

A domain ma Rackhost-parkolón áll (91.227.139.235, „Ez a domain a Rackhost-nál került regisztrálásra”), tehát szabad, a DNS-t mi kezeljük a Rackhost-adminban.

## 2. A 17 oldal, sablononként

### A) „Megkerülhetetlen széria” sablon — 9 oldal (podcast-epizód ajánló)
Szerkezet a Notion szerint: felül Megkerülhetetlen (series) text-logó → rövid leírás + werkfotó → beágyazott YouTube-videó → „Meghallgatom Spotify-on” + „Megnézem YouTube-on” gomb → két bekezdéses kivonat, váltott oldalon werkfotókkal → az oldal alján néhány gondolat a könyv folytatásáról.

| # | Fejezet | Notion-slug | Videó | Megjegyzés |
|---|---|---|---|---|
| 1 | Storytelling | /karizma | youtube 1LrShjuliN8 (Karizma Podcast #133, Bolya Imre csatornája) | werkfotók: STILLS EXPORT Drive-mappa (publikus) |
| 2 | Storytelling | /megkerülhetetlen_Gundel_Takacs_Gabor | **nincs** | |
| 3 | Rendszerek | /megkerülhetetlen_Kocsis_Attila | **nincs** | |
| 4 | Rendszerek | /megkerülhetetlen_Godor_Zola | **nincs** | |
| 5 | Rendszerek | /megkerülhetetlen_Tusnadi_Roland | **nincs** | |
| 6 | Rendszerek | /megkerülhetetlen_Bese_Nora | **nincs** | |
| 7 | Rendszerek | /megkerülhetetlen_Bolya_Imre | **nincs** | |
| 8 | Stratégia | /megkerülhetetlen_Szauer_Tamas | **nincs** | |
| 9 | Stratégia | /megkerülhetetlen_hormonmentes | **nincs** | |

### B) „Nova storytelling oldal” sablon — 3 oldal (videó + fotóalbum + pár gondolat)
| # | Fejezet | Slug | Videó | Megjegyzés |
|---|---|---|---|---|
| 10 | Rendszerek | /idokapszula | XThr6gDvqY4 „Saját szabályokat írunk” (publikus) | szöveg nincs, a videó leiratából írható |
| 11 | Stratégia | /luminance | XCVth2kInlI „Luminance doku” (unlisted) | album + pohárköszöntő-átirat (`anyagok/poharkoszonto-atirat.txt`) |
| 12 | Stratégia | /megkerulhetetlen_werk | **ugyanaz a Luminance-videó** van beírva | valószínűleg copy-paste hiba, a nagyforgatás werk-videó hiányzik |

### C) „Marketing elem” sablon — 5 oldal (lead magnet + Kajabi-űrlap)
| # | Fejezet | Slug | Mi van meg | Mi hiányzik |
|---|---|---|---|---|
| 13 | – | /storycanvas | teljes copy, VSL (VQChFnGw1A0, unlisted), Kajabi form-embed (2149744349), köszönőoldal Kajabin | munkafüzet-kép |
| 14 | Rendszerek | /stressz_teszt | teljes könyv-copy + a meglévő Kajabi-oldal szövege (nova.mykajabi.com/stressz-teszt) | Kajabi form-embed ID, a 15 perces videó |
| 15 | Stratégia | /kamera-elotti-magabiztossag | videó 5dUyEBMdQkk (unlisted, „ws draft”) | copy, ajánlat, űrlap |
| 16 | Stratégia | /podcast_booster | referencia-szerkezet: nova.mykajabi.com/trustfunnel_adastematika (hero → ígéret → 4 pontos „miért” → űrlap) | copy, űrlap |
| 17 | Stratégia | /branding_roadmap | semmi | minden |

## 3. Technikai terv

- **Hely:** `~/megkerulhetetlen-hu/` (ez a mappa), új GitHub-repo `gyovaiadam97/megkerulhetetlen-hu`, GitHub Pages a `docs/` mappából, CNAME = megkerulhetetlen.hu. Ugyanaz a bevált séma, mint a trustfunnel.hu és a kezdobefekteto.hu. (A novastudio.hu-nál beragadt cert itt nem kockázat: a domain parkolón áll, nincs élő forgalom, amit megzavarnánk.)
- **Nem WordPress, nem Kajabi:** sima statikus HTML, nulla futásidejű függőség, a Kajabi csak az űrlap-embed és a köszönőoldal.
- **Build:** egy kis Python-szkript (`build.py`) + 3 HTML-sablon + oldalanként egy rövid markdown/JSON tartalomfájl (`content/<slug>.md`). Így az új epizód-oldal = egy 20 soros tartalomfájl, nem egy kézzel másolt HTML. (token-efficiency szerint: a sablont egyszer írjuk meg, a többi determinisztikus.)
- **Dizájn — DÖNTÉST KÉR:** a Notion-brief „a könyv sötét, neonkék világát” kéri, üvegszerű dizájnnal. A **végleges borító (2026-10-08, Ádám küldte) viszont világos**: fehér-szürke, elmosott tömeg a háttérben, mély kékes-teal címfelirat, fekete ing, vastag geometrikus sans. Javaslat: a végleges borítót kövessük, ne a régi sötét-arany koncepciót — világos alap, elmosott fotós háttér-sáv a hero mögött, a borító teal-kékje (kb. #2F6F8F) kiemelésnek, fekete szöveg, finom üveg-kártyák. Ha Kalti ragaszkodik a sötét verzióhoz, a borító teal-kékjével sötét alapon is megépíthető — a sablon mindkettőt tudja egy színtoken-cserével. **Menüsáv nélkül, mobilra tervezve** (QR-ról telefonon nyílik). Betűk: a borító betűjéhez illő geometrikus sans (Unbounded a Nova-arculatból, ellenőrizni a borítóval) + Poppins szövegnek.
- **Képek:** werkfotók WebP-re konvertálva, max 1600 px, lazy-load; a Drive-ról egyszer letöltve a repóba.
- **Videó:** YouTube-embed privacy-módban (youtube-nocookie), csak kattintásra tölt (facade), hogy a mobil ne legyen lassú.
- **Mérés:** oldalanként OG-kép + cím (megosztáshoz); Meta Pixel / GA csak ha Kalti kéri.
- **QR-kódok:** a build legenerálja minden oldal QR-jét SVG-ben és PNG-ben (`qr/<slug>.svg`) a nyomdának — a slug ezért print előtt legyen végleges.
- **Gyökér (megkerulhetetlen.hu/):** a könyv sales-landingje (`~/kalti-konyv-landing`, Kalti viszi) — ide egyelőre egy egyszerű nyitóoldal kerül a 3 fejezet aloldalaival; döntés kell, hogy a sales-landing ide költözik-e.

### Javasolt slug-változtatás (döntést kér)
A Notion-slugok ékezetesek és aláhúzásosak (`/megkerülhetetlen_Gundel_Takacs_Gabor`). Nyomtatott QR-hoz ASCII, kisbetűs, kötőjeles slugot javaslok, mert az ékezetes URL a QR-ben hosszabb, és egyes olvasók/böngészők kódolva (`%C3%BC`) mutatják. Javaslat: `/gundel-takacs-gabor`, `/kocsis-attila`, `/godor-zola`, `/tusnadi-roland`, `/bese-nora`, `/bolya-imre`, `/szauer-tamas`, `/hormonmentes`, `/karizma`, `/idokapszula`, `/luminance`, `/werk`, `/storycanvas`, `/stressz-teszt`, `/kamera-elotti-magabiztossag`, `/podcast-booster`, `/branding-roadmap`. A Notion-slugok átirányításként megmaradhatnak.

## 4. Hiányzó bemenetek (Kaltitól / Novától)

1. **8 széria-epizód:** YouTube-link, Spotify-link, 1 mondatos leírás és a kétbekezdéses kivonat (vagy a leirat, amiből megírjuk). A Nova-csatornán csak a régi S1-epizódok vannak (Bese Nóra, Zola, Tusnádi) — ezek a régiek, vagy új „Megkerülhetetlen” felvételek?
2. **Spotify-műsor linkje** (a „Meghallgatom Spotify-on” gombhoz).
3. **Werkfotó-mappa:** a „Nova podcast werkfotó mappa” Drive-link bejelentkezést kér — megosztás vagy letöltés kell. (A STILLS EXPORT mappa publikus, azt le tudom tölteni.)
4. **Megkerülhetetlen text-logó** fájl + a **végleges borító nagy felbontásban** (PNG/PDF, a hero-hoz és az OG-képekhez; a chatben kapott kép csak előnézet).
5. **„Néhány gondolat a könyv folytatásáról”** — mi a folytatás? (Kaltitól 3-4 mondat, vagy megírjuk a Behind the Book leiratokból.)
6. **Werk-oldal videója** (a Notionban a Luminance-videó van duplán) + a Luminance-album fotói.
7. **Stressz teszt** Kajabi form-embed ID-ja + a 15 perces videó linkje.
8. **Kamera előtti magabiztosság:** mi az ajánlat (ingyenes workshop-videó? jelentkezés?), copy, űrlap.
9. **Podcast Booster** és **Branding Roadmap:** teljes brief hiányzik (ajánlat, copy, űrlap).
10. **Gyökéroldal:** a sales-landing költözik ide, vagy marad külön?
11. **Slug-döntés** (3. pont).

## 5. Ütemezés (szeletenként, mindegyik végén a user néz rá a dev-oldalon)

1. **Alap:** repo + build-szkript + dizájn-tokenek + A-sablon → a **/karizma** oldal teljesen készen (minden anyag megvan hozzá). Ezen hagyjuk jóvá a vizuális irányt, mielőtt a többi 16 készülne.
2. **C-sablon:** /storycanvas (minden megvan) + /stressz-teszt (űrlap-ID-ra placeholder).
3. **B-sablon:** /idokapszula (leirat → draft copy, humanizerrel), /luminance (pohárköszöntő-átirat → copy), /werk placeholderrel.
4. **A többi 8 széria-oldal** a beérkező anyagokból — tartalomfájl + build, oldalanként pár perc.
5. **Kamera / Booster / Roadmap** a brief beérkezésekor.
6. **Élesítés:** GitHub Pages + CNAME + Rackhost DNS (A-rekordok a GitHub IP-kre, www CNAME), HTTPS-kényszerítés, QR-ok legenerálva, nyomda előtt minden QR telefonnal kipróbálva.

## 6. Ellenőrzések (a „kész” feltétele)

- minden oldal mobilon (375 px) és asztalon rendben, nincs vízszintes görgetés;
- Lighthouse mobil ≥ 90 teljesítmény az A-sablonon;
- minden külső link (YouTube, Spotify, Kajabi) 200-at ad;
- a Kajabi-űrlapok valódi beküldéssel végpróbázva, a köszönőoldalra érkezés ellenőrizve;
- QR → oldal próba telefonról, élesben, HTTPS-sel;
- a 17 oldal OG-címe és leírása egyedi.

## Döntések (Ádám, 2026-10-08)
- Dizájn: világos, teal-kék, a végleges borító stílusa (a Notion „sötét neonkék” kérése téves).
- Slugok: ASCII, kötőjeles.
- Gyökér: a könyv sales-landingje, utoljára hagyjuk.
- Széria-podcastok még nincsenek megvágva → YouTube/Spotify-gombok placeholderrel, később cserélve.
- Werk-oldal: placeholder (a videó sincs kész).
- Podcast Booster: a nova.mykajabi.com/trustfunnel_adastematika szerkezete alapján.
- Branding Roadmap: nincs kész, egyelőre amit lehet (váz).
- Kalti első 3 leírása (Karizma, Gundel, Storycanvas) a minta a többihez.
- Borító legnagyobb felbontása: Drive-mappa 1tTSz5ZT0NEw-tabuODmdgP0Bv7iNwSzH.
- Stressz teszt űrlap-ID: Ádám később adja.

## Hogyan működik (új sessionnek)
- `content/<slug>.json` = egy oldal tartalma (sablon: `series` | `story` | `lead`). `_`-vel kezdődő fájlok segédanyagok.
- `templates/` = Jinja2-sablonok (base, _parts makrók, series, story, lead). `docs/assets/css/style.css` = a teljes dizájn.
- `python3 build.py` → `docs/<slug>/index.html` + alias-átirányítások + `docs/qr/<slug>.svg|png`. **Élesítéskor `python3 build.py --cname`** (addig CNAME nélkül, hogy a github.io előnézet működjön).
- Deploy: `git add -A && git commit && git push` (repo gyovaiadam97/megkerulhetetlen-hu, Pages a main `/docs`-ból).
- Előnézet: https://gyovaiadam97.github.io/megkerulhetetlen-hu/ (ideiglenes lista) · lokálisan `cd docs && python3 -m http.server 8795`.
- Forrásanyagok (gitignore alatt): `anyagok/kezirat/*.txt` (a 3 fejezet kézirata), `anyagok/kezirat-qr-kontextus.txt` (a QR-helyek szövegkörnyezete), `anyagok/stills/` (Karizma werkfotók), `anyagok/poharkoszonto-atirat.txt`, `anyagok/karizma-leirat.txt`.

## Állapot oldalanként (2026-10-08)
| Oldal | Kész | Hiányzik |
|---|---|---|
| /karizma | teljes (videó, 8 werkfotó, kivonat, idézetek) | Spotify-link (Karizma Podcast) |
| /storycanvas | teljes (copy, Kajabi-űrlap 2149744349, VSL) | munkafüzet borítóképe (most teal placeholder) |
| /stressz-teszt | teljes (copy, Kajabi-űrlap 2149712715) | a 15 perces bevezető videó |
| /kamera-elotti-magabiztossag | teljes (90 perces workshop-videó, copy) | – |
| /idokapszula | videó + copy + 12 csapatportré, hero a Luminance csapatfotó | – |
| /luminance | videó + pohárköszöntő-gondolatok + 12 képes galéria a teljes albumból | – |
| /werk | váz + stúdiófotó-galéria (HQ) | werkvideó, a nagyforgatás saját fotói |
| /podcast-booster | copy + az e-book valódi borítója (Drive, Lead magnetek) | Kajabi-űrlap ID |
| /branding-roadmap | váz, zárszó-copy | az anyag maga + űrlap |
| 8 Edition-epizód | hero (Kristóf-fotó ideiglenesen) + „miért ez a beszélgetés” a kéziratból, placeholder videó | YouTube/Spotify-link, kivonat, vendég-werkfotók (a „Nova Podcast werkfotók” mappa NEM látszik a service-accountnak, megosztás kell: shorts-torlo@ceges-gmail-claudenak.iam.gserviceaccount.com; Gódor és Hormonmentes almappa ott sincs) |

## Napló
- 2026-10-08 (később): a Nova marketing Drive-mappa (1j9X5uU1…) a short-ütemező service-accountjával elérhető → Luminance-album (223 kép), csapatportrék, HQ-stúdiófotók, Kristóf-fotók, Podcast Booster e-book letöltve (`anyagok/drive/`, eszközök: `anyagok/drive_ls.py`, `anyagok/drive_get.py`, kulcs Bitwarden `SHORTS_DRIVE_SA_JSON`). Fotók beépítve, push kész.
- 2026-10-08: build-rendszer + 3 sablon + 17 oldal megépítve a kézirat szövegére építve; repo + Pages él (előnézet github.io alatt). A Drive werkfotó-mappa letöltését a jogosultsági szűrő blokkolta → Ádám tölti le vagy megosztja. Borító: ideiglenes placeholder (`docs/assets/img/borito.jpg`), a végleges fájl kell.
- 2026-10-08: végleges borító megérkezett (világos, teal-kék cím) — ütközik a Notion „sötét, neonkék” kérésével, döntés kell.
- 2026-10-08: Notion-brief kinyerve API-n át (17 sor + aloldal-tartalmak), referencia-anyagok megnézve, terv megírva. Jóváhagyásra vár.
