"""Prenese sezname iger."""

import requests
import os

url = 'https://store.steampowered.com/search/?category1=998&filter=topsellers&page='

pot = 'spletne_strani'

def prenesi_strani(delni_url, stevilo):
	os.makedirs(pot, exist_ok=True)
	for index in range(1, stevilo + 1):
		stran = requests.get(delni_url + '{}'.format(index))
		with open(os.path.join(pot, 'stran_{}.html'.format(index)),
		'w', encoding='utf-8') as datoteka:
			datoteka.write(stran.text)
		print(os.path.join(pot, 'stran_{}.html'.format(index)))

print('Program bo sedaj prenesel 334 spletnih strani.')
prenesi_strani(url, 334)