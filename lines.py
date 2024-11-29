import numpy as np
import cv2
from scipy import interpolate
from sklearn.linear_model import RANSACRegressor

def fit_lane_lines(binary_input, method="polynomial"):
  
    lane_hist = np.sum(binary_input[binary_input.shape[0] // 2:, :], axis=0)
    
    mid_point = len(lane_hist) // 2
    left_start = np.argmax(lane_hist[:mid_point])
    right_start = np.argmax(lane_hist[mid_point:]) + mid_point
    
    total_windows = 9
    window_height = binary_input.shape[0] // total_windows

    active_pixels = binary_input.nonzero()
    y_coords = np.array(active_pixels[0])
    x_coords = np.array(active_pixels[1])
    
    left_pos = left_start
    right_pos = right_start
    
    search_margin = 100
    min_pixels_per_window = 50
    
    left_lane_pixels = []
    right_lane_pixels = []
    
    for step in range(total_windows):
        y_min = binary_input.shape[0] - (step + 1) * window_height
        y_max = binary_input.shape[0] - step * window_height
        
        x_left_min = left_pos - search_margin
        x_left_max = left_pos + search_margin
        x_right_min = right_pos - search_margin
        x_right_max = right_pos + search_margin
        
        left_window_pixels = ((y_coords >= y_min) & (y_coords < y_max) & 
                              (x_coords >= x_left_min) & (x_coords < x_left_max)).nonzero()[0]
        right_window_pixels = ((y_coords >= y_min) & (y_coords < y_max) & 
                               (x_coords >= x_right_min) & (x_coords < x_right_max)).nonzero()[0]
        
        left_lane_pixels.append(left_window_pixels)
        right_lane_pixels.append(right_window_pixels)
        
        if len(left_window_pixels) > min_pixels_per_window:
            left_pos = np.mean(x_coords[left_window_pixels]).astype(int)
        if len(right_window_pixels) > min_pixels_per_window:
            right_pos = np.mean(x_coords[right_window_pixels]).astype(int)
    
    left_lane_pixels = np.concatenate(left_lane_pixels)
    right_lane_pixels = np.concatenate(right_lane_pixels)
    
    
    left_x = x_coords[left_lane_pixels]
    left_y = y_coords[left_lane_pixels]
    right_x = x_coords[right_lane_pixels]
    right_y = y_coords[right_lane_pixels]
    
    if method == "polynomial":
        left_fit = np.polyfit(left_y, left_x, 2)
        right_fit = np.polyfit(right_y, right_x, 2)
    elif method == "linear":
        left_fit = np.polyfit(left_y, left_x, 1)
        right_fit = np.polyfit(right_y, right_x, 1)
    elif method == "b_splines":
        left_spline = interpolate.BSpline(left_y, left_x, k=3, t=left_y[::len(left_y) // 10])
        right_spline = interpolate.BSpline(right_y, right_x, k=3, t=right_y[::len(right_y) // 10])
        left_fit = left_spline
        right_fit = right_spline
    elif method == "ransac":
        ransac_left = RANSACRegressor()
        ransac_right = RANSACRegressor()
        ransac_left.fit(left_y.reshape(-1, 1), left_x)
        ransac_right.fit(right_y.reshape(-1, 1), right_x)
        left_fit = ransac_left.estimator_.coef_[0], ransac_left.estimator_.intercept_
        right_fit = ransac_right.estimator_.coef_[0], ransac_right.estimator_.intercept_
    
    return left_fit, right_fit


def compute_lane_curvature(binary_img, left_fit, right_fit, method="polynomial"):
    height = binary_img.shape[0]
    y_values = np.linspace(0, height - 1, height)


    if method in ["polynomial", "linear"]:
        left_x_vals = left_fit[0] * y_values**2 + left_fit[1] * y_values + left_fit[2] if method == "polynomial" else left_fit[0] * y_values + left_fit[1]
        right_x_vals = right_fit[0] * y_values**2 + right_fit[1] * y_values + right_fit[2] if method == "polynomial" else right_fit[0] * y_values + right_fit[1]
    elif method == "b_splines":
        left_x_vals = left_fit(y_values)
        right_x_vals = right_fit(y_values)

    # Konverzija iz piksela u metre
    y_to_m = 30 / 720  # metri po pikselu vertikalno 
    x_to_m = 3.7 / 700  # metri po pikselu horizontalno 

    # Konvertovanje piksela u metre za fitovanje traka
    left_fit_meters = np.polyfit(y_values * y_to_m, left_x_vals * x_to_m, 2)
    right_fit_meters = np.polyfit(y_values * y_to_m, right_x_vals * x_to_m, 2)

    y_max = np.max(y_values)

    # Zakrivljenost leve trake
    left_curvature = ((1 + (2 * left_fit_meters[0] * y_max * y_to_m + left_fit_meters[1])**2)**1.5) / abs(2 * left_fit_meters[0])

    # Zakrivljenost desne trake
    right_curvature = ((1 + (2 * right_fit_meters[0] * y_max * y_to_m + right_fit_meters[1])**2)**1.5) / abs(2 * right_fit_meters[0])

    
    center_position = (left_x_vals[-1] + right_x_vals[-1]) / 2  # Središnja tačka traka na dnu slike
    image_center = binary_img.shape[1] / 2  # Centar slike (horizontalna sredina)

    # Pozicija vozila u odnosu na centar slike (pozitivno ili negativno pomerenje)
    vehicle_offset = (center_position - image_center) * x_to_m  # U metrima

    return left_curvature, right_curvature, vehicle_offset
