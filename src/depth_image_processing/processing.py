import cv2
import numpy 

def find_shaddow(img_depth,img_raw,color_L,color_H):
    #TO-DO
    image_mask = cv2.inRange(img_depth,color_L,color_H)
    image_contour,contours,hierarchy = cv2.findContours(image_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    img_output = cv2.drawContours(img_raw, contours,-1,(0,255,0),3)
    return 0
