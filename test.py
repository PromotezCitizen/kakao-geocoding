REST_API_KEY = 'YOUR_KAKAO_REST_KEY'

import requests

AUTHORIZATION = f'KakaoAK {REST_API_KEY}'
FORMAT = 'json'

def getGeometryFromKeywords(keywords: str) -> dict:
    '''
        docs : https://developers.kakao.com/docs/latest/ko/local/dev-guide#search-by-keyword
    '''
    keyword_uri = f'https://dapi.kakao.com/v2/local/search/keyword.{FORMAT}'
    res = requests.get(url=keyword_uri,
                    headers={
                        'Authorization': AUTHORIZATION  
                    },
                    params= {
                        'query': keywords
                    })
    return res.json()['documents']

def getGeometryFromAddress(address) -> dict:
    '''
        docs : https://developers.kakao.com/docs/latest/ko/local/dev-guide#address-coord
    '''
    address_uri = f'https://dapi.kakao.com/v2/local/search/address.{FORMAT}'
    res = requests.get(url=address_uri,
                    headers={
                        'Authorization': AUTHORIZATION  
                    },
                    params= {
                        'query': address
                    })
    return res.json()['documents']

def getAddressFromGeometry(geometry: list) -> dict:
    # geometry[0]: x, geometry[1]: y
    '''
        docs : https://developers.kakao.com/docs/latest/ko/local/dev-guide#coord-to-address
    '''
    geo_uri = f'https://dapi.kakao.com/v2/local/geo/coord2address.{FORMAT}'
    res = requests.get(url=geo_uri,
                    headers={
                        'Authorization': AUTHORIZATION  
                    },
                    params= {
                        'x': geometry[0],
                        'y': geometry[1]
                    })
    return res.json()['documents']

datas = getGeometryFromKeywords('빅게임랜드')
for data in datas:
    geometry = [ data['x'], data['y'] ]
    road_address = data['road_address_name']
    print(f"x(long): {geometry[0]}, y(lat): {geometry[1]}, road_address: {road_address}")

data = datas[-1]
x, y = data['x'], data['y']

print("*"*50)
datas = getGeometryFromAddress('경북 구미시 구미중앙로 120-1')
for data in datas:
    geometry = [ data['x'], data['y'] ]
    road_address = data['road_address']['address_name']
    print(f"x(long): {geometry[0]}, y(lat): {geometry[1]}, road_address: {road_address}")

print("*"*50)
datas = getAddressFromGeometry([x, y])
for data in datas:
    road_address_name = data['road_address']['address_name']
    print(road_address_name)