from camera import Camera
import cv2

cap = Camera(0)

cap.conf()
print(cap.teclado_roi)
while True:
    print(cap.teclas())
    if cv2.waitKey(500) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break


cap.release()