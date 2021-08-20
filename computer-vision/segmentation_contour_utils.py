import cv2
import matplotlib.pyplot as plt
import numpy as np
import inspect
import os

def isimageformat(file_str):
    '''Return true if file has image extension'''
    exts = [".png",".jpg",".jpeg",".tif",".tiff",".bmp"]
    for ext in exts:
        if file_str.lower().endswith(ext):
            return ext[1:]
    return False

def find_scale_byFolder(f, basepath="./", images = []):
    '''Procura por barra de escala em imagens da pasta fornecida.'''
    acc = []
    for file in os.listdir(basepath):
        filepath = os.path.join(basepath, file)
        if os.path.isfile(filepath) and isimageformat(filepath) and (file in images):
            print("File:", filepath)

            # Lendo imagem
            img = cv2.imread(filepath)

            img_out = f(img)

            # Resultados
            small = (14,14)
            #imgplot(img_out, size=small)

            ### Obtendo contornos
            contours, img_contours = get_contours(img, img_out, color=(0,255,0), thickness=3)
            #imgplot(img_contours, size=small)

            # Ordenando lista de contornos
            contours = find_scale_contour(contours)

            #Desenhando Contornos na imagem original
            verde = (0,255,0)
            img_contours = cv2.drawContours(img.copy(), contours[0:1], -1, verde, 3)
            imgplot(img_contours, size=small, name=file)

def find_scale_contour(contours):
    '''Função para ordenar lista de contornos com objetivo de encontrar aquele que mais se 
    parece com uma linha de escala'''

    # Filtrando contornos com área pequena
    contours = [c for c in contours if cv2.contourArea(c)> 100]

    #Ordenando Lista de Contornos
    def thinness(contour):
        x,y,w,h = cv2.boundingRect(contour)
        return (w/h)

    contours = sorted(contours, key = thinness, reverse = True)
    return contours

def filter0(img):
    '''Canny'''
    return cv2.Canny(img,100,200)

def filter1(img):
    '''filter1: Canny + Custom sobel'''
    # Conversão de uma imagem para outro sistema de cores
    #img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Aplicando Canny
    edges = cv2.Canny(img,100,200)

    # Aplicando filtro de sobel implementado na mão
    img_sobel = custom_sobel_bruno(edges).astype(np.uint8)

    return img_sobel

def filter2(img, c=0):
    '''filter2: Sobel y'''
    #sobelx = cv2.Sobel(img,cv.CV_8U,1,0,ksize=5)

    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    sobely = custom_sobely(img_gray)

    #thresh, img_thresh = cv2.threshold(sobely,140,255,cv2.THRESH_BINARY_INV)
    #thresh, img_thresh = cv2.threshold(sobely,0,255,cv2.THRESH_OTSU)

    img_thresh = cv2.adaptiveThreshold(sobely, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 199, -1) 
    # C=[-1..0] deu bons resultados

    return img_thresh

def filter3(img):
    '''filter3: Custom sobel bruno + otsu'''
    # Conversão de uma imagem para outro sistema de cores
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Aplicando filtro de sobel manual
    img_sobel = custom_sobel_bruno(img_gray).astype(np.uint8)

    # Aplicando Threshold Otsu
    thresh, img_thresh = cv2.threshold(img_sobel,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    return img_thresh

def filter4(img):
    '''filter4: bilateral smoothing + convolution + not'''
    # Convertendo para escala de cinza
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Suavização
    img_gray = cv2.bilateralFilter(img_gray,9,75,75)

    # Criando filtro
    #width = int( img_gray.shape[0]/10 )
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (31,3))
    if np.sum(kernel)!=0:
        kernel = kernel/np.sum(kernel)

    img_convolved = cv2.filter2D(img_gray, -1, kernel)

    # Invertendo
    img_not = cv2.bitwise_not(img_convolved)

    return img_not

def filter5(img):
    '''filter5: bilateral smoothing + custom sobely + not'''
    # Convertendo para escala de cinza
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Suavização
    img_gray = cv2.bilateralFilter(img_gray,9,75,75)

    # Sobel
    img_convolved = custom_sobely(img_gray, ksize=15)

    # Invertendo
    img_not = cv2.bitwise_not(img_convolved)

    return img_not

