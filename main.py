from hashlib import sha1
from logging import captureWarnings
# from multiprocessing import Process as process
from fastapi import FastAPI, Path, Query
from pydantic import BaseModel
import cv2
import uvicorn

app = FastAPI()

count = 0
# free_cam = True
cap = []


class capture():

    def __init__(self, name, show_img=False, recording=False, cam_id=0):
        if name == None:
            self.name = f"video #{count}"
        else:
            self.name = name
        self.recording = recording
        self.show_img = show_img

        self.cap = cv2.VideoCapture(cam_id)
        self.close = False

    def start(self):
        while True:
            video_name = self.name + '.mp4'
            _, frame = self.cap.read()
            if self.show_img:
                cv2.imshow('video', frame)
                cv2.setWindowTitle('video', video_name)
            if (cv2.waitKey(1) == 27) or self.close:
                break
        self.cap.release()
        cv2.destroyAllWindows()

    def rename(self, new_name):
        self.name = new_name

    def stop(self):
        self.close = True


# =============================================================================

@app.post("/cam_start")
def cam_start(name: str = None):
    global cap
    global count
    try:
        if not name:  # == None:
            count += 1
            print(f"session #{count} started")
        cap = capture(name, show_img=True)
        cap.start()
    except:
        print("error starting video")


@app.put("/video_rename")
def video_rename(name: str):
    global cap
    print(name)
    cap.rename(name)
# @app.put("/record")
# def record():
#     try:
#         # cap.record()
#         ...
#     except:
#         ...


@app.put("/reset_counter")
def reset_counter():
    global count
    try:
        count = 0
        return count
    except:
        print("Error resetting counter")


@app.get("/get_counter")
def get_counter():
    return count


@ app.delete("/cam_stop")
def cam_stop():
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


# uvicorn main:app --reload
if __name__ == "__main__":
    uvicorn.run("main:app", host="1.1.1.1", port=8000, log_level="info")
