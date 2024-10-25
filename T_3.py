import cv2
import numpy as np

# Checkerboard dimensions viz. the number of internal corners
CHECKERBOARD = (13, 9)  

# The points in world coordinates of the checkerboard
wp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
wp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)

# Arrays to store object points and image points from all frames
w_points = []  # 3d points in world coordinates
i_points = []  # 2d points in image coordintes

# Define termination criterion for opencv's corner detector(cornerSubPix)
# The max iterations and accuracy threshold are specified
criteria = (cv2.TERM_CRITERIA_MAX_ITER+ cv2.TERM_CRITERIA_EPS, 30, 0.001)


# Funtion to calculate the reprojection error to evaluate the calibration accuracy.
def calculate_reprojection_error(object_points, image_points, rvecs, tvecs, camera_matrix, dist_coeffs):
    total_error = 0
    total_points = 0
    for i in range(len(object_points)):
        imgpoints2, _ = cv2.projectPoints(object_points[i], rvecs[i], tvecs[i], camera_matrix, dist_coeffs)
        error = cv2.norm(image_points[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
        total_error += error
        total_points += len(imgpoints2)
    return total_error / total_points

cap = cv2.VideoCapture(0)

prev_error = float('inf')
min_change_threshold = 1e-5  # minimal error for convergence
calibrated = False # Flag indicating calibration status

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Find the chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)

    if ret:
        # Refine corner positions for more accurate calibration
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

        # Save the points
        w_points.append(wp)
        i_points.append(corners2)

        # Draw the corners for visualization
        cv2.drawChessboardCorners(frame, CHECKERBOARD, corners2, ret)

        # Calibrate the camera with the world and image points collected
        ret, intrinsics, dist_coeffs, rotv, transv = cv2.calibrateCamera(w_points, i_points, gray.shape[::-1], None, None)

        reprojection_error = calculate_reprojection_error(w_points, i_points, rotv, transv, intrinsics, dist_coeffs)

        # Check if the reprojection error during each frame is converging to a constant minimum
        if abs(prev_error - reprojection_error) < min_change_threshold:
            calibrated = True
            print("Calibration complete. Reprojection error stabilized.")
        else:
            prev_error = reprojection_error

    cv2.imshow('Calibration', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Print final calibration parameters
if calibrated:
    print("Final camera matrix:\n", np.round(intrinsics, 4))
    print("Distortion coefficients:\n", np.round(dist_coeffs, 4))
    print(f"Final reprojection error: {reprojection_error}")

    # Save intrinsic parameters to a text file for readability for documentation
    # Save to a single text file with a simpler format
    with open("close_camera_parameters.txt", "w") as f:
        f.write("Camera Matrix:\n")
        np.savetxt(f, intrinsics, fmt='%.4f')
        f.write(" \n")
        f.write("Distortion Coefficients:\n")
        np.savetxt(f, dist_coeffs, fmt='%.4f')

    # Save intrinsic parameters to a array file
    np.savez("close_camera_calibration.npz", camera_matrix=intrinsics, distortion_coeffs=dist_coeffs, rvecs=rotv, tvecs=transv)
    print("Camera calibration parameters saved to 'camera_calibration.npz'.")
