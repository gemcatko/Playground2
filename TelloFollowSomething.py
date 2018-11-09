# working version 1
# author: Arun Ponnusamy
# website: https://www.arunponnusamy.com

# object detection webcam example
# usage: python object_detection_webcam.py

# right now YOLOv3 is being used for detecting objects.
# It's a heavy model to run on CPU. You might see the latency
# in output frames.
# To-Do: Add tiny YOLO for real time object detection

# import necessary packages
import cvlib as cv
from cvlib.object_detection import draw_bbox
import cv2

# variable definition
#objectToFolow = 'person'
objectToFolow = 'cell phone'
Xresolution = 680
Yresolution = 480
bbox = [[1,1,1,1]]
percentObjectToFolow = 0.5 # to define how far objectToFolow should be it 0.2 = 20%
#variable normalization
x1percento = Xresolution/100
stredX = Xresolution/2
#boxLengh = bbox[0][2] - bbox[0][0]
def getNavCoordinates():
    #X 680*Y 480
    #[[X1 371,X2 18,Y1 639,Y2 388]]
    global boxLengh
    global boxMiddleX
    global diffFromMiddleX
    boxLengh = bbox[label.index(objectToFolow)][2] - bbox[label.index(objectToFolow)][0]
    # boxMiddleX(stred boundig buxu na X ose) = (bboxleght X1 /2) + suradnica X1 <-- kedze suradnic moze byt viac napr: [[272, 294, 440, 480], [-5, 133, 439, 491]] ['remote', 'person'] [0.9549392461776733, 0.6422694325447083] treba volat s indexom label.index(objectToFolow)
    boxMiddleX = ((boxLengh/2) + bbox[label.index(objectToFolow)][0])
    # diffFromMiddleX = abs (stred predpopevedaneho objektu x - stred x podla rozlisenia) # is used for speed of rotation to the object
    diffFromMiddleX = abs(boxMiddleX - stredX)
    pass

def navigate():
    #print(label)
    #print(type(label))
    #checking if object to folow othervise cannot calculate, to fu
    if objectToFolow in label:
        label.index(objectToFolow)
        #print("index(objectToFolow:", label.index(objectToFolow) )
        getNavCoordinates()
        #navigatemiddle()
        navigateForwardBackward()
        navigateSide()
    pass

def navigateWhere():
    print(type(bbox))
    print("Suradnice vsetky:", bbox)
    print("Suradnica X1:", bbox[0][0])
    print("Suradnica X2:", bbox[0][1])
    print("Suradnica Y1:", bbox[0][2])
    print("Suradnica Y2:", bbox[0][3])
    pass

def navigatemiddle():
    if boxMiddleX < stredX:
        if diffFromMiddleX > ( Xresolution * 0.1 ):
            #call funktion to rotate right fast
            print("doprva rychlo")
        else:
            #print("boxMiddleX", boxMiddleX)
            print("doprva")
            #call funktion to rotate right
            pass
        pass
    if boxMiddleX > stredX:
        if diffFromMiddleX > ( Xresolution * 0.1 ):
            print("dolava rychlo")
            #call funktion to rotate right fast
        else:
            #print("boxMiddleX", boxMiddleX)
            print("dolava")
            #call fuction to rotate dolava
            pass
        pass
    print(stredX,"diffFromMiddleX", diffFromMiddleX, "boxMiddleX", boxMiddleX)
    #print("boxLengh",boxLengh)
    #print("boxMiddleX",boxMiddleX)
    pass

def navigateForwardBackward():
    #boxLengh = bbox[label.index(objectToFolow)][2] - bbox[label.index(objectToFolow)][0]
    if boxLengh < (Xresolution * percentObjectToFolow):
        # go forward
        print("go forward")
        pass

    if boxLengh > (Xresolution * percentObjectToFolow):
        # go forward
        print ("go backward")
        pass
    pass
def navigateSide():
    if boxMiddleX < stredX:
        if diffFromMiddleX > ( Xresolution * 0.1 ):
            #call funktion to sideway right fast
            print("sideway right fast")
        else:
            #print("boxMiddleX", boxMiddleX)
            print("sideway right")
            #call sideway right fast
            pass
        pass
    if boxMiddleX > stredX:
        if diffFromMiddleX > ( Xresolution * 0.1 ):
            print("sideway left fast")
            #call function go sideway left fast
        else:
            print("sideway left")
            #call function go sideway left
            pass
        pass

    #call function go sideway right
    #call function go sideway leftight
    pass
# open webcam
webcam = cv2.VideoCapture(0)

if not webcam.isOpened():
    print("Could not open webcam")
    exit()

# loop through frames
while webcam.isOpened():

    # read frame from webcam
    status, frame = webcam.read()

    if not status:
        print("Could not read frame")
        exit()

    # apply object detection
    bbox, label, conf = cv.detect_common_objects(frame)
    print(bbox, label, conf)
    navigate()

    # draw bounding box over detected objects
    out = draw_bbox(frame, bbox, label, conf)

    # display output
    cv2.imshow("Real-time object detection", out)
    # press "Q" to stop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# release resources
webcam.release()
cv2.destroyAllWindows()

