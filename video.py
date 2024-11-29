import os
import cv2
from calibration import undistort_image
from transformation import warp_binary_image
from binarna_slika import binary_image
from overlay import overlay_lane_on_image
from lines import fit_lane_lines

def detect_edges_in_videos(input_folder, output_folder, mtx, dist):
 
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for video_name in os.listdir(input_folder):
        input_video_path = os.path.join(input_folder, video_name)
        output_video_path = os.path.join(output_folder, f"processed_{video_name}")

        
        cap = cv2.VideoCapture(input_video_path)
        if not cap.isOpened():
            print(f"Cannot open video: {input_video_path}")
            continue

       
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)

       
        out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'XVID'), fps, (frame_width, frame_height))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            
            processed_frame = process_video_frame(frame, mtx, dist)  

            out.write(processed_frame)

        
        cap.release()
        out.release()

    cv2.destroyAllWindows()

def process_video_frame(frame, mtx, dist):
   
    # 1. Uklanjanje distorzije
    undistorted_frame = undistort_image(frame, mtx, dist)

    # 2. Kreiranje binarne slike
    binary_frame = binary_image(undistorted_frame)

    # 3. Perspektivna transformacija
    warped_frame, M, Minv = warp_binary_image(binary_frame)

    # 4. Fitting lane lines
    left_fit, right_fit = fit_lane_lines(warped_frame)

    # 5. Overlay traka na sliku
    result_frame = overlay_lane_on_image(warped_frame, undistorted_frame, left_fit, right_fit, Minv)

    return result_frame

def detect_edges_in_videos(input_folder, output_folder, mtx, dist):
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    
    for video_name in os.listdir(input_folder):
        input_video_path = os.path.join(input_folder, video_name)
        output_video_path = os.path.join(output_folder, f"processed_{video_name}")
       
        cap = cv2.VideoCapture(input_video_path)
        if not cap.isOpened():
            print(f"Cannot open video: {input_video_path}")
            continue

        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'XVID'), fps, (frame_width, frame_height))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            processed_frame = process_video_frame(frame, mtx, dist)

            
            out.write(processed_frame)

        
        cap.release()
        out.release()

    cv2.destroyAllWindows()

