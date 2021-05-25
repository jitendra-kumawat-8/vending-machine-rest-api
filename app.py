from flask import Flask, jsonify, request, make_response
app = Flask(__name__)
app.debug = True
class vendingMachine:
    data = {
        'coins' : {'1' : 10,
            '5' : 4,
            '10' : 25,
            '25' : 10},
    'productPrices' : {'coke' : 25,
               'pepsi' : 32,
               'soda' : 47},
    'quantityAvailable' : {'coke' : 15,
               'pepsi' : 15,
               'soda' : 15}
    }
    
    def __init__(self):
        self.coins = {'1' : 0,
            '5' : 0,
            '10' : 0,
            '25' : 0}
        self.request = ''
        self.cancel = False
        self.amount = 0
        self.change = 0
        self.refund = {'1' : 0,
            '5' : 0,
            '10' : 0,
            '25' : 0}
    def displayProducts(self):
        for i in range(0,len(self.data['productPrices'].keys())):
            name = list(self.data['productPrices'].keys())[i]
            price = list(self.data['productPrices'].values())[i]
            print(i+1,name,price)
    def placeRequest(self, title):
        self.request = title
        if(self.data['quantityAvailable'][self.request]==0):
            self.cancelRequest()
            return({'Error' : 'Product Unavailable'})
    def acceptAmount(self, amount):
        self.amount = amount
        print(amount)
        if(amount<self.data['productPrices'][self.request]):
            self.cancelRequest()
            return({'Error' : 'Insufficient Amount'})
        for i in self.data['coins'].keys():
            self.data['coins'][i] += self.coins[i]
        if(amount == self.data['productPrices'][self.request]):
            self.giveProduct(self.refund)
        elif(amount > self.data['productPrices'][self.request]):
            self.change = amount - self.data['productPrices'][self.request]
            coins25 = self.data['coins']['25']
            coins10 = self.data['coins']['10']
            coins5 = self.data['coins']['5']
            coins1 = self.data['coins']['1']
            while(coins25>0 and (self.change - 25) >=0):
                coins25 -= 1
                self.change-=25
            while(coins10>0 and (self.change - 10) >=0):
                coins10 -= 1
                self.change-=10
            while(coins5>0 and (self.change-5)>=0):
                coins5 -= 1
                self.change-=5
            while(coins1>0 and (self.change-1)>=0):
                coins1 -= 1
                self.change-=1
            if(self.change>0):
                self.cancelRequest()
                return({'Error' : 'Insufficient change, Please pay exact coins or try again with a different amount'})
            else:
                self.refund['1'] = self.data['coins']['1'] - coins1
                self.refund['5'] = self.data['coins']['5'] - coins5
                self.refund['10'] = self.data['coins']['10'] - coins10
                self.refund['25'] = self.data['coins']['25'] - coins25
                self.data['coins']['1'] = coins1
                self.data['coins']['5'] = coins5
                self.data['coins']['10'] = coins10
                self.data['coins']['25'] = coins25
                toReturn = self.giveProduct(self.refund)
                return(toReturn)
    def giveProduct(self, refund):
        toReturn = {}
        toReturn['drink'] = self.request
        if(sum(refund.values()) > 0):
            print('Here\'s Your refund')
            for i in refund.keys():
                if(refund[i]!=0):
                    if(i=='1'):
                        name = 'penny'
                        toReturn[name] = refund[i]
                    elif(i=='5'):
                        name = 'nickle'
                        toReturn[name] = refund[i]
                    elif(i=='10'):
                        name = 'dime'
                        toReturn[name] = refund[i]
                    elif(i=='25'):
                        name = 'quarter'
                        toReturn[name] = refund[i]
        return(toReturn)
    def cancelRequest(self):
        self.cancel = True
        self.coins = {'1' : 0,
            '5' : 0,
            '10' : 0,
            '25' : 0}
        self.request = ''
        self.amount = 0
        self.change = 0
        self.refund = {'1' : 0,
            '5' : 0,
            '10' : 0,
            '25' : 0}
    def process(self,nickle,penny,dime,quarter,title):
        if title not in ['pepsi','coke','soda']:
            self.cancelRequest()
            return({'Error' : 'Invalid choice'}) 
        if(self.cancel == False):
            self.placeRequest(title)
        if(self.cancel == False):
            self.coins['1'] = int(penny)
            self.coins['5'] = int(nickle)
            self.coins['10'] = int(dime)
            self.coins['25'] = int(quarter)
            amount = self.coins['1']*1 + self.coins['5']*5 + self.coins['10'] * 10 + self.coins['25'] * 25
            toReturn = self.acceptAmount(amount)
            return(toReturn)
    def reset(self):
        data = {
        'coins' : {'1' : 20,
            '5' : 20,
            '10' : 30,
            '25' : 20},
    'productPrices' : {'coke' : 25,
               'pepsi' : 32,
               'soda' : 47},
    'quantityAvailable' : {'coke' : 30,
               'pepsi' : 20,
               'soda' : 30}
    }
@app.route('/customer', methods=['GET','POST','PUT'])
def customer():
    obj = vendingMachine()
    title = request.args.get('drink')
    nickle = request.args.get('nickle')
    penny = request.args.get('penny')
    dime = request.args.get('dime')
    quarter = request.args.get('quartet')
    toReturn = obj.process(nickle,penny,dime,quarter,title)
    return make_response(toReturn, 200)
@app.route('/supplier',methods = ['PUT','GET'])
def supplier():
    obj = vendingMachine()
    obj.reset()
    return make_response({'message': 'reset successful'},200)
if __name__ == '__main__':
    app.run(port = 5000, debug=True)
