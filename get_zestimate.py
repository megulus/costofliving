__author__ = 'megdahlgren'

import requests
import xml.etree.ElementTree as ET
import locale
import json


'''
this command-line program does the following
1) given an address, returns the zpid
2) given a zpid, returns a zestimate

my zws_id: X1-ZWz1a6057c0y6j_2rqd6

'''



def get_zpid(zwsid, address, citystatezip):
    '''
    :param: zwsid: Zillow web service id
    :param: address: address (e.g. '2114+Bigelow+Ave')
    :param: citystatezip: city+state ('Seattle%2C+WA') AND/OR zip code
    :return: zpid for the property address
    '''
    #sample call = 'http://www.zillow.com/webservice/GetSearchResults.htm?zws-id=<ZWSID>&address=2114+Bigelow+Ave&citystatezip=Seattle%2C+WA'
    url = 'http://www.zillow.com/webservice/GetSearchResults.htm?zws-id={0}&address={1}&citystatezip={2}'.format(zwsid, address, citystatezip)
    data = requests.get(url).text
    root = ET.fromstring(data)
    for zpid_el in root.iter('zpid'):
        return zpid_el.text


def get_zestimate(zwsid, zpid):
    '''
    :param: zwsid: Zillow web service id
    :param zpid: Zillow property id for an address
    :return: zestimate for that property
    '''
    url = 'http://www.zillow.com/webservice/GetZestimate.htm?zws-id={0}&zpid={1}'.format(zwsid, zpid)
    data = requests.get(url).text
    root = ET.fromstring(data)
    locale.setlocale(locale.LC_ALL, 'en_US')
    for amount_el in root.iter('amount'):
        return locale.currency(int(amount_el.text), grouping=True)

def get_monthly_mortgage_pmt(zwsid, price, down=20, dollarsdown=None, zip=None):
    '''
    :param: zwsid: Zillow web service id
    :param: price: property price
    :param: down: down payment percentage - if omitted, 20% assumed
    :param: dollarsdown: dollar amount that will be used as down payment (use in place of down)
    :param: zip: zip code in which property located - if used, estimated monthly insurance/tax data will be returned
    :return: dictionary containing: estimated monthly mortgage pmt for that property, and optionally:
            estimated monthly insurance/tax payments
    '''
    #sample call: http://www.zillow.com/webservice/GetMonthlyPayments.htm?zws-id=<ZWSID>&price=300000&down=15&zip=98104
    data_dict_to_return = {}
    if zip != None:
        zip_string = '&zip={0}'.format(zip)
    else:
        zip_string = ''
    price_list = price.strip('$').strip('.00').split(',')
    price_str = price_list[0] + price_list[1]
    url = 'http://www.zillow.com/webservice/GetMonthlyPayments.htm?zws-id={0}&output=json&price={1}'.format(zwsid, price_str)
    if dollarsdown != None:
        url = url + '&dollarsdown={0}{1}'.format(dollarsdown, zip_string)
    else:
        url = url + '&down={0}{1}'.format(down, zip_string)
    data = requests.get(url).text
    data = json.loads(data)
    #print json.dumps(data, sort_keys=True, indent=4)
    return data



def main():
    zwsid = 'X1-ZWz1a6057c0y6j_2rqd6' # since this isn't going to change, would this be an instance when a global variable would be ok?
    test_zpid = get_zpid(zwsid, '93+Hillside+Ave', 'Metuchen%2C+NJ')
    test_zestimate = get_zestimate(zwsid, test_zpid)
    print 'Zestimate:', test_zestimate
    monthly_housing_exp_data = get_monthly_mortgage_pmt(zwsid, test_zestimate, zip='08840')
    monthly_pmt_fifteen_fixed = monthly_housing_exp_data['response']['fifteenYearFixed']['monthlyPrincipalAndInterest']
    monthly_pmt_thirty_fixed = monthly_housing_exp_data['response']['thirtyYearFixed']['monthlyPrincipalAndInterest']
    down_pmt_fifteen_fixed = monthly_housing_exp_data['response']['downPayment']
    monthly_pmt_five_one_arm = monthly_housing_exp_data['response']['fiveOneARM']['monthlyPrincipalAndInterest']

    print 'Down payment amount (15-year fixed):', down_pmt_fifteen_fixed
    print 'Estimated mortgage payment (15-year fixed):', monthly_pmt_fifteen_fixed
    print 'Estimated mortgage payment (30-year fixed):', monthly_pmt_thirty_fixed
    print 'Estimated mortgage payment (five-one ARM'):, monthly_pmt_five_one_arm



if __name__ == '__main__':
    main()

