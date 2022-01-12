import os
image_files = []
for filename in os.listdir(os.getcwd()+"/"+os.path.join("darknet", "data","obj")):
    if filename.endswith(".jpg"):
        image_files.append("data/obj/" + filename)

with open(os.getcwd()+"/darknet/data/train.txt", "w") as outfile:
    for image in image_files:
        outfile.write(image)
        outfile.write("\n")
    outfile.close()