import pyrealsense2 as rs
import numpy as np
import cv2
import config_custom as setup
import processing

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, setup.img_width, setup.img_height, rs.format.z16, setup.fps)
config.enable_stream(rs.stream.color, setup.img_width, setup.img_height, rs.format.bgr8, setup.fps)

# Start streaming
pipeline.start(config)

# Mouse Click Event for depth_color_map
def color_info(event,x,y,flag,param):
    if event == cv2.EVENT_LBUTTONDOWN:  
        pixel = depth_colormap[y,x]
        upper_limit = np.array([pixel[0] + 10, pixel[1] + 10, pixel[2] + 40])
        lower_limit = np.array([pixel[0] - 10, pixel[1] - 10, pixel[2] - 40])
        print("HSV Pixel:",pixel)
        print("Lower_Limit: ",lower_limit)
        print("Upper_Limit: ",upper_limit)
        print('\n')
        #Display the masking result of the threshold value
        image_mask = cv2.inRange(depth_colormap,lower_limit,upper_limit)
        cv2.imshow("Mask",image_mask)

try:
    while True:

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=setup.alpha_map), cv2.COLORMAP_JET)

        # Find the shaddow of the objects in depth colormap


        # Stack both images horizontally
        images = np.hstack((color_image, depth_colormap))

        # Show images
        cv2.namedWindow('Raw VS Result', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('Raw VS Result', images)

        # New window for mouse click
        # cv2.imshow ('Depth:',depth_colormap)
        # cv2.setMouseCallback('Depth:',color_info)  

        key = cv2.waitKey(1)

        # Press esc or 'q' to close the image window
        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break

finally:
    # Stop streaming
    pipeline.stop()