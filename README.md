# cryoEM-SPA
some code about cryoEM SPA

与冷冻电镜单颗粒分析相关的一些代码

## orientation_sampling.py

近似均匀地采样欧拉角(phi, theta)，可用于对3D物体的各取向均匀的投影。取向可以用端点在单位球面上的单位向量表示，代码给出的采样结果为P94_step9.png与SK97_N1163.png。

参考文献：

"P.R. Baldwin, Pawel A. Penczek. The Transform Class in SPARX and EMAN2. Journal of Structural Biology, 2007, 250-261"

"E.B. Saff, A.B.J. Kuijlaars. Distributing Many Points on a Sphere. The Mathematical Intelligencer, 1997, 5-11"
