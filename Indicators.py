#### Implements the two indicators (Simple Moving Average and Directional)



class SimpleMovingAverage:

    def calculate(self, quotes: 'list of closing prices', days: int) -> float:
        '''
        Takes a list of closing prices and calculates the simple moving average
        '''
        indicators = []

        for position in range(len(quotes)):
            if (position + 1) < days:
                indicators.append('-')

            else:
                calc = sum(quotes[(position+1)-days: position+1])
                average = '{:.2f}'.format(calc/days)
                average = float(average)
                indicators.append(average)

        return indicators


class Directional:
    
    def calculate(self, quotes: 'list of closing prices', days: int) -> int:
        '''
        Takes a list of closing prices and calculates the directional indicator
        '''
        indicators = []

        for position in range(len(quotes)):
            count = 0
            previous = 0
            
            if position < days:
                new_list = quotes[:position+1]
                
                for i in new_list:
                    previous = new_list.index(i)-1
                    if (i != new_list[0]) and (i > new_list[previous]):
                        count += 1
                    elif (i != new_list[0]) and (i < new_list[previous]):
                        count -= 1

            else: ## position >= days
                new_list = quotes[position-days:position+1]

                for i in new_list:
                    previous = new_list.index(i)-1
                    if (i != new_list[0]) and (i > new_list[previous]):
                        count += 1
                    elif (i != new_list[0]) and (i < new_list[previous]):
                        count -= 1

            indicators.append(count)
                
        return indicators
                    

def run_indicator (c: 'class', quotes: 'list of closing prices'):
    '''
    Returns a list of indicators
    '''
    cond = True
    while cond:

        days = input('How many days would you like to calculate an average for? ')

        try:
            days = int(days)   
            return c.calculate(quotes, days)

        except:
            print('***** Invalid Number of Days *****')

            

