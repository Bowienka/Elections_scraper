"""
projekt_3.py: treti projekt do Engeto Online Python Akademie
author: Helena Vyplelová
email: vyplelhel@seznam.cz
discord: Helena V. /.helenav.
"""

import sys
import csv
import requests
from bs4 import BeautifulSoup


# funkce ke scrapingu dat 
def ziskej_data(odkaz):
    odp_serveru_poprve = requests.get(odkaz) # získání raw html
    soup = BeautifulSoup(odp_serveru_poprve.content, "html.parser") # parsování html 
    
    vsechny_tabulky = soup.find_all("table", {"class": "table"}) # vyhledání tabulek
    
    data_seznam = []
    # procházení dat a jejich "vyzobávání" pomoci for cyklu
    for tabulka in vsechny_tabulky:
        vsechny_obce = tabulka.find_all("tr")[2:]
    
        for obec in vsechny_obce:
            kod_obce_element = obec.find("td", {"class": "cislo"})
            if kod_obce_element is not None:
                kod_obce = kod_obce_element.text
            else:
                kod_obce = "N/A"
                
            nazev_obce_element = obec.find("td", {"class": "overflow_name"})
            if nazev_obce_element is not None:
                nazev_obce = nazev_obce_element.text
            else:
                nazev_obce = "N/A" 
            
            odkaz_z_obce = obec.find("a")
            if odkaz_z_obce is not None:            
                odkaz_na_data = "https://volby.cz/pls/ps2017nss/" + obec.find("a")["href"]

            data_z_odkazu = ziskej_data_z_odkazu(odkaz_na_data)
            hlasy = ziskej_hlasy_z_odkazu(odkaz_na_data) 
        
            data_seznam.append({
                "kód_obce": kod_obce,
                "název_obce": nazev_obce,
                **data_z_odkazu, # **přidání_slovníků
                **hlasy
            })
        
    return data_seznam

# funkce získá dílčí data v zanořeném linku - voliči, obálky, platné hlasy - a vrátí je v podobě slovníku
def ziskej_data_z_odkazu(data_odkaz):
    odpoved_serveru_podruhe = requests.get(data_odkaz)
    data_soup = BeautifulSoup(odpoved_serveru_podruhe.content, "html.parser")
    
    volici = data_soup.find("td", headers="sa2").text
    vydane_obalky = data_soup.find("td", headers="sa3").text
    platne_hlasy = data_soup.find("td", headers="sa6").text
            
    return {
        "počet_voličů": volici,
        "vydané_obálky": vydane_obalky,
        "platné_hlasy": platne_hlasy,    
    }
# funkce získá dílčí data v zanořeném linku - počty hlasů pro jednotlivé strany - a vrátí je v podobě slovníku
def ziskej_hlasy_z_odkazu(data_odkaz):
    odpoved_serveru_potreti = requests.get(data_odkaz)
    data_soup = BeautifulSoup(odpoved_serveru_potreti.content, "html.parser")

    vsechny_strany_tab1 = data_soup.find_all("td", headers="t1sa1 t1sb2")
    vsechny_hlasy_tab1 = data_soup.find_all("td", headers="t1sa2 t1sb3")

    vsechny_strany_tab2 = data_soup.find_all("td", headers="t2sa1 t2sb2")
    vsechny_hlasy_tab2 = data_soup.find_all("td", headers="t2sa2 t2sb3")

    hlasy_stran = {}
    for s in range(len(vsechny_strany_tab1)):
        nazev_strany = vsechny_strany_tab1[s].text.strip()
        pocet_hlasu = vsechny_hlasy_tab1[s].text.strip()
        hlasy_stran[nazev_strany] = pocet_hlasu

    for s in range(len(vsechny_strany_tab2)):
        nazev_strany = vsechny_strany_tab2[s].text.strip()
        pocet_hlasu = vsechny_hlasy_tab2[s].text.strip()
        hlasy_stran[nazev_strany] = pocet_hlasu

    return hlasy_stran

# funkce zapíše data do CSV tabulky
def zapis_data(data: list, jmeno_souboru: str) -> str:
    
    with open(jmeno_souboru, mode="w", encoding="utf-8", newline="") as csv_soubor:
        sloupce = data[0].keys()

        zapis = csv.DictWriter(csv_soubor, fieldnames=sloupce)
        zapis.writeheader()
        zapis.writerows(data)    
        
# hlavní funkce spustí program 
def main():
    if len(sys.argv) != 3:
        print("Zadej dva argumenty: <odkaz_na_uzemni_celek> <jmeno_vystupniho_souboru.csv>.")
        return
    
    odkaz = sys.argv[1]
    jmeno_souboru = sys.argv[2]

    if not odkaz.startswith("https://"):
        print("První argument musí být webová adresa, druhý název výstupního souboru.")
    else:
        print(f"Načítám data z: {odkaz}")

    try:
        data = ziskej_data(odkaz)
        if data is not None:
            zapis_data(data, jmeno_souboru)
            print(f"Ukládám data do souboru: {jmeno_souboru}")
        else:
            print("Nastala chyba při získávání dat.")
    except Exception as e:
        print(f"Nastala chyba: {e}")

    print("Ukončuji program.")

if __name__ == "__main__":
    main()
