import cv2


class capture():

    def __init__(self):
        #close = False
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
        #global close
        self.close = True
        # self.cap.release()
        # cv2.destroyAllWindows()
        # break


if __name__ == "__main__":

    cap = capture()
    while True:
        print("1 - start recording")
        print("2 - stop recording")
        print("3 - exit")
        ans = input("_")

        if ans == '1':
            # start
            cap.iniciar()
        elif ans == '2':
            # stop
            cap.kill()
        elif ans == '3':
            break
