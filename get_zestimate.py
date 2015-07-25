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



def get_zpid(params_dict):
    '''
    :param: params_dict: dictionary with parameters for the GetSearchResults API call (zws-id, address, citystatezip)
    zwsid: Zillow web service id
    address: street address (e.g. '2114 Bigelow Ave')
    citystatezip: 'Seattle WA' AND/OR zip code
    :return: zpid for the property address
    '''
    #sample call = 'http://www.zillow.com/webservice/GetSearchResults.htm?zws-id=<ZWSID>&address=2114+Bigelow+Ave&citystatezip=Seattle%2C+WA'

    url = 'http://www.zillow.com/webservice/GetSearchResults.htm'
    data = requests.get(url, params=params_dict)
    #print data.url
    root = ET.fromstring(data.text)
    for zpid_el in root.iter('zpid'):
        return zpid_el.text


def get_zestimate(params_dict):
    '''
    :param: params_dict: dictionary with parameters for GetZestimate API call (zws-id, zpid)
    zws-id: Zillow web service id
    zpid: Zillow property id for an address
    :return: dictionary containing price formatted as currency and as an ordinary string (e.g., '123456')
    '''
    price_dict = {}
    url = 'http://www.zillow.com/webservice/GetZestimate.htm'
    data = requests.get(url, params=params_dict)
    root = ET.fromstring(data.text)
    locale.setlocale(locale.LC_ALL, 'en_US')
    for amount_el in root.iter('amount'):
        price_dict['zestimate'] = amount_el.text
        price_dict['zestimate_currency'] = locale.currency(int(amount_el.text), grouping=True)
        return price_dict

def get_monthly_mortgage_pmt(params_dict):
    '''
    :param: params_dict: dictionary containing parameters for GetMonthlyPayments API call url
    zws-id: Zillow web service id
    price: property price
    down: down payment percentage - if omitted, 20% assumed
    dollarsdown: dollar amount that will be used as down payment (use in place of down)
    zip: zip code in which property located - if used, estimated monthly insurance/tax data will be returned
    :return: dictionary containing: estimated monthly mortgage pmt for that property, and optionally:
            estimated monthly insurance/tax payments
    '''
    #sample call: http://www.zillow.com/webservice/GetMonthlyPayments.htm?zws-id=<ZWSID>&price=300000&down=15&zip=98104
    #data_dict_to_return = {} for now, returning json object and not using this
    url = 'http://www.zillow.com/webservice/GetMonthlyPayments.htm'
    data = requests.get(url, params=params_dict)
    data = json.loads(data.text)
    #print json.dumps(data, sort_keys=True, indent=4)
    return data



def main():
    zwsid = 'X1-ZWz1a6057c0y6j_2rqd6' # since this isn't going to change, would this be an instance when a global variable would be ok?
    url_params_dict = {'zws-id': zwsid, 'address': '93 Hillside Ave', 'citystatezip': 'Metuchen NJ 08840'}
    test_zpid = get_zpid(url_params_dict)
    url_params_dict['zpid'] = test_zpid
    test_zestimate_dict = get_zestimate(url_params_dict)
    print 'Zestimate:', test_zestimate_dict['zestimate_currency']
    url_params_dict['price'] = test_zestimate_dict['zestimate']
    url_params_dict['zip'] = '08840'
    url_params_dict['down']= '20'
    monthly_housing_exp_data = get_monthly_mortgage_pmt(url_params_dict)
    monthly_pmt_fifteen_fixed = monthly_housing_exp_data['response']['fifteenYearFixed']['monthlyPrincipalAndInterest']
    monthly_pmt_thirty_fixed = monthly_housing_exp_data['response']['thirtyYearFixed']['monthlyPrincipalAndInterest']
    down_pmt_fifteen_fixed = monthly_housing_exp_data['response']['downPayment']
    monthly_pmt_five_one_arm = monthly_housing_exp_data['response']['fiveOneARM']['monthlyPrincipalAndInterest']
    #print 'Down payment amount (15-year fixed):', down_pmt_fifteen_fixed
    #print 'Estimated mortgage payment (15-year fixed):', monthly_pmt_fifteen_fixed
    #print 'Estimated mortgage payment (30-year fixed):', monthly_pmt_thirty_fixed
    #print 'Estimated mortgage payment (five-one ARM):', monthly_pmt_five_one_arm



if __name__ == '__main__':
    main()

