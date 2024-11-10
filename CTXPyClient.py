import jpype as jp
from jpype import JClass, JArray, JString
import numpy as np
import glob
import random
from time import sleep

class CTXPyClient:

    def __init__(self, jar_dir) -> None:

        self.SeqNum = 1
        self.TickSize = 1
        self.xMinMarketOrder = 20
        self.xMinLimitOrder = 50
        self.alpha = 1

        self.MarketOrderStr = 'MarketOrder'
        self.LimitOrderStr = 'LimitOrder'
        self.CancelOrderStr = 'CancelOrder'

        self.sentOrders = []

        # Specify the directory containing JAR files

        # # Get a list of JAR files in the directory
        jar_directory = "/home/henrique/CoinTossX/ClientSimulator/build/install/ClientSimulator/lib/"
        jar_files = glob.glob(jar_directory + '*.jar')

        # # Start JVM with individual JAR file paths
        # jp.startJVM(jp.getDefaultJVMPath(), "-ea", classpath=jar_files)

        jp.startJVM(jp.getDefaultJVMPath(), "-ea", classpath = jar_files)
        # Import the class containing the reqired methods
        utilities = jp.JClass("example.Utilities")

        #----- Login and start session -----#
        clientId = 1
        securityId = 5
        self.client = utilities.loadClientData(clientId, securityId)
        self.client.sendStartMessage()

    def SendMarketBid(self):
        volume = self.SampleOrderVolume('MarketOrder')
        self.SendOrder(volume, 0, 'Buy', 'Market')

    def SendMarketAsk(self):
        volume = self.SampleOrderVolume('MarketOrder')
        self.SendOrder(volume, 0, 'Sell', 'Market')
    
    def SendAgressiveBid(self):
        v_Bid = self.client.getBidQuantity()

        if v_Bid > 0:
            price = self.client.getBid()
        else:
            v_Ask = self.client.getOfferQuantity()
            if v_Ask > 0:
                price = self.client.getOffer() - random.randint(1, 10) * self.TickSize
            else:
                price = 100

        volume = self.SampleOrderVolume('LimitOrder')

        self.SendOrder(volume, price, 'Buy', 'Limit')
        
    def SendPassiveBid(self):
        v_Bid = self.client.getBidQuantity()

        if v_Bid > 0:
            price = self.client.getBid() - self.TickSize
        else:
            v_Ask = self.client.getOfferQuantity()
            if v_Ask > 0:
                price = self.client.getOffer() - random.randint(1, 10) * self.TickSize
            else:
                price = 100

        volume = self.SampleOrderVolume('LimitOrder')

        self.SendOrder(volume, price, 'Buy', 'Limit')

    def SendAgressiveAsk(self):
        v_Ask = self.client.getOfferQuantity()

        if v_Ask > 0:
            price = self.client.getOffer()
        else:
            v_Bid = self.client.getBidQuantity()
            if v_Bid > 0:
                price = self.client.getBid() + random.randint(1, 10) * self.TickSize
            else:
                price = 99

        volume = self.SampleOrderVolume('LimitOrder')
        
        self.SendOrder(volume, price, 'Sell', 'Limit')

    def SendPassiveAsk(self):
        v_Ask = self.client.getOfferQuantity()

        if v_Ask > 0:
            price = self.client.getOffer() + self.TickSize
        else:
            v_Bid = self.client.getBidQuantity()
            if v_Bid > 0:
                price = self.client.getBid() + random.randint(1, 10) * self.TickSize
            else:
                price = 99

        volume = self.SampleOrderVolume('LimitOrder')
        
        self.SendOrder(volume, price, 'Sell', 'Limit')
    
    def SendAggressiveCancelationBid(self):
        v_Bid = self.client.getBidQuantity()   # Best bid volume

        if v_Bid == 0:
            return
    
        book = self.GetLOB()
        relevantOrders = []

        if book is None:
            return

        for st in book:
            if st is None:
                return
            if 'Buy' in st:
                relevantOrders.append(st)

        if len(relevantOrders) == 0:
            return
        
        for order in relevantOrders:
            sleep(0.2)
            #order = str(order)
            orderToCancel = order #.split(",")
            ord = orderToCancel[0]
            # intOrd = int(orderToCancel[3])
            intOrd = int(orderToCancel[2])
            self.client.cancelOrder(ord, "Buy", intOrd) # Cancel limit order
            self.sentOrders.remove([ord, "Buy", intOrd])
        #Find and cancel all orders on bid
    
    def SendAggressiveCancelationAsk(self):
        v_Ask = self.client.getOfferQuantity() # Best ask volume

        if v_Ask == 0:
            return
        
        book = self.GetLOB()
        relevantOrders = []

        if book is None:
            return

        for st in book:
            if st is None:
                return
            if 'Sell' in st:
                relevantOrders.append(st)

        if len(relevantOrders) == 0:
            return

        for order in relevantOrders:
            sleep(0.2)
            #order = str(order)
            orderToCancel = order #.split(",")
            ord = orderToCancel[0]
            # intOrd = int(orderToCancel[3])
            intOrd = int(orderToCancel[2])
            self.client.cancelOrder(ord, "Sell", intOrd) # Cancel limit order
            self.sentOrders.remove([ord, "Sell", intOrd])
        #Find and cancel all orders on bid
    
    def SendPassiveCancelationBid(self):
        v_Bid = self.client.getBidQuantity()   # Best bid volume

        if v_Bid == 0:
            return
    
        book = self.GetLOB()
        relevantOrders = []

        if book is None:
            return

        for st in book:
            if st is None:
                return
            if 'Buy' in st:
                relevantOrders.append(st)

        if len(relevantOrders) == 0:
            return
        
        orderToCancel = relevantOrders[random.randint(0, len(relevantOrders) - 1)]

        #orderToCancel = str(orderToCancel)
        #orderToCancel = orderToCancel.split(",")
        ord = orderToCancel[0]
        # intOrd = int(orderToCancel[3])
        intOrd = int(orderToCancel[2])

        self.client.cancelOrder(ord, "Buy", intOrd) # Cancel limit order
        self.sentOrders.remove([ord, "Buy", intOrd])

        #Find and cancel random order not on best bid
    
    def SendPassiveCancelationAsk(self):
        v_Ask = self.client.getOfferQuantity() # Best ask volume

        if v_Ask == 0:
            return
    
        book = self.GetLOB()
        relevantOrders = []

        if book is None:
            return

        for st in book:
            if st is None:
                return
            if 'Sell' in st:
                relevantOrders.append(st)

        if len(relevantOrders) == 0:
            return
        
        orderToCancel = relevantOrders[random.randint(0, len(relevantOrders) - 1)]
        
        #orderToCancel = str(orderToCancel)
        #orderToCancel = orderToCancel.split(",")
        ord = orderToCancel[0]
        # intOrd = int(orderToCancel[3])
        intOrd = int(orderToCancel[2])

        self.client.cancelOrder(ord, "Sell", intOrd) # Cancel limit order
        self.sentOrders.remove([ord, "Sell", intOrd])

        #Find and cancel random order not on best bid
       
    def SendOrder(self, volume: int, price: int, side: str, ordType: str) -> None:
        #self.client.submitOrder("1", 1000, 99, "Buy", "Limit", "Day", 1000, 0, 0) # Buy limit order

        if ordType == "Limit":
            self.sentOrders.append([str(self.SeqNum), side, price])

        self.client.submitOrder(str(self.SeqNum), volume, price, side, ordType, "Day", volume, 0, 0)
        self.SeqNum += 1

    def GetSpread(self) -> int:
        bid = self.client.getBid()   # Best bid price
        ask = self.client.getOffer() # Best ask price
        return (ask-bid)/self.TickSize
    
    def GetImbalance(self) -> float:
        v_Bid = self.client.getBidQuantity()   # Best bid volume
        v_Ask = self.client.getOfferQuantity() # Best ask volume

        if v_Bid + v_Ask == 0:
            return 0

        return ((v_Bid - v_Ask) / (v_Bid + v_Ask))/self.TickSize
    
    def Shutdown(self) -> None:
        self.client.sendEndMessage()
        self.client.close()
        jp.shutdownJVM()

    def SampleOrderVolume(self, type: str) -> int:

        random_number = np.random.power(self.alpha, 1)
        
        if type == self.MarketOrderStr:
            volume = self.xMinMarketOrder * (1.0 - random_number)**(-1.0 / self.alpha)
        elif type == self.LimitOrderStr:
            volume = self.xMinLimitOrder * (1.0 - random_number)**(-1.0 / self.alpha)

        return int(np.round(volume.item(), 0))
    
    def GetLOB(self) -> list:
        # lob = self.client.lobSnapshot() # Snapshot of the entire LOB
        # python_list_of_lists = [lob.get(i) for i in range(lob.size())]
        python_list_of_lists = self.sentOrders
        return python_list_of_lists
