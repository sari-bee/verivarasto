# Tietokantasovellus: Verivarasto

Heroku: https://verivarasto.herokuapp.com/

## Tilanne palautuksessa 3.4.:

Käyttäjä- ja kirjautumistoiminnallisuutta ei vielä ole toteutettu, joten etusivulta siirrytään varsinaiseen sovellukseen suoraan klikkaamalla linkkiä. Varsinaisessa sovelluksessa navigoidaan ylälaidan linkkien avulla. Huomioitavaa on että missään lomakkeissa ei vielä ole varsinaisia validointeja (osassa virheellisiä syötteitä on virhekäsittely, mutta ei vielä virheilmoituksia käyttöliittymään).

Sovellus avautuu sivulle, jossa voi katsella ja hakea verivalmisteita eri hakuehdoilla. Hakuehdot täydentyvät vielä. Luovutusnumerohakuun voi napata numeron esimerkiksi Kaikki valmisteet-hausta, jossa luovutusnumero on jokaisen yksittäisen hakutuloksen ensimmäinen tietue. Tähän sivuun pääsee takaisin Verivarasto-linkistä. Verivarastotoiminnallisuuksista puuttuu vielä mahdollisuus siirtää valmiste toiseen varastoon ja mahdollisuus hävittää valmiste.

Verensiirron kirjaus-linkissä voi kirjata verensiirron. Alasvetovalikoissa on vaihtoehtoja vain, jos järjestelmässä on Käytettävissä olevia verivalmisteita (valmisteita, jotka eivät ole siirrettyjä potilaille tai vanhentuneita), ja jos järjestelmään on syötetty potilaita ja hoitoyksiköitä. Siirtopäivän voi toistaiseksi valita vapaasti, siinä ei ole validointia. Sovelluksessa ei myöskään toistaiseksi ole validointia valmisteen ja potilaan veriryhmän välillä. Lisäksi puuttuu valmisteen palautus varastoon (verensiirron peruminen). Verensiirron kirjauksessa ei tällä hetkellä tarkisteta sitä, yritetäänkö hoitoyksikköön lähettää sellaista valmistetta, joka on siinä verikeskuksessa, joka palvelee ko. hoitoyksikköä.

Verivalmisteen sisäänkirjauksessa voi sisäänkirjata verivalmisteen tiettyyn varastoon. Ne kentät, joissa ei ole alasvetovalikkoa, voi täyttää vapaasti. Fenotyypit-kenttä ei ole pakollinen. Kannattaa testata myös esimerkiksi jo valmiiksi vanhentuneen valmisteen syöttö ja huomata että sen tilaksi tulee Vanhentunut ja toisaalta sisäänkirjata valmiste, jonka sitten kirjaa siirretyksi potilaalle, jolloin huomaa, että valmisteen tilaksi muuttuu Siirretty.

Potilaat-sivulla voi hakea alasvetovalikosta tietyn potilaan tiedot ja verensiirrot tai lisätä potilaan. Potilaan tiedot voi toistaiseksi syöttää vapaasti. Fenotyyppivaatimukset-kenttä ei ole pakollinen. Sovelluksesta puuttuu mahdollisuus lisätä fenotyyppivaatimuksia jo kannassa olevalle potilaalle.

Ylläpitotoiminnoissa voi selata ja lisätä verivarastoja, hoitoyksiköitä ja valmistetyyppejä. Nämä voi syöttää vapaasti (poislukien hoitoyksikköä palvelevan verivaraston, joka valitaan alasvetovalikosta). Käyttäjä- ja kirjautumistoiminnallisuus tulee myöhemmin. Myöskään käyttäjiin liittyvää tietokantataulua ei vielä ole luotu.

## Alkuperäisidea:

Sovellus mallintaa verikeskuksen verivaraston hallintaa. Verivarastoja on useita, ja ne palvelevat kukin tiettyjä hoitoyksiköitä. Jokaiseen verivarastoon voidaan sisäänkirjata verivalmisteita, lähettää niitä potilaille, palauttaa, lähettää verivarastojen välillä tai hävittää. Verivalmisteet tulee kirjata siirretyiksi tietyille potilaille, valmisteen saaja tulee olla jäljitettävissä. Kaikesta toiminnasta jää lokitieto. Tätä varten sovellukseen tulee kirjautua.

Sovelluksessa käsitellään ainakin seuraavia erillisiä tietoja (tietokantatauluja):
- Verivarastot, joissa on tietyt verivalmisteet ja jotka palvelevat tiettyjä hoitoyksiköitä
- Hoitoyksiköt, joita palvelee tietty verivarasto; jokainen potilas saa yksittäisen verivalmisteen tietyssä hoitoyksikössä, mutta potilas voi saada valmisteita myös useassa hoitoyksikössä
- Potilaat, jotka saavat verivalmisteita. Potilaalla on ominaisuuksia (mm. veriryhmä), jotka ohjaavat verivalmisteen valintaa.
- Verivalmisteet, jotka ovat tietyssä verivarastossa, joita annetaan tietylle potilaalle tietyssä hoitoyksikössä, ja joilla on tietty tila (esim. varastossa, vanhentunut, siirretty, hävitetty). Verivalmisteilla on myös ominaisuuksia (mm. veriryhmä), jotka ohjaavat valmisteen valintaa potilaalle.
- Verensiirtotapahtumat, joihin liittyy tietty hoitoyksikkö, potilas ja verivalmiste
- Käyttäjät, jotka käsittelevät verivalmisteita eri tavoin (mm. sisäänkirjaus, lähetys potilaalle, hävitys)

Toisin sanoen verivarastoon sisäänkirjattuja verivalmisteita voidaan tietyin säännöin (mm. veriryhmäsopivuus) lähettää potilaille siirrettäväksi. Valmisteita voidaan myös palauttaa, lähettää toiseen verivarastoon tai hävittää. Verivalmisteiden sisäänkirjauksessa syötetään määrämuotoista dataa (mm. luovutusnumero, käytettävä ennen -tieto, veriryhmä), jonka oikeellisuus on tarkistettava. Vastaavasti potilaasta syötetään tietokantaan määrämuotoista dataa (mm. hetu, veriryhmä). Potilas lisätään sovelluksen kautta, jos potilas ei vielä ole tietokannassa.
Sovelluksesta tulee pystyä hakemaan listauksia eri kriteereillä (esimerkiksi tietylle potilaalle siirretyt verivalmisteet, hoitoyksikössä siirretyt verivalmisteet, tietyn verivaraston kaikki verivalmisteet, tietyn verivaraston voimassa olevat verivalmisteet, tietyn verivaraston valmisteet veriryhmän mukaan) sekä yksittäisen verivalmisteen tietoja luovutusnumeron perusteella.

Mallisovellukseen syötetään testidataa, jota ei voida sekoittaa todellisiin verivalmiste- tai potilastietoihin.

Valitsin aiheen, koska työskentelen verensiirtolääketieteen parissa ja haluan tutkia, minkälaisella tietomallilla verivarastokokonaisuutta voidaan hallita.
