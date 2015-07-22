__author__ = 'megdahlgren'

import requests
import xml.etree.ElementTree as ET
import locale


'''
this command-line program does the following
1) given an address, returns the zpid
2) given a zpid, returns a zestimate

my zws_id: X1-ZWz1a6057c0y6j_2rqd6

'''



def get_zpid(zwsid, address, citystatezip):
    '''given zwsid (zillow web services id), address (url encoded property address) and citystatezip (url encoded city+state AND/OR zip code),returns zpid'''
    #sample call = 'http://www.zillow.com/webservice/GetSearchResults.htm?zws-id=<ZWSID>&address=2114+Bigelow+Ave&citystatezip=Seattle%2C+WA'
    url = 'http://www.zillow.com/webservice/GetSearchResults.htm?zws-id={0}&address={1}&citystatezip={2}'.format(zwsid, address, citystatezip)
    data = requests.get(url).text
    root = ET.fromstring(data)
    for zpid_el in root.iter('zpid'):
        return zpid_el.text


def get_zestimate(zwsid, zpid):
    '''
    :param zpid: given zpid for a property
    :return: zestimate for that property
    '''
    url = 'http://www.zillow.com/webservice/GetZestimate.htm?zws-id={0}&zpid={1}'.format(zwsid, zpid)
    data = requests.get(url).text
    root = ET.fromstring(data)
    locale.setlocale(locale.LC_ALL, 'en_US')
    for amount_el in root.iter('amount'):
        return locale.currency(int(amount_el.text), grouping=True)



def main():
    zwsid = 'X1-ZWz1a6057c0y6j_2rqd6' # since this isn't going to change, would this be an instance when a global variable would be ok?
    test_zpid = get_zpid(zwsid, '93+Hillside+Ave', 'Metuchen%2C+NJ')
    test_zestimate = get_zestimate(zwsid, test_zpid)
    print test_zestimate

if __name__ == '__main__':
    main()

