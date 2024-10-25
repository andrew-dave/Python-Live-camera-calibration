# Python-Live camera calibration
 Calibration of generic mobile camera using zhang's method in a live setting
The approach to camera calibration has been simply performed using OpenCV’s calibrateCamera() method
which returns the camera intrinsics, extrinsics and all the distortion parameters(radial and tangential) using a classic
16x9 checkerboard for more accuracy during calibration due to more data points. Here, an approach using the live
video feed from a smartphone to capture frames and calibrating the camera is used while making sure the reprojection
error is converging to a minimal value. The code to this task is named T_3.py with relavant documentation.
Calibration Rig within 1 Meter:
K =


1254.4269 0.0000 313.5035
0.0000 1255.9546 225.1007
0.0000 0.0000 1.0000

 dist =


0.0569
1.5890
−0.0007
0.0016
−18.6526


Description:
• fx = 1254.4269 and fy = 1255.9546 are comparatively higher in value.
• (cx, cy) = (313.5035, 225.1007); the image center is generally constant.
• The distortion coefficients are:
– k1 = 0.0569, k2 = 1.5890, k3 = −18.6526 (radial distortion) - Higher by comparison.
– p1 = −0.0007, p2 = 0.0016 (tangential distortion).
Calibration Rig between 2-3 Meter:
K =


1184.1177 0.0000 283.9069
0.0000 1186.4043 266.7395
0.0000 0.0000 1.0000

 dist =


−0.1772
5.2629
−0.0075
−0.0107
−40.4775


Description:
• fx = 1184.1177 and fy = 1186.4043 are comparatively lower.
• (cx, cy) = (283.9069, 266.7395); the image center is generally constant but there are variations here.
• The distortion coefficients are:
– k1 = −0.1772, k2 = 5.2629, k3 = −40.4775 (radial distortion) - Lower in comparison.
– p1 = −0.0075, p2 = −0.0107 (tangential distortion).
Reasons:
• The values of (cx, cy) are generally constant. But, we can observe that they vary possibly due the change in
field of view due to the distance which could possibly affect how the principle point of the camera is perceived.
• The effective focal length is varying here since the perspective effects more pronounced at closer distances
leading to higher effective focal lengths since it captures a larger area of the target whereas to accommodate a
wider FOV when farther away for the same sized target the effective focal lengths decrease
• The radial distortion parameters k1, k2, k3 are higher when closer to the checkerboard due to more apparent
distortion at the edges of the lens. When farther away the curves become more straight and the distortion
generally reduces. The same goes for tangential distortion.
