import cv2
import numpy as np
ri, gi, bi = 0,0,0
rs, gs, bs = 1,1,1

def setri(rn):
    global ri
    ri = rn
    apply()

def setgi(gn):
    global gi
    gi = gn
    apply()

def setbi(bn):
    global bi
    bi = bn
    apply()


def setrs(rn):
    global rs
    rs = rn
    apply()


def setgs(gn):
    global gs
    gs = gn
    apply()


def setbs(bn):
    global bs
    bs = bn
    apply()

def apply():
    global ri,gi,bi,rs,gs,bs, imagem
    lower = [bi,gi,ri]
    upper = [bs,gs,rs]
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")

    # find the colors within the specified boundaries and apply
    # the mask
    mask = cv2.inRange(imagem, lower, upper)
    output = cv2.bitwise_and(imagem, imagem, mask=mask)

    # show the images
    cv2.imshow("limites", np.hstack([imagem, output]))

imagem = cv2.imread("acha limites.png")
cv2.imshow("limites", np.hstack([imagem,imagem]))
trackbarName = "Ri"
cv2.createTrackbar(trackbarName,"limites",ri,255,setri)
trackbarName = "Gi"
cv2.createTrackbar(trackbarName,"limites",gi,255,setgi)
trackbarName = "Bi"
cv2.createTrackbar(trackbarName,"limites",bi,255,setbi)
trackbarName = "Rs"
cv2.createTrackbar(trackbarName,"limites",rs,255,setrs)
trackbarName = "Gs"
cv2.createTrackbar(trackbarName,"limites",gs,255,setgs)
trackbarName = "Bs"
cv2.createTrackbar(trackbarName,"limites",bs,255,setbs)

cv2.waitKey(0)
cv2.destroyAllWindows()
