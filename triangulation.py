# %%
import numpy as np
from scipy.spatial.transform import Rotation as rot
import cv2 as cv
import open3d as o3d
from scipy.optimize import minimize

# %% Declare properties of camera
# Camera positions
cam1_pos = np.array([1, 1, 2])
cam2_pos = np.array([1, 3, 2])
demo_pt = np.array([2., 2., 1.])    # Actual point in world (corres)
# Camera intrinsic matrices (3x3 shape)
f = 3.5e2
cx, cy = 300, 300   # 600, 600 image shape
cam1_K = np.array([
    [f, 0, cx],
    [0, f, cy],
    [0, 0, 1]], float)
cam2_K = cam1_K.copy()

# Rotation of cameras (1 & 2) w.r.t. world (extrinsic)
r1 = rot.from_euler("yz", [10, 30], degrees=True).as_matrix()
r2 = rot.from_euler("yz", [10, -30], degrees=True).as_matrix()
# XYZ directions of camera is different
rc = np.array([ # Cam XYZ axis w.r.t. world XYZ
    [0., 0., 1.],
    [-1., 0., 0.],
    [0., -1., 0.]])

# %% Lambda functions for helping
# Position to 4x4 homogeneous transformation
pos2ht = lambda pos: np.concatenate((
        np.concatenate((np.eye(3), pos.reshape(-1, 1)), axis=1),
        np.array([[0, 0, 0, 1]])))
# Rotation matrix to 4x4 homogeneous transformation
rotm2ht = lambda rotm: np.concatenate((
        np.concatenate((rotm, np.zeros((1, 3)))),
        np.array([[0, 0, 0, 1]]).T), axis=1)
# Position & rotation matrix from 4x4 homogeneous transformation
ht2pos = lambda ht: ht[0:3, 3]
ht2rotm = lambda ht: ht[0:3, 0:3]

# %% Camera projection model
# {cam} (1 and 2) in {world} -> ^W_C T
tf_cam1 = pos2ht(cam1_pos) @ rotm2ht(r1) @ rotm2ht(rc)
tf_cam2 = pos2ht(cam2_pos) @ rotm2ht(r2) @ rotm2ht(rc)
# Camera projection: KR[I|-X_c]
def cam_project(cam_tf, cam_K, X_pts):
    """
        Project a set of points using camera transformation and the
        intrinsic properties of the camera.

        Parameters:
        - cam_tf: The 4x4 camera transform (in world frame)
        - cam_K: The 3x3 camera intrinsic matrix
        - X_pts: 3D points in the world. Shape: (N, 3) or (3,)

        Returns:
        - x_pix: Pixel coordinates (x, y) in the image. Shape (N, 2)
    """
    # Extract camera extrinsic properties
    X_cam = ht2pos(cam_tf)  # Position of camera in world
    R_world_cam = ht2rotm(cam_tf) # {camera} in {world} (Rot. Matrix)
    R_cam = R_world_cam.T   # {world} in {camera} (vect. projection)
    I_Xc = np.concatenate((np.eye(3), -X_cam.reshape(3, 1)), axis=1)
    P = cam_K @ R_cam @ I_Xc
    # Convert world points to homogeneous
    X_3d = X_pts.reshape(-1, 3).T   # Points as columns: (3, N)
    X_hpts = np.concatenate((X_3d, np.ones((1, X_3d.shape[1]))))
    # Project world points in the camera
    x_hpx = P @ X_hpts
    # De-homogenize pixel coordinates
    proj_pts = x_hpx[:2]/x_hpx[2]
    x_pix = proj_pts.T   # (2, N) -> (N, 2)
    return x_pix

# %% Project a world point
c1_demo = cam_project(tf_cam1, cam1_K, demo_pt)
c2_demo = cam_project(tf_cam2, cam2_K, demo_pt)
# Pixel coordinates (as observed). Don't expose `demo_pt`
p_img1 = c1_demo.astype(int)
p_img2 = c2_demo.astype(int)

# %% Pixel correspondence
# Convert to (u, v) pixel (as floats) and then homogeneous
p1 = p_img1.astype(float).flatten()
p2 = p_img2.astype(float).flatten()
p1_h = np.concatenate((p1.reshape(-1, 1), [[1]]))
p2_h = np.concatenate((p2.reshape(-1, 1), [[1]]))
# Rotation matrix for camera in world
R_world_cam1 = ht2rotm(tf_cam1)
R_world_cam2 = ht2rotm(tf_cam2)
# Project to vectors in the world
vect1 = R_world_cam1 @ np.linalg.inv(cam1_K) @ p1_h
vect2 = R_world_cam2 @ np.linalg.inv(cam2_K) @ p2_h
# Convert to (X, Y, Z) flattened vectors
v1 = (vect1 / np.linalg.norm(vect1)).flatten()
v2 = (vect2 / np.linalg.norm(vect2)).flatten()

# %%
# Minimize distance between the projected points
def l2_dist_func(ab_vals, pos_cam1, vect1, pos_cam2, vect2):
    """
        L2 squared distance function to minimize.
        - ab_vals: (alpha, beta): Scaling along respective vectors
        - pos_cam1: (x, y, z) Position of camera 1
        - vect1: 3D direction vector from camera 1
        - pos_cam2: (x, y, z) Position of camera 2
        - vect2: 3D direction vector from camera 2
    """
    # alpha, beta (for camera 1 and camera 2)
    al, be = ab_vals[0], ab_vals[1]
    # Get points
    pt1 = pos_cam1 + al * vect1
    pt2 = pos_cam2 + be * vect2
    # Convert to distance (cost)
    dvect = (pt2 - pt1)
    dist_sq = dvect[0]**2 + dvect[1]**2 + dvect[2]**2
    return dist_sq


# %%
pos_cam1 = ht2pos(tf_cam1)
pos_cam2 = ht2pos(tf_cam2)

# %%
# Use "Sequential Least Squares Programming" (SLSQP) to minimize
res = minimize(l2_dist_func, (0, 0), method="SLSQP",
    args=(pos_cam1, v1, pos_cam2, v2))

# %%
# Get the points on the lines
alpha, beta = res.x
pt1 = pos_cam1 + alpha * v1
pt2 = pos_cam2 + alpha * v2
pt_mid = (pt1 + pt2)/2  # Mid-point is the result
# Error from demo
dist_demo = np.linalg.norm(demo_pt - pt_mid)
print(f"Point 1: {pt1}""\n" \
    f"Point 2: {pt2}""\n" \
    f"End point: {pt_mid}""\n" \
    f"Actual point: {demo_pt}""\n" \
    f"\tError: {dist_demo}")

# %%

# %% Experimental section
