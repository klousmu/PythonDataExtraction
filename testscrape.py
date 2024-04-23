
import requests
import pandas as pd
from bs4 import BeautifulSoup

url = 'https://www.statista.com/statistics/215655/number-of-registered-weapons-in-the-us-by-state/'

soup = BeautifulSoup(requests.get(url).content, 'html.parser')

tds = soup.select('#statTableHTML td')
data = []
for td1, td2 in zip(tds[::2], tds[1::2]):
    data.append({'State':td1.text, 'Number': td2.text})

df = pd.DataFrame(data)
df.to_excel('testscrape.xlsx', index=False)
print(df)
