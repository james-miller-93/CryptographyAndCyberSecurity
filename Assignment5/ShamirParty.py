import random

#create class for each party in Shamir Secret Sharing scheme
class Party:

    
    
    def __init__(self, index):
        #each party has unique index
        self.index = index

        #set Shamir parameters, default is 1 out of 4
        self.t = 1
        self.n = 4
        self.q = 65701
        self.shares = [0]*self.n
        self.reshares = []

        #connect to server at given port number

    def Share(self, message, parties):
        #create t out of n secret shares for given message
        #distribute each share to each party in parties

        #create polynomial
        if (self.t <= 1):
            polycoeffs = [0]
        else:
            polycoeffs = [0]*(self.t-1)

        #embed message into 0 value
        polycoeffs[0] = message

        #generate remaining coeff
        if (self.t != 1):
            for i in range(self.t-1):
                polycoeffs.append(random.randint(0,self.q))

        i = 1
        for party in parties:
            party.ReceiveSecretShare(EvalPoly(polycoeffs,i))
            i += 1
        

    def ReceiveSecretShare(self, message):
        #receive original secret share given from other party
        #store in order to reconstruct later
        self.secretshare = message

    def ReceiveShare(self, message,index):
        #receive share in order to reconstruct
        self.shares[index-1] = message


    def ReceiveReShare(self, message):
        #receive and store reshared share
        #will be used for Reconst2
        self.reshares.append(message)
    
    def SendShare(self, parties):
        for party in parties:
            party.ReceiveShare(self.secretshare,self.index)

    def Reconstruct(self):
        message = InterpolatePoly(self.shares,0)
        print(message)

    
    #def ReShare(newParty, newPartyIndex):
        #reshare your share to create a new share for a new party

    #def Reconst2(parties):
        #send share to each party in parties
        #receive other shares
        #use these shares and reshared shares to reconstruct message


def EvalPoly(coefficients, input):
    output = 0
    i = 0
    for coeff in coefficients:
        output += (coeff)*(input**i)
        i += 1
    
    return output

def InterpolatePoly(shares, input):
    k = len(shares)
    output = 0
    i = 0
    for share in shares:
        numerator = 1
        denominator = 1
        for j in range(k):
            if (i != j):
                numerator = numerator * (input - j)
                denominator = denominator * (i - j)
        output += share*numerator/denominator
    return output

        