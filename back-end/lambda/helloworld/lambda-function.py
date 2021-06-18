import json

print('loading function')

def lambda_handler(event, context):
    #1. parse out query string params
    transactionId = event['queryStringParameters']['transactionId']
    transactioType = event['queryStringParameters']['type']
    transactionAmount = event['queryStringParameters']['amount']

    print('id=', transactionId)
    print('type=', transactioType)
    print('ammount=', transactionAmount)
    
    #2. construct response
    transactionResponse = {}
    transactionResponse['transactionId'] = transactionId
    transactionResponse['type'] = transactioType
    transactionResponse['amount'] = transactionAmount
    transactionResponse['message'] = 'Hello world from lambda.'

    #3. construct the http response object
    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps(transactionResponse)

    return responseObject


#https://tevqwyqov0.execute-api.sa-east-1.amazonaws.com/test/transactions?transactionId=5&type=purchase&amount=500