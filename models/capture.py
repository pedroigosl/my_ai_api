import cv2


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

        # Video writer object
        self.writer = None

    # Starts and runs video
    def run(self):
        while not self.close:
            title = self.vid_name
            _, frame = self.cap.read()
            if self.show_img:
                cv2.imshow('video', frame)
                cv2.setWindowTitle('video', title)

            # Records frames
            if self.recording:
                self.writer.write(frame)

            if (cv2.waitKey(1) == 27):
                self.stop()
            elif (cv2.waitKey(1) == 32):
                self.screenshot()
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
        _, pic = self.cap.read()

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
