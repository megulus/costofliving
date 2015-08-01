

import requests
import json
import arrow


gmap_api_key = 'AIzaSyBwp2FaIFGQyGZfMJvXVngGUYGSHGf2mIM'

def get_driving_time(origin, destination, avoid=None, departure_time='now', arrival_time=None, units='imperial'):
    '''
    :param origin: origin address or location (string), e.g., '93 Hillside Ave Metuchen NJ 08840' or 'Brooklyn NY'
    :param destination: destination address or location
    :param avoid: optional - can avoid tolls, highways or ferries
    :param units: defaults to imperial (other option is metric)
    :param departure_time: defaults to now; can specify as integer in seconds since midnight, 01.01.1970
    :param arrival_time: optional
    :return:
    '''
    url_params = {'origins': origin, 'destinations': destination, 'avoid': avoid, 'departure_time': departure_time, 'arrival_time': arrival_time, 'units': units}
    url = 'http://maps.googleapis.com/maps/api/distancematrix/json'
    data = requests.get(url, params=url_params)
    data = json.loads(data.text)
    return data


def get_rush_hour_departure_time():
    '''
    assumes rush hour departure means a weekday morning
    :return:
    '''
    now = arrow.utcnow()
    day_of_week = now.weekday()
    locale_instance = arrow.locales.get_locale('en_us')



def main():
    test_driving_results = get_driving_time('209 4th St Jersey City NJ', '86 Chambers St New York NY')
    # again, should I ultimately aim to have helper functions that do the following json parsing?
    driving_time = test_driving_results['rows'][0]['elements'][0]['duration']['text']
    origin = test_driving_results['origin_addresses'][0]
    destination = test_driving_results['destination_addresses'][0]
    print 'origin:', origin
    print 'destination:', destination
    print 'driving time:', driving_time



if __name__ == '__main__':
    main()

