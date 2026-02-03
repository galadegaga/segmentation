# zdem image segmentation example

- 2026-01-23
- 维护人：邓玥

## 简介

该目录演示采用Python、zdem完成系列岩石图像分割和属性分类

- 分割模型：双路径深度学习模型
- 接触模型：采用hertz-Mindlin模型 和 bond粘结模型
- 参考文献
    1. 李长圣 (2019) 基于离散元的褶皱冲断带构造变形定量分析与模拟. 博士论文. 南京大学.
    2. Wang Z, Hou Z, Cao D. Edge-guided segmentation of digital rock images: Integrating a pretrained edge aware path with the main segmentation path[J]. Computers & Geosciences, 2025, 197: 105884.
    3. Morgan JK (2015) Effects of cohesion on the structural and mechanical evolution of fold and thrust belts and contractional wedges: Discrete element simulations. Journal of Geophysical Research: Solid Earth 120:3870-3896.

## 目录简介

PART1部分文件夹不可随意更改，在raw_train_photos和label_folder文件夹中要有数量一致且相同的图片
property.dat 和 xy_mapping.csv需要手动整合数据
处理后的照片经处理后将变为分辨率512×512图片，统一转换为30000×30000的正方形照片

数据目录中内容如下：
```
|-- 1-1
|   |-- data
|   |-- job.sh
|   `-- push.py
|-- 1-2
|   |-- data
|   |-- detach.py
|   |-- job.sh
|   `-- property_xyr.dat
|-- PART1
|   |-- DU1
|   |-- __pycache__
|   |-- change.py
|   |-- edge.pth
|   |-- label1
|   |-- label_folder
|   |-- net.py
|   |-- pred1.py
|   |-- raw_train_photos
|   |-- test1
|   `-- train_main1.py
|-- PART2
|   |-- coordinates.csv
|   |-- pp5.py
|   |-- xy.py
|   |-- xy.txt
|   `-- xy_mapping.csv
|-- PART3
|   |-- find2.py
|   |-- init_xyr.dat
|   |-- property.dat
|   `-- property_xyr.dat
`-- REDME.md
```

## 使用方法

当前计算实现方式，是
1. 在PART1文件夹中执行`change.py`把照片转化成.npy格式, `train_main1.py` `pred1.py`训练分割模型
2. 在PART2文件夹中执行 `pp5.py` 进行岩石属性分类,保存在coordinates.csv文件中。执行`xy.py`将像素位置转化成实际位置，保存在xy_mapping.csv文件中。
3. 将两个.csv文件整合成property.dat文件
4. 在1-1文件夹中运行zdem生成init_xyr.dat文件
5. 在PART3文件夹中执行 `find2.py` 给init_xyr.dat文件赋属性生成property_xyr.dat文件
6. 在1-2文件夹中运行zdem生成带属性的岩石颗粒接触模型

## 参考

- 该图像分割模型源自https://github.com/wzq0802/Ziqiang ,本人在此基础上进行修改，感谢原作者的无私分享。
- 以上试验又参考自李长圣（2019）博士论文 第四章褶皱冲断带变形机制及影响因素 4.1 参数选取与调试。
