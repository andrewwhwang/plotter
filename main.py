import numpy as np
import cv2
import argparse
import stepper, dc
import crosshatch
import RPi.GPIO as GPIO
from multiprocessing import Process
from time import sleep

parser = argparse.ArgumentParser()
parser.add_argument('file', metavar='file', help='image file to be printed(jpg or png)')
parser.add_argument('-ch', '--crosshatch', help='crosshatch mode enabled', action='store_true')
parser.add_argument('-p', '--preview', help='no print, just compute image', action='store_true')
args = parser.parse_args()

DIM = 400
SPEED = .005
SPACING = 10

def getContour(level, image):
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    # ret, thresh = cv2.threshold(blur,level,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    im2, c, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    c =  [x for x in c if cv2.contourArea(x) >= 100]
    return [c]

def getContourCrossHatch(image):
    funcs = [crosshatch.drawDiagonalDown,crosshatch.drawDiagonalUp,crosshatch.drawUp,crosshatch.drawLeft]
    contours = []
    for i in range(4):
        level = (i + 1) * 51
        # ret, thresh = cv2.threshold(blur,level,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        ret, thresh = cv2.threshold(blur,level,255,0)
        im2, c, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
        c = [x for x in c if cv2.contourArea(x) >= 100]

        image = np.zeros((DIM,DIM,3))
        cv2.drawContours(image, c, -1, (0,255,0), -1)
        lines, endpoints = funcs[i](DIM, SPACING)
        image = cv2.bitwise_and(image, lines)

        if i < 2:
            contours.append(crosshatch.getVectorsDiag(endpoints, image))
        else:
            contours.append(crosshatch.getVectorsOrth(endpoints, image))

    return contours


def CNCprint(contours):
    ver_motor = stepper.motor(7,11)
    hor_motor = stepper.motor(24,26)
    dc_motor = dc.DCmotor(13,15)

    dc_motor.up()
    hor_motor.reset()
    ver_motor.reset()


    for contour in contours:

        pX = Process(target=hor_motor.goto, args=(contour[0][0][0],SPEED))
        pY = Process(target=ver_motor.goto, args=(contour[0][0][1],SPEED))
        pX.start()
        pY.start()
        pX.join()
        pY.join()


        hor_motor.set_pos(contour[0][0][0])
        ver_motor.set_pos(contour[0][0][1])


        x_dis = [j[0][0]-i[0][0] for i, j in zip(contour[:-1], contour[1:])]
        y_dis = [j[0][1]-i[0][1] for i, j in zip(contour[:-1], contour[1:])]


        x_dir = [1 if x > 0 else 0 for x in x_dis]
        y_dir = [1 if y > 0 else 0 for y in y_dis]

        x_mag = [abs(x) for x in x_dis]
        y_mag = [abs(y) for y in y_dis]


        dc_motor.down()
        pX = Process(target=hor_motor.move, args=(zip(x_mag,x_dir),SPEED))
        pY = Process(target=ver_motor.move, args=(zip(y_mag,y_dir),SPEED))
        pX.start()
        pY.start()
        pX.join()
        pY.join()
        dc_motor.up()

        hor_motor.set_pos(contour[-1][0][0])
        ver_motor.set_pos(contour[-1][0][1])

    GPIO.cleanup()

if __name__ == '__main__':
    im = cv2.imread(args.file, 1)
    scale = float(DIM)/max(im.shape[0], im.shape[1])
    resize = cv2.resize(im, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    flip = cv2.flip(resize, 1)
    imgray = cv2.cvtColor(flip, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(imgray,(5,5),0)
    contours = []
    
    if args.crosshatch:
        contours = getContour(127, blur)
    else:
        contours = getContourCrossHatch(blur)
        
    if not args.preview:
        try:
            for c in contours:
                CNCprint(c)
        except KeyboardInterrupt:
            GPIO.cleanup()
    else:
        black_background = np.zeros((DIM,DIM,3))
        flatten_list = [item for sublist in contours for item in sublist]
        final = cv2.drawContours(black_background, flatten_list, -1, (0,255,0), 1)
        cv2.imwrite('final.jpg', cv2.flip(final,1))
