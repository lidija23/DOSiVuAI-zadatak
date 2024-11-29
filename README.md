## Writeup Template

**Lane Finding Project**


### Writeup / README

#### 1. Provide a Writeup that includes all the rubric points and how you addressed each one.


For the initial run of the program, you should keep the video processing function call commented out, ensuring that all the images are processed correctly. After that, uncomment the function call #detect_edges_in_videos(video_dir, result_video_dir, mtx, dist) on the last line of the main function so that the program processes all the output videos. Keep in mind that with this change, the execution time of the program will be significantly longer.

### Camera Calibration

#### 1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.
This function implements the camera calibration process using a chessboard pattern. First, the chessboard parameters (number of rows and columns) and criteria for
precise corner detection are defined. Then, 3D coordinates of the corners on the board are generated. In the calibrate_camera function, images with the chessboard areloaded, converted to grayscale, and cv2.findChessboardCorners is used to find the corners. Once the corners are detected, cv2.cornerSubPix is applied to further refine them, and the 2D and corresponding 3D points are added to lists. These points are used to calculate the camera parameters (camera matrix and distortion) using cv2.calibrateCamera. The function returns the camera matrix and distortion, which are then used for undistorting images in the undistort_image function. The undistort_image function corrects image distortion using the provided camera matrix and distortion coefficients.

### Pipeline (single images)

#### 1. Provide an example of a distortion-corrected image.

In folder undistort is example.

#### 2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.

The binarna_slika.py/binary_image function uses several techniques to create a binary image with color and edge detection. First, the image is converted to the HSV color space, which makes it easier to identify specific colors like yellow and white using the cv2.inRange function to create binary masks. These masks are then combined using a bitwise OR operation. Next, Gaussian blur is applied to the combined mask to remove noise, followed by the use of the Canny edge detector to extract edges from the image. The result is a binary image with white pixels where edges of yellow and white objects are detected, and black pixels in the rest of the image. An example of the output from this function is saved in the binary_image_dir folder.

#### 3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

The transformation.py/generate_points function calculates the source (src) and destination (dst) points for a perspective transformation, based on the image size (img_size) and optional parameters such as offset and vertical_shift. The source points are selected from the center and bottom corners of the original image, defining the region to be transformed, while the destination points specify where the source points will be mapped in the transformed image, typically into a rectangular shape. The cv2.getPerspectiveTransform function is then used to compute a perspective matrix, which defines how the source points should be mapped to the destination points. The cv2.warpPerspective function applies this matrix to the original image, resulting in a new image that has been warped to the desired perspective.

#### 4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?

The lane pixels are found using a sliding window approach using the lines.py/fit_lane_lines function. First, the histogram helps locate the starting points of the left and right lanes. Then, the windows are slid down the image to find the lane pixels, adjusting the window positions based on the detected pixels. After collecting the lane pixels, a polynomial is used to fit the lane lines. This yields the equations for the left and right lanes, which are the output of the function.

#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

To find the radius of curvature of the lane and the position of the vehicle relative to the center of the lane, I first identify the lane positions using polynomial fitting or similar methods. To calculate the radius of curvature, I use quadratic polynomials for both lanes, which gives x values ​​at the height of the image. Then I apply the curvature formula based on the coefficients of the polynomial to calculate the curvature at the bottom of the image. For the vehicle position, I find the midpoint between the left and right lanes at the bottom and compare it to the center of the image to calculate the vehicle displacement in meters. I do this in the function lines.pj/compute_lane_curvature.

#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

The resulting images are saved in the result_images folder.

### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).


The output folder for processed videos is set to result_videos. However, the program encounters a crash when attempting to process the video file challenge03.mp4.

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

One of the main challenges in this project was accurately detecting lane lines with significant curvature. The pipeline often struggled to fit polynomial curves to the lane lines when the road had sharp turns, leading to inaccurate lane overlays and incorrect curvature calculations. Additionally, it fails to process videos with very sharp curves, such as challenge03.mp4, where the lane detection becomes unreliable. To improve the pipeline, I could fine-tune the parameters for lane detection, such as adjusting the thresholds for binarization or modifying the region of interest to better capture curved lanes. Another potential improvement would be to smooth the detected lane positions across multiple frames, which could help reduce errors in detecting sharp curves.

