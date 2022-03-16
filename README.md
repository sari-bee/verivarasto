# Tietokantasovellus: Verivarasto

Sovellus mallintaa verikeskuksen verivaraston hallintaa. Verivarastoja on useita,
ja ne palvelevat kukin tiettyjä hoitoyksiköitä. Jokaiseen verivarastoon voidaan
sisäänkirjata verivalmisteita, lähettää niitä potilaille, palauttaa, lähettää verivarastojen
välillä tai hävittää. Verivalmisteet tulee kirjata siirretyiksi tietyille potilaille, valmisteen saaja tulee olla jäljitettävissä. Kaikesta toiminnasta jää lokitieto. Tätä varten sovellukseen tulee kirjautua.

Sovelluksessa käsitellään ainakin seuraavia erillisiä tietoja (tietokantatauluja):
- Verivarastot, joissa on tietyt verivalmisteet ja jotka palvelevat tiettyjä hoitoyksiköitä
- Hoitoyksiköt, joita palvelee tietty verivarasto; jokainen potilas saa yksittäisen verivalmisteen tietyssä hoitoyksikössä, mutta potilas voi saada valmisteita myös useassa hoitoyksikössä
- Potilaat, jotka saavat verivalmisteen/valmisteita tietyssä hoitoyksikössä. Potilaalla on ominaisuuksia (mm. veriryhmä), jotka ohjaavat verivalmisteen valintaa.
- Verivalmisteet, jotka ovat tietyssä verivarastossa, joita annetaan tietylle potilaalle tietyssä hoitoyksikössä, ja joilla on tietty tila (esim. varastossa, vanhentunut, siirretty, hävitetty). Verivalmisteilla on myös ominaisuuksia (mm. veriryhmä), jotka ohjaavat valmisteen valintaa potilaalle.
- Verensiirtotapahtumat, joihin liittyy tietty hoitoyksikkö, potilas ja verivalmiste
- Käyttäjät, jotka käsittelevät verivalmisteita eri tavoin (mm. sisäänkirjaus, lähetys potilaalle, hävitys)

Toisin sanoen verivarastoon sisäänkirjataan verivalmisteita, joita voidaan tietyin säännöin (mm. veriryhmäsopivuus) lähettää potilaille siirrettäväksi. Valmisteita voidaan myös palauttaa, lähettää toiseen verivarastoon,
tai hävittää. Verivalmisteiden sisäänkirjauksessa syötetään määrämuotoista dataa (mm. luovutusnumero, käytettävä ennen -tieto, veriryhmä), jonka oikeellisuus on tarkistettava.
Vastaavasti potilaasta syötetään tietokantaan määrämittaista dataa. Myös potilaiden lisäys onnistuu sovelluksen kautta, jos potilas ei vielä ole tietokannassa.
Sovelluksesta tulee pystyä hakemaan listauksia eri kriteereillä (esimerkiksi tietylle
potilaalle siirretyt verivalmisteet, hoitoyksikössä siirretyt verivalmisteet, tietyn verivaraston kaikki verivalmisteet, tietyn verivaraston voimassa olevat verivalmisteet, tietyn verivaraston valmisteet veriryhmän mukaan).

Mallisovellukseen syötetään testidataa, jota ei voida sekoittaa todellisiin verivalmiste-
tai potilastietoihin.

Valitsin aiheen, koska työskentelen verensiirtolääketieteen parissa ja haluan tutkia, 
minkälaisella tietomallilla verivarastokokonaisuutta voidaan hallita.
