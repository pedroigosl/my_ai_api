import cv2


class capture():
    def __init__(self, name, show_img=False, recording=False, cam_id=0):
        self.extension = ".mp4"
        if name == None:
            self.name = f"capture{self.extension}"
        else:
            self.name = f"{name}{self.extension}"
        self.recording = recording
        self.show_img = show_img
        self.cam_id = cam_id
        self.close = False

        self.cap = cv2.VideoCapture(self.cam_id)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.writer = None

    def start(self):
        while (cv2.waitKey(1) != 27) and not self.close:
            title = self.name
            _, frame = self.cap.read()
            if self.show_img:
                cv2.imshow('video', frame)
                cv2.setWindowTitle('video', title)

            if self.recording:
                self.writer.write(frame)
        self.stop()
        # self.cap.release()
        # if self.recording:
        #     self.writer.release()
        # cv2.destroyAllWindows()

    def rename(self, new_name):
        if self.recording:
            print("Already recording, name not changed")
            return
        self.name = f"{new_name}{self.extension}"

    def record(self, new_name=None, path="videos/"):
        if self.recording:
            print("Already recording")
            return
        if new_name:
            print("in")
            self.rename(new_name)
        self.writer = cv2.VideoWriter(
            f"{path}{self.name}", cv2.VideoWriter_fourcc(*'mp4v'), 20,
            (self.width, self.height))
        self.recording = True

    def stop(self):
        self.close = True
        self.cap.release()
        if self.recording:
            self.writer.release()
        cv2.destroyAllWindows()
