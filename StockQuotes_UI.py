## Implements the user interface of the Stock Quotes Program

import Indicators
import SignalStrategies
import DownloadQuotes


def run_user_interface(): # nothing -> interaction
    '''
    Handles the interaction between the user and the program
    '''
    print('Welcome to the Stock Quotes Program!\n')

    cond = True
    while cond:
        symbol = input('Enter a ticker symbol: ')
        print('In the format YYYY-MM-DD,')
        start_date = input('   Enter a start date: ')
        end_date = input('   Enter an end date: ')

        if DownloadQuotes.format_date(start_date) < DownloadQuotes.format_date(end_date):
            try:
                info = ask_for_quote_info(symbol.upper(), start_date, end_date)
                final_report = generate_final_report(symbol.upper(), info)
                cond = False
            except:
                print('***** Invalid ticker symbol, start date, or end date *****')
        else:
            print('***** Invalid dates. Make sure the start date is earlier than the end date *****')
            

    print('\nThank you. Good-bye!')
        


def ask_for_quote_info(symbol, start_date, end_date):
    '''
    Prints out a detailed report of the specified symbol. Returns a list of
    closing prices and a list of dates
    '''
    quotes = DownloadQuotes.get_quotes(symbol, start_date, end_date)
    report = quote_format(quotes, symbol, start_date, end_date)
    closing_prices = DownloadQuotes.closing_prices(quotes)
    dates = DownloadQuotes.dates(quotes)
    return closing_prices, dates



def quote_format(quotes: 'response from get_quotes', symbol, start, end):
    '''
    Formats the response (quotes) received from the Yahoo Finance page
    ''' 
    print('\n----- Here is a detailed report for {} between {} and {} -----\n'.format(
        symbol, start, end))

    format_str = '{:12} {:8} {:8} {:8} {:8} {:10} {:8}'
    print('Date         Open     High     Low      Close    Volume     Adj Close')
    for date in quotes[2:]:
        format_date_info = date.split(',')
        print(format_str.format(format_date_info[0], format_date_info[1], format_date_info[2],
                                format_date_info[3], format_date_info[4], format_date_info[5],
                                format_date_info[6]))

    print('\n----------------------------------------------------------------------------')



MENU = """
Which signal strategy would you like to use to generate buy and sell signals?
   s: Simple moving average
   d: Directional indicator
"""



def generate_final_report (symbol, info: 'ask_for_quote_info') -> 'final report':
    '''
    Formats the final analysis report
    '''
    closing_prices = info[0]
    dates = info[1]

    format_str = '{:<14} {:<10} {:<10} {:<10}'

    response = input(MENU)
    if response.strip() == 's':
        result = SignalStrategies.run_signal_strategy(Indicators.SimpleMovingAverage(), info[0])
        indicator = result[0]
        signal = result [1]
        days = result[2]

        print('\n--------------------- Here is the final analysis report ---------------------\n')
        print('SYMBOL: {} \nSTRATEGY: Simple moving average ({}-day)\n'.format(symbol, days))
        print('DATE           CLOSE      INDICATOR  SIGNAL')
        for i in range(len(indicator)):
            print(format_str.format(dates[i], closing_prices[i], indicator[i], signal[i]))

    elif response.strip() == 'd':
        buy_threshold = input('Enter a buy threshold: ')
        sell_threshold = input('Enter a sell threshold: ')

        result = SignalStrategies.run_signal_strategy(Indicators.Directional(), info[0])
        indicator = []
        signal = []
        days = result[2]

        for i in result[0]:
            if i > 0:
                indicator.append('+{}'.format(i))
            else:
                indicator.append(i)

        for i in range(len(result[1])):
            if result[1][i] == result[1][i-1]:
                result[1][i] = '-'
                signal.append(result[1][i])
            else:
                signal.append(result[1][i])
                
        print('\n--------------------- Here is the final analysis report ---------------------\n')
        print('SYMBOL: {}\nSTRATEGY: Directional ({}-day), buy above +{}, sell below {}\n'.format(
            symbol, days, buy_threshold, sell_threshold))
        print('DATE           CLOSE      INDICATOR  SIGNAL')
        for i in range(len(indicator)):
            print(format_str.format(dates[i], closing_prices[i], indicator[i], signal[i]))
        



if __name__ == '__main__':
    run_user_interface()
