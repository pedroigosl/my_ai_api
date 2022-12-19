from hashlib import sha1
from logging import captureWarnings
# from multiprocessing import Process as process
from fastapi import FastAPI, Path, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Required
import uvicorn

#from core import capture as cp
from controllers import cam_controller as cc
from controllers import ai_controller as ai
from utils import session_data as sd

description = """
API for controlling camera, recording and applying computer vision

"""

app = FastAPI(title="Remote Camera API",
              description=description,
              version="1.1.0",
              contact={
                    "name": "Pedro Igo SL",
                    "url": "https://github.com/pedroigosl",
                    "email": "pedroigosl@gmail.com",
              })

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================

name_regex = "^\w{1,25}"
path_regex = "^(?:\w+/){0,2}$"

# =============================================================================

session = sd.data()

# =============================================================================


@app.post("/open_camera")
def open_camera(name: str = Query(default=None, regex=name_regex),
                cam_id: int = Query(default=0)):
    return cc.startCam(session, name, cam_id)


@app.put("/video_rename")
def video_rename(name: str = Query(default=Required, regex=name_regex)):
    return cc.renameVideo(session, name)


@app.put("/record")
def record(name: str = Query(default=None, regex=name_regex),
           path: str = Query(default="videos/", regex=path_regex)):
    return cc.record(session, name, path)


@ app.post("/take_pic")
def take_pic(name: str = Query(default=None, regex=name_regex),
             path: str = Query(default="pictures/", regex=path_regex)):
    return cc.takePic(session, name, path)


@ app.delete("/close_camera")
def close_camera():
    return cc.stopCam(session)


# =============================================================================


@ app.put("/reset_video_counter")
def reset_counter():
    return cc.resetCounter(session)


@ app.get("/get_video_counter")
def get_counter():
    return cc.getCounter(session)


# =============================================================================


@ app.post("/mask")
def mask():
    return ai.mask(session)

@app.put("/unmask")
def unmask():
    return ai.unmask(session)


@ app.put("/set_paths")
def set_paths(model_path: str = Query(default='models/coco/model.tflite', regex=path_regex),
              labels_path: str = Query(default='models/coco/labelmap.txt', regex=path_regex)):
    return ai.set_paths(model_path, labels_path)


# =============================================================================

# port=$1
# ip=$(hostname -I | awk '{print $1}')
# (uvicorn main:app --host "$ip" --port "$port")

# uvicorn main:app --reload

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")
