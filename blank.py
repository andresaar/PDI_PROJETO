from camera import Camera
import numpy as np
import cv2
import mido

cap = Camera(0)
isTeclas = [False] * 12
isControler = [False] * 4
e_do = [60,62,64,65,67,69,71,72,74,76,77,79]
e_dos = np.add(e_do,1)
e_re = np.add(e_dos,1)
e_res = np.add(e_re,1)
e_mi = np.add(e_res,1)
e_fa = np.add(e_mi,1)
e_fas = np.add(e_fa,1)
e_sol = np.add(e_fas,1)
e_sols = np.add(e_sol,1)
e_la = np.add(e_sols,1)
e_las = np.add(e_la,1)
e_si = np.add(e_las,1)

escalas = [e_do,e_dos,e_re,e_res,e_mi,e_fa,e_fas,e_sol,e_sols,e_la,e_las,e_si]
n_escalas = ["C/Am", "C#/A#m", "D/Bm", "D#/Cm", "E/C#m", "F/Dm", "F#/D#m", "G/Em", "G#/Fm", "A/F#m", "A#/Gm", "B/G#m"]
escala = e_do
x=0

text = np.ones([70,100])*255

def mudaEscala(i):
    global escala
    escala = escalas[i]
    text = np.zeros([100, 300],dtype=np.uint8)
    cv2.putText(text,n_escalas[i],(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
    cv2.imshow("Escala", text)

names = mido.get_output_names()
print(names)
output = mido.open_output(names[2])

cap.conf()
print(cap.teclado_roi)

mudaEscala(0)
cv2.createTrackbar("Escala", "Escala", 0, 11, mudaEscala)

while True:
    teclas, controler = cap.teclas()
    for i in range(len(teclas)):
        if teclas[i] == 0:
            output.send(mido.Message('note_off', note=escala[i], velocity=0))
            isTeclas[i] = False
        else:
            if not isTeclas[i]:
                output.send(mido.Message('note_on', note=escala[i], velocity=64))
            isTeclas[i] = True
        for i in range(len(controler)):
            if controler[i] == 0:
                output.send(mido.Message('control_change', control=i, value=0))
                isControler[i] = False
            else:
                if not isControler[i]:
                    output.send(mido.Message('control_change', control=i, value=1))
                isControler[i] = True

    if cv2.waitKey(30) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break


cap.release()