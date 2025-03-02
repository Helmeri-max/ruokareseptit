# Ruokareseptit


## Tavoitteet:

- Sovelluksessa käyttäjät pystyvät jakamaan ruokareseptejään. Reseptissä lukee tarvittavat ainekset ja valmistusohje.
- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä pystyy lisäämään reseptejä ja muokkaamaan ja poistamaan niitä.
- Käyttäjä näkee sovellukseen lisätyt reseptit.
- Käyttäjä pystyy etsimään reseptejä hakusanalla.
- Käyttäjäsivu näyttää, montako reseptiä käyttäjä on lisännyt ja listan käyttäjän lisäämistä resepteistä.
- Käyttäjä pystyy valitsemaan reseptille yhden tai useamman luokittelun (esim. alkuruoka, intialainen, vegaaninen).
- Käyttäjä pystyy antamaan reseptille kommentin ja arvosanan. Reseptistä näytetään kommentit ja keskimääräinen arvosana.

## Sovelluksen lopullinen tila
- Käyttäjä pysyy luomaan tunnuksen ja kirjautumaan sovellukseen
- Käyttäjä voi luoda, katsella, muokata, poistaa ja hakea reseptejä hakusanalla
- Käyttäjä voi kommentoida omia ja muiden reseptejä, sekä muokata/poistaa kommenttinsa
- Käyttäjätunnuksilla on omat sivunsa jossa näkyy käyttäjän reseptit
- Lisättäessä reseptille voi antaa luokituksia

## Sovelluksen asennus

Asenna flask-kirjasto:
```$ pip install flask```

Tietokantatiedosto database.db tulee repon mukana, mutta sen tyhjentäminen muutamista testiresepteistä onnistuu komennoilla:

```
$ rm database.db
$ sqlite3 database.db < schema.sql
```

Voit käynnistää sovelluksen näin:

```$ flask run```


## Sovelluksen suorituskyky suurella datamäärällä
Indeksien ja sivutuksen lisäämisen jälkeen etusivu latautuu n. 0.2 sekunnissa, seed.py tiedostossa generoidulla tietokannan sisällöllä. (100k reseptiä, 1M kommenttia). 
