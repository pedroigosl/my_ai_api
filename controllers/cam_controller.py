from core import capture as cp
import cv2

# =============================================================================


def startCam(session, name, cam_id):
    if not name:  # == None:
        session.vid_count += 1
        print(f"session #{session.vid_count} started")
        name = f"video #{session.vid_count}"
    session.cap = cp.capture(
        name, show_img=True, recording=False, cam_id=cam_id)
    session.cap.run()


def renameVideo(session, name):
    print(name)
    session.cap.rename(name)


def record(session, name, path):
    session.cap.record(name, path)


def takePic(session, name, path):

    if not name:  # == None:
        session.pic_count += 1
        print(f"pic #{session.pic_count} taken")
        name = f"pic #{session.pic_count}"
    session.cap.screenshot(name, path)


def stopCam(session):

    session.cap.stop()
    session.cap = None


def resetCounter(session):
    try:
        session.vid_count = 0
        return session.vid_count
    except:
        print("Error resetting counter")


def getCounter(session):
    return session.vid_count
