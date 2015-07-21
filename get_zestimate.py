__author__ = 'megdahlgren'

import requests
import xml.etree.ElementTree as ET


'''
this command-line program does the following
1) given an address, returns the zpid
2) given a zpid, returns a zestimate
'''



def get_zpid(zwsid, address, citystatezip):
    '''given zwsid (zillow web services id), address (url encoded property address) and citystatezip (url encoded city+state AND/OR zip code),returns zpid'''
    #url = 'http://www.zillow.com/webservice/GetSearchResults.htm?zws-id=<ZWSID>&address=2114+Bigelow+Ave&citystatezip=Seattle%2C+WA'
    url = 'http://www.zillow.com/webservice/GetSearchResults.htm?zws-id={0}&address={1}&citystatezip={2}'.format(zwsid, address, citystatezip)
    data = requests.get(url).text
    root = ET.fromstring(data)
    for zpid_el in root.iter('zpid'):
        return zpid_el.text



def main():
    test_zpid = get_zpid('X1-ZWz1a6057c0y6j_2rqd6', '93+Hillside+Ave', 'Metuchen%2C+NJ')
    print test_zpid

if __name__ == '__main__':
    main()

