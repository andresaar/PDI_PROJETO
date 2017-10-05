import cv2
import numpy as np
from math import sqrt

class Camera:
    def __init__(self, port):
        self.cap = cv2.VideoCapture(port)
        # self.white = [255,255,255]
        # self.black = [0,0,0]
        # self.red = [255,0,0]
        # self.green = [0,255,0]
        # self.blue = [0,0,255]

        self.boundaries = [
            ([0, 0, 152], [27, 159, 255]),
            ([223, 0, 0], [255, 217, 100]),
            ([25, 146, 190], [62, 174, 250]),
            ([103, 86, 65], [145, 133, 128])
        ]

    def teste(self):
        while True:
            _, frame = self.cap.read()
            _, frame = self.cap.read()

            frame2 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype("float32")
            (h, s, v) = cv2.split(frame2)
            s = s * 2
            s = np.clip(s, 0, 255)
            frame2 = cv2.merge([h, s, v])
            frame2 = cv2.cvtColor(frame2.astype("uint8"), cv2.COLOR_HSV2BGR)
            cv2.imshow("image", np.hstack([frame, frame2]))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break


    def achaCores(self):
        ret, frame = self.cap.read()
        ret, frame = self.cap.read()
        frame = cv2.blur(frame,(5,5))
        if not ret:
            raise Exception("Não capturou imagem")

        heigh, width, depth = frame.shape

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype("float32")
        (h, s, v) = cv2.split(frame)
        s = s * 2
        s = np.clip(s, 0, 255)
        frame = cv2.merge([h, s, v])
        frame = cv2.cvtColor(frame.astype("uint8"), cv2.COLOR_HSV2BGR)

        cv2.imshow("original",frame)
        cv2.waitKey(0)

        for (lower, upper) in self.boundaries:
            # create NumPy arrays from the boundaries
            lower = np.array(lower, dtype="uint8")
            upper = np.array(upper, dtype="uint8")

            # find the colors within the specified boundaries and apply
            # the mask
            mask = cv2.inRange(frame, lower, upper)
            output = cv2.bitwise_and(frame, frame, mask=mask)

            # show the images
            cv2.imshow("images", np.hstack([frame, output]))
            cv2.waitKey(0)
        cv2.destroyAllWindows()



        # for l in range(heigh):
        #     for c in range(width):
        #         menor, cor = self.distancia(frame[l,c], self.white), self.white
        #         if self.distancia(frame[l,c], self.black) < menor :
        #             menor, cor = self.distancia(frame[l,c], self.black), self.black
        #         if self.distancia(frame[l,c], self.red) < menor :
        #             menor, cor = self.distancia(frame[l,c], self.red), self.red
        #         if self.distancia(frame[l,c], self.green) < menor :
        #             menor, cor = self.distancia(frame[l,c], self.green), self.green
        #         if self.distancia(frame[l,c], self.blue) < menor :
        #             menor, cor = self.distancia(frame[l,c], self.blue), self.blue
        #         frame[l,c] = cor


    def distancia(self, p1, p2):
        return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2)
