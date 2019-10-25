import os
from os import walk, getcwd
from PIL import Image

""" Class label (BDD) """
# same order with yolo format class annotation
classes = [ "bike" , "bus" , "car", "motor", "person", "rider", "traffic light", "traffic sign", "train", "truck"]

""" Inverse convert function """
def i_convert(size, box):
    x = box[0]*size[0]
    y = box[1]*size[1]
    w = box[2]*size[0]
    h = box[3]*size[1]
    xmin = x - w/2
    xmax = x + w/2
    ymin = y - h/2
    ymax = y + h/2
    return (xmin, xmax, ymin, ymax)
    
mypath = "./labels/100k/train/"   # txt file path 

wd = getcwd()
txt_outfile =open('gt_bdd_train.json','w') # output json file name 
txt_outfile.write("[\n")

""" Get input text file list """
txt_name_list = []
for (dirpath, dirnames, filenames) in walk(mypath):
    txt_name_list.extend(filenames)
    break

""" Process """
start = 0

for txt_name in txt_name_list:
    """ Open input text files """
    txt_path = mypath + txt_name
    txt_file = open(txt_path, "r")
    lines = txt_file.read().splitlines()

    """ Open input image file """
    img_path = txt_path.replace("labels","images")    
    img_path = img_path.replace("txt", "jpg")
    img = Image.open(img_path)
    img_size = img.size

    """ Convert the YOLO format to BDD evaluation format """
    for line in lines:
        if(len(line) > 0):
            if start != 0:
                txt_outfile.write(",\n")
            else :
                start = 1
            elems = line.split()
            cls_id = int(elems[0])
            x = elems[1]
            y = elems[2]
            w = elems[3]
            h = elems[4]
            box = (float(x), float(y), float(w), float(h))
            xmin, xmax, ymin, ymax = i_convert(img_size, box)

            txt_outfile.write("\t{\n\t\t\"name\":\"%s\",\n\t\t\"category\":\"%s\",\n\t\t\"bbox\":[%f,%f,%f,%f]\n\t}" %(os.path.splitext(txt_name)[0],classes[cls_id],xmin,ymin,xmax,ymax))

txt_outfile.write("\n]")
txt_outfile.close()

