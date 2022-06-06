import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re

url = 'https://slickdeals.net'
results = requests.get(url)

soup = BeautifulSoup(results.text, "html.parser")

#Information Storage
itemName = []
salePrice = []
originalPrice = []
savings = []
likes = []
links = []

def convertToNum(s):
    a = s[:0]
    b = s[1:]
    try:
        return float(a+b)
    except: 
        return 0

bestDeals_div = soup.find_all('li', class_='bp-p-socialDealCard bp-p-dealCard bp-c-card bp-c-card--border')

for container in bestDeals_div:
    name = container.find('a', class_='bp-c-card_title bp-c-link').text
    itemName.append(name)
    
    price = container.find('span', class_='bp-p-dealCard_price').text if container.find('span', class_='bp-p-dealCard_price') else '-'
    salePrice.append(price)
    price = convertToNum(price)

    oPrice = container.find('span', class_='bp-p-dealCard_originalPrice').text if container.find('span', class_='bp-p-dealCard_originalPrice') else '-'
    originalPrice.append(oPrice)
    oPrice = convertToNum(oPrice)

    savings.append(abs(oPrice-price))
    
    like = container.find('span', class_='bp-p-votingThumbsPopup_voteCount js-votingThumbsPopup_voteCount').text if container.find('span', class_='bp-p-votingThumbsPopup_voteCount js-votingThumbsPopup_voteCount') else '-'
    likes.append(like)

    link = container.find('a', attrs={'href':re.compile("/f")})
    linkA = link.get('href')
    links.append(url+linkA)

dealList = pd.DataFrame({
    'Name' : itemName,
    'Sale Price' : salePrice,
    'Original Price' : originalPrice,
    'Savings' : savings,
    '# of Likes' : likes,
    'Link' : links,
})

dealList.to_csv('deals.csv')