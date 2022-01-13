# Traffic-Sign-Yolo-Mapillary
This is a repository to analysis the recognition performance about Mapillary Dataset.

# Darknet
```
git clone https://github.com/AlexeyAB/darknet
```

# Dataset
```
Download from https://www.mapillary.com/dataset/trafficsign and extract at dataset/mapilary
```
data_organizer.py : raw dataset -> organizaed_dataset
data_converter.py : organized_dataset -> yolo_data

# Set Up Darknet

- copy data to darknet folder
```
cp -r yolo/yolo_data darknet/data/obj
```

- add darknet/data/obj.names
```
Stop Sign
```

- add darknet/data/obj.data
```
classes= 1
train  = data/train.txt
valid  = data/test.txt
names = data/obj.names
backup = backup
```

- generate train.txt
```
python generate_train_txt.py
```

- make cfg file
```
cp darknet/cfg/yolov3.cfg darknet/cfg/yolov3_traffic_signal.cfg
sed -i 's/batch=1/batch=32/' darknet/cfg/yolov3_traffic_signal.cfg
sed -i 's/subdivisions=1/subdivisions=8/' darknet/cfg/yolov3_traffic_signal.cfg
sed -i 's/max_batches = 500200/max_batches = 2200/' darknet/cfg/yolov3_traffic_signal.cfg
sed -i 's/steps=400000,450000/steps=1600,1800/' darknet/cfg/yolov3_traffic_signal.cfg
sed -i 's/filters=255/filters=18/g' darknet/cfg/yolov3_traffic_signal.cfg
sed -i 's/classes=80/classes=1/g' darknet/cfg/yolov3_traffic_signal.cfg
```

or 

```
cp config/yolov3_traffic_signal.cfg darknet/cfg/yolov3_traffic_signal.cfg
```

- build darknet
```
# change makefile to have GPU and OPENCV enabled
sed -i 's/OPENCV=0/OPENCV=1/' darknet/Makefile
sed -i 's/GPU=0/GPU=1/' darknet/Makefile
sed -i 's/CUDNN=0/CUDNN=1/' darknet/Makefile
sed -i 's/NVCC=nvcc/NVCC="/usr/local/cuda-11.5/bin/nvcc"' darknet/Makefile
```

or 

```
cp config/Makefile darknet/Makefile
```

```
# verify CUDA
/usr/local/cuda/bin/nvcc --version

# make darknet (build)
cd  darknet
make
```

## Training

wget http://pjreddie.com/media/files/darknet53.conv.74
wget https://pjreddie.com/media/files/yolov3.weights
./darknet detector train data/obj.data cfg/yolov3_traffic_signal.cfg darknet53.conv.74 -dont_show


## Test
./darknet detector map data/obj cfg/yolov3_traffic_signal.cfg backup/yolov3_traffic_signal_final.weights 
./darknet detector map data/obj cfg/yolov3_traffic_signal.cfg backup/b32s8/yolov3_traffic_signal_final.weights 
./darknet detector test data/obj.names cfg/yolov3_traffic_signal.cfg backup/b32s8/yolov3_traffic_signal_final.weights  -dont_show -ext_output < data/train.txt > result.txt