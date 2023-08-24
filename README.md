
# ELECTIONS SCRAPER

## Popis projektu
Tento program slouží k získávání volebních dat z parlamentních voleb 2017 a jejich uložení v podobě tabulky do CSV souboru. Odkaz na zdrojovou stránku [zde](https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ). 
## Instalace knihoven
V kódu jsou použity knihovny requests pro stahování webových stránek a knihovny BeautifulSoup pro parsování HTML obsahu. Tyto knihovny lze nainstalovat ze souboru ```requirements.txt``` pomocí následujících příkazů:
```ruby
> pip3 --version #overeni verze manazeru
> pip3 install -r requirements.txt #instalace knihoven
```
## Spuštění programu
Po nainstalování knihoven spustíte skript ``main.py`` v příkazovém řádku zadáním *dvou povinných argumentů*:

- **odkaz_na_uzemni_celek**: webová adresa, kde jsou dostupná volební data
- **jmeno_vystupniho_souboru.csv**: název výstupního CSV souboru, do něhož budou data uložena

### Příklad spuštění:
1. **argument:** https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6201
2. **argument:** vysledky_blansko.csv
```ruby 
python main.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6201" vysledky_blansko.csv
```
<sub>POZN. Umístěním odkazu do uvozovek předejdete problémům se zakázanými znaky v url.<\sub>

### Průběh stahování:
```ruby
Načítám data z: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6201
Ukládám data do souboru: vysledky_blansko.csv
Ukončuji program.
```
### Částečný výstup:
```ruby
kód_obce,název_obce,počet_voličů,vydané_obálky...
581291,Adamov,3 668,2 157,2 138,208,3,5,222,0,76,241,37,18,28...
581313,Bedřichov,205,155,153,16,0,2,10,0,3,4,0,3,8,0,0,13,0,6...
```
Extrahovaná data se následně uloží do souboru s příponou `.csv`.
## Kontakt

Pokud máte nějaké dotazy, nápady nebo připomínky k tomuto skriptu, neváhejte kontaktovat autora:

- **Autor:** Helena Vyplelová
- **E-mail:** vyplelhel@seznam.cz
- **Discord:** Helena V. /.helenav. Tato funkce 
