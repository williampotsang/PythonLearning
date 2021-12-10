
> ### [jupyter notebook的基本使用---學習記錄2.23](https://tw511.com/a/01/26230.html)
> ### [Anaconda（三）jupyter notebook使用、汉化、设置工作路径](https://www.bilibili.com/read/cv12134802)
> ### [修改Anaconda中的Jupyter Notebook預設工作路徑的四種方式](https://www.itread01.com/content/1544590095.html)

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
> ### [安装tensorflow（使用WHL）,手把手,教,whl](https://www.pythonf.cn/read/163419)
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

#
# Conda & Anaconda
Conda是一个包管理器；Anaconda才是一个python发行版。虽然conda是用Anaconda打包的， 但是它们两个的目标是完全不同的。

> Conda，有命令”conda install”, “conda update”, “conda remove”, 所以很明显， conda是包管理器。包管理器是自动化软件安装，更新，卸载的一种工具。
> Anaconda才是一个python发行版软件发行版是在系统上提前编译和配置好的软件包集合， 装好了后就可以直接用。再来说说， Anaconda 和 Miniconda. Anaconda发行版会预装很多pydata生态圈里的软件，而Miniconda是最小的conda安装环境， 一个干净的conda环境

> ### conda ≈ pip（python包管理） + virtualenv（虛擬環境） + 非python依賴包管理

* 級別不一樣conda和yum比較類似，可以安裝很多庫，不限於Python。conda是建立一個區域性的環境，並安裝相應包；pip是安裝包到原有的環境中。
* pip install會檢查一些依賴包並給你安裝，而conda的這種檢查更多，甚至會把你已有的卸了替換成他認為合適的...反正conda我只是拿來管理，安裝一直是pip install...conda install真心不太喜歡亂檢測亂適配....