def get_contours(img, img_thresh, color=(0,255,0), thickness=3):
    #Desenhando borda na imagem
    y,x = img_thresh.shape
    img_thresh[:,   0] = 0; img_thresh[:, x-1] = 0; img_thresh[0,   :] = 0; img_thresh[y-1, :] = 0

    #Gerando Lista de Contornos
    cv2MajorVersion = cv2.__version__.split(".")[0]
    if int(cv2MajorVersion) >= 4:
        contours, _= cv2.findContours(img_thresh,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    else:
        _, contours, _ = cv2.findContours(img_thresh,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    #Ordenando Lista de Contornos de acordo com a área
    contours = sorted(contours, key = cv2.contourArea, reverse = True)

    #Desenhando Contornos na imagem original
    img_contours = cv2.drawContours(img.copy(), contours, -1, color, thickness)

    return contours, img_contours

def convolution(image, kernel): #kernel é um array
    '''Filtro de convolução implementado com laços.'''
    y, x = image.shape
    ky, kx = kernel.shape
    divisor = np.sum(kernel) if (np.sum(kernel))!=0 else 1
    
    minusy= int((ky)/2)
    plusy = ky - minusy - 1
    minusx= int((kx)/2)
    plusx = kx - minusx - 1

    image_temp = np.zeros([minusy+y+plusy, minusx+x+plusx])+np.mean(image)
    image_temp[minusy:minusy+y, minusx:minusx+x] = np.copy(image)
    image_new = np.zeros((y,x))

    for i in range(minusy, minusy+y):
        for j in range(minusx, minusx+x):
            soma = 0
            for k in range(ky):
                for l in range(kx):
                    soma += image_temp[-minusy+i+k, -minusx+j+l]*kernel[k,l]
                    #print("soma:", soma)
                    #print("i,j,k,l,soma:",i,j,k,l,-minusy+i+k,-minusx+j+l)
            #print("total:", soma)        
            image_new[i-minusy,j-minusx] = soma/divisor
    return image_new.astype(np.float64)

def custom_sobely(img_gray, ksize=3):
    '''Takes a GRAY image, converts it to uint8, take the sobel y, normalizes and returns the square root.'''
    img_gray = img_gray.astype(np.uint8)

    img_sobel_y = cv2.Sobel(img_gray, ddepth=-1, dx=0, dy=1, ksize=ksize)

    img_norm = img_sobel_y - np.min(img_sobel_y)
    img_norm = 255.0*img_norm/np.max(img_norm)

    img_norm = np.uint8(np.sqrt(img_norm))
    return img_norm

def custom_sobelxy(image):
    '''Filtro de sobel implementado com convolução de laços.'''
    kernel_sobel_x = np.array([[-1, -2, -1],
                            [ 0,  0,  0],
                            [ 1,  2,  1]], dtype=int)

    kernel_sobel_y = np.array([[-1, 0, 1],
                            [-2, 0, 2],
                            [-1, 0, 1]], dtype=int)
    imgx = convolution(image, kernel_sobel_x)
    imgy = convolution(image, kernel_sobel_y)
    
    img = imgx + imgy
    
    #Normalizando para 8bits (0-255)
    img = img - np.min(img)
    img = 255.0*img/np.max(img)
    
    return  np.uint8(np.sqrt(img))

def custom_sobel_bruno(image):
    kernel_sobel_x = np.array([[-1, -2, -1],
                               [ 0,  0,  0],
                               [ 1,  2,  1]], dtype=int)

    kernel_sobel_y = np.array([[-1, 0, 1],
                               [-2, 0, 2],
                               [-1, 0, 1]], dtype=int)
    imgx = convolution(image, kernel_sobel_x)
    imgy = convolution(image, kernel_sobel_y)
    
    img = imgx + imgy
    
    #Normalizando para 8bits (0-255)
    img = img - np.min(img)
    img = 255.0*img/np.max(img)
    
    return  np.uint8(np.sqrt(img))

def imgplot(img, name="", size=(7,7)):
    '''Função para plotar imagem (numpy array) com tamanho e título fixos'''
    if name == "":
        try:
            name = retrieve_name(img)
        except:
            pass
    plt.figure(figsize=size)
    plt.title(name)
    plt.imshow(img, "gray")

def retrieve_name(var):
        """
        Gets the name of var. Does it from the out most frame inner-wards.
        :param var: variable to get name from.
        :return: string
        """
        for fi in reversed(inspect.stack()):
            names = [var_name for var_name, var_val in fi.frame.f_locals.items() if var_val is var]
            if len(names) > 0:
                return names[0]
