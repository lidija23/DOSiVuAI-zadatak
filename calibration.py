import numpy as np
import cv2
import glob
import numpy as np
import cv2
import glob


# Parametri sahovske table
ROWS = 6
COLS = 9


CRITERIA = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# 3D koordinate
def generate_object_points(rows, cols):
    object_points = np.zeros((rows * cols, 3), np.float32)
    object_points[:, :2] = np.mgrid[0:cols, 0:rows].T.reshape(-1, 2)
    return object_points


OBJECT_POINTS = generate_object_points(ROWS, COLS)

# Kalibracija kamere 
def calibrate_camera():
    object_points_array = []  # 3D koordinate
    image_points_array = []   # 2D koordinate

    image_paths = glob.glob('camera_cal/calibration*.jpg')
    
    # Prolazak kroz slike
    for path in image_paths:
        img = cv2.imread(path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Pronalazenje uglova 
        ret, corners = cv2.findChessboardCorners(gray, (COLS, ROWS), None)
        if ret:
            
            refined_corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), CRITERIA)

            object_points_array.append(OBJECT_POINTS)
            image_points_array.append(refined_corners)

            
            img_with_corners = cv2.drawChessboardCorners(img, (COLS, ROWS), refined_corners, ret)
           

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
        object_points_array, image_points_array, gray.shape[::-1], None, None
    )
    
    total_error = compute_calibration_error(
        object_points_array, image_points_array, rvecs, tvecs, mtx, dist
    )

    return mtx, dist

def compute_calibration_error(object_points_array, image_points_array, rvecs, tvecs, mtx, dist):
    total_error = 0
    for i in range(len(object_points_array)):
        img_points, _ = cv2.projectPoints(object_points_array[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv2.norm(image_points_array[i], img_points, cv2.NORM_L2) / len(img_points)
        total_error += error
    return total_error / len(object_points_array)



def undistort_image(img, camera_matrix, distortion_coeffs):
   
    if img is None:
        raise ValueError("Slika nije ucitana")
    
    if not isinstance(camera_matrix, np.ndarray) or not isinstance(distortion_coeffs, np.ndarray):
        raise TypeError("Matrica i koeficijenti nisu validni")

    undistorted = cv2.undistort(img, camera_matrix, distortion_coeffs, None, camera_matrix)
    
    return undistorted


