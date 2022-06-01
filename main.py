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
            self.name = f"video #{count}.mp4"
        else:
            self.name = name + '.mp4'
        self.recording = recording
        self.show_img = show_img
        self.cam_id = cam_id
        self.close = False

        self.cap = cv2.VideoCapture(self.cam_id)
        self.width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.writer = None

    def start(self):
        while True:
            title = self.name
            _, frame = self.cap.read()
            if self.show_img:
                cv2.imshow('video', frame)
                cv2.setWindowTitle('video', title)
            if (cv2.waitKey(1) == 27) or self.close:
                break

            if self.recording == True:
                self.writer.write(frame)
        self.cap.release()
        if self.recording == True:
            self.writer.release()
        cv2.destroyAllWindows()

    def rename(self, new_name):
        if self.recording:
            print("Already recording, name not changed")
            return
        self.name = new_name

    def record(self, new_name=None):
        if new_name:
            self.rename(new_name)
        self.recording = True
        self.writer = cv2.VideoWriter(
            self.name, cv2.VideoWriter_fourcc(*'mp4v'), 20,
            (self.width, self.height))

    def stop(self):
        self.close = True


# =============================================================================

@app.post("/cam_start")
def cam_start(name: str = None, cam_id: int = 0):
    global cap
    global count
    try:
        if not name:  # == None:
            count += 1
            print(f"session #{count} started")
        cap = capture(name, show_img=True, recording=False, cam_id=cam_id)
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
