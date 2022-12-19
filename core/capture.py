import cv2
import time


# Video capture object
class capture():
    def __init__(self, vid_name, show_img=False, recording=False, cam_id=0):
        # Extensions
        self.vid_ext = ".mp4"
        self.pic_ext = ".png"

        # Video naming
        if vid_name == None:
            self.vid_name = f"capture"
        else:
            self.vid_name = f"{vid_name}"

        # Video variables
        self.recording = recording
        self.show_img = show_img
        self.cam_id = cam_id
        self.close = False

        # Video object and attributes
        self.cap = cv2.VideoCapture(self.cam_id)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.frame = None
        # Frame timer
        self.timer = {'start': 0, 'end': 0}

        # Video text overlay attributes
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 0.5
        self.font_color = (0, 255, 0)
        self.font_thickness = 2
        self.pos = (5, 15)

        # Video writer object
        self.writer = None

        # Image modifier
        self.mask = None
        self.mask_args = None

    # Starts and runs video

    def run(self):
        self.timer['start'] = time.time()
        self.timer['end'] = time.time()
        while not self.close:
            title = self.vid_name
            _, frame = self.cap.read()

            # fps overlay
            self.timer['end'] = time.time()
            frame = self.fps_overlay(frame)
            self.timer['start'] = self.timer['end']

            # Records frames
            if self.recording:
                self.writer.write(frame)

            if self.mask:
                if self.mask_args:
                    frame = self.mask(frame, self.mask_args)
                else:
                    frame = self.mask(frame)

            if self.show_img:
                cv2.imshow('video', frame)
                cv2.setWindowTitle('video', title)

            key = cv2.waitKey(1)
            if (key == 27):
                self.stop()
            elif (key == 32):
                self.screenshot()
            self.frame = frame
        self.cap.release()
        if self.recording:
            self.writer.release()
        cv2.destroyAllWindows()

    # Renames video (only works before recording)
    def rename(self, new_name):
        if self.recording:
            print("Already recording, name not changed")
            return
        self.vid_name = new_name

    # Takes picture
    def screenshot(self, name=None, path="pictures/"):
        pic = self.frame
        if name == None:
            name = f"{self.vid_name} screenshot"
        cv2.imwrite(f"{path}{name}{self.pic_ext}", pic)
        print(f"picture '{name}' taken")

    # Starts video recording
    def record(self, new_name=None, path="videos/"):
        if self.recording:
            print("Already recording")
            return
        if new_name:
            self.rename(new_name)
        self.writer = cv2.VideoWriter(
            f"{path}{self.vid_name}{self.vid_ext}", cv2.VideoWriter_fourcc(
                *'mp4v'), 20,
            (self.width, self.height))
        self.recording = True

    def masking(self, func, args=None):
        self.mask = func
        self.mask_args = args

    def fps_overlay(self, frame):
        text = f"fps: {int(1/(self.timer['end'] - self.timer['start']))}"
        cv2.putText(frame, text, self.pos,
                    self.font, self.font_scale, self.font_color, self.font_thickness)
        return frame

    # Stops video
    def stop(self):
        self.close = True
        # self.cap.release()
        # if self.recording:
        #     self.writer.release()
        # cv2.destroyAllWindows()

    #     self.__del__()

    # def __del__(self):
    #     self.close = True
        # self.cap.release()
        # if self.recording:
        #     self.writer.release()
        # cv2.destroyAllWindows()
