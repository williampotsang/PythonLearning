

# Conda 虛擬環境設置
### 设置虚拟环境 (非必要)
建议在虚拟环境中安装tensorflow，搭配使用版本低一些的Python。在Anaconda Prompt里面设置环境，命名为py36（使用Python3.6)。
```
conda create --n py36 python=3.6
```

### 激活虚拟环境 (非必要)
```
conda activate py36
```

#
> # [安装tensorflow（使用WHL）,手把手,教,whl](https://www.pythonf.cn/read/163419)
> 
# Python 虛擬環境設置
要建立新的虛擬環境，請選擇 Python 解譯器，並建立用來存放的 .\venv 目錄：
```
python -m venv --system-site-packages .\venv
```

啟動虛擬環境：
```.\venv\Scripts\activate```

在不影響主機系統設定的情況下，在虛擬環境中安裝套件。首先，請升級 pip：
```
pip install --upgrade pip
pip list  # show packages installed within the virtual environment
```

之後再離開虛擬環境：
```deactivate  # don't exit until you're done using TensorFlow```




### 安装whl文件
将whl文件放置到pip所在文件夹，如C:\Program Files(x86)\Anaconda3\envs\py36\Scripts

将cmd设置到当前目录，使用
```pip install tensorflow-1.13.1-cp36-cp36m-win_amd64.whl```即可。建议尝试几次，因为安装过程中可能会有一些网络问题。
