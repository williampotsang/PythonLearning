

> [安装tensorflow（使用WHL）,手把手,教,whl](https://www.pythonf.cn/read/163419)

### 设置虚拟环境 (非必要)
建议在虚拟环境中安装tensorflow，搭配使用版本低一些的Python。在Anaconda Prompt里面设置环境，命名为py36（使用Python3.6)。
```
conda create --n py36 python=3.6
```

### 激活虚拟环境 (非必要)
```
conda activate py36
```


### 安装whl文件
将whl文件放置到pip所在文件夹，如C:\Program Files(x86)\Anaconda3\envs\py36\Scripts

将cmd设置到当前目录，使用
```pip install tensorflow-1.13.1-cp36-cp36m-win_amd64.whl```即可。建议尝试几次，因为安装过程中可能会有一些网络问题。
