import os
from shutil import copyfile, rmtree, copytree
import pandas as pd
import matplotlib.pyplot as plt
import json
from collections import Counter

home_dir = os.getcwd()+'/dataset'
mapilary_dir = home_dir+'/mapilary'
new_mapilary_dir = home_dir+'/organized_mapilary_dataset'
new_fully_mapilary_dir = new_mapilary_dir+'/fully'
new_partially_mapilary_dir = new_mapilary_dir+'/partially'
new_fully_img_mapilary_dir = new_fully_mapilary_dir+'/img'
new_partially_img_mapilary_dir = new_partially_mapilary_dir+'/img'

if not 'mapilary' in os.listdir() :
    assert Exception
if 'organized_mapilary_dataset' in os.listdir() :
    rmtree(new_mapilary_dir)
    print('OVERWRITTING to "organized_mapilary_dataset" directory. organized_mapilary_dataset is already exist.')
os.mkdir(new_mapilary_dir)

all_dirs = list(filter(lambda x : not "." in x, os.listdir(mapilary_dir)))
fully_annotated_dir = ''
partially_annotated_dir = ''
img_files = []
for dir in all_dirs :
    if 'mtsd_v2_fully_annotated' in os.listdir(mapilary_dir+'/'+dir) :
        fully_annotated_dir = mapilary_dir+'/'+dir+'/mtsd_v2_fully_annotated/annotations'
    elif 'mtsd_v2_partially_annotated' in os.listdir(mapilary_dir+'/'+dir) :
        partially_annotated_dir = mapilary_dir+'/'+dir+'/mtsd_v2_partially_annotated/annotations'
    else :
        for img_file in os.listdir(mapilary_dir+'/'+dir+'/images') :
            img_files.append(mapilary_dir+'/'+dir+'/images/'+img_file)

copytree(fully_annotated_dir, new_fully_mapilary_dir+'/annotations')
copytree(partially_annotated_dir, new_partially_mapilary_dir+'/annotations')

os.mkdir(new_fully_img_mapilary_dir)
os.mkdir(new_partially_img_mapilary_dir)

fully_annotations = list(map(lambda x : x.split('.json')[0], os.listdir(fully_annotated_dir)))
partially_annotations = list(map(lambda x : x.split('.json')[0], os.listdir(partially_annotated_dir)))

fully_labels = []
partially_labels = []

for img_file in img_files :
    # full
    file = img_file.split('/')[-1]
    filename = file.split('.jpg')[0] 
    if filename in fully_annotations :
        f = open(fully_annotated_dir+'/'+filename+'.json')
        objects = json.load(f)["objects"]
        for obj in objects :
            fully_labels.append(obj['label'])

        copyfile(img_file, new_fully_img_mapilary_dir+'/'+file)

    # partial
    if filename in partially_annotations :
        f = open(partially_annotated_dir+'/'+filename+'.json')
        objects = json.load(f)["objects"]
        for obj in objects :
            partially_labels.append(obj['label'])
        copyfile(img_file, new_partially_img_mapilary_dir+'/'+file)


fully_label_counts = Counter(fully_labels)
f = open(new_mapilary_dir+'/fully_labels.txt', 'a') 
for key, value in zip(fully_label_counts.keys(), fully_label_counts.values()) :
    f.write(key+'\t'+str(value)+'\n')
f.close()

df = pd.DataFrame.from_dict(fully_label_counts, orient='index')
plot = df.plot(kind='bar')
fig = plot.get_figure()
fig.savefig("fully_labels.png")



partially_label_counts = Counter(partially_labels)
f = open(new_mapilary_dir+'/partially_labels.txt', 'a') 
for key, value in zip(partially_label_counts.keys(), partially_label_counts.values()) :
    f.write(key+'\t'+str(value)+'\n')
f.close()

df = pd.DataFrame.from_dict(partially_label_counts, orient='index')
plot = df.plot(kind='bar')
fig = plot.get_figure()
fig.savefig("partially_labels.png")


total_labels = partially_labels + fully_labels

total_label_counts = Counter(total_labels)
f = open(new_mapilary_dir+'/total_labels.txt', 'a') 
for key, value in zip(total_label_counts.keys(), total_label_counts.values()) :
    f.write(key+'\t'+str(value)+'\n')
f.close()

df = pd.DataFrame.from_dict(total_label_counts, orient='index')
plot = df.plot(kind='bar')
fig = plot.get_figure()
fig.savefig("total_labels.png")



# fig, ax = plt.subplots()
# total_df = partially_df.append(fully_df)
# total_hist = total_df.hist(ax=ax)
# ax.tick_params(labelrotation=90)
# fig.savefig(new_mapilary_dir+'/total_annotation.png')

# total_list = total_df.to_list()
# f = open(new_mapilary_dir+'/labels.txt', 'a') 
# for l in list(set(total_list)) :
#     f.write(l+'\t'+str(total_list.count(l))+'\n')
# f.close()