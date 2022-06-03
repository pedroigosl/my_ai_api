from models import capture as cp

vid_count = 0

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


def resetCounter():
    global vid_count
    try:
        vid_count = 0
        return vid_count
    except:
        print("Error resetting counter")


def getCounter():
    return vid_count


def stopCam():
    global cap

    cap.stop()
    cap = None


def takePic():
    global cap
    cap.screenshot()


# @app.get("/get_pic")
# async def getPic(id: int):
#     ...
