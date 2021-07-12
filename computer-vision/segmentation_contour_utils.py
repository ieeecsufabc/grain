import cv2
import matplotlib.pyplot as plt
import numpy as np
import inspect

def find_scale_contour(contours):
    '''Função para ordenar lista de contornos com objetivo de contrar aquele que mais se 
    parece com uma linha de escala'''

    # Filtrando contornos com área pequena
    #contours = [c for c in contours_original if cv2.contourArea(c)> 100]

    #Ordenando Lista de Contornos
    def thinness(contour):
        x,y,w,h = cv2.boundingRect(contour)
        return (w/h)

    contours = sorted(contours, key = thinness, reverse = True)
    return contours

def scale_processing(img):
    '''Função para encontrar lista de contornos com o objetivo de encontrar o contorno que mais se parece com a barra de escala'''
    
    # Conversão de uma imagem para outro sistema de cores
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Aplicando Canny
    #edges = cv2.Canny(img,100,200)
    #plt.subplot(121),plt.imshow(img,cmap = 'gray')
    #plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    #plt.subplot(122),plt.imshow(edges,cmap = 'gray')
    #plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

    # Filtros para realçar as bordas certas
    # Filtro de sobel
    # https://docs.opencv.org/3.4.2/d5/d0f/tutorial_py_gradients.html

    img_sobel = sobel(img_gray).astype(np.uint8)
    #plt.figure(figsize=(10,10)); plt.title("img_sobel"); fig=plt.imshow(img_sobel, "gray")

    #Aplicando Threshold
    thresh, img_thresh = cv2.threshold(img_sobel,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    #thresh, img_thresh = cv2.threshold(img_sobel,140,255,cv2.THRESH_BINARY_INV)
    #thresh, img_thresh = cv2.threshold(img_blur,0,255,cv2.THRESH_BINARY_INV)
    plt.figure(figsize=(7,7)); plt.title("img_thresh"); fig=plt.imshow(img_thresh, "gray")
    #cv2.imshow("OTSU Image", img_thresh)
    #cv2.waitKey(0)

    #APLICANDO EROSÃO
    kernel = np.ones((3,3))
    '''img_open = cv2.morphologyEx(img_thresh,cv2.MORPH_OPEN,kernel, iterations = 1)
    img_eroded = cv2.erode(img_open,kernel,iterations=3)
    plt.figure(figsize=(10,10)); plt.title("img_eroded"); fig=plt.imshow(img_eroded, "gray")'''
    '''dilation = cv2.dilate(img_thresh, kernel, iterations=1) 
    plt.figure(figsize=(10,10)); plt.title("img_dilated"); fig=plt.imshow(dilation, "gray")'''

def get_contours(img_thresh, color=(0,255,0), thickness=3):
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
