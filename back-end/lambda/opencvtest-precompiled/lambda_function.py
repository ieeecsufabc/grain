import json
import cv2
import time
from segmentation import processing_memory_fix

# Reference: https://www.youtube.com/watch?v=uFsaiEhr1zs
# https://github.com/ryfeus/lambda-packs/tree/master/Opencv_pil/source36


print('loading function')

def lambda_handler(event, context):
    print(event)
    #1. parse out query string params
    startTime = time.time()
    try:
        id = event['queryStringParameters']['id']
        scale = event['queryStringParameters']['scale']
        blob = event['queryStringParameters']['blob']
    except:
        id = 0
        scale = 0
        blob = 'empty'

    print('id=', id)
    print('scale=', scale)
    #print('blob=', blob)

    result = 0
    if blob.lower() == "test":
        img = cv2.imread("Aco224.jpg")
        parameters = [1, 191, 3, 5, 0, 2, 0, 41] # Simulated Annealing
        #parametros = [1, 99, 5, 3, 1, 5, 0, 31] # Genetic Algorithms
        _, result = processing_memory_fix(img, parameters)
    totalTime = time.time() - startTime
    
    #2. construct response
    transactionResponse = {}
    transactionResponse['id'] = id
    transactionResponse['scale'] = scale
    transactionResponse['blob'] = blob
    transactionResponse['message'] = 'Hello world from lambda.'
    transactionResponse['count'] = result
    transactionResponse['time'] = float('{:0.2f}'.format(totalTime) )

    #3. construct the http response object
    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-scale'] = 'application/json'
    responseObject['body'] = json.dumps(transactionResponse)

    return responseObject

# https://tevqwyqov0.execute-api.sa-east-1.amazonaws.com/test/transactions?id=1&scale=100&blob=test

# Local testing
if __name__ == "__main__":
    startTime = time.time()
    img = cv2.imread("./Aco224.jpg")
    parameters = [1, 191, 3, 5, 0, 2, 0, 41] # Simulated Annealing
    #parametros = [1, 99, 5, 3, 1, 5, 0, 31] # Genetic Algorithms
    _, result = processing_memory_fix(img, parameters)

    totalTime = time.time() - startTime
    transactionResponse = {}
    transactionResponse['count'] = result
    transactionResponse['time'] = float('{:0.2f}'.format(totalTime) )
    print(transactionResponse)
