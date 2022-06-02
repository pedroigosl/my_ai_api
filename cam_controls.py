from models import capture as cp

count = 0

cap = None

# =============================================================================


def startCam(name, cam_id):
    global cap
    global count

    if not name:  # == None:
        count += 1
        print(f"session #{count} started")
    cap = cp.capture(name, show_img=True, recording=False, cam_id=cam_id)
    cap.start()


def renameVideo(name):
    global cap
    print(name)
    cap.rename(name)


def record(name, path):
    global cap
    cap.record(name, path)


def resetCounter():
    global count
    try:
        count = 0
        return count
    except:
        print("Error resetting counter")


def getCounter():
    return count


def stopCam():
    global cap
    try:
        cap.stop()
    except:
        print("Error stopping camera")

# @app.post("/take_pic")
# async def takePic():
#     ...


# @app.get("/get_pic")
# async def getPic(id: int):
#     ...
