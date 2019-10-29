# Gaussian YOLOv3: An Accurate and Fast Object Detector Using Localization Uncertainty for Autonomous Driving
**[Gaussian YOLOv3 implementation](https://github.com/jwchoi384/Gaussian_YOLOv3)**

This repository contains the code for our **ICCV 2019** [Paper](http://openaccess.thecvf.com/content_ICCV_2019/html/Choi_Gaussian_YOLOv3_An_Accurate_and_Fast_Object_Detector_Using_Localization_ICCV_2019_paper.html)

The proposed algorithm is implemented based on the [YOLOv3 official code](https://github.com/pjreddie/darknet).

<img src="https://user-images.githubusercontent.com/56669525/67075282-d2dc1200-f1c5-11e9-8af9-9f874e89197d.png" width="100%">

*The provided example weight file ("[Gaussian_yolov3_BDD.weights](https://drive.google.com/open?id=1Eutnens-3z6o4LYe0PZXJ1VYNwcZ6-2Y)") is not the weight file used in the paper, but newly trained weight for release code validation. Because this weight file is more accurate than the weight used in the paper, we provide this file in the repository.*

Poster
------
<img src="https://user-images.githubusercontent.com/56669525/67777222-c64c9900-faa4-11e9-861d-4ea3b36db986.PNG" width="100%">

Citation
--------
```
@InProceedings{Choi_2019_ICCV,
author = {Choi, Jiwoong and Chun, Dayoung and Kim, Hyun and Lee, Hyuk-Jae},
title = {Gaussian YOLOv3: An Accurate and Fast Object Detector Using Localization Uncertainty for Autonomous Driving},
booktitle = {The IEEE International Conference on Computer Vision (ICCV)},
month = {October},
year = {2019}
}
```

Requirements
----------------------
The code was tested on 

`Ubuntu 16.04, NVIDIA GTX 1080 Ti with CUDA 8.0 and cuDNNv7, OpenCV 3.4.0`

`Ubuntu 16.04, NVIDIA Titan Xp with CUDA 9.0 and cuDNNv7, OpenCV 3.3.0`


Setup
------
Please see the YOLOv3 website instructions [setup](https://pjreddie.com/darknet/yolo/)


Dataset
-------
We tested our algorithm using Berkeley deep drive (BDD) dataset.

If you want to use BDD dataset, please see [BDD website](https://bdd-data.berkeley.edu/) and download the dataset.

Training
--------
For training, you must make image list file (*e.g.,* "train_bdd_list.txt") and ground-truth data. Please see these websites: [YOLOv3](https://pjreddie.com/darknet/yolo/), [How to train YOLO](https://timebutt.github.io/static/how-to-train-yolov2-to-detect-custom-objects/)

`List files ("train_bdd_list.txt", "val_bdd_list.txt", "test_bdd_list.txt") in the repository are an example. You must modify the directory of the file name in the list to match the path where the dataset is located on your computer.`

Download pre-trained weights [darknet53.conv.74](http://pjreddie.com/media/files/darknet53.conv.74)

Download the code
```Swift
git clone https://github.com/jwchoi384/Gaussian_YOLOv3
```

```Swift
cd Gaussian_YOLOv3
```

Compile the code
```Swift
make
```

Set batch=64 and subdivisions=16 in the cfg file.

*We used 4 gpus in our experiment. If your computer runs out of GPU memory when training, please increase subdivision size in the cfg file.* 

Start training by using the command line
```Swift
./darknet detector train cfg/BDD.data cfg/Gaussian_yolov3_BDD.cfg darknet53.conv.74
```
If you want to use multiple gpus,
```Swift
./darknet detector train cfg/BDD.data cfg/Gaussian_yolov3_BDD.cfg darknet53.conv.74 -gpus 0,1,2,3
```

Inference
---------
Download the Gaussian_YOLOv3 example weight file. [Gaussian_yolov3_BDD.weights](https://drive.google.com/open?id=1Eutnens-3z6o4LYe0PZXJ1VYNwcZ6-2Y)

Set batch=1 and subdivisions=1 in the cfg file.

Run the following commands.
1. `make`
2. `./darknet detector test cfg/BDD.data cfg/Gaussian_yolov3_BDD.cfg Gaussian_yolov3_BDD.weights data/example.jpg`

You can see the result:

<img src="https://user-images.githubusercontent.com/56669525/67030475-7091fb80-f14a-11e9-8eeb-e71a8f3b4ee2.jpg" width="80%">

Evaluation
----------
Download the Gaussian_YOLOv3 example weight file. [Gaussian_yolov3_BDD.weights](https://drive.google.com/open?id=1Eutnens-3z6o4LYe0PZXJ1VYNwcZ6-2Y)

For evaluation, you MUST change the batch and subdivision size in cfg file.
Like this: `batch = 1, subdivision = 1`

Run the following commands. You can get a detection speed of more than 42 FPS.
1. `make`

2. `./darknet detector valid cfg/BDD.data cfg/Gaussian_yolov3_BDD.cfg Gaussian_yolov3_BDD.weights`

3. `cd bdd_evaluation/` (We got this code from https://github.com/ucbdrive/bdd-data)

4. `python evaluate.py det gt_bdd_val.json ../results/bdd_results.json`

You will get:
```
AP : 9.45 (bike)
AP : 40.28 (bus)
AP : 40.56 (car)
AP : 8.66 (motor)
AP : 16.85 (person)
AP : 10.59 (rider)
AP : 7.91 (traffic light)
AP : 23.15 (traffic sign)
AP : 0.00 (train)
AP : 40.28 (truck)
[9.448295420802772, 40.28022967768842, 40.562338308273596, 8.658317480713093, 16.85103955706777, 10.588396343004272, 7.914563796458698, 23.147189144825003, 0.0, 40.27786994583501] 

9.45 40.28 40.56 8.66 16.85 10.59 7.91 23.15 0.00 40.28

mAP 19.77 (512 x 512 input resolution)
```

If you want to get the mAP for BDD test set, 
1. `make`
2. `Change the list file in cfg file ("val_bdd_list.txt" --> "test_bdd_list.txt" in "cfg/BDD.data")`
3. `./darknet detector valid cfg/BDD.data cfg/Gaussian_yolov3_BDD.cfg Gaussian_yolov3_BDD.weights`
4. `Upload result file ("results/bdd_results.json") on BDD evaluation server` [Link](https://bdd-data.berkeley.edu/portal.html)

On the BDD test set, we got 19.2 mAP (512 x 512 input resolution).


Contact
-------
For questions about our paper or code, please contact Jiwoong Choi. 

<jwchoi384@gmail.com>
