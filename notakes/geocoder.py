import requests

API_KEY = '8013b162-6b42-4997-9691-77b7074026e0'


def geocoder(address):
    server_address = 'http://geocode-maps.yandex.ru/1.x/?'
    api_key = API_KEY
    # Готовим запрос.
    geocoder_request = f'{server_address}apikey={api_key}&geocode={address}&format=json'

    # Выполняем запрос.
    response = requests.get(geocoder_request)
    print(response)
    if response:
        # Преобразуем ответ в json-объект
        json_response = response.json()
    else:
        raise RuntimeError('')
    features = json_response['response']['GeoObjectCollection']['featureMember']
    return features[0]['GeoObject'] if features else None


def get_address_coords(address):
    toponym = geocoder(address)
    if not toponym:
        return None, None
    toponym_address = toponym['metaDataProperty']['GeocoderMetaData']['text']
    toponym_coords = toponym['Point']['pos']
    toponym_longitude, toponym_lattitude = toponym_coords.split(' ')
    return float(toponym_longitude), float(toponym_lattitude)


def get_ll(address):
    toponym = geocoder(address)
    if not toponym:
        return None, None
    toponym_coords = toponym['Point']['pos']
    toponym_longitude, toponym_lattitude = toponym_coords.split(' ')
    ll = ','.join([toponym_lattitude, toponym_longitude])
    envelope = toponym['boundedBy']['Envelope']
    l, b = envelope['lowerCorner'].split(' ')
    r, t = envelope['upperCorner'].split(' ')
    dx = abs(float(l) - float(r)) / 2
    dy = abs(float(t) - float(b)) / 2
    span = f'{dx},{dy}'
    return ll, span


def show_map(ll_spn,map_type='map', add_params=None):
    if ll_spn:
        map_request = f'https://yandex.ru/1.x/?{ll_spn}&l={map_type}'
    else:
        map_request = '/?l={map_type}'

    if add_params:
        map_request += '&' + add_params
    response = requests.get(map_request)