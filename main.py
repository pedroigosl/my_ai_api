from hashlib import sha1
from logging import captureWarnings
# from multiprocessing import Process as process
from fastapi import FastAPI, Path, Query
from pydantic import BaseModel
import uvicorn

from models import capture as cp
import cam_controls as cc

description = """
API for controlling camera, recording and applying computer vision

"""

app = FastAPI(title="Remote Camera API",
              description=description,
              version="0.0.1",
              contact={
                    "name": "Pedro Igo SL",
                    "url": "https://github.com/pedroigosl",
                    "email": "pedroigosl@gmail.com",
              },
              license_info={
                  "name": "Apache 2.0",
                  "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
              })

count = 0

cap = None


# =============================================================================

@app.post("/open_camera")
def open_camera(name: str = None, cam_id: int = 0):
    return cc.startCam(name, cam_id)


@app.put("/video_rename")
def video_rename(name: str):
    return cc.renameVideo(name)


@app.put("/record")
def record():
    return cc.record()


@app.put("/reset_video_counter")
def reset_counter():
    return cc.resetCounter()


@app.get("/get_video_counter")
def get_counter():
    return cc.count


@ app.delete("/close_camera")
def close_camera():
    return cc.stopCam()

# =============================================================================


# uvicorn main:app --reload
if __name__ == "__main__":
    uvicorn.run("main:app", host="1.1.1.1", port=8000, log_level="info")
