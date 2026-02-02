Dual-path Network Package
===========================

###########Environment
Linux or Windows
Python3.9
PyTorch1.7.1

All codes outline
change.py        // 把照片转化成.npy格式，在raw_train_photos和label_folder文件夹中要有数量一致且相同的图片      
train-main1.py  // running the code for the main training program
net.py         // contains all models of this project.
pred1.py      // running the code for the pred program
pp5.py       // 图像分割区域并赋属性，在.csv文件中删除第三列手动保存到.dat文件中
xy.py       // 像素位置转化成实际位置，保存在.csv文件中
将两个.csv文件整合成property.dat文件
运行zdem生成init_xyr.dat文件（1-1）
find2.py // 给init_xyr.dat文件赋属性生成.dat文件
运行zdem生成颗粒（1-2）



All codes detailed imformation
train-main.py
############# 
Description of data:
We set the input and output to 256*256 two-dimensional data.
(You can also adjust the training scale according to the needs of different research areas.)
The input data is 256*256 two-dimensional data of digital rock images 
The label data is 256*256 two-dimensional data of segmentation result (Pores are set to 0, and matrix is set to 1.)

pred.py
############# 
Since the final segmented image is a binary image, we set the threshold value to 0.5 as in typical binary images, 
where pixels with values less than 0.5 are set to 0, and those greater than or equal to 0.5 are set to 1.

