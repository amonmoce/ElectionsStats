# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################
import requests
from lxml import html
import unicodedata

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    # response.flash = T("Hello World")
    return dict(message=T('Welcome to Elections Stats!'))


def getCodesAndCountries():
    return {
        '223': 'Turkey',
        '226': 'Taiwan'
    }



def encode_data(numbers):
    encode_numbers = []
    for array in numbers:
        new_array = []
        for element in array:
            new_array.append(element.encode('ascii','ignore'))
        encode_numbers.append(new_array)
    print encode_numbers
    return encode_numbers


def scrapeData(countryValue, whichData):
    countryValue = '226'
    url = 'http://www.idea.int/vt/countryview.cfm?id='+countryValue
    page = requests.get(url)
    tree = html.fromstring(page.content)
    data = tree.xpath('//table[@id="viewData"]')
    data_years = data[1].xpath('//td/text()')
    data_years = data_years[21:]
    data_years = data_years[:-6]
    data = data[1].xpath('//td/div/text()')
    data = data[7:]
    data = data[:-3]
    year_index = 0
    presidentials = {}
    parliamentaries = {}
    numbers = []
    line = []
    parliamentary_years_size = 0
    for i in range(0, len(data_years)):
        if data_years[i] < data_years[i+1]:
            break
        parliamentary_years_size = parliamentary_years_size + 1
    for i, em in enumerate(data):
        if em == 'No' or em == 'Yes':
            numbers.append(line)
            year_index =+1
            line = []
        else:
             line.append(data[i])
    data = {}
    numbers = encode_data(numbers)
    for i in range(0, len(data_years)):
        if i <= parliamentary_years_size:
            parliamentaries[data_years[i]] = numbers[i]
        else:
            presidentials[data_years[i]] = numbers[i]
    #0,VT 1,TV 2,R 4,VAP 5,P 6,IV
    if whichData == 'VT':
        return presidentials, parliamentaries, 0
    if whichData == 'TV':
        return presidentials, parliamentaries, 1
    if whichData == 'R':
        return presidentials, parliamentaries, 2
    if whichData == 'VAP':
        return presidentials, parliamentaries, 4
    if whichData == 'P':
        return presidentials, parliamentaries, 5
    if whichData == 'IV':
        return presidentials, parliamentaries, 6


def getPresidentialsByCountry():
    countryValue = request.vars['country']
    whichData = request.vars['whichData']
    presidentials, parliamentaries, specificData = scrapeData(str(countryValue), str(whichData))
    response.headers['Content-Type'] = 'text/html'
    results = []
    for year in presidentials:
        results.append("Year:"+year +", Data:"+ presidentials[year][specificData])
    results.append("<a href='/ElectionsStats/default/index'>Go back</a>")
    return '<br>'.join(results)


def getPresidentialsByYear():
    year = request.vars['year']
    whichData = request.vars['whichData']
    results = []
    countries_and_codes = getCodesAndCountries()
    for code in countries_and_codes:
        presidentials, parliamentaries, specificData = scrapeData(str(code), str(whichData))
        results.append(countries_and_codes[code])
        if presidentials.has_key(year):
            results.append("Year:"+year +", Data:"+ presidentials[year][specificData])
        else:
            results.append("Year:"+year +", Data: No Elections or Not available")
    response.headers['Content-Type'] = 'text/html'
    results.append("<a href='/ElectionsStats/default/index'>Go back</a>")
    return '<br>'.join(results)


def getParliamentariesByCountry():
    countryValue = request.vars['country']
    whichData = request.vars['whichData']
    presidentials, parliamentaries, specificData = scrapeData(str(countryValue), str(whichData))
    response.headers['Content-Type'] = 'text/html'
    results = []
    for year in parliamentaries:
        results.append("Year: "+year +", Data: "+ parliamentaries[year][specificData])
    results.append("<a href='/ElectionsStats/default/index'>Go back</a>")
    return '<br>'.join(results)


def getParliamentariesByYear():
    year = request.vars['year']
    whichData = request.vars['whichData']
    results = []
    countries_and_codes = getCodesAndCountries()
    for code in countries_and_codes:
        presidentials, parliamentaries, specificData = scrapeData(str(code), str(whichData))
        results.append(countries_and_codes[code])
        if parliamentaries.has_key(year):
            results.append("Year:"+year +", Data: "+ parliamentaries[year][specificData])
        else:
            results.append("Year:"+year +", Data: No Elections or Not available")
    response.headers['Content-Type'] = 'text/html'
    results.append("<a href='/ElectionsStats/default/index'>Go back</a>")
    return '<br>'.join(results)
