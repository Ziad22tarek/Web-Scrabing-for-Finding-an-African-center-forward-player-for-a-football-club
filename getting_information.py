import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

land_id=['149','173','124','4','107','54','31','105','85','6','21','38','82','159']
page=0
PlayersList = []
ValuesList = []
Age=[]
Nationality=[]
links=[]
full_link=[]
clubs=[]
heights=[]
dates=[]
Citizenship=[]
u=0
for i in land_id:
    page='https://www.transfermarkt.com/spieler-statistik/wertvollstespieler/marktwertetop/plus/0/galerie/0?ausrichtung=Sturm&spielerposition_id=14&altersklasse=23-30&jahrgang=0&land_id='+i+'&kontinent_id=0&yt0=Show'
    
    result = requests.get(page, headers=headers)
    src=result.content
    pageSoup=BeautifulSoup(src,'lxml')

    Players = pageSoup.find_all("a", {"class": "spielprofil_tooltip"})
    Values = pageSoup.find_all("td", {"class": "rechts hauptlink"})
    print(i)

    
    for x in range(0,23):
        try:
            PlayersList.append(Players[x].text)
        except:
            PlayersList.append('N/A')
        try:
            val=Values[x].text
            dot=val.find('.')
            ValuesList.append(val[0:dot])
        except:
            ValuesList.append('N/A')
        try:
            a=Players[x].attrs['href']
            links.append(a)
        except:
            print('No Result')

        
for i in links:
    a='https://www.transfermarkt.com'+str(i)
    full_link.append(a)
    print('Run')
for i in full_link:
    page_link=str(i)
    result_link = requests.get(page_link, headers=headers)
    src_link=result_link.content
    pageSoup_link=BeautifulSoup(src_link,'lxml')
    Club=pageSoup_link.find('span',{'class':'hauptpunkt','itemprop':'affiliation'})
    Date_of_birth=pageSoup_link.find('span',{'itemprop':'birthDate','class':'dataValue'})
    Height=pageSoup_link.find('span',{'itemprop':'height','class':'dataValue'})
    Nationality=pageSoup_link.find('span',{'itemprop':'nationality'})
    print(i)
    try:
        Citizenship.append(Nationality.text)
    except:
        Citizenship.append('N/A')
    try:
        clubs.append(Club.text)
    except:
        clubs.append('N/A')
    try:
        dates.append(Date_of_birth.text.strip()[:12])
    except:
        dates.append('N/A')
    try:
        heights.append(Height.text)
    except:
        heights.append('N/A')

        
        
df=pd.DataFrame({'Players':PlayersList,'Values':ValuesList ,'Club':clubs,'Height':heights, 'Date_of_birth':dates, 'Citizenship':Citizenship,'Links':full_link })


writer = pd.ExcelWriter('center forward.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1', index=False)
writer.save()

        
