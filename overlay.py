import cv2
import numpy as np
from lines import compute_lane_curvature

def overlay_lane_on_image(warped_binary, original_image, left_poly, right_poly, inverse_matrix):

    vertical_pixels = np.arange(warped_binary.shape[0])
    
    left_lane_x = left_poly[0] * vertical_pixels**2 + left_poly[1] * vertical_pixels + left_poly[2]
    right_lane_x = right_poly[0] * vertical_pixels**2 + right_poly[1] * vertical_pixels + right_poly[2]
    
    blank_image = np.zeros_like(warped_binary).astype(np.uint8)
    color_image = np.dstack((blank_image, blank_image, blank_image))
    
    left_points = np.vstack((left_lane_x, vertical_pixels)).T
    right_points = np.flipud(np.vstack((right_lane_x, vertical_pixels)).T)

    # Kombinovanje leve i desne tačke u jedan niz za popunjavanje
    polygon_points = np.hstack((left_points, right_points))
    polygon_points = polygon_points.reshape((-1, 1, 2))
    polygon_points = polygon_points.astype(np.int32)
    
    # Popunjavanje slike sa prepoznatim trakom
    cv2.fillPoly(color_image, [polygon_points], (0, 255, 0))

    # Projekcija punog traka natrag u originalnu sliku pomoću inverzne matrice
    warped_image = cv2.warpPerspective(color_image, inverse_matrix, (original_image.shape[1], original_image.shape[0]))
    
    # Kombinovanje originalne slike sa projektovanim trakom
    final_image = cv2.addWeighted(original_image, 1, warped_image, 0.3, 0)

    # Računanje pozicije vozila (vehicle offset)
    center_of_image = original_image.shape[1] // 2
    
    # Srednja tačka između leve i desne trake na dnu slike
    middle_of_lanes = (left_poly[0] * 0**2 + left_poly[1] * 0 + left_poly[2] + right_poly[0] * 0**2 + right_poly[1] * 0 + right_poly[2]) / 2
    
    # Izračunavanje pomeraja vozila u odnosu na centar
    vehicle_offset = center_of_image - middle_of_lanes
    
    # Prikazivanje pozicije vozila na slici
    cv2.putText(final_image, f"Vehicle Offset: {vehicle_offset:.2f}m", 
                (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    left_curvature, right_curvature, vehicle_offset = compute_lane_curvature(warped_binary, left_poly, right_poly)
    
    # Prikazivanje radijusa krivine za levo i desno vozilo
    cv2.putText(final_image, f"Left Curvature: {left_curvature:.2f}m", 
                (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(final_image, f"Right Curvature: {right_curvature:.2f}m", 
                (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    return final_image
