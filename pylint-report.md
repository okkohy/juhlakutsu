# Pylint-raportti

Pylint antaa seuraavan tulosteen:
```
************* Module app
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:21:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:28:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:37:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
app.py:56:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:64:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:65:4: R1705: Unnecessary "elif" after "return", remove the leading "el" from "elif" (no-else-return)
app.py:90:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:91:4: R1705: Unnecessary "elif" after "return", remove the leading "el" from "elif" (no-else-return)
app.py:126:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:163:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:178:4: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
app.py:187:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:195:4: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
app.py:206:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:218:4: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
app.py:232:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:247:4: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
app.py:261:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:263:4: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
app.py:275:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:2:0: W0611: Unused import time (unused-import)
************* Module src.db
src/db.py:1:0: C0114: Missing module docstring (missing-module-docstring)
src/db.py:6:0: C0116: Missing function or method docstring (missing-function-docstring)
src/db.py:13:0: C0116: Missing function or method docstring (missing-function-docstring)
src/db.py:13:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
src/db.py:21:0: C0116: Missing function or method docstring (missing-function-docstring)
src/db.py:25:0: C0116: Missing function or method docstring (missing-function-docstring)
src/db.py:25:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
************* Module src.users
src/users.py:1:0: C0114: Missing module docstring (missing-module-docstring)
src/users.py:7:0: C0116: Missing function or method docstring (missing-function-docstring)
src/users.py:13:4: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
src/users.py:22:0: C0116: Missing function or method docstring (missing-function-docstring)
src/users.py:37:0: C0116: Missing function or method docstring (missing-function-docstring)
src/users.py:67:0: C0116: Missing function or method docstring (missing-function-docstring)
src/users.py:75:4: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
src/users.py:81:0: C0116: Missing function or method docstring (missing-function-docstring)
src/users.py:86:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module src.party
src/party.py:1:0: C0114: Missing module docstring (missing-module-docstring)
src/party.py:8:0: C0116: Missing function or method docstring (missing-function-docstring)
src/party.py:16:0: C0116: Missing function or method docstring (missing-function-docstring)
src/party.py:35:4: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
src/party.py:59:0: C0116: Missing function or method docstring (missing-function-docstring)
src/party.py:98:0: C0116: Missing function or method docstring (missing-function-docstring)
src/party.py:132:0: C0116: Missing function or method docstring (missing-function-docstring)
src/party.py:164:0: C0116: Missing function or method docstring (missing-function-docstring)
src/party.py:171:0: C0116: Missing function or method docstring (missing-function-docstring)
src/party.py:205:0: C0116: Missing function or method docstring (missing-function-docstring)
src/party.py:249:0: C0116: Missing function or method docstring (missing-function-docstring)
src/party.py:262:0: C0116: Missing function or method docstring (missing-function-docstring)
src/party.py:275:0: C0116: Missing function or method docstring (missing-function-docstring)
src/party.py:282:0: C0116: Missing function or method docstring (missing-function-docstring)
src/party.py:290:0: C0116: Missing function or method docstring (missing-function-docstring)
src/party.py:303:0: C0116: Missing function or method docstring (missing-function-docstring)
src/party.py:307:0: C0116: Missing function or method docstring (missing-function-docstring)
src/party.py:311:0: C0116: Missing function or method docstring (missing-function-docstring)
src/party.py:312:4: R1705: Unnecessary "elif" after "return", remove the leading "el" from "elif" (no-else-return)
src/party.py:1:0: R0801: Similar lines in 2 files
==src.party:[60:66]
==src.users:[38:44]
    SELECT parties.id
    , parties.title
    , parties.description
    , parties.start_date
    , parties.entry_fee
    , parties.user_id (duplicate-code)

------------------------------------------------------------------
Your code has been rated at 8.36/10 (previous run: 8.35/10, +0.00)
```

Raportti on generoitu sen jälkeen kun kaikki olennaiset korjaukset on tehty

## Docstring-ilmoitukset

```
src/db.py:1:0: C0114: Missing module docstring (missing-module-docstring)
src/db.py:6:0: C0116: Missing function or method docstring (missing-function-docstring)
src/db.py:13:0: C0116: Missing function or method docstring (missing-function-docstring)
```

Nämä ilmoitukset tarkoittavat sitä, että moduulia tai funktiota ei ole dokumentoitu docstring kommentilla. Tätä ei ole tehty, koska kyseessä ei ole kirjasto ja sen sijaan on panostettu siihen, että koodi on valmiiksi niin luettavaa, ettei kommenttiin jäisi mitään sanottavaa


## Tarpeeton else

Raportissa on seuraavat ilmoitukset liittyen `else`-haaroihin:

```
app.py:90:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:91:4: R1705: Unnecessary "elif" after "return", remove the leading "el" from "elif" (no-else-return)
```

Esimerkiksi ensimmäinen ilmoitus koskee seuraavaa koodia:

```python
if ...:
    return redirect(f"/party/{party_id}")
else:
    abort(make_response("Illegal method"))
```

Tämä koodi olisi mahdollista kirjoittaa seuraavasti tiiviimmin:

```python
if ...:
    return redirect(f"/party/{party_id}")

abort(make_response("Illegal method"))
```

Kuitenkin sovelluksen on selkeämpää kirjoittaa `else`-haara, koska se tuo esille kaksi vaihtoehtoa, miten koodi voi toimia eri tilanteissa. (Kyseisessä funktiossa kolme)




## Vaarallinen oletusarvo

Raportissa on seuraavat ilmoitukset liittyen vaaralliseen oletusarvoon:

```
db.py:10:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
db.py:20:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
```

Esimerkiksi ensimmäinen ilmoitus koskee seuraavaa funktiota:

```python
def execute(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params)
    con.commit()
    g.last_insert_id = result.lastrowid
    con.close()
```

Tässä parametrin oletusarvo `[]` on tyhjä lista. Tässä ongelmaksi voisi tulla, että sama oletusarvona oleva tyhjä listaolio on jaettu kaikkien funktion kutsujen kesken ja jos jossain kutsussa listan sisältöä muutettaisiin, tämä muutos näkyisi myös muihin kutsuihin. Käytännössä tässä tapauksessa tämä ei kuitenkaan haittaa, koska koodi ei muuta listaoliota.


## Toistettua koodia

```
src/party.py:1:0: R0801: Similar lines in 2 files
==src.party:[60:66]
==src.users:[38:44]
    SELECT parties.id
    , parties.title
    , parties.description
    , parties.start_date
    , parties.entry_fee
    , parties.user_id (duplicate-code)

```
Pylint valittaa, koska yllä oleva koodi on duplikoitu kahteen eri funktioon, mutta koska kyseessä on SQL kysely, ei ole turvallista abstrahoida tätä mitenkään. Toisessa funktiossa etsitään käyttäjän id:n perusteella ja toisessa juhlien (party) id:n mukaan. Ei ole turvallista dynaamisesti luoda kyselyä merkkijonojen manipulaatiolla tms.
