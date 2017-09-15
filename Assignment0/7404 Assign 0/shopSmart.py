"""
Here's the intended output of this script, once you fill it in:

Welcome to shop1 fruit shop
Welcome to shop2 fruit shop
For orders:  [('apples', 1.0), ('oranges', 3.0)] best shop is shop1
For orders:  [('apples', 3.0)] best shop is shop2
"""

import shop

def shopSmart(orderList, fruitShops):
    """
        orderList: List of (fruit, numPound) tuples
        fruitShops: List of FruitShops
    """    
    "*** YOUR CODE HERE ***"
    totalPrices = []
    for fruitShop in fruitShops:
      totalPrice = fruitShop.getPriceOfOrder(orderList)
      totalPrices.append(totalPrice)
    return fruitShops[totalPrices.index(min(totalPrices))]
    
def shopArbitrage(orderList, fruitShops):
    """
    input: 
        orderList: List of (fruit, numPound) tuples
        fruitShops: List of FruitShops
    output:
        maximum profit in amount
    """
    "*** YOUR CODE HERE ***"
    profit = 0.0
    for fruit, numPound in  orderList:
      priceList = []
      for fruitShop in  fruitShops:
        price = fruitShop.getCostPerPound(fruit)
        priceList.append(price)
      profit += (max(priceList) - min(priceList)) * numPound
    print(profit)
    return profit


def shopMinimum(orderList, fruitShops):
    """
    input: 
        orderList: List of (fruit, numPound) tuples
        fruitShops: List of FruitShops
    output:
        Minimun cost of buying the fruits in orderList
    """
    "*** YOUR CODE HERE ***"
    cost = 0.0
    for fruit, numPound in  orderList:
      priceList = []
      for fruitShop in  fruitShops:
        price = fruitShop.getCostPerPound(fruit)
        priceList.append(price)
      cost += min(priceList) * numPound
    print(cost)
    return cost

if __name__ == '__main__':
  "This code runs when you invoke the script from the command line"
  orders = [('apples',1.0), ('oranges',3.0)]
  dir1 = {'apples': 2.0, 'oranges':1.0}
  shop1 =  shop.FruitShop('shop1',dir1)
  dir2 = {'apples': 1.0, 'oranges': 5.0}
  shop2 = shop.FruitShop('shop2',dir2)
  shops = [shop1, shop2]
  print("For orders ", orders, ", the best shop is", shopSmart(orders, shops).getName())
  orders = [('apples',3.0)]
  print("For orders: ", orders, ", the best shop is", shopSmart(orders, shops).getName())
