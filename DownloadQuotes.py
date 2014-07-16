## Downloads quotes from Yahoo Finance


import datetime
import urllib.request



def get_quotes(symbol, start, end) -> 'response':
    '''
    Takes a ticker symbol, start date, and end date as inputs and downloads quotes
    '''
    ## year should be in the format YYYY-MM-DD
    start = format_date(start)
    end = format_date(end)
    
    url = 'http://ichart.yahoo.com/table.csv?s={}&a={}&b={}&c={}&d={}&e={}&f={}&g=d'.format(
        symbol, start.month-1, start.day, start.year, end.month-1, end.day, end.year)

    response = urllib.request.urlopen(url)

    print('\n----------------------------------------------------------------------------\n')
    print('The status code was {}.\n'.format(response.status))

    if response.status != 200:
        print('We didn\'t get the file we wanted.')
    else:
        print('Returned headers:')

    for response_header in response.getheaders():
        header_name, header_value = response_header

        print('  {} --- {}'.format(header_name, header_value))

    return data_split(response)



def data_split(response) -> 'list of date info':
    '''
    Adds the data (date, opening price, high, low, close, volume,
    and adjusted closing price) for each date to a list
    '''
    response_bytes = response.read()
    response_text = response_bytes.decode(encoding = 'utf-8')

    line = response_text.split()

    response.close()

    return line



def closing_prices(line: 'response from get_quotes') -> 'list of closing prices':
    '''
    Adds all of the adjusted closing prices to a list
    '''
    prices = []
    adj_close = []

    for date in line[2:]:
        ''' adds all the closing prices to a list '''
        format_date_info = date.split(',')
        prices.append(eval(format_date_info[6]))
    for price in reversed(prices):
        ''' orders the adjusted closing prices by date (oldest first) '''
        adj_close.append(price)    

    return adj_close



def dates(line: 'data_split') -> 'response from get_quotes':
    '''
    Adds all of the dates to a list
    '''
    dates = []
    ordered_dates = []
    
    for date in line[2:]:
        ''' adds all the dates to a list '''
        format_date_info = date.split(',')
        dates.append(format_date_info[0])
    for day in reversed(dates):
        ''' puts the list of dates in ascending order '''
        ordered_dates.append(day)    

    return ordered_dates



def format_date(date) -> datetime:
    '''
    Converts the date given in YYYY-MM--DD format to a datetime object
    '''
    date_objects = date.split('-')
    date_format = datetime.date(int(date_objects[0]), int(date_objects[1]), int(date_objects[2]))

    return date_format
