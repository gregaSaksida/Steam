pot = 'spletne_strani'
import re
import os

iskani_niz = re.compile(
	r'<a href="(?P<url>http://store.steampowered.com/app/.*?)"  data-ds.*?'
	r'<span class="title">(?P<ime>.+?)</span>'
	r'.*?'
	r'row">(?P<datum>\d{1,2} [A-Z][a-z]{2}, (?P<leto>\d{4}))</div>'
	r'.*?'
	r'br&gt;(?P<odstotek>\d{1,2})% of the (?P<stevilo_ocen>(\d|,)*) user'
	r'.*?</span>',
	flags=re.DOTALL
)

def igre_stran(niz, stran):
    """Poišče opise vseh iger na spletni strani
	in jih shrani v seznam.
	"""
    seznam_iger = []
    m = niz.finditer(stran)
    for ujemanje in m:
        seznam_iger.append((ujemanje.group('ime'), ujemanje.group('datum'), 
                      ujemanje.group('odstotek'), ujemanje.group('stevilo_ocen')))
        print(ujemanje.groupdict()['odstotek'])
    return seznam_iger

def igre_stran1(niz, stran):
    """Poišče opise vseh iger na spletni strani
	in jih shrani v seznam.
	"""
    m = niz.search(stran)
    if m:
        print(m.group('stevilo_ocen'))
        

with open(os.path.join(pot, 'stran_1.html'), encoding="utf-8") as stran:
    vsebina_strani = stran.read()
#igre_stran(iskani_niz, vsebina_strani)
igre_stran1(iskani_niz, vsebina_strani)
print('konec')