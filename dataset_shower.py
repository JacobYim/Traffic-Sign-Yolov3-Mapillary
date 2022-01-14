import os
from re import T
import cv2
import numpy as np
import json


ORGANIZED_DATASET_DIR = "dataset/organized_mapilary_dataset"
FULLY_DIR = ORGANIZED_DATASET_DIR +"/fully"
ANNOTATION_DIR = FULLY_DIR + "/annotations"
IMG_DIR = FULLY_DIR + "/img"

annotation_files = os.listdir(ANNOTATION_DIR)
img_files = os.listdir(IMG_DIR)
annotation_files.sort()
img_files.sort()

def visualize_annotation(annotation_path, img_path) :
    f = open(ANNOTATION_DIR+"/"+annotation_path)
    data = json.load(f)
    img  = cv2.imread(IMG_DIR+'/'+img_path)
    for object in data['objects'] :
        bbox = object['bbox']
        print(bbox)
        p1 = (int(bbox['xmin']),int(bbox['ymin']))
        p2 = (int(bbox['xmax']),int(bbox['ymax']))
        img = cv2.rectangle(img, p1, p2, (255,255,0), 10 )
    cv2.imwrite("annotated_"+img_path, img)


CONVERTED_DATASET_DIR = "yolo/yolo_data"
converted_files = os.listdir(CONVERTED_DATASET_DIR)
converted_img_files = list(filter(lambda x : '.jpg' in x , converted_files))
converted_txt_files = list(filter(lambda x : '.txt' in x , converted_files))
converted_img_files.sort()
converted_txt_files.sort()

def visualize_conveted_annotation(txt_path, img_path) :
    f = open(CONVERTED_DATASET_DIR+"/"+txt_path)
    img  = cv2.imread(CONVERTED_DATASET_DIR+'/'+img_path)
    lines = f.readlines()
    print(lines)
    lines = list(map(lambda x : x.replace('\n', ''), lines))
    for line in lines :
        items = line.split(' ')
        p1 = (int(float(items[1])),int(float(items[2])))
        p2 = (int(float(items[1])+float(items[3])),int(float(items[2])+float(items[4])))
        img = cv2.rectangle(img, p1, p2, (255,255,0), 10 )
    cv2.imwrite("annotated_converted_"+img_path, img)


if __name__ == "__main__" :
    img_file = converted_img_files[0]
    txt_file = converted_txt_files[0]
    json_file = txt_file.replace('.txt', '.json')
    print(img_file, txt_file, json_file)
    visualize_conveted_annotation(txt_file, img_file)
    visualize_annotation(json_file, img_file)