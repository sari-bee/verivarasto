# Tietokantasovellus: Verivarasto

Heroku: https://verivarasto.herokuapp.com/

## Tilanne palautuksessa 3.4.:

Sovelluksessa voi tällä hetkellä toteuttaa perustoiminnallisuudet: lisätä verivalmisteita, potilaita, valmistetyyppejä, verivarastoja ja hoitoyksiköitä, sekä kirjata verensiirron potilaalle. Verivalmiste vanhenee automaattisesti syötetyn viimeisen käyttöpäivän mukaan, jolloin se ei ole enää potilaalle siirrettävissä. Vastaavasti potilaalle siirretyksi kirjattu valmiste ei ole enää käytettävissä muille. Edistyneempiä valmisteen käsittelyjä (esim. palautus hoitoyksiköstä, hävitys, siirto toiseen verivarastoon) ei ole vielä toteutettu. Myöskään sisäänkirjautumistoimintoa (käyttäjätietoja) ei ole vielä toteutettu, tämän vuoksi sovelluksesta ei vielä synny lokitietoa.

Sovelluksen lomakkeet ohjaavat tietojen syötössä. Niissä kentissä, joihin tulee syöttää määrämuotoista tietoa, vaihtoehto valitaan dropdown-valikosta (tai päivämäärän osalta kalenterista). Muihin kenttiin voi syöttää vapaamuotoista tekstiä. Syötettyjen tietojen validointi on kesken; vain osasta virheellisiä syötteitä tulee virheilmoitus, joka ei lisäksi vielä näy käyttöliittymässä; osa virheistä aiheuttaa palvelinvirheen ja osaa tarvittavista validoinneista ei ole vielä huomioitu lainkaan.

Sovellukseen ei ole vielä toteutettu hakutoiminnallisuuksia. Tietojen syötön yhteydessä näytetään kaikki ko. tiedosta tietokannassa oleva data.

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
