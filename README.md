# RRC Summer School (Summer 2022) - MVG (4/4)

Class 4 of 4 on Multi-View Geometry covered in RRC Summer School 2022. The following topics are included here.

- Stereo camera depth estimation
- Triangulation
- PnP Formulation

## Table of contents

- [RRC Summer School (Summer 2022) - MVG (4/4)](#rrc-summer-school-summer-2022---mvg-44)
    - [Table of contents](#table-of-contents)
    - [Contents](#contents)
    - [References](#references)

## Contents

The contents of this repository are as follows

| S. No. | Item Name | Description |
| :----- | :-------- | :---------- |
| 1a | [stereo_to_depth.ipynb](./notebooks/stereo_to_depth.ipynb) | Convert stereo rectified images to point clouds |
| 1b | [stereo_to_depth_tsukuba.ipynb](./notebooks/stereo_to_depth_tsukuba.ipynb) | Same thing as `1a`, but with `tsukuba` (see difference between BFMatcher) |
| 2 | [triangulation.ipynb](./notebooks/triangulation.ipynb) | Triangulation of a single point |

The repository also contains the following

| S. No. | Item Name | Description |
| :----- | :-------- | :---------- |
| A | [Slides - MVG4.pptx](./Presentation/Slides%20-%20MVG4.pptx) | Presentation |

## References

- RRC Summer School 2022
    - Schedule: [laksh-nanwani.notion.site](https://laksh-nanwani.notion.site/laksh-nanwani/Robotics-Research-Center-Summer-School-2022-8ee9a9ff7fc445619c2b650a1557e946)
- Stereo camera depth estimation
    - Start with code: [intelrealsense.com](https://www.intelrealsense.com/stereo-depth-vision-basics/)
    - ML approaches: [learnopencv.com](https://learnopencv.com/depth-estimation-using-stereo-matching/)
    - Conceptual overview: [medium.com](https://medium.com/analytics-vidhya/distance-estimation-cf2f2fd709d8)
    - C++ implementation with GUI controls: [learnopencv.com](https://learnopencv.com/depth-perception-using-stereo-camera-python-c/)
    - Results and review: [adept.net.au](https://www.adept.net.au/news/newsletter/201211-nov/article_3D_stereo.shtml)
- Triangulation
    - Triangulation on [Wikipedia](https://en.wikipedia.org/wiki/Triangulation_(computer_vision))
    - Group triangulation on OpenCV through SFM: [docs](https://docs.opencv.org/4.x/d0/dbd/group__triangulation.html)
    - Optimizers
        - [scipy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html#scipy.optimize.minimize) (using [SLSQP](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-slsqp.html#optimize-minimize-slsqp))
        - [pyopt](http://www.pyopt.org/index.html) (using [SLSQP](http://www.pyopt.org/reference/optimizers.slsqp.html#pySLSQP))
- PnP Algorithm
    - PnP on [Wikipedia](https://en.wikipedia.org/wiki/Perspective-n-Point)
    - PnP overview on [OpenCV docs](https://docs.opencv.org/4.x/d5/d1f/calib3d_solvePnP.html)
    - P3P
        - Earliest works (1999): [Linear N-Point Camera Pose Determination](https://hal.inria.fr/file/index/docid/590105/filename/Quan-pami99.pdf)
        - Recent solution (2003): [Complete solution classification for the perspective-three-point problem](https://ieeexplore.ieee.org/document/1217599)
        - Faster and more accurate (2018): [Lambda Twist: An Accurate Fast Robust Perspective Three Point (P3P) Solver](https://openaccess.thecvf.com/content_ECCV_2018/papers/Mikael_Persson_Lambda_Twist_An_ECCV_2018_paper.pdf)
    - PnP
        - Efficient O(n) PnP (2009): [EPnP: An Accurate O(n) Solution to the PnP Problem](https://link.springer.com/content/pdf/10.1007/s11263-008-0152-6.pdf)
        - SQPnP - non-polynomial solver which casts PnP as non-linear quadratic problem - (2020): [A Consistently Fast and Globally Optimal Solution to the Perspective-n-Point Problem](https://www.ecva.net///papers/eccv_2020/papers_ECCV/html/1969_ECCV_2020_paper.php)
- Other underlying theory
    - Understand camera intrinsic matrix: [towardsdatascience.com](https://towardsdatascience.com/camera-intrinsic-matrix-with-example-in-python-d79bf2478c12)

[![Developer TheProjectsGuy][dev-shield]][dev-profile-link]

[dev-shield]: https://img.shields.io/badge/Developer-TheProjectsGuy-blue
[dev-profile-link]: https://github.com/TheProjectsGuy
