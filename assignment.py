#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 12:10:06 2019

@author: manzar
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
url = "http://www.btma.org/supplier-directory.php?diameter_from=0&diameter_to=0&prismatic_length_from=0&prismatic_length_to=0&prismatic_width_from=0&prismatic_width_to=0&prismatic_height_from=0&prismatic_height_to=0&supplierSpeciality=0&supplierMaterial=0&supplierQuality=0&region=0&search="

req = requests.get(url)
soup = BeautifulSoup(req.text, 'lxml')
li = soup.findAll('td', {'class': 'companyName'})
links = []
for link in li:
    links.append(urljoin(url, link.a.attrs['href']))
header = "Company nmae, Telephone, Fax, Email, Links\n"
file = open('assignment.csv', 'w')
file.write(header)
for scrap in links:
    req = requests.get(scrap)
    soup = BeautifulSoup(req.text, 'lxml')
    ul = soup.findAll('ul', {'class': 'list-group'})
    li = ul[0].findAll('li', {'class': 'list-group-item'})
    name = soup.findAll('h3', {'id': 'companyInfo'})
    name = name[0].text.lstrip().replace(',', '')
    #print(name)
    num = []
    for value in li[1:]:
        val = value.text.lstrip()
        if(not any(c.isalpha() for c in val)):
            num.append(val)
    for value in li[1:]:
        if('@' in value.text.lstrip()):
            email = value.text.lstrip()
            #print(value.text.lstrip())
    
    ref = []
    for value in li[1:]:
        if('www' in value.text.lstrip()):
            ref.append(value.text.lstrip())
           # print(ref)
    
    count = 0
    re = ''
    for i in range(len(ref)): 
        if(count == len(ref) - 1):
            re = re + str(ref[i])
        else:
            re = re + str(ref[i]) + str(' | ')
        count += 1
    #print(re)
    
    if(len(num) == 2):
        tel = num[0]
        fax = num[1]
    elif(len(num) == 1):
        tel = num[0]
        fax = 'NaN'
    print(tel, fax)
    
    file.write(name + ', ' + tel + ', ' + fax + ', ' + email + ', ' + re + '\n')
file.close()