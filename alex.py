from logging import captureWarnings
from fastapi import FastAPI
import cv2
import uvicorn

app = FastAPI()


class capture():

    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.close = False

    def iniciar(self):
        video_name = 'test' + '.mp4'
        while True:
            _, frame = self.cap.read()
            cv2.imshow(video_name[:-4], frame)
            if (cv2.waitKey(1) == 27) or self.close:
                break
        self.cap.release()
        cv2.destroyAllWindows()

    def kill(self):
        self.close = True


# =============================================================================
captures = []


@app.post("/img_show")
def imgShow():
    captures.append(capture())
    captures[0].iniciar()


@app.get("/img_close")
def imgClose():
    captures[0].kill()
    captures.pop()

# @app.post("/take_pic")
# async def takePic():
#     ...


# @app.get("/get_pic")
# async def getPic(id: int):
#     ...

if __name__ == "__main__":
    uvicorn.run("alex:app", reload=True)
