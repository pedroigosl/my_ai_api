from logging import captureWarnings
from fastapi import FastAPI
import cv2
import uvicorn

app = FastAPI()
# close = False


class capture():
    #cap = []

    def __init__(self):
        self.close = False
        self.cap = cv2.VideoCapture(0)

        video_name = 'test' + '.mp4'
        while True:
            _, frame = self.cap.read()
            cv2.imshow(video_name[:-4], frame)
            if (self.close):
                break
            if (cv2.waitKey(1) == 27):
                break
        self.cap.release()
        cv2.destroyAllWindows()

    def kill(self):
        self.close = True
        self.cap.release()
        cv2.destroyAllWindows()
        # break


#cap = []
# =============================================================================


# =============================================================================

# pics: List[] = []
# =============================================================================


@app.post("/img_show")
async def imgShow():
    cap = capture()


@app.get("/img_close")
async def imgClose():
    #close = True
    cap.kill()

# @app.post("/take_pic")
# async def takePic():
#     ...


# @app.get("/get_pic")
# async def getPic(id: int):
#     ...

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")
