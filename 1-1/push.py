######################################
# title: 一个实例学会ZDEM
# date: 2021-04-25
# authors: 李长圣
# E-mail: sheng0619@163.com
# note:
# 括号内参数可根据模型大小及个人需要修改
# 脚本命令不区分大小写
# 用16个核心，实际用时<1小时
# 计算费用约<2元
# more info, see www.geovbox.com
#######################################
#程序初始化
START
#颗粒设为球，计算颗粒体积用4/3*pi*r^3计算
SET disk off
#设置研究范围 
BOX left 0.0 right 31000.0 bottom 0.0 height 110000.0 kn=0e10 ks=0e10 fric 0.00 
#设置挡板墙，这里模型采用hertz接触模型，挡板墙的kn ks无效，计算时取颗粒的参数
WALL ID 0, NODES (      0.0 ,     10.0 ) (  30000.0 ,     10.0 ), kn=0e10 ks=0e10 fric 0.0 COLOR black
WALL ID 1, NODES (     10.0 ,  100000.0 ) (     10.0 ,     10.0 ), kn=0e10 ks=0e10 fric 0.0 COLOR blue
WALL ID 2, NODES (  30000.0 ,     10.0 ) (  30000.0 ,  100000.0 ), kn=0e10 ks=0e10 fric 0.0 COLOR red
#在矩形范围内生成颗粒
GEN NUM 15000000 rad discrete 200.0 220.0,  x ( 10.0, 30000.0), y ( 10.0, 100000.0), COLOR black GROUP ball_rand
#设置颗粒的微观参数　density 密度，firc 摩擦系数，shear 剪切模量，poiss　泊松比，damp 局部阻尼常数，heart　Hertz-Mindlin接触模型
PROP density 2.0e3, fric 0.0, shear 2.9e9, poiss 0.2, damp 0.4, hertz
#设置时间步及重力加速度
SET  DT 5e-2,  GRAVITY  0.0,  -9.8 
#设置每1000步保存一次vtk格式的计算结果
SET  vtk 1000
#设置每1000步保存一次ps格式的计算结果
SET  ps 1000
#设置每1000步保存一次dat格式的计算结果
SET  print 1000
#沉积，计算5000步
CYC 5000
#删除4000米以上的颗粒
DEL RANGE y 30000.0 9990000.0
#平衡，计算1000步
CYC 1000
#输出包含颗粒的[x y r]信息的初始模型 init_xyr.dat
EXP init_xyr.dat

#设置bond粘结，使颗粒具有粘聚力，ebmod 杨氏模量，　gbmod 剪切模量，tstrength 抗拉强度，sstrength　聚合强度，　firc 摩擦系数
PROP ebmod 2e8 gbmod 2e8  tstrength 2e7 sstrength 4e7 fric 0.3 
#给地层赋上颜色
PROP COLOR lg          range y    0.0   5000.0
PROP COLOR green       range y  5000.0  10000.0
PROP COLOR yellow      range y 10000.0  15000.0
PROP COLOR red         range y 15000.0  20000.0
PROP COLOR black       range y 20000.0  25000.0
PROP COLOR mg          range y 25000.0  30000.0
PROP COLOR blue        range y 30000.0  35000.0
PROP COLOR gb          range y 35000.0  40000.0
PROP COLOR violet      range y 40000.0  45000.0

#设置挡板墙摩擦系数
WALL id 0 fric 0.3
WALL id 1 fric 0.3
WALL id 2 fric 0.3
#设置墙的挤压速度 x方向速度为2.0
WALL id 1 xv 2.0
#设置墙的挤压量x方向推进10000.0，每挤压2000.0保存一次计算结果
IMPLE wall id 1 xmove 10000.0 save 2000.0 print 1000.0 ps 1000.0 vtk 1000.0
#计算停止