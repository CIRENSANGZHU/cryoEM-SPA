# cryoEM-SPA
some code about cryoEM SPA

与冷冻电镜单颗粒分析相关的一些代码

## orientation_sampling.py

近似均匀地采样欧拉角(phi, theta)，可用于对3D物体的各取向均匀的投影。取向可以用端点在单位球面上的单位向量表示，代码给出的采样结果为orientation_sampling_P94_step9.png与orientation_sampling_SK97_N1163.png。

参考文献：

"P.R. Baldwin, Pawel A. Penczek. The Transform Class in SPARX and EMAN2. Journal of Structural Biology, 2007, 250-261"

"E.B. Saff, A.B.J. Kuijlaars. Distributing Many Points on a Sphere. The Mathematical Intelligencer, 1997, 5-11"

## CTF.py

根据给定参数生成CTF，并给（干净的投影）图像加上CTF。


参考文献：

'CTF Simulation': https://ctfsimulation.streamlit.app

'cryoSPARC CTF estimation': https://guide.cryosparc.com/processing-data/all-job-types-in-cryosparc/ctf-estimation

CTFFIND4: Fast and accurate defocus estimation from electron micrographs. Alexis Rohou and Nikolaus Grigorieff. Journal of Structural Biology 192 (2015) 216–221.

Computational Methods for Single-Particle Cryo-EM. Amit Singer and Fred J. Sigworth. Annual Review of Biomedical Data Science, Vol. 3, pp. 163-190, 2020.

