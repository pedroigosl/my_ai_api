from core import capture as cp
from core import cv_masker as msk
import cv2

vid_count = 0

pic_count = 0

cap = None

# =============================================================================


def startCam(name, cam_id):
    global cap
    global vid_count

    if not name:  # == None:
        vid_count += 1
        print(f"session #{vid_count} started")
        name = f"video #{vid_count}"
    cap = cp.capture(name, show_img=True, recording=False, cam_id=cam_id)
    cap.run()


def renameVideo(name):
    global cap
    print(name)
    cap.rename(name)


def record(name, path):
    global cap
    cap.record(name, path)


def takePic(name, path):
    global cap
    global pic_count

    if not name:  # == None:
        pic_count += 1
        print(f"pic #{pic_count} taken")
        name = f"pic #{pic_count}"
    cap.screenshot(name, path)


def stopCam():
    global cap

    cap.stop()
    cap = None


def resetCounter():
    global vid_count
    try:
        vid_count = 0
        return vid_count
    except:
        print("Error resetting counter")


def getCounter():
    return vid_count


def grayscale(img):

    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def classify(img):
    mask = msk.classifier('models/coco/model.tflite',
                          'models/coco/labelmap.txt')

    return mask.classify(img)


def mask():
    global cap
    # args = ['hey', 'hoo']
    cap.masking(classify)

# @app.get("/get_pic")
# async def getPic(id: int):
#     ...
