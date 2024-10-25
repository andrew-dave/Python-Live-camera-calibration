# Python-Live camera calibration
<p style="text-align: justify;">
   Calibration of generic mobile camera using zhang's method in a live setting. The camera calibration was performed using OpenCV’s `calibrateCamera()` method. This approach retrieves the camera intrinsics, extrinsics, and all distortion parameters (both radial and tangential) using a 16x9 checkerboard for increased calibration accuracy due to more data points. The calibration uses frames from a live video feed on a smartphone, with an emphasis on minimizing reprojection error. 
</p> 
   Another aspect is to understand the effects of calibration at varying distances, particularly looking into how the intrinsic parameters and the distortion values vary when performing the calibration procedure when close and far away from the checkerboard used for calibration. The variations in parameters and the discussion relating to the effects are as follows:-

## Calibration at Different Distances

### Calibration Rig within 1 Meter

**Camera Matrix (K):**

| 1254.4269 | 0.0000    | 313.5035 |
|-----------|-----------|----------|
| 0.0000    | 1255.9546 | 225.1007 |
| 0.0000    | 0.0000    | 1.0000   |

**Distortion Coefficients:**

| Value |
|-------|
| 0.0569 |
| 1.5890 |
| -0.0007 |
| 0.0016 |
| -18.6526 |

#### Description:
- **fx = 1254.4269** and **fy = 1255.9546** are comparatively higher values.
- **(cx, cy) = (313.5035, 225.1007)**; the image center is generally consistent.
- **Distortion Coefficients**:
  - **Radial Distortion**: k1 = 0.0569, k2 = 1.5890, k3 = -18.6526 (higher by comparison)
  - **Tangential Distortion**: p1 = -0.0007, p2 = 0.0016

### Calibration Rig between 2-3 Meters

**Camera Matrix (K):**

| 1184.1177 | 0.0000    | 283.9069 |
|-----------|-----------|----------|
| 0.0000    | 1186.4043 | 266.7395 |
| 0.0000    | 0.0000    | 1.0000   |

**Distortion Coefficients:**

| Value |
|-------|
| -0.1772 |
| 5.2629 |
| -0.0075 |
| -0.0107 |
| -40.4775 |

#### Description:
- **fx = 1184.1177** and **fy = 1186.4043** are comparatively lower.
- **(cx, cy) = (283.9069, 266.7395)**; while generally constant, variations are present here.
- **Distortion Coefficients**:
  - **Radial Distortion**: k1 = -0.1772, k2 = 5.2629, k3 = -40.4775 (lower in comparison)
  - **Tangential Distortion**: p1 = -0.0075, p2 = -0.0107

### Observations and Reasoning

- The values of **(cx, cy)** are generally constant but vary slightly, possibly due to changes in field of view as distance varies, affecting the perceived principal point of the camera.
- The **effective focal length** varies with distance: at closer distances, the perspective effects are more pronounced, leading to higher effective focal lengths since a larger area of the target is captured. At farther distances, effective focal lengths decrease to accommodate a wider FOV for the same target size.
- **Radial Distortion Parameters (k1, k2, k3)** are higher when the camera is closer to the checkerboard due to more pronounced edge distortion. As the camera moves farther away, the curves straighten, and distortion generally reduces. The same trend applies to **Tangential Distortion**.
