import pyrealsense2 as rs
import numpy as np
import cv2

#設定深度影像與RGB影像串流
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# 開始影像串流
pipeline.start(config)

try:
    while True:
        # 讀取一個完整深度、顏色的Frame
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue

        # 將影像轉換為Numpy陣列
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # 將深度影像應用為一般影像(必須將影像轉換為每像素8位元)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        # 水平堆疊兩個影像(RGB影像與深度影像)
        images = np.hstack((color_image, depth_colormap))

        # 顯示影像
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)
        cv2.waitKey(1)

finally:

    # 關閉影像串流
    pipeline.stop()
