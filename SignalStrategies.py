#### Implements the signal strategies.


import collections
import Indicators
import DownloadQuotes


class SimpleSignal:
    
    def signal(self, quotes: 'list of closing prices', indicator: 'list of indicators'):
        '''
        Generates buy signals and sell signals
        '''
        signal_strategies = []
        days = indicator.count('-') + 1  ## days + 1 = the number of days being averaged

        for i in range(0, days):
            signal_strategies.append('-')
            
        for i in range(days, len(indicator)):

            if (quotes[i] > indicator[i]) and (quotes[i-1] < indicator[i-1]):
                signal_strategies.append('BUY')
            elif (quotes[i] < indicator[i]) and (quotes[i-1] > indicator[i-1]):
                signal_strategies.append('SELL')
            else:
                signal_strategies.append('-')

        return signal_strategies



class DirectionalSignal:

    def signal(self, quotes: 'list of closing prices', indicator: 'list of indicators'):
        '''
        Generates buy signals and sell signals
        '''
        buy_threshold = int(input('Enter a buy threshold: '))
        sell_threshold = int(input('Enter a sell threshold: '))
        
        signal_strategies = []

        for i in range(len(indicator)):
            if (indicator[i] > indicator[i-1]) and (indicator[i] > buy_threshold):
                signal_strategies.append('BUY')
            elif (indicator[i] < indicator[i-1]) and (indicator[i] < sell_threshold):
                signal_strategies.append('SELL')
            else:
                signal_strategies.append('-')

        return signal_strategies



def indicator_to_signal(c: 'Indicator class') -> 'signal strategy':
    '''
    Creates a relationship between the indicator specified and the
    signal strategy to be used to generate buy and sell signals
    '''
    signal_strategy = None
    
    if type(c) == Indicators.SimpleMovingAverage:
        signal_strategy = SimpleSignal()
    elif type(c) == Indicators.Directional:
        signal_strategy = DirectionalSignal()
    else:
        print('***** Invalid Indicator *****')

    return signal_strategy


def run_signal_strategy(c: 'Indicator class', quotes: 'list of closing prices'):
    '''
    Returns indicators using the method specified, as well as the
    buy and sell signals
    '''
    cond = True
    while cond:
        
        days = input('\nHow many days would you like to calculate an average for? ')

        try:
            days = int(days)
            indicator = c.calculate(quotes, days)
            signal = indicator_to_signal(c).signal(quotes, indicator)
            return indicator, signal, days

        except:
            print('***** Invalid Number of Days *****')


