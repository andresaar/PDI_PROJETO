from camera import Camera
import cv2
import mido

cap = Camera(0)
isTeclas = [False] * 12
isControler = [False] * 4
e_do = [60,62,64,65,67,69,71,72,74,76,77,79]
names = mido.get_output_names()
print(names)
output = mido.open_output(names[2])

cap.conf()
print(cap.teclado_roi)
while True:
    teclas, controler = cap.teclas()
    for i in range(len(teclas)):
        if teclas[i] == 0:
            output.send(mido.Message('note_off', note=e_do[i], velocity=0))
            isTeclas[i] = False
        else:
            if not isTeclas[i]:
                output.send(mido.Message('note_on', note=e_do[i], velocity=64))
            isTeclas[i] = True
        for i in range(len(controler)):
            if controler[i] == 0:
                output.send(mido.Message('control_change', control=i, value=0))
                isControler[i] = False
            else:
                if not isControler[i]:
                    output.send(mido.Message('control_change', control=i, value=1))
                isControler[i] = True

    if cv2.waitKey(1000) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break


cap.release()