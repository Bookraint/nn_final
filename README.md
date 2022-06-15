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

最后结果位于网盘地址task1_result/文件夹下
# Task2:

## Prepare
将下载好的预训练权重放入/faster_rcnn/backnone

## 训练
运行train_random_init.py,train_imagenet.py和train_maskrcnn.py可以分别训练随机初始化、ImageNet预训练以及coco在Mask R-CNN预训练的Faster R-CNN模型

# Task3: 
## Prepare
将model.zip放入 /CIFAR-100_vit/checkpoint

## 训练：
```
python train_vit.py -net vit/resnet18 -gpu -lr 0.1 -method none
```
## 结果:
训练好的模型参数存入checkpoint文件夹下，tensorboard所画曲线存入runs文件夹下
