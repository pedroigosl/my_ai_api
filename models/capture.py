import cv2


class capture():
    def __init__(self, name, show_img=False, recording=False, cam_id=0):
        if name == None:
            self.name = "capture.mp4"
        else:
            self.name = name + '.mp4'
        self.recording = recording
        self.show_img = show_img
        self.cam_id = cam_id
        self.close = False

        self.cap = cv2.VideoCapture(self.cam_id)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

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

            if self.recording:
                self.writer.write(frame)
        self.cap.release()
        if self.recording:
            self.writer.release()
        cv2.destroyAllWindows()

    def rename(self, new_name):
        if self.recording:
            print("Already recording, name not changed")
            return
        self.name = new_name

    def record(self, new_name=None, path="videos/"):
        if self.recording:
            print("Already recording")
            return
        if new_name:
            self.rename(new_name)
        self.writer = cv2.VideoWriter(
            f"{path}{self.name}", cv2.VideoWriter_fourcc(*'mp4v'), 20,
            (self.width, self.height))
        self.recording = True

    def stop(self):
        self.close = True
