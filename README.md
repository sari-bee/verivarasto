# Tietokantasovellus: Verivarasto

## Tilanne palautuksessa 3.4.:

Sovellukseen on luotu tarvittavat tietokantataulut poislukien käyttäjätietojen tallentamiseen (sisäänkirjautumistoimintoihin) tarvittavat taulut. Kaikkia sovelluksen käyttöön tarvittavia tietoja voidaan tallentaa sovellukseen. Käytön helpottamiseksi tässä vaiheessa tietojen syöttösivuilla listataan mahdolliset vaihtoehdot niiden tietojen osalta, joiden täytyy vastata aiemmin syötettyjä tietoja (esim. tietty verivalmiste, potilas, verivarasto...).  Jos listausta ei ole, niin kenttään voi syöttää mitä vain tietoja. Huomioi että jos vaihtoehtolistaus on sivulla mutta siellä ei ole vaihtoehtoja, niin ensin pitää lisätä ko. vaihtoehto. Esimerkiksi jotta voisit sisäänkirjata verivalmisteita, sinun pitää huolehtia, että olet kirjannut sovellukseen mahdollisia valmistetyyppejä, vastaavasti jotta voisit lisätä hoitoyksiköitä, sinulla pitää olla lisättynä verivarastoja, jotka voivat palvella ko. hoitoyksiköitä. Tämä hieman epäkäytännöllinen listaus toki muuttuu erilaiseksi ratkaisuksi lopulliseen sovellukseen. Syöttösivuilla on myös listaus kaikista tietokantaan syötetyistä kyseiseen sivuun liittyvistä tiedoista. Laajempia/monipuolisempia hakutoiminnallisuuksia en ole vielä toteuttanut. Mitään validointeja ei tietojen syötössä vielä ole, eli jos tietokantaan yritetään syöttää virheellistä tietoa, se johtaa palvelinvirheeseen. Ja esimerkiksi henkilötunnuksen muodolle ei ole mitään validointia toistaiseksi.

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
