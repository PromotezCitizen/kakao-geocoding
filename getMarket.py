import requests
import multiprocessing
from bs4 import BeautifulSoup as bs
import csv
import json

gasStation = []

KEY = 'YOUR_KAKAO_REST_KEY'

def kakaoMap(station):
    print(station)
    URI = f"https://dapi.kakao.com/v2/local/search/address.json?query={station}"
    res = requests.get(
        URI,
        headers= {
            'Authorization' : f'KakaoAK {KEY}' 
        }
    ).json()
    
    try:
        return res['documents'][0]
    except:
        return []

def gimhaesi():
    i = 1
    while True:
        DOMAIN="https://www.gimhae.go.kr/"
        URL=f"/00847/03380/07784.web?cpage={i}&stype=name&sstring=주유"

        data = requests.get(DOMAIN + URL).content

        soup = bs(data, 'html.parser')
        soup.prettify()

        table = soup.select('#body_content > div.list2table1 > table > tbody > tr')
        for td in table:
            name = td.select('td:nth-child(2)').pop().text
            address = td.select('td:nth-child(3)').pop().text.removesuffix(name).strip()
            l = len(address.split(' '))
            if l > 6:
                address = ' '.join(address.split(' ')[:l//2])

            gasStation.append([name, address])

        count = int(soup.select('#body_content > div.infomenu1.mg0 > div.left > div > b').pop().text) // 10 + 1

        if count == i:
            break
        
        i = i+1

    print(len(gasStation))
    for i, station in enumerate(gasStation):

        res = kakaoMap(station[1])

        try:
            res = [res["x"], res["y"]]
        except:
            res = [35.212527323063, 128.852741701312]
        gasStation[i].append(float(res[1]))
        gasStation[i].append(float(res[0]))

    with open("gimhaesi.csv", "w", newline="") as f:
        writer = csv.writer(f)
        for station in gasStation:
            print(station)
            writer.writerow(station)

def gyeongsangnamdo():
    temp = dict()
    gasStation = []
    with open("gyeongsangnamdo.json", "r", encoding="utf-8") as f:
        datas = json.load(f)

    for data in datas:
        name = data['AFLT_NM']
        address = data['AFLT_ROAD_ADDR']
        temp[name] = address

    for name, address in temp.items():
        res = kakaoMap(address) # 역지오코딩

        try:
            x = res['x']
            y = res['y']
        except:
            x = 0
            y = 0

        gasStation.append([name, address, y, x])

    with open("gyeongsangnamdo.csv", "w", newline="") as f:
        writer = csv.writer(f)
        for station in gasStation:
            print(station)
            writer.writerow(station)

# gyeongsangnamdo()
# print(kakaoMap("빅게임랜드"))


def test():
    URI = f"https://search.map.kakao.com/mapsearch/map.daum?callback=jQuery18103216564319496906_1697458921673&q=금오공대&msFlag=A&sort=0"
    res = requests.get(URI)
    return res.text
print(test())