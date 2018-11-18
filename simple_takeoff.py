from time import sleep
import sys
import traceback
import tellopy
import av
import cv2.cv2 as cv2  # for avoidance of pylint error
import numpy
import time
import cvlib as cv
# from TelloFollowSomething import getnavcoordinates, navigatewhere,navigatemiddle,navigateForwardBackward
from cvlib.object_detection import draw_bbox
import logging

# variable definition
# objectToFolow = 'person'
objectToFolow = 'sports ball'
# Xresolution = 680
# Yresolution = 480
Xresolution = 960
Yresolution = 720
bbox = [[1, 1, 1, 1]]
percentObjectToFolow = 0.5  # to define how far objectToFolow should be it 0.2 = 20%
# variable normalization
x1percento = Xresolution / 100
stredX = Xresolution / 2
drone = tellopy.Tello()


def getnavcoordinates(bbox, label):
    # X 680*Y 480
    # [[X1 371,X2 18,Y1 639,Y2 388]]
    global boxLengh
    global boxMiddleX
    global diffFromMiddleX
    global objectToFolow
    try:
        if not objectToFolow in label:
            global boxMiddleX
            boxMiddleX = stredX
            pass
        boxLengh = bbox[label.index(objectToFolow)][2] - bbox[label.index(objectToFolow)][0]
        # boxMiddleX(stred boundig buxu na X ose) = (bboxleght X1 /2) + suradnica X1
        # <-- kedze suradnic moze byt viac napr:
        # [[272, 294, 440, 480], [-5, 133, 439, 491]] ['remote', 'person'] [0.9549392461776733, 0.6422694325447083]
        # treba volat s indexom label.index(objectToFolow)
        boxMiddleX = ((boxLengh / 2) + bbox[label.index(objectToFolow)][0])
        # diffFromMiddleX = abs (stred predpopevedaneho objektu x - stred x podla rozlisenia)
        #  is used for speed of rotation to the object
        diffFromMiddleX = abs(boxMiddleX - stredX)
    except ValueError as err:
        print('There is an problem in getnavcoordinates () ValueError:', err)
        pass
    else:
        pass
    pass


def navigatemiddle(bbox, label, conf, frame):
    global boxLengh
    global boxMiddleX
    global diffFromMiddleX
    try:
        if objectToFolow in label:
            drone.takeoff()
            pass
        if "cell phone" in label:
            drone.land()
            pass
        if "spoon" in label:
            drone.clockwise(100)
            pass
        if "fork" in label:
            drone.counter_clockwise(100)
            pass
        if "apple" in label:
            drone.flip_forward()
            pass
        if "orange" in label:
            drone.flip_back()
            pass
        if ("fork" or "spoon") not in label:
            drone.counter_clockwise(0)
            pass
        if boxMiddleX < stredX:
            if diffFromMiddleX > (Xresolution * 0.1):
                # call funktion to rotate right fast
                print("doprva rychlo")
                pass
            else:
                # print("boxMiddleX", boxMiddleX)
                print("doprava")
                # call funktion to rotate right
                pass
            pass
        if boxMiddleX > stredX:
            if diffFromMiddleX > (Xresolution * 0.1):
                print("lavo rychlo")
                # call funktion to rotate right fast
                # drone.counter_clockwise(20)
            else:
                # print("boxMiddleX", boxMiddleX)
                print("lavo")
                # call fuction to rotate dolava

                pass
            pass
        print("stredX:", stredX, "diffFromMiddleX:", diffFromMiddleX, "boxMiddleX:", boxMiddleX)

        # print("boxLengh",boxLengh)
        # print("boxMiddleX",boxMiddleX)
    except Exception as e:
        logging.error(traceback.format_exc())
        print("There was exception at navigate middle error is:", e)
    else:
        print("navigate middle() executeted succesfully")
    pass


def handler(event, sender, data, **args):
    drone = sender
    if event is drone.EVENT_FLIGHT_DATA:
        print(data)


def test():
    # drone = tellopy.Tello()
    try:
        drone.subscribe(drone.EVENT_FLIGHT_DATA, handler)
        drone.connect()
        drone.wait_for_connection(60.0)
        drone.takeoff()
        sleep(5)
        drone.down(50)
        sleep(5)
        drone.land()
        sleep(5)
    except Exception as ex:
        print(ex)
    finally:
        drone.quit()


def right():
    drone = tellopy.Tello()
    try:
        drone.subscribe(drone.EVENT_FLIGHT_DATA, handler)
        drone.connect()
        drone.wait_for_connection(60.0)
        drone.takeoff()
        sleep(5)
        drone.clockwise(100)
        sleep(5)
        drone.land()
        sleep(5)
    except Exception as ex:
        print(ex)
    finally:
        drone.quit()


def video():
    # drone = tellopy.Tello()

    try:
        drone.connect()
        drone.wait_for_connection(60.0)

        container = av.open(drone.get_video_stream())
        print("type(container)", type(container))

        # skip first 300 frames
        frame_skip = 300
        while True:
            for frame in container.decode(video=0):
                if 0 < frame_skip:
                    frame_skip = frame_skip - 1
                    continue
                start_time = time.time()
                image = cv2.cvtColor(numpy.array(frame.to_image()), cv2.COLOR_RGB2BGR)
                # height, width, channels = image.shape
                # print("height, width, channels of the picture are:", height, width, channels)

                # cv2.imshow('Original', image)
                # cv2.imshow('Canny', cv2.Canny(image, 100, 200))
                # apply object detection
                # status, frame = webcam.read()
                # bbox, label, conf = cv.detect_common_objects(image)
                # faces, confidences = cv.detect_face(image)
                # print("faces, confidences", faces, confidences)
                # label = ["person"]
                # labelos = [[faces]] ['faces'] [confidences]
                # out = draw_bbox(image,[faces],['person'],[confidences])
                bbox, label, conf = cv.detect_common_objects(image)
                print(bbox, label, conf)
                out = draw_bbox(image, bbox, label, conf)
                # display output
                cv2.imshow("Real-time object detection", out)
                getnavcoordinates(bbox, label)
                navigatemiddle(bbox, label, conf, frame)
                # press "Q" to stop
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                # cv2.imshow("Real-time object detection")
                # cv2.waitKey(1)
                frame_skip = int((time.time() - start_time) / frame.time_base)

    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        print(ex)
    finally:
        drone.quit()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    # test()
    # right()
    video()
