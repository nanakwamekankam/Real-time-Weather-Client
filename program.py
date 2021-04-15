import collections
import requests

loc = collections.namedtuple('location', 'city state country')
weather = collections.namedtuple('weather_data', 'location temp units description category')
# Report the weather


def show_header():

    print('-------------------------------')
    print('     Weather Client APP')
    print('-------------------------------')
    print()


def get_location_request():

    location = input("Location(e.g Portland, USA): ")
    print(f"You entered {location}")

    return location


def convert_to_plaintext(location):

    if not location or not location.strip:
        return None

    location = location.lower().strip()
    parts = location.split(',')

    city = ''
    state = ''
    country = ''

    if len(parts) == 1:
        city = parts[0].strip()
        country = 'GH'
    elif len(parts) == 2:
        city = parts[0].strip()
        country = parts[1].strip()
    elif len(parts) == 3:
        city = parts[0].strip()
        state = parts[1].strip()
        country = parts[2].strip()
    else:
        return None

    return loc(city, state, country)


def get_report_from_api(loc, units):

    url = f'https://weather.talkpython.fm/api/weather?city={loc.city}&country={loc.country}&units={units}'

    if loc.state:
        url += f'&state={loc.state}'

    resp = requests.get(url)
    if resp.status_code != 200:
        print(f'Error: {resp.text}')
        return None

    data = resp.json()

    return data


def user_friendly_report(data):

    temp = data.get('forecast').get('temp')
    temperature = data.get('forecast').get('feels_like')

    description = data.get('weather').get('description')
    category = data.get('weather').get('category')

    return temp, temperature, description, category


def main():

    show_header()
    location_text = get_location_request()
    location = convert_to_plaintext(location_text)
    print(f'City = {location.city.capitalize()}, State = {location.state.upper()}, Country = {location.country.upper()}')
    print()

    conversion = input('[S]tandard, [M]etric, [I]mperial: ')
    conversion = conversion.lower().strip()
    units = None

    if conversion == 's':
        units = 'standard'
    elif conversion == 'm':
        units = 'metric'
        scale = 'C'
    elif conversion == 'i':
        units = 'imperial'
        scale = 'F'

    weather_data = get_report_from_api(location, units)
    temp, temperature, description, category = user_friendly_report(weather_data)

    print()
    print(f"Weather in {location.city.capitalize()}, {location.country.upper()}")
    print(f'Temperature = {temp} {scale}, feels like {temperature} {scale}')
    print(f'{description.capitalize()}: {category.capitalize()}')


if __name__ == '__main__':
    main()
