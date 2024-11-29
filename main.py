import cv2
import numpy as np
import os
from calibration import calibrate_camera, undistort_image
from transformation import warp_binary_image
from binarna_slika import binary_image
from overlay import overlay_lane_on_image
from lines import fit_lane_lines, compute_lane_curvature
from video import detect_edges_in_videos
import warnings


# Funkcija za učitavanje slike i njenu distorziju
def load_and_undistort_image(image_path, mtx, dist):
    image = cv2.imread(image_path)
    return undistort_image(image, mtx, dist)

# Funkcija za snimanje slika u direktorijum
def save_image(image, directory, image_name, prefix=""):
    if not os.path.exists(directory):
        os.makedirs(directory)
    cv2.imwrite(os.path.join(directory, f'{prefix}{image_name}'), image)

# Funkcija koja obavlja proces učenja i primene kalibracije kamere
def calibrate_and_undistort():
    mtx, dist = calibrate_camera()
    calibration_image = 'camera_cal/calibration1.jpg'
    undistorted_img = load_and_undistort_image(calibration_image, mtx, dist)
    save_image(undistorted_img, './undistort', 'calibration1_undistort.jpg')
    return mtx, dist

# Funkcija koja obavlja binarnu sliku i transformaciju perspektive za svaku sliku
def process_image(image, mtx, dist, image_name):
    undistorted_img = undistort_image(image, mtx, dist)
    binary_img = binary_image(undistorted_img)

    # Spremanje binarne slike
    save_image(binary_img, binary_image_dir, image_name, prefix="binary_")
    
    # Perspektivna transformacija
    warped_img, M, Minv = warp_binary_image(binary_img)
    
    # Spremanje transformisane slike
    save_image(warped_img, warper_image_dir, image_name, prefix="warped_")
    
    # Nalazenje i crtamo linije sa fitovanjem
    left_fit, right_fit = fit_lane_lines(warped_img)

    # Prebacivanje rezultata na originalnu sliku
    result_img = overlay_lane_on_image(warped_img, image, left_fit, right_fit, Minv)
    
    return result_img


if __name__ == "__main__":
    mtx, dist = calibrate_and_undistort()
    
    image_dir = './test_images/'
    result_image_dir = './result_images/'
    binary_image_dir = './binary_image/'
    warper_image_dir = './warper/'
    video_dir= './test_videos/'
    result_video_dir = './result_videos/'

    # Obrada svih slika u testnom direktorijumu
    for image_name in os.listdir(image_dir):
        image_path = os.path.join(image_dir, image_name)
        image = cv2.imread(image_path)
        
        result_image = process_image(image, mtx, dist, image_name)

        # Snimanje rezultata
        save_image(result_image, result_image_dir, image_name, prefix="result_")

        # SNIMANJE VIDEA-SKLONITI KOMENTAR LINIJE ISPOD.
        #detect_edges_in_videos(video_dir, result_video_dir, mtx, dist)
