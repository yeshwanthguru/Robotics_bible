---
title: Classical Vision & Image Processing
---

# Classical Computer Vision and Image Processing

:::tip[The 30-second version]
Before deep learning, vision was done with **hand-designed filters and geometry**: blur to remove noise, find edges and corners, match features, measure with calibrated cameras. These methods are still everywhere in robots because they are **fast, predictable, explainable and need no training data**. Even deep-learning pipelines use them for pre-processing, calibration and geometry.
:::

## 1. What an image is

A grayscale image is a grid of numbers (0–255); a colour image has three channels (R, G, B). Common colour spaces:

| Space | Why use it |
|---|---|
| **RGB / BGR** | native camera format (OpenCV uses BGR order, a classic bug) |
| **HSV / HLS** | separates hue from brightness; good for colour thresholding |
| **Lab** | perceptually uniform colour differences |
| **Grayscale** | most feature detectors |
| **Depth / disparity** | geometry, not appearance |

## 2. Filtering: smoothing and sharpening

A **kernel** (small matrix) slides over the image; each output pixel is a weighted sum of its neighbours (convolution or correlation).

| Filter | Effect |
|---|---|
| **Box / mean blur** | simple smoothing |
| **Gaussian blur** | smoothing with less ringing; first step before edges |
| **Median filter** | removes salt-and-pepper noise, keeps edges |
| **Bilateral filter** | smooths while preserving edges |
| **Sharpening (unsharp mask)** | boosts edges |

## 3. Edges, corners and features

| Method | What it finds | Idea |
|---|---|---|
| **Sobel / Scharr** | intensity gradients | derivative filters |
| **Canny edge detector** | thin, clean edges | gradient → non-maximum suppression → hysteresis thresholds |
| **Hough transform** | lines and circles | edge pixels vote for shapes |
| **Harris / Shi–Tomasi corners** | corner points | eigenvalues of local gradient matrix |
| **FAST** | corners (very fast) | compare a pixel with a circle around it |
| **SIFT / SURF** | scale-invariant keypoints + descriptors | robust but heavier |
| **ORB** | FAST + binary descriptor (BRIEF) | real-time, used in ORB-SLAM |
| **SuperPoint + LightGlue / SuperGlue** | learned keypoints and matching | state of the art matching |

**Matching features:** compare descriptors (L2 for float, Hamming for binary), ratio test, then **RANSAC** to reject wrong matches.

## 4. Segmentation and shape analysis (classical)

- **Thresholding:** global, adaptive, **Otsu** (automatic threshold).
- **Colour segmentation:** threshold in HSV (e.g. find a red ball).
- **Morphology:** erosion, dilation, opening (remove specks), closing (fill gaps).
- **Connected components and contours:** label blobs, measure area, bounding box, moments, convex hull.
- **Watershed / GrabCut:** region-based segmentation.
- **Background subtraction:** detect motion by comparing to a background model.

## 5. Geometry and calibration

### Camera model
Pinhole: $u=f_xX/Z+c_x,\; v=f_yY/Z+c_y$ plus lens distortion (radial, tangential). **Intrinsics** are $f_x,f_y,c_x,c_y$ and distortion; **extrinsics** place the camera in the world.

### Calibration
Photograph a checkerboard or AprilTag board from many angles; solve for intrinsics and distortion (Zhang's method, `cv2.calibrateCamera`). Check reprojection error (< 0.5 px is good). Calibrate stereo pairs, camera–LiDAR and camera–IMU (Kalibr) too.

### Multi-view geometry
| Concept | Use |
|---|---|
| **Homography** | planar scenes, panoramas, image rectification |
| **Fundamental / essential matrix** | relative pose from matched points |
| **Triangulation** | 3-D point from two views |
| **PnP** | camera pose from known 3-D points |
| **Stereo rectification and disparity** | depth from two cameras: $Z=fB/d$ |
| **Structure from motion / SLAM** | reconstruct scene and trajectory |

### Optical flow
Estimating per-pixel motion between frames: **Lucas–Kanade (KLT)** for tracking sparse points, **Farnebäck** for dense flow, **RAFT** (deep) for state-of-the-art flow.

## 6. Practical pipeline example (find a coloured object and its position)

```python
import cv2, numpy as np
img = cv2.imread("scene.png")
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, (0, 120, 70), (10, 255, 255))      # reddish hues
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))   # remove specks
cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
c = max(cnts, key=cv2.contourArea)                          # biggest blob
(x, y), r = cv2.minEnclosingCircle(c)
print("object at pixel", x, y)       # with depth Z: X=(x-cx)Z/fx, Y=(y-cy)Z/fy
```

## 7. When to use classical versus deep learning

| Prefer classical | Prefer deep learning |
|---|---|
| fixed, controlled lighting and objects | varied, cluttered, natural scenes |
| tight latency or tiny compute | semantic understanding (what is it?) |
| need explainability and guarantees | no hand-crafted rule can capture the variation |
| calibration, geometry, measurement | detection, segmentation, depth from one image |

Best practice: **combine them**: deep nets for recognition, classical geometry for precise 3-D measurement and calibration.

## Interview Q&A

**How does the Canny edge detector work?**
*Simply:* blur, find gradients, keep only the thinnest ridge of each edge, and link strong and weak edges. *Deeper:* non-maximum suppression plus hysteresis thresholds.

**Why Gaussian blur before edge detection?**
*Simply:* noise creates false edges. *Deeper:* derivative filters amplify noise; the blur trades detail for stability.

**What is a homography?**
*Simply:* a 3×3 mapping between two views of a plane. *Deeper:* needs four correspondences (DLT), used for rectification and stitching.

**ORB versus SIFT?**
*Simply:* ORB is much faster and binary; SIFT is more robust to scale and blur but slower. *Deeper:* ORB suits real-time SLAM.

**How do you calibrate a camera?**
*Simply:* photograph a known pattern from many angles and solve for intrinsics. *Deeper:* minimise reprojection error; check distortion model and coverage of the image.

**Why does BGR vs RGB matter?**
*Simply:* OpenCV loads images as BGR; feeding them to an RGB-trained network swaps colour channels and hurts accuracy.
