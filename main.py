from pytreemap import TreeMap
from lxml import etree
import argparse
from itertools import zip_longest
from datetime import datetime

class MyTreeMap(TreeMap):
    
    def __init__(self, comparator=None):
        super().__init__(comparator)

class OrderParser:
    
    def __init__(self) -> None:
        pass
    
    def parseAddOrder(self, element):
        price = float(element.get('price'))
        bookId  = element.get('book')
        operation = element.get('operation')
        volume = float(element.get('volume'))
        orderId = int(element.get('orderId'))
        return bookId, operation, price, volume, orderId
    
    def parseDelOrder(self, element):
        bookId = element.get('book')
        orderId = int(element.get('orderId'))
        return bookId, orderId
    
class OrderBook:
    
    def __init__(self, bookId) -> None:
        self.bookId = bookId
        self.buyOrders = MyTreeMap()
        self.sellOrders = MyTreeMap()

    def match(self, operation, price, orderId):
        if operation == "BUY":
            # find matches in self.sellOrders
            return self.sellOrders.get_floor_entry((price, orderId))
        else:
            # find matches in self.buyOrders
            # return largest key greater than (price, orderId)
            for buyEntry in self.buyOrders.descending_key_set():
                buyPrice, buyOrderId = buyEntry
                if buyPrice >= price:
                    buyVolume = self.buyOrders[(buyPrice, buyOrderId)]
                    return (buyPrice, buyOrderId, buyVolume)
            return None

    def addBuyOrder(self, price, orderId, volume):
        if not self.buyOrders and not self.sellOrders:
            self.buyOrders[(price, orderId)] = volume
            return
        
        while (match := self.match("BUY", price, orderId)) and volume != 0:
            sellPrice, sellOrderId = match.get_key()
            sellVolume = match.get_value()

            if sellVolume <= volume:
                volume -= sellVolume
                self.sellOrders.remove((sellPrice, sellOrderId))
            else:
                sellVolume -= volume
                volume = 0
                self.sellOrders.put((sellPrice, sellOrderId), sellVolume)
        
        if volume != 0:
            self.buyOrders.put((price, orderId), volume)
        
    def addSellOrder(self, price, orderId, volume):
        if not self.sellOrders and not self.buyOrders:
            self.sellOrders[(price, orderId)] = volume
            return

        while (match := self.match("SELL", price, orderId)) and volume != 0:            
            buyPrice, buyOrderId, buyVolume = match            

            if buyVolume <= volume:
                volume -= buyVolume
                self.buyOrders.remove((buyPrice, buyOrderId))
            else:
                buyVolume -= volume
                volume = 0
                self.buyOrders.put((buyPrice, buyOrderId), buyVolume)

        if volume != 0:
            self.sellOrders.put((price, orderId), volume)
    
    def get_entry_on_orderId(self, orderId, which="1"):
        match = None
        if which == "1":
            for entry in self.buyOrders.entry_set():
                entryPrice, entryOrderId = entry.get_key()
                if entryOrderId == orderId:
                    match = (entryPrice, entryOrderId)
                    break
        else:
            for entry in self.sellOrders.entry_set():
                entryPrice, entryOrderId = entry.get_key()
                if entryOrderId == orderId:
                    match = (entryPrice, entryOrderId)
                    break
        return match

    def delOrder(self, orderId):        
        match1 = self.get_entry_on_orderId(orderId)
        match2 = self.get_entry_on_orderId(orderId, "2")

        if match1:
            self.buyOrders.remove(match1)
        if match2:
            self.sellOrders.remove(match2)

    def printBook(self):
        print(f"book: {self.bookId}")
        print(" "*12 + "Buy -- Sell" + " "*12)
        print("="*35)
            
        for buyEntry, sellEntry in zip_longest(self.buyOrders.descending_key_set(), self.sellOrders.descending_key_set(), fillvalue=None):
            line = ""

            if buyEntry:
                buyPrice, buyOrderId = buyEntry                
                buyVolume = self.buyOrders[(buyPrice, buyOrderId)]
                line = str(buyVolume) + "@" + str(buyPrice)
            
            line = line + " -- "

            if sellEntry:
                sellPrice, sellOrderId = sellEntry                
                sellVolume = self.sellOrders[(sellPrice, sellOrderId)]
                line += str(sellVolume) + "@" + str(sellPrice)            
            print(line)
        
if __name__ == '__main__':    
    argParser = argparse.ArgumentParser()
    argParser.add_argument("file", help="the input xml file")
    args = argParser.parse_args()

    xml_file_path = args.file
    context = etree.iterparse(xml_file_path, events=("start", "end"))

    XMLparser = OrderParser()
    bookMap = {}
    
    for event, element in context:
        if event == "start":
            if element.tag == "Orders":
                continue            
            
            if element.tag == "AddOrder":
                bookId, operation, price, volume, orderId = XMLparser.parseAddOrder(element)
                if bookId not in bookMap:
                    bookMap[bookId] = OrderBook(bookId)

                if operation == "BUY":                
                    bookMap[bookId].addBuyOrder(price, orderId, volume)
                else:
                    bookMap[bookId].addSellOrder(price, orderId, volume)

            else:
                bookId, orderId = XMLparser.parseDelOrder(element)
                if bookId not in bookMap:
                    continue
                
                bookMap[bookId].delOrder(orderId)
            # print(f"processed cnt = {cnt}")
        if event == "end":
            # Clear the element from memory to save memory
            element.clear()

    # Release resources
    del context

    # print output
    current_datetime = datetime.now()
    start_formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    print(f"Processing started at: {start_formatted_datetime}")
    for _, book in bookMap.items():
        book.printBook()
        print()
    end_datetime = datetime.now()
    end_formatted_datetime = end_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    print(f"Processing completed at: {end_formatted_datetime}")
    print(f"Processing Duration: {end_datetime - current_datetime} seconds")