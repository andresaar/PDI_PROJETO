import cv2
import numpy as np
import imutils
from copy import copy

class Camera:
    def __init__(self, port):
        self.cap = cv2.VideoCapture(port)
        # self.white = [255,255,255]
        # self.black = [0,0,0]
        # self.red = [255,0,0]
        # self.green = [0,255,0]
        # self.blue = [0,0,255]

        #limites em HSV - vermelho, azul, verde, amarelo
        self.boundaries = [
            ((0, 100, 58), (12, 255, 255), (0,0,255)),
            ((94, 77, 42), (122, 255, 255), (255,0,0)),
            ((31, 89, 38), (82, 255, 255), (0,255,0)),
            ((19, 115, 120), (45, 255, 255), (0,255,255))
        ]

        self.teclado = []
        self.teclado_coord = []
        self.teclado_roi = []
        self.controles = []
        self.controles_coord = []
        self.controles_roi = []
        self.slide = []
        self.slide_roi = None

    def teste(self):
        while True:
            _, frame = self.cap.read()
            _, frame = self.cap.read()
            frame = cv2.flip(frame, 0)
            frame = cv2.flip(frame, 1)
            frame = imutils.resize(frame, width=900)

            # resize the frame, blur it, and convert it to the HSV
            # color space
            # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            low, high, _ = self.boundaries[0]

            mask = cv2.inRange(hsv,low, high)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)
            cv2.rectangle(frame,(100, 200), (800,400), (0,0,0), 2)

            cv2.imshow("teste", frame)
            cv2.imshow("mask", mask)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

    def achaCores(self):
        
        ret, fram = self.cap.read()
        ret, fram = self.cap.read()
        if not ret:
            raise Exception("Não capturou imagem")
        fram = cv2.flip(fram,0)
        fram = cv2.flip(fram, 1)
        fram = imutils.resize(fram, width=900)
        frame = copy(fram)
        frame = cv2.blur(frame,(5,5))


        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        heigh, width, depth = frame.shape

        cv2.imshow("original",fram)
        cv2.waitKey(0)

        for (lower, upper, color) in self.boundaries:

            # find the colors within the specified boundaries and apply
            # the mask
            mask = cv2.inRange(hsv, lower, upper)
            mask = cv2.erode(mask, None, iterations=3)
            mask = cv2.dilate(mask, None, iterations=3)
            output = cv2.bitwise_and(frame, frame, mask=mask)

            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            center = None

            if len(cnts) > 0:
                for fig in cnts:
                    ((x, y), radius) = cv2.minEnclosingCircle(fig)
                    M = cv2.moments(fig)
                    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                    if radius > 10 and radius < 25:
                        # draw the circle and centroid on the frame,
                        # then update the list of tracked points
                        cv2.circle(frame, (int(x), int(y)), int(radius), color, 2)
                        cv2.circle(frame, center, 2, (255,255,255), -1)
                        if color == (0,0,255):
                            self.teclado.append(center)
                        if color == (255,0,0):
                            self.slide.append(center)
                        if color == (0,255,0):
                            self.controles.append(center)
            # show the images
        if len(self.teclado) == 2:
            x_ant = self.teclado[1][0]
            for x in range(self.teclado[1][0]+int(abs(self.teclado[0][0] - self.teclado[1][0])/12), self.teclado[0][0] + 10 , int(abs(self.teclado[0][0] - self.teclado[1][0])/12)):
                cv2.rectangle(frame,(x_ant, self.teclado[1][1]), (int(x), self.teclado[0][1]), (100,100,100), 2)
                self.teclado_coord.append((self.teclado[1][1] + 70, self.teclado[1][1] + 150, x_ant + 3 , x - 3))
                cv2.imshow("tecla",frame[self.teclado[1][1] + 70: self.teclado[1][1] + 150, x_ant + 3 : x - 3])
                cv2.waitKey(0)
                x_ant = int(x)
        else:
            print("Erro: Sem coordenadas de teclado")
        if len(self.controles) == 2:
            x_ant = self.controles[1][0]
            for x in range(self.controles[1][0]+int(abs(self.controles[0][0] - self.controles[1][0])/4), self.controles[0][0]  , int(abs(self.controles[0][0] - self.controles[1][0])/4)):
                cv2.rectangle(frame,(x_ant, self.controles[1][1]), (int(x), self.controles[0][1]), (100,100,100), 2)
                self.controles_coord.append((self.controles[1][1] + 20, self.controles[0][1] - 20, x_ant + 3, x - 3))
                x_ant = int(x)
        else:
            print("Erro: Sem coordenadas de controles")
        if len(self.slide) == 2:
            cv2.rectangle(frame, self.slide[1], self.slide[0], (100,100,100), 2)
        else:
            print("Erro: Sem coordenadas de slide")
        cv2.imshow("images", frame)
        if cv2.waitKey(0) & 0xFF == ord('r'):
            cv2.destroyAllWindows()
            self.conf()
        else:
            for (y1, y2, x1, x2) in self.teclado_coord:
                self.teclado_roi.append(cv2.mean(cv2.cvtColor(frame[y1:y2,x1:x2],cv2.COLOR_BGR2GRAY))[0])
            for (y1,y2,x1,x2) in self.controles_coord:
                self.controles_roi.append(cv2.mean(cv2.cvtColor(frame[y1:y2, x1:x2], cv2.COLOR_BGR2GRAY))[0])
            cv2.destroyAllWindows()

    def release(self):
        self.cap.release()
        del self

    def conf(self):
        self.teste()
        self.achaCores()

    def teclas(self):
        ret, fram = self.cap.read()
        ret, fram = self.cap.read()
        fram = cv2.flip(fram, 0)
        fram = cv2.flip(fram, 1)
        if not ret:
            raise Exception("Não capturou imagem")
        fram = imutils.resize(fram, width=900)
        frame = copy(fram)
        frame = cv2.blur(frame, (5, 5))

        saida_tec = np.zeros(12)
        saida_con = np.zeros(4)
        i = 0
        for (y1, y2, x1, x2) in self.teclado_coord:
            media = cv2.mean(cv2.cvtColor(frame[y1:y2, x1:x2], cv2.COLOR_BGR2GRAY))[0]
            if self.teclado_roi[i] - 20 > media:
                saida_tec[i] = 1
            else:
                saida_tec[i] = 0
            #self.teclado_roi[i] = media
            i += 1

        i=0
        for (y1, y2, x1, x2) in self.controles_coord:
            media = cv2.mean(cv2.cvtColor(frame[y1:y2, x1:x2], cv2.COLOR_BGR2GRAY))[0]
            if media < self.controles_roi[i] - 20 :
                saida_con[i] = 1
            else:
                saida_con[i] = 0
            # self.controles_roi[i] = media
            i += 1

        cv2.imshow("play", frame)
        return saida_tec, saida_con




