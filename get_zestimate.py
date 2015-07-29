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
    :param: params_dict: dictionary with parameters for the GetSearchResults API call (zws-id, address, citystatezip)
    zwsid: Zillow web service id
    address: street address (e.g. '2114 Bigelow Ave')
    citystatezip: 'Seattle WA' AND/OR zip code
    :return: zpid for the property address
    '''
    #sample call = 'http://www.zillow.com/webservice/GetSearchResults.htm?zws-id=<ZWSID>&address=2114+Bigelow+Ave&citystatezip=Seattle%2C+WA'
    params_dict = {'zws-id': zwsid, 'address': address, 'citystatezip': citystatezip}
    url = 'http://www.zillow.com/webservice/GetSearchResults.htm'
    data = requests.get(url, params=params_dict)
    root = ET.fromstring(data.text)
    for zpid_el in root.iter('zpid'):
        return zpid_el.text


def get_zestimate(zwsid, zpid):
    '''
    :param: params_dict: dictionary with parameters for GetZestimate API call (zws-id, zpid)
    zws-id: Zillow web service id
    zpid: Zillow property id for an address
    :return: dictionary containing price formatted as currency and as an ordinary string (e.g., '123456')
    '''
    price_dict = {}
    params_dict = {'zws-id': zwsid, 'zpid': zpid}
    url = 'http://www.zillow.com/webservice/GetZestimate.htm'
    data = requests.get(url, params=params_dict)
    root = ET.fromstring(data.text)
    locale.setlocale(locale.LC_ALL, 'en_US')
    for amount_el in root.iter('amount'):
        price_dict['zestimate'] = amount_el.text
        price_dict['zestimate_currency'] = format_as_currency(amount_el.text)
        return price_dict

def get_monthly_mortgage_pmt(zwsid, price, down=20, dollarsdown=None, zip=None):
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
    params_dict = {'zws-id': zwsid, 'price': price, 'zip': zip, 'output': 'json'}
    if dollarsdown != None:
        params_dict['dollarsdown'] = dollarsdown
    else:
        params_dict['down'] = down
    url = 'http://www.zillow.com/webservice/GetMonthlyPayments.htm'
    data = requests.get(url, params=params_dict)
    data = json.loads(data.text)
    return data

def format_as_currency(num_as_text):
    return locale.currency(int(num_as_text), grouping=True)

def main():
    zwsid = 'X1-ZWz1a6057c0y6j_2rqd6'
    test_zpid = get_zpid(zwsid, '93 Hillside Ave', 'Metuchen NJ')
    test_zestimate_dict = get_zestimate(zwsid, test_zpid)
    print 'Zestimate:', test_zestimate_dict['zestimate_currency']
    # QUESTION: should I write little helper functions to handle the following?
    monthly_housing_exp_data = get_monthly_mortgage_pmt(zwsid, test_zestimate_dict['zestimate'], down=20, zip='08840')
    monthly_pmt_fifteen_fixed = monthly_housing_exp_data['response']['fifteenYearFixed']['monthlyPrincipalAndInterest']
    monthly_pmt_thirty_fixed = monthly_housing_exp_data['response']['thirtyYearFixed']['monthlyPrincipalAndInterest']
    down_pmt_fifteen_fixed = monthly_housing_exp_data['response']['downPayment']
    monthly_pmt_five_one_arm = monthly_housing_exp_data['response']['fiveOneARM']['monthlyPrincipalAndInterest']
    print 'Down payment amount (15-year fixed):', format_as_currency(down_pmt_fifteen_fixed)
    print 'Estimated mortgage payment (15-year fixed):', format_as_currency(monthly_pmt_fifteen_fixed)
    print 'Estimated mortgage payment (30-year fixed):', format_as_currency(monthly_pmt_thirty_fixed)
    print 'Estimated mortgage payment (five-one ARM):', format_as_currency(monthly_pmt_five_one_arm)
    if monthly_housing_exp_data['response']['monthlyHazardInsurance'] != None:
        monthly_hazard_ins_pmt = monthly_housing_exp_data['response']['monthlyHazardInsurance']
        print 'Estimated monthly hazard insurance premium:', format_as_currency(monthly_hazard_ins_pmt)
    if monthly_housing_exp_data['response']['monthlyPropertyTaxes'] != None:
        monthly_property_tax_pmt = monthly_housing_exp_data['response']['monthlyPropertyTaxes']
        print 'Estimated property taxes:', format_as_currency(monthly_property_tax_pmt)







if __name__ == '__main__':
    main()

