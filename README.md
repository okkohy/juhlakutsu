# Juhlakutsu

Kurssille tietokannat ja web-ohjelmointi

## Sovelluksen toiminnot

Tulossa...

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

flask --app src/main run
```

[Nix]: <https://nixos.org/> "Nix package manager"
