from time import sleep
import sys
import traceback
import tellopy
import av
import cv2.cv2 as cv2  # for avoidance of pylint error
import numpy
import time
import cvlib as cv
from TelloFollowSomething import getnavcoordinates, navigatewhere,navigatemiddle,navigateForwardBackward
from cvlib.object_detection import draw_bbox


def handler(event, sender, data, **args):
    drone = sender
    if event is drone.EVENT_FLIGHT_DATA:
        print(data)


drone = tellopy.Tello()
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
    #drone = tellopy.Tello()

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
                #height, width, channels = image.shape
                #print("height, width, channels of the picture are:", height, width, channels)

                #cv2.imshow('Original', image)
                #cv2.imshow('Canny', cv2.Canny(image, 100, 200))
                # apply object detection
                #status, frame = webcam.read()
                #bbox, label, conf = cv.detect_common_objects(image)
                #faces, confidences = cv.detect_face(image)
                #print("faces, confidences", faces, confidences)
                #label = ["person"]
                #labelos = [[faces]] ['faces'] [confidences]
                #out = draw_bbox(image,[faces],['person'],[confidences])
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
                #cv2.imshow("Real-time object detection")
                #cv2.waitKey(1)
                frame_skip = int((time.time() - start_time)/frame.time_base)

    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        print(ex)
    finally:
        drone.quit()
        cv2.destroyAllWindows()



if __name__ == '__main__':
    #test()
    #right()
    video()