import numpy as np
import cv2 as cv
from pyapriltags import Detector
import time

# Load camera parameters from npz file
calibration_data = np.load('close_camera_calibration.npz')  # Adjust the filename as necessary

# Assuming the file contains 'camera_matrix' and 'dist_coeffs'
camera_matrix = calibration_data['camera_matrix']
dist_coeffs = calibration_data['distortion_coeffs']

# Define a cube's vertices (8 points)
cube_size = 0.05  # Size of the cube
cube_vertices = np.array([
    [-cube_size, -cube_size, 0],
    [cube_size, -cube_size, 0],
    [cube_size, cube_size, 0],
    [-cube_size, cube_size, 0],
    [-cube_size, -cube_size*0, -cube_size * 2],
    [cube_size, -cube_size*0, -cube_size * 2],
    [cube_size, cube_size*0, -cube_size * 2],
    [-cube_size, cube_size*0, -cube_size * 2]
])

# Define the edges that connect the vertices
edges = [
    [0, 1], [1, 2], [2, 3], [3, 0],  # Base
    [4, 5], [5, 6], [6, 7], [7, 4],  # Top
    [0, 4], [1, 5], [2, 6], [3, 7]   # Sides
]

# Open the video capture (0 for default camera)
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Initialize the AprilTag detector within the pyapriltag binding
#nthreads - number of cpu threads to use
#quad_decimate - reduces the resolution of the image by a factor
#refine_edges - refines the edges for better pose estimation
#decode_sharpening - to sharpen the image 
detector = Detector(families='tag36h11',nthreads=1, quad_decimate=1.0, quad_sigma=0.0, refine_edges=1, decode_sharpening=0.25)
i=0
while True:
    # Capture frame-by-frame from the camera
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Convert the frame to grayscale
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Detect AprilTags
    tags = detector.detect(gray, estimate_tag_pose=True, camera_params=(camera_matrix[0, 0], camera_matrix[1, 1], camera_matrix[0, 2], camera_matrix[1, 2]), tag_size=0.1)

    # Loop over the detected tags
    for tag in tags:
        # Get the tag's pose from the detector's outcome
        tag_pose_R = tag.pose_R  # Rotation matrix
        tag_translation = tag.pose_t.reshape(3, 1)  # Translation vector

        # Transform the cube's vertices to the tag's coordinate system
        # 3x8 = (3x3 @ (8x3)T)T + [tx, ty, tz]
        # After rotation each vertice is translated to the Apriltag's coordinate system
        cube_vertices_transformed = (tag_pose_R @ cube_vertices.T).T + tag_translation.flatten()

        # Project 3D points onto the image plane, outpts projected points onto image plane and a jacobian(currently not required)
        projected_points, _ = cv.projectPoints(cube_vertices_transformed, np.eye(3), np.zeros(3), camera_matrix, dist_coeffs)

        # Draw the edges of the cube
        for edge in edges:
            pt1 = tuple(projected_points[edge[0]][0].astype(int))
            pt2 = tuple(projected_points[edge[1]][0].astype(int))
            cv.line(frame, pt1, pt2, (0, 255, 0), 2)

        # Draw the tag's center point
        center = (int(tag.center[0]), int(tag.center[1]))
        cv.circle(frame, center, 5, (0, 0, 255), -1)

        # Display the tag's ID close to the center point
        cv.putText(frame, f"ID: {tag.tag_id}", (center[0] - 10, center[1] - 10),
                   cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # Show the frame with the cube and AprilTag
    cv.imshow("AprilTag Detection with Cube", frame)
    if cv.waitKey(1) & 0xFF == ord('c'):
        filename = f"frame_{i+1}.jpg"
        cv.imwrite(filename, frame)
        print(f"Captured {filename}")
        i=i+1
    # Exit if 'q' is pressed
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close any OpenCV windows
cap.release()
cv.destroyAllWindows()
