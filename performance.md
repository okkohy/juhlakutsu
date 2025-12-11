# Sovelluksen testaaminen suurella tietomäärällä

Olin toteuttanut sovellukseen jo sivutuksen valmiiksi ennen suuren tietomäärän luomista.

Ensiki [seed.py](./seed.py) skriptillä luotiin 1000 käyttäjää, 100 000 juhlaa ja 1 000 000 ilmottautumista tietokantaan.

Lisäsin [app.py](./app.py) seuraavat rivit:
```py
@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    elapsed_time = round(time.time() - g.start_time, 2)
    print("elapsed time:", elapsed_time, "s")
    return response
```

Sen jälkeen avasin sovelluksen ja etusivu latautui melko nopeasti. Myös haku toimi suhteellisen nopeasti sopivalla hakutermillä. Kun hakuun laittoi sellaisenkin hakutermin, joka palautti useita tuhansia tuloksia niin haun prosessoinnissa kesti vain n. 1 s. Nyt toisaalta hakutuloksien selaaminen on aika raskasta, joten hakutuloksien sivuttaminen ei olisi huono idea.

```
elapsed time: 0.02 s
127.0.0.1 - - [11/Dec/2025 13:27:59] "GET / HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [11/Dec/2025 13:27:59] "GET /static/styles.css HTTP/1.1" 304 -
elapsed time: 0.0 s
127.0.0.1 - - [11/Dec/2025 13:28:04] "GET /search HTTP/1.1" 308 -
elapsed time: 0.0 s
127.0.0.1 - - [11/Dec/2025 13:28:04] "GET /search/ HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [11/Dec/2025 13:28:04] "GET /static/styles.css HTTP/1.1" 304 -
elapsed time: 0.0 s
127.0.0.1 - - [11/Dec/2025 13:28:09] "GET /search?query=123 HTTP/1.1" 308 -
elapsed time: 0.03 s
127.0.0.1 - - [11/Dec/2025 13:28:09] "GET /search/?query=123 HTTP/1.1" 200 -
```

Kun taas yritin avata käyttäjäsivua /user/488, sovellus jäi jumiin useaksi (yli 10) minuutiksi ja minun oli tapettava se.

Tämä korjautui sillä, kun vaihtoi `get_attended`-funktion SQL kyselyn RIGHT JOIN lausekkeen LEFT JOIN lausekkeeksi


```
elapsed time: 0.14 s
127.0.0.1 - - [11/Dec/2025 13:56:59] "GET /party/91370 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [11/Dec/2025 13:56:59] "GET /static/styles.css HTTP/1.1" 304 -
elapsed time: 0.09 s
127.0.0.1 - - [11/Dec/2025 13:57:41] "GET /user/109 HTTP/1.1" 200 -
```

Nyt sivut kuitenkin latautuivat huomattavasti hitaammin kuin etusivu (0.14 s vs. 0.01 s).

Joten lisäsin yksi kerrallaan (välissä testaten uudestaan) kaksi indeksiä: 
```sql
CREATE INDEX idx_user_attended ON guests (user_id);
CREATE INDEX idx_party_guests ON guests (party_id);
```

Näiden jälkeen kaikki sovelluksen toiminnot tapahtuivat sopivan nopeasti (0.14s -> 0.01 s).

```
elapsed time: 0.01 s
127.0.0.1 - - [11/Dec/2025 14:35:43] "GET /party/5 HTTP/1.1" 200 -
```

/login ja /register toiminnot kestivät suunnilleen 0.05 s kumpikin tämän jälkeen, mutta indeksin luominen ei näyttänyt vaikuttavan siihen, joten en tehnyt niille mitään. Kun nämä kaksi indeksiä oli lisätty en möyskään nähnyt tarpeelliseksi lisätä ideksiä esimerkiksi kategoria tauluun (party\_categories )
