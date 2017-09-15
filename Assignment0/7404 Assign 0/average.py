
"""
Run python autograder.py 
"""

def average(priceList):
    "Return the average price of a set of fruit"
    "*** YOUR CODE HERE ***"
    newPriceList = list(set(priceList))
    return float(sum(newPriceList))/len(newPriceList)
