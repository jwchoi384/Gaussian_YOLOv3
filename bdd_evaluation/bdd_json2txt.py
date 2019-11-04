# -*- coding: utf-8 -*-

import os
from os import walk, getcwd
from PIL import Image
import json

""" Class label (BDD) """
classes = ["bike" , "bus" , "car", "motor", "person", "rider", "traffic light", "traffic sign","train", "truck"]

""" Convert function """
def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)
    
""" Configure Paths"""   
mypath = "./labels/100k/train/"         # json file path
outpath = "./labels/100k/train_yolo/"   # txt file path

if not os.path.isdir(outpath):
    os.mkdir(outpath, 0755)

wd = getcwd()
list_file = open('%s/train_bdd_list.txt'%(wd), 'w')

""" Get input text file list """
txt_name_list = []
for (dirpath, dirnames, filenames) in walk(mypath):
    txt_name_list.extend(filenames)
    break


""" Process """
for txt_name in txt_name_list:
    """ Open input json files """
    txt_path = mypath + txt_name
    txt_file = open(txt_path, "r")
    j_data = json.load(txt_file)

    """ Open input image files """
    img_path = txt_path.replace("labels","images")
    img_path = img_path.replace("json", "jpg")
    img = Image.open(img_path)
    img_size = img.size

    """ Open output text files """
    txt_outpath = outpath + txt_name.replace("json","txt")
    txt_outfile = open(txt_outpath, 'w')

    """ Convert the BDD format to YOLO format """
    lines = len(j_data['frames'][0]['objects'])

    ct = 0
    for line in range(lines):
        cls = j_data['frames'][0]['objects'][line]['category']
        exit = 0
        if cls not in classes:
            exit = 1
        if exit == 0:
            ct = ct + 1
            cls_id = classes.index(cls)
            xmin = j_data['frames'][0]['objects'][line]['box2d']['x1']
            xmax = j_data['frames'][0]['objects'][line]['box2d']['x2']
            ymin = j_data['frames'][0]['objects'][line]['box2d']['y1']
            ymax = j_data['frames'][0]['objects'][line]['box2d']['y2']

            box = (float(xmin), float(xmax), float(ymin), float(ymax))
            bb = convert(img_size, box)
            txt_outfile.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

    txt_outfile.close()

    if(ct != 0):
        list_file.write('%s/images/100k/train_yolo/%s.jpg\n'%(wd, os.path.splitext(txt_name)[0]))
            
list_file.close()       
