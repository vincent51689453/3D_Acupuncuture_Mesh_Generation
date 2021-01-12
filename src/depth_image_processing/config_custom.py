"""
------------------------- Colormap Configuration -------------------------

1. doi : distance of interest in [cm]
It is indicating the range of distance that will be included in the color map. 
If d >= doi, they will be treated as the same color in the map. 
The map will only conisder < doi.

2. alpha_map : parameter for cv2.convertScaleAbs(depth_image, alpha=??)  in [mm]
This parameter represents the conversion from doi to alpha of cv2.convertScaleAbs.
In, cv2. convertScaleAbs, valid_distance*alpha = 255.
"""
doi = 43
alpha_map = 255 / (doi*10)


"""
------------------------- Image Caputre Configuration -------------------------
1. img_width  : number of horizontal pixels
2. img_height : number of vertical pixels
3. fps        : frame per second
"""
img_width = 640
img_height = 480
fps = 30


"""
------------------------- Detection Configuration -------------------------
1. shaddow_hsv_L : shaddows color of depth image after HSV conversion (lower limit)
2. shaddow_hsv_H : shaddows color of depth image after HSV conversion (upper limit)
"""
shaddow_hsv_L = [118, -10, -40]
shaddow_hsv_H = [138, 10, 40]