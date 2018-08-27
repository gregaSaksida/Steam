# Analiza iger na Steamu:

Zajeti podatki:
  - ime,
  - leto izdaje,
  - delež dobrih ocen,
  - število vseh ocen,
  - cena,
  - razvijalec,
  - izdajatelj,
  - potreben RAM,
  - potreben prostor na trdem disku,
  - žanri.

Zajeti podatki, ki niso bili uporabljeni:
  - kategorije: podobno kot žanri, le da jih definirajo igralci. Ravno zato so neuporabne, saj si jih igralci skorajda izmišljujejo.
  - datum izdaje: točnega datuma nisem potreboval, v njem nisem videl večjega smisla.

Analiza: predvsem odvisnost lastnosti iger od cene in razvijalcev.

---------------------------------------------------------------

Datoteka "<b>prenos_strani_1.py</b>" prenese spletne strani s seznami iger.

Datoteka "<b>prenos_strani_22.py</b>" prebere te shranjene spletne strani, na podlagi URL naslovov v njih obišče in prenese spletne strani s podrobnejšimi opisi iger.

Datoteka "<b>podatki_strani.py</b>" prebere shranjene spletne strani s podrobnejšimi opisi iger, izlušči iz njih podatke in jih shrani v .json in .csv datoteke.

Datoteka "<b>analiza.ipynb</b>" vsebuje analizo podatkov.

Ostale pythonove datoteke, ki so bile zgolj poskusne, sem pobrisal.