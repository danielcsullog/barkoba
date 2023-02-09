# Barkóba

Feladat
  - Készítsünk egy barkóba alkalmazást. A szerver legyen képes kiszolgálni
több klienst. A szerver válasszon egy egész számot 1..100 között
véletlenszerűen. A kliensek próbálják kitalálni a számot.

Kliens
  - A kliens üzenete egy összehasonlító operátor: <, >, = és egy egész szám, melyek jelentése: kisebb-e, nagyobb-e, mint az egész szám, illetve
  rákérdez a számra. A kérdésekre a szerver Igen/Nem/Nyertél/Kiestél/Vége üzenetekkel tud válaszolni. 
  A Nyertél és Kiestél válaszok csak a rákérdezés (=) esetén lehetségesek.
  - Nyertél, Kiestél és Vége üzenet fogadása esetén a kliens bontja a kapcsolatot és terminál. Igen/Nem esetén folytatja a kérdezgetést.
  - A kliens logaritmikus keresés segítségével találja ki a gondolt számot. A kliens tudja, hogy milyen intervallumból választott a szerver.
  - Kliens NE a standard inputról dolgozzon.
  - Minden kérdés küldése előtt véletlenszerűen várjon 1-5 mp-et. Ezzel több kliens tesztelése is lehetséges lesz.
  - Üzenet formátuma a klienstől a szerver felé: 
    - bináris formában egy db karakter, 32 bites egész szám
    - karakter lehet: <: kisebb-e, >: nagyobb-e, =: egyenlő-e
  - Parancssori argumentumok a futtatáshoz
    - client.py <server_address> <server_port>
  
Szerver
  - A kommunikációhoz TCP-t használjunk!
  - Ha egy kliens kitalálta a számot, akkor a szerver minden újabb kliens üzenetre az „Vége” üzenetet küldi, amire a kliensek kilépnek. 
  A szerver addig nem választ új számot, amíg minden kliens ki nem lépett.
  - Üzenet formátuma a szervertől a kliens felé:
    - ugyanaz a bináris formátum mint a kliensnél, de a számnak nincs szerepe (bármi lehet)
    - karakter lehet: I: Igen, N: Nem, K: Kiestél, Y: Nyertél, V: Vége
  - Parancssori argumentumok a futtatáshoz
    - server.py <bind_address> <bind_port> 
