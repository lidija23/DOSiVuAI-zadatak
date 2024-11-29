import numpy as np
import cv2

def generate_points(img_size, offset=55, vertical_shift=100):
  
    center_x = img_size[0] / 2
    center_y = img_size[1] / 2
    sixth_x = img_size[0] / 6
    third_x = img_size[0] / 4
    three_fourth_x = img_size[0] * 3 / 4
    full_height = img_size[1]

    # Računanje src tačaka
    src = np.float32([
        [center_x - offset, center_y + vertical_shift],           # Središnja tačka sa offset-om
        [sixth_x - 10, full_height],                             # Levo donje
        [three_fourth_x + offset, full_height],                  # Desno donje
        [center_x + offset, center_y + vertical_shift]           # Središnja tačka sa offset-om
    ])

    # Računanje dst tačaka
    dst = np.float32([
        [third_x, 0],                                            # Levo gornje
        [third_x, full_height],                                   # Levo donje
        [three_fourth_x, full_height],                            # Desno donje
        [three_fourth_x, 0]                                       # Desno gornje
    ])

    return src, dst

def warp_binary_image(input_image, shift_x=55, shift_y=100):
 
    image_dimensions = (input_image.shape[1], input_image.shape[0])
    
    # Generisanje tačaka
    points_src, points_dst = generate_points(image_dimensions, shift_x, shift_y)
    
    # Kreiranje transformacionih matrica
    perspective_matrix = cv2.getPerspectiveTransform(points_src, points_dst)
    inverse_perspective_matrix = cv2.getPerspectiveTransform(points_dst, points_src)
    
    # Primena perspektivne transformacije
    transformed_image = cv2.warpPerspective(input_image, perspective_matrix, image_dimensions, flags=cv2.INTER_NEAREST)
    
    return transformed_image, perspective_matrix, inverse_perspective_matrix
