# Tietokantasovellus: Verivarasto

Sovelluksen tarkoituksena on mallintaa verikeskuksen verivarastojen hallintaa. Verikeskuksessa on useita verivarastoja, joissa käsitellään verivalmisteita. Verivalmisteita sisäänkirjataan verivarastoon, josta ne lähetetään potilaille hoitoyksiköihin. Verivalmisteiden jäljitettävyys on tärkeää, joten jokaisesta sisäänkirjatusta verivalmisteesta tulee tietää, mitä sille on tapahtunut: mille potilaalle se on siirretty, tai onko se vanhentunut tai muuten hävitetty. Verikeskuksen toiminnot on rajattu tietylle käyttäjäryhmälle, joten kaikki sovelluksen näkymät ja toiminnot vaativat kirjautumisen.

Mallisovellukseen tulee syöttää testidataa, jota ei voida sekoittaa todellisiin potilas- tai verivalmistetietoihin.

Sovellus on käyttötarkoituksensa vuoksi käytettävissä työasemalla tai tabletilla, mutta sitä ei ole optimoitu puhelimen näytölle. 

## Sovelluksen käyttö Herokussa:

Heroku: https://verivarasto.herokuapp.com/

Sovellus aukeaa kirjautumissivulle, josta pääset rekisteröitymään Rekisteröidy-linkin kautta. Ellet halua rekisteröityä, voit käyttää yhteiskäyttötunnuksia
```bash
aku.ankka
Ankkalinna
```
Ethän vaihda yhteiskäyttötunnuksen salasanaa, kiitos!

## Sovelluksen käyttö paikallisesti:

1. Varmista, että koneellesi on asennettuna Python ja PostgreSQL.
2. Kloonaa projekti koneellesi.
3. Siirry projektin kansioon ja luo Pythonin virtuaaliympäristö komennolla 
```bash
python3 -m venv venv
```
4. Aktivoi virtuaaliympäristö komennolla
```bash
source venv/bin/activate
```
5. Asenna projektin riippuvuudet komennolla
```bash
pip install -r requirements.txt
```
6. Aseta ympäristömuuttujat luomalla projektikansioon tiedosto .env ja lisäämällä tiedoston sisällöksi seuraavat muuttujat:

DATABASE_URL=PostgreSQL:n [connection string](https://www.postgresql.org/docs/12/libpq-connect.html#LIBPQ-CONNSTRING)

SECRET_KEY=satunnainen merkkijono

7. Alusta tietokanta komennolla
```bash
psql < schema.sql
```
8. Käynnistä sovellus komennolla
```bash
flask run
```

Jatkossa voit käynnistää sovelluksen suorittamalla kohdat 4 ja 8. Virtuaaliympäristöstä voit poistua komennolla
```bash
deactivate
```

Tarvittaessa voit uudelleenalustaa tietokannan suorittamalla komennot
```bash
psql < drop_tables.sql
```
```bash
psql < schema.sql
```

## Sovelluksen näkymät

Käyttöliittymä ohjaa tarvittaessa syöttämään sovelluksen kenttiin oikean muotoista tietoa.

### Verivarasto

Verivarasto-sivulla voit hakea valmisteita eri hakuehdoilla. Valtaosassa hauista hakuehto valitaan pudotusvalikosta. Hae luovutusnumerolla - haku on kirjainkokoriippumaton ja tunnistaa myös osittaisen hakutermin. (Hakua varten tiedoksi, että valmisteen luovutusnumero on hakutuloksissa tietueen ensimmäinen tieto.) Varaston Käytettävissä-tilaiset verivalmisteet merkitään automaattisesti Vanhentunut-tilaan Käytettävä ennen -päivän jälkeen.

### Verensiirrot

Verensiirrot-sivulla voit kirjata verensiirron tai hakea hoitoyksikön verensiirtoja. Jälleen valtaosin tiedot valitaan pudotusvalikosta. Verensiirron voi kirjata vain, jos varastossa on Käytettävissä-tilassa olevia verivalmisteita. Siirron päivämäärää ei ole rajattu.

### Potilaat

Potilaat-sivulla voit hakea potilaan verensiirrot, potilas valitaan pudotusvalikosta. Lisäksi sivulla voi lisätä potilaan. Fenotyyppivaatimukset-kenttä ei ole pakollinen.

### Valmistetoiminnot

Valmistetoiminnot-sivulla voi sisäänkirjata valmisteen. Fenotyypit-kenttä ei ole pakollinen. Jälleen valtaosa tiedoista valitaan pudotusvalikosta. Käytettävä ennen -päivämäärää ei ole rajattu (jos Käytettävä ennen on menneisyydessä, valmiste siirtyy suoraan Vanhentunut-tilaan).

### Ylläpito

Ylläpito-sivulla voi lisätä verivarastoja, hoitoyksiköitä ja valmistetyyppejä sekä vaihtaa salasanansa.

### Loki

Loki-sivulle kertyy tietoa sovelluksessa tehdyistä toimenpiteistä.

## Jatkokehitysideat

Mahdollisia jatkokehitysideoita, joita osittain toteutan loppupalautukseen:
- Luovutusnumerolla hakiessa pitäisi löytää potilas, jolle verivalmiste on siirretty.
- Mahdollisuus palauttaa potilaalle kirjattu valmiste.
- Rajaus, että verivalmisteen voi lähettää hoitoyksikköön vain siitä verivarastosta, joka palvelee ko. hoitoyksikköä.
- Mahdollisuus lisätä potilaalle jälkikäteen fenotyyppivaatimuksia.
- Mahdollisuus poistaa voimasta verivarastoja, hoitoyksiköitä ja valmistetyyppejä.
- Lokitietoihin mahdollisuus rajata tietoja tai sivutus.

Todellisuudessa käyttäjät eivät voisi tämän tyyppisessä sovelluksessa rekisteröityä itse, vaan esim. pääkäyttäjä lisäisi (ja poistaisi) käyttäjätunnukset. Tähän sovellukseen olen lähinnä käytännön syistä toteuttanut itserekisteröitymisen enkä myöskään toteuttanut erillistä pääkäyttäjäroolia.

Sovelluksen lomakkeissa on useita kohtia, joissa valinta tehdään pudotusvalikosta. Tämä ei ole kovinkaan skaalautuva ratkaisu. Tein tämän ratkaisun tässä kontekstissa lähinnä siksi, että sovelluksen testaaminen on helpompaa kun kenttiin ei tarvitse osata vapaatekstinä antaa tietoja, joita tietokannasta jo löytyy. Todellisessa sovelluksessa tietenkin esimerkiksi potilaan haku verensiirron kirjauksessa tehtäisiin syöttämällä henkilötunnus vapaatekstinä.

Verivalmisteita potilaalle lähetettäessä olisi mahdollista tarkistaa, että verivalmisteen veriryhmä sopii potilaalle. Tämä vaatii monimutkaista päättelyä erikoistapauksineen, joten tätä ei ole sovellukseen toteutettu. Käytännössä verikeskuksen työntekijöiden vastuulla on aina varmistaa, että valmisteen veriryhmä sopii potilaalle.