import os
import web3
import json
provider = ""
Web3 = web3.Web3(web3.Web3.HTTPProvider(provider))
CONNECTION = Web3.isConnected()

def getBalance(account):
  bal = Web3.eth.get_balance(account)
  return Web3.fromWei(bal,'ether')
  
def checkTransaction(txHex):
  tx = Web3.eth.getTransaction(txHex)
  return tx

def connectWallet(address,id):
  id = str(id)
  f = open("./utils/db/details.json","r")
  data = json.load(f)
  if id not in data.keys(): 
    data[id] = (address)
    f1 = open("./utils/db/details.json","w")
    json.dump(data,f1)
    f1.close()
  f.close()
  return data[id]

def getwallet(id):
  id = str(id)
  f = open("./utils/db/details.json","r")
  data = json.load(f)
  f.close()
  if id not in data.keys():
    return None
  return data[id]


def sendTransaction(sender, receiver,amt):
  address1 = Web3.toChecksumAddress(sender)
  address2 = Web3.toChecksumAddress(receiver)
  no = Web3.eth.getTransactionCount(address1)
  tx = {
    'nonce':no, 
    'to':address2, 
    'from': address1,
    'value':Web3.toWei(amt,'ether'), 
    'gas':6721975,
    'gasPrice': Web3.toWei(amt,'gwei')
  }
  transact = Web3.eth.sendTransaction(tx)
  return transact.hex()
