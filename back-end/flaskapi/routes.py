import flask
from flask import request, jsonify
from flaskapi import app
from flaskapi.segmentation import *

import base64
import cv2
from PIL import Image
import io
import numpy as np
from urllib.parse import unquote

# Helper functions
def decodeImage(input_b64):
    input_b64 = unquote(input_b64)                        # replaces characters like '%xx'
    input_b64 = input_b64.split(",",1)[1]                 # removes base64 prefix from string
    input_dec = base64.urlsafe_b64decode(input_b64+"===") # adds padding and decode
    input_img = np.frombuffer(input_dec, dtype=np.uint8)  # transforms to numpy array
    input_img = cv2.imdecode(input_img, cv2.IMREAD_COLOR) # reads image from buffer
    return input_img

def encodeImage(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)            # converts cv2 (BGR) to PIL (RBG)
    img = Image.fromarray(img.astype("uint8"))            # prepares image to save in buffer
    raw_bytes = io.BytesIO()                              # creates image buffer
    img.save(raw_bytes, "JPEG")                           # saves image to buffer
    raw_bytes.seek(0)                                     # sets stream position to 0
    img_b64 = base64.b64encode(raw_bytes.read())          # encode bytes to b64 string
    return str(img_b64)

# Main processing route
@app.route('/process', methods=['GET','POST'])
def process():
    if request.method == 'POST' and "inputImage" in request.get_json():
        # decoding base64
        input_b64 = request.get_json().get('inputImage', '')
        input_img = decodeImage(input_b64)

        # processing        
        out_img, result = processing(input_img)[3:]

        # encoding image to base64
        out_b64 = encodeImage(out_img)

        # preparing json
        out_json = { 
            'name': "post_image",
            'count': result,
            'outputImage': out_b64
            }
        
    elif request.method == 'GET' and "inputImage" in request.args:
        # decoding base64
        input_b64 = request.args['inputImage']
        input_img = decodeImage(input_b64)

        # processing        
        out_img, result = processing(input_img)[3:]

        # encoding image to base64
        out_b64 = encodeImage(out_img)

        # preparing json
        out_json = { 
            'name': "get_image",
            'count': result,
            'outputImage': out_b64
            }

    else:
        print("sample")
        # opening default image
        input_img = cv2.imread("./data/steel.jpg")

        # processing        
        out_img, result = processing(input_img)[3:]

        # encoding image to base64
        out_b64 = encodeImage(out_img)

        # preparing json
        out_json = { 
            'name': "sample_image_steel_224",
            'count': result,
            'outputImage': out_b64
            }

    return jsonify(out_json)

'''
# deprecated
# processing route
@app.route('/process/get', methods=['GET'])
def processget():
    if "inputImage" in request.args:
        # decoding base64
        input_img = decodeImage(request.args['inputImage'])

        # processing        
        out_img, result = processing(input_img)[3:]
        out_shape = str(out_img.shape)

        # encoding image to base64
        out_b64 = encodeImage(out_img)

        # preparing json
        out_json = { 
            'name': "sent_image",
            'count': result,
            'outputImage': out_b64
            }
        return jsonify(out_json)
    else:
        # opening default image
        input_img = cv2.imread("./data/steel.jpg")

        # processing        
        out_img, result = processing(input_img)[3:]
        out_shape = str(out_img.shape)

        # encoding image to base64
        out_b64 = encodeImage(out_img)

        # preparing json
        out_json = { 
            'name': "sample_image_steel_224",
            'count': result,
            'outputImage': out_b64
            }
        return jsonify(out_json)

@app.route('/process/steel', methods=['GET'])
def processSteel():
    # reading sample image
    img = cv2.imread("./data/steel.jpg")
    shape = img.shape
    input_enc = base64.urlsafe_b64encode(img)
    input_enc_utf = input_enc.decode("utf-8")
    input_enc_utf = re.sub(r'\=', r'', input_enc_utf)

    # decoding base64
    input_dec = base64.urlsafe_b64decode(input_enc_utf+"===")
    input_img = np.frombuffer(input_dec, dtype=np.uint8)
    input_img.shape = shape #(1342, 1600, 3)
    
    # processing
    out_img, result = processing(input_img)[3:]
    out_shape = str(out_img.shape)

    # encoding results
    out_enc = base64.urlsafe_b64encode(out_img)
    out_enc_utf = out_enc.decode("utf-8")
    out_enc_utf = re.sub(r'\=', r'', out_enc_utf)

    # preparing json
    out_json = { 
        'name': "sample_image_steel_224",
        'count': result,
        'outputImage': out_enc_utf,
        'outputShape': out_shape
        }
    return jsonify(out_json)
'''