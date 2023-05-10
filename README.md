use DNN in PIV method

目标:

端到端的流场分析

粒子基本形状是3x3的矩阵，四个角是1，四条边是2，中心是3，然后再随机加上[0, 1)的噪声
粒子密度很大，单个颗粒很小

- [x] 构造一个函数，能够在指定位置放入一个粒子

- [x] ~~想一个办法，能够模拟粒子从背景底部出现，并按照出现位置的速度计算下一帧的位置~~
    - ~~但是目前的人工流场在Y方向上的速度都是相同的，且X方向上的速度为0，是否应该简化涉及，直接根据所在x轴，画出若干帧的位置？~~

- [ ] 发现一些成熟的PIV图像生成方法，应首先使用这些方法作为数据集来源。
    - can only use the velocity field from matlab and place some particle in it.
    - consider add some pepper noise
    - consider add some noise when particle move

- [ ] 读更多论文，看看这个领域最新最好的方法是什么？
    - for now is FlowNet and FlowNet2
    - also can check PIV-FlowNet and PTV-FlowNet
    
    - the key content is how to extract feature in two frame and also the relation between them
    - beside that, how to reconstruct the feature map into velocity field with original shape is very important 

- [ ] 至少第一个月不写代码，多研究理论，以及把基础的那几个网络暂时搭出来
    - [ ] build FlowNetS and FlowNetC
    - [ ] build FlowNet2.0