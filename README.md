# Tietokantasovellus: Verivarasto

Sovelluksen tarkoituksena on mallintaa verikeskuksen verivarastojen hallintaa. Verikeskuksessa on useita verivarastoja, joissa käsitellään verivalmisteita. Verivalmisteita sisäänkirjataan verivarastoon, josta ne lähetetään potilaille hoitoyksiköihin. Verivalmisteiden jäljitettävyys on tärkeää, joten jokaisesta sisäänkirjatusta verivalmisteesta tulee tietää, mitä sille on tapahtunut: mille potilaalle se on siirretty, tai onko se vanhentunut tai muuten hävitetty. Verikeskuksen toiminnot on rajattu tietylle käyttäjäryhmälle, joten kaikki sovelluksen näkymät ja toiminnot vaativat kirjautumisen.

Mallisovellukseen tulee syöttää testidataa, jota ei voida sekoittaa todellisiin potilas- tai verivalmistetietoihin.

Sovellus on käyttötarkoituksensa vuoksi käytettävissä työasemalla tai tabletilla, mutta sitä ei ole optimoitu puhelimen näytölle. 

## Sovelluksen käyttö Herokussa:

Heroku: https://verivarasto.herokuapp.com/

Sovellus aukeaa kirjautumissivulle, josta pääset rekisteröitymään Rekisteröidy-linkin kautta. Ellet halua rekisteröityä, voit käyttää yhteiskäyttötunnuksia
```bash
aku.ankka
Ankkalinna1
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

Verivarasto-sivulla voit hakea valmisteita eri hakuehdoilla. Valtaosassa hauista hakuehto valitaan pudotusvalikosta. Hae luovutusnumerolla -haku on kirjainkokoriippumaton ja tunnistaa myös osittaisen hakutermin. (Hakua varten tiedoksi, että valmisteen luovutusnumero on hakutuloksissa tietueen ensimmäinen tieto.) Varaston Käytettävissä-tilaiset verivalmisteet merkitään automaattisesti Vanhentunut-tilaan Käytettävä ennen -päivän jälkeen (Käytettävä ennen = käytettävä ennen päivän loppua, tyypillisesti verivalmisteissa ilmaistu esim. käytettävä ennen 6.5.2022 23:59).

### Verensiirrot

Verensiirrot-sivulla voit kirjata verensiirron, hakea yksittäisen verensiirron tiedot tai hakea hoitoyksikön verensiirrot. Jälleen valtaosin tiedot valitaan pudotusvalikosta. Verensiirron voi kirjata vain, jos varastossa on Käytettävissä-tilassa olevia verivalmisteita. Siirron päivämäärää ei ole rajattu.

### Potilaat

Potilaat-sivulla voit hakea potilaan verensiirrot, potilas valitaan pudotusvalikosta. Potilaan valittuasi voit lisätä hänelle fenotyyppivaatimuksia. Lisäksi sivulla voi lisätä uuden potilaan. Fenotyyppivaatimukset-kenttä ei ole potilasta lisättäessä pakollinen.

### Valmistetoiminnot

Valmistetoiminnot-sivulla voi sisäänkirjata valmisteen. Fenotyypit-kenttä ei ole pakollinen. Jälleen valtaosa tiedoista valitaan pudotusvalikosta. Käytettävä ennen -päivämäärää ei ole rajattu (jos Käytettävä ennen on menneisyydessä, valmiste siirtyy suoraan Vanhentunut-tilaan). Lisäksi sivulla voi palauttaa potilaalle lähetetyn valmisteen, hävittää varastossa olevan valmisteen tai siirtää valmisteen verivarastosta toiseen.

### Ylläpito

Ylläpito-sivulla voi lisätä verivarastoja, hoitoyksiköitä ja valmistetyyppejä sekä vaihtaa salasanansa.

### Loki

Loki-sivulle kertyy tietoa sovelluksessa tehdyistä toimenpiteistä. Tietoja voi rajata päivämäärien perusteella.

## Ongelmat ja jatkokehitysideat

Todellisuudessa käyttäjät eivät voisi tämän tyyppisessä sovelluksessa rekisteröityä itse, vaan esim. pääkäyttäjä lisäisi (ja poistaisi) käyttäjätunnukset. Tähän sovellukseen olen lähinnä käytännön syistä toteuttanut itserekisteröitymisen enkä myöskään toteuttanut tässä vaiheessa erillistä pääkäyttäjäroolia.

Sovelluksen lomakkeissa on useita kohtia, joissa valinta tehdään pudotusvalikosta. Tämä ei ole kovinkaan skaalautuva ratkaisu. Tein tämän ratkaisun tässä kontekstissa lähinnä siksi, että sovelluksen testaaminen on helpompaa kun kenttiin ei tarvitse osata vapaatekstinä antaa tietoja, joita tietokannasta jo löytyy. Todellisessa sovelluksessa tietenkin esimerkiksi potilaan haku verensiirron kirjauksessa tehtäisiin syöttämällä henkilötunnus vapaatekstinä (tai lukemalla viivakoodilta).

Verivarastoja, hoitoyksiköitä ja valmistetyyppejä voisi olla tarve poistaa voimasta. Tällöin kuitenkaan vanhat jo syötetyt tiedot eivät saa hävitä. Koska tällaisia muutoksia tapahtuu harvoin, en toteuttanut käyttöliittymään mahdollisuutta tähän.

Verivalmisteita sisäänkirjatessa voisi valmisteen veriryhmän valinta mukautua valmisteen tyypin mukaan (osassa valmisteita huomioidaan ABO- ja RhD-veriryhmät, osassa vain ABO). Tämä vaatisi kuitenkin mahdollisten veriryhmävaihtoehtojen syöttöä myös valmistetyyppejä lisätessä, joten tätä ei ole tässä vaiheessa toteutettu.

Verivalmisteiden lähetyksen hoitoyksiköihin voisi rajata niin, että valmisteen voi lähettää hoitoyksikköön vain, jos se on siinä verivarastossa, joka palvelee ko. hoitoyksikköä. Tätä toiminnallisuutta en kuitenkaan tässä vaiheessa toteuttanut. Käytännössä, oikeassa käytössä sovellusta käytettäisiin niin, että verivalmisteen etiketistä luettaisiin viivakoodinlukijalla valmisteen luovutusnumero ja tällöin tietysti valmisteen pitää olla fyysisesti paikan päällä oikeassa verivarastossa. Näin ollen ohjelmallisesti tätä ei välttämättä ole tarpeen rajata. Ohjelmassa valmisteiden kirjaus tiettyyn verivarastoon ja mahdollisuus siirtää verivarastosta toiseen palvelee varastonhallintaa: sovelluksesta saa nopeasti käsityksen, minkä verran ja minkälaisia valmisteita kussakin verivarastossa on.

Verivalmisteita potilaalle lähetettäessä olisi mahdollista tarkistaa, että verivalmisteen veriryhmä sopii potilaalle. Tämä vaatii monimutkaista päättelyä erikoistapauksineen, joten tätä ei ole sovellukseen toteutettu. Käytännössä verikeskuksen työntekijöiden vastuulla on aina varmistaa, että valmisteen veriryhmä sopii potilaalle.