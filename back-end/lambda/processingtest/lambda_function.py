# Reference: https://www.youtube.com/watch?v=uFsaiEhr1zs
# https://github.com/ryfeus/lambda-packs/tree/master/Opencv_pil/source36

# Imports
if True:
    import base64
    import cv2
    from PIL import Image
    import io
    import numpy as np
    from urllib.parse import unquote
    import gc
    import json
    import time
    from segmentation import processing_memory_fix

print('loading function')

# Helper functions
def decodeImage(input_b64):
    input_b64 = unquote(input_b64)                        # replaces characters like '%xx'
    input_b64 = input_b64.split(",",1)[1]                 # removes base64 prefix from string
    input_dec = base64.urlsafe_b64decode(input_b64+"==="); del input_b64 # adds padding and decode
    input_img = np.frombuffer(input_dec, dtype=np.uint8); del input_dec  # transforms to numpy array
    input_img = cv2.imdecode(input_img, cv2.IMREAD_COLOR) # reads image from buffer
    return input_img

def encodeImage(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)            # converts cv2 (BGR) to PIL (RBG)
    img = Image.fromarray(img.astype("uint8"))            # prepares image to save in buffer
    raw_bytes = io.BytesIO()                              # creates image buffer
    img.save(raw_bytes, "JPEG"); del img                  # saves image to buffer
    raw_bytes.seek(0)                                     # sets stream position to 0
    img_b64 = base64.b64encode(raw_bytes.read()); del raw_bytes # encode bytes to b64 string
    return str(img_b64)

def lambda_handler(event, context):
    print(event)
    #1. parse out query string params
    startTime = time.time()
    try:
        id = event['queryStringParameters']['id']
        scale = event['queryStringParameters']['scale']
        inputImage = event['queryStringParameters']['inputImage']
        print("queryStringParameters")
    except:
        try:
            id = event['body']['id']
            scale = event['body']['scale']
            inputImage = event['body']['inputImage']
            print("post parameters")
        except:
            id = 0
            scale = 0
            inputImage = 'none'
            print("no parameters")

    print('id=', id)
    print('scale=', scale)
    print('inputImage=', inputImage[:10], "...")

    #2. processing

    # parameter list
    #parameters = [1, 191, 3, 5, 0, 2, 0, 41] # Simulated Annealing
    parametros = [1, 99, 5, 3, 1, 5, 0, 31] # Genetic Algorithms

    # conditions and error catching
    if inputImage[:4].lower() == 'none':
        print('error: no image sent')
        result = 0
        outputImage = ''
        message = 'error: no image sent'
    else:
        if inputImage[:4].lower() != 'test':
            try:
                print('decoding base64')
                # decoding base64
                input_img = decodeImage(inputImage); del inputImage
                message = 'success: user'
            except:
                print('error: decoding fail')
                message = 'error: decoding fail'
        else:
            try:
                print('opening default image')
                # opening default image
                input_img = cv2.imread("Aco224.jpg")
                message = 'success: default'
            except:
                print('error: default image reading fail')
                message = 'error: default image reading fail'
        
        try:
            # processing        
            out_img, result = processing_memory_fix(input_img, parameters); del input_img
            # encoding image to base64
            outputImage = encodeImage(out_img); del out_img
            message = message+'image processed'
        except:
            print('error: processing fail')
            message = ' error: processing fail'
            outputImage = ''

    totalTime = time.time() - startTime
    
    #3. construct response
    transactionResponse = {}
    transactionResponse['id'] = id
    transactionResponse['scale'] = scale
    transactionResponse['outputImage'] = outputImage
    transactionResponse['message'] = message
    transactionResponse['count'] = result
    transactionResponse['time'] = float('{:0.2f}'.format(totalTime) )

    #4. construct the http response object
    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-scale'] = 'application/json'
    responseObject['headers']['Access-Control-Allow-Origin'] = '*'
    responseObject['headers']['Access-Control-Allow-Credentials'] = 'true'
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
