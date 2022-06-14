# 模型和数据网盘地址: 
[链接：https://pan.baidu.com/s/11m7F_d506XMzyK1kvyi27g?pwd=rgnv](https://pan.baidu.com/s/11m7F_d506XMzyK1kvyi27g?pwd=rgnv )
提取码：rgnv

# Task1: 
### 使用deeplabv3处理图片处理视频流

## Prepare
将test.mp4放入 /task1_deeplabv3/video  

将deeplabv3_cityscapes_train.zip文件解压到 /task1_deeplabv3/model

## 操作指令：
处理视频 
```
python deeplabv_video.py 
```
执行结果放置于  ./result/

# Task2: 
## Prepare
将model.zip放入 /Task2_CIFAR-100_vit/checkpoint

## 训练：
```
python train_it.py -net vit/resnet18 -gpu -lr 0.1 -method none
```
## 结果:
训练好的模型参数存入checkpoint文件夹下，tensorboard所画曲线存入runs文件夹下
