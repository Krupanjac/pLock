# pLock - Timer Aplikacija

Jednostavna aplikacija za upravljanje vremenom tokom prezentacija ili kvizova.

![pLock Screenshot](assets/screenshot.png)

## Sadržaj
- [Instalacija](#instalacija)
- [Upotreba](#upotreba)
- [Postavke](#postavke)
- [Prečice](#prečice)
- [Licenca](#licenca)

## Instalacija

1. **Obavezni preduvjeti**:
   - Python 3.x
   - Tkinter (obično već instaliran sa Pythonom)
   - Pillow biblioteka:  
     ```bash
     pip install Pillow
     ```

2. **Font**:
   - Preuzmite font [DS-Digital](https://www.dafont.com/ds-digital.font)
   - Kreirajte folder `fonts` u projektu
   - Postavite `DS-DIGIT.ttf` u `fonts` folder

3. **Slike**:
   - Kreirajte folder `assets` sa sledećim fajlovima:
     - `replika.png` (60s)
     - `pitanje.png` (90s)
     - `novarec.png` (120s)
     - `tehnickareplika.png` (30s)

## Upotreba

### Osnovne funkcije
- **Timer A** (levo):
  - Podrazumevano 20:00
  - Klikom na vreme resetuje se na početnu vrednost
  - "Pauziraj/Nastavi" dugme

- **Timer B** (desno):
  - Postavlja se prečicama 1-4
  - "Pauziraj T2/Nastavi T2" dugme

### Opcije (dugmad 1-4):
1. **Replika** - 60 sekundi
2. **Pitanje** - 90 sekundi 
3. **Nova Reč** - 120 sekundi
4. **Tehnička Replika** - 30 sekundi

Prelazom miša preko dugmeta prikazuje se naziv opcije.

## Postavke

Pristup preko dugmeta "Podešavanja":
- Promena početnog vremena za Timer A
- Izmena trajanja za svaku opciju
- Sve promene se primenjuju odmah

## Prečice

- **1-4**: Pokretanje odgovarajuće opcije
- **Klik na Timer A**: Resetovanje
- **ALT + F4**: Zatvaranje aplikacije

## Licenca

Ovaj projekat je licenciran pod MIT licencom. Pogledajte [LICENSE](LICENSE) fajl za detalje.
