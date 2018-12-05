# COCO-python-script-for-object-detection

- Download this repo https://github.com/cocodataset/cocoapi
- Install the dependencies with the Makefile in PythonApi folder
- Download the train/val annotations of 2017 images here
http://images.cocodataset.org/annotations/annotations_trainval2017.zip
- move the annotation folder you downloaded in the cocoapi repo directory
- move the file create_data.py of this repo in PythonApi folder
- create a directory 'data' in the PythonApi folder
- run create_data.py

# Description

create_data.py will create a .txt file per image. Each file contains in char format the value of each pixel of the image
in RGB mode. the images are padded so that the size of each image is 640x640. So each .txt file contains 640x640x3 values
separated with commas. In addition the file will contain the values always in char format x,y,h,w,category_object for each object
in the image. x,y are the coordinates value of the box of the object starting from the left corner, h,w are the sizes of the box
of the object and category_object is a number identifying the object. The category_object id can be seen here:
https://github.com/nightrome/cocostuff/blob/master/labels.txt

So, for instance if we have an image with 3 objects we have:
640x640x2 values separated with commas and then   ...,x1,y1,h1,w1,id1,x2,y2,h2,w2,id2,x3,y3,h3,w3,id3,
