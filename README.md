# Juhlakutsu

Kurssille tietokannat ja web-ohjelmointi

## Sovelluksen toiminnot


- [x] Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- [x] Käyttäjä pystyy luomaan juhlia. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään juhlia.
- [x] Käyttäjä näkee listan juhlista. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien juhlat.
- [x] Käyttäjä pystyy hakemaan juhlia hakusanalla. Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä tietokohteita.
- [x] Käyttäjä pystyy ilmottautumaan ja perumaan ilmottautumisen juhliin.
- [x] Sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä tilastoja ja käyttäjän lisäämät juhlat.
- [x] Käyttäjä pystyy valitsemaan juhlille yhden tai useamman luokittelun. Luokat ovat tietokannassa.
- [x] Sovelluksessa on pääasiallisen juhlien lisäksi toissijainen tietokohde ilmottautuminen, joka täydentää juhlaa.

## Sovelluksen testaaminen suurella tietomäärällä

[Raportti](./performance.md)

## Sovelluksen asentaminen

Helpointa on käyttää [Nix] työkalua:

```sh
# Ajetaan kehitysversio
nix run
```
Voidaan myös käynnistää kehitysympäristö:
```
nix develop
```

On mahdollista myös käyttää valmiiksi asennettua Pythonia. Projekti on tehty Python versiolla 3.11.14. Jos jokin seuraavista ohjeista ei toimi, kannattaa katsoa `flake.nix` tiedostoa, mitä komentoja pitäisi suorittaa.


```sh
python3 -m venv .venv
source .venv/bin/activate

pip3 install -U flask

sqlite3 database.db < schema.sql
sqlite3 database.db < init.sql

flask --app src/main run
```

[Nix]: <https://nixos.org/> "Nix package manager"
