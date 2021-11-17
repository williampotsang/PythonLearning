

# Key Word: 如何系统地学习Python 中 matplotlib, numpy, scipy, panda
#

# Python科学计算的笔记：包括Python基础、Numpy、Pandas、Matplotlib等包的学习笔记，很全。
https://link.zhihu.com/?target=https%3A//github.com/lijin-THU/notes-python
#


# Numpy，Pandas，Matplotlib，Scipy，Scikit-learn
### Numpy：来存储和处理大型矩阵，比Python自身的嵌套列表（nested list structure)结构要高效的多，
本身是由C语言开发。这个是很基础的扩展，其余的扩展都是以此为基础。数据结构为ndarray,一般有三种方式来创建。Python对象的转换通过类似工厂函数numpy内置函数生成：np.arange,np.linspace.....从硬盘读取，loadtxt
> 快速入门：[Quickstart tutorial](https://link.zhihu.com/?target=https%3A//docs.scipy.org/doc/numpy-dev/user/quickstart.html)

### Pandas: 基于NumPy 的一种工具，该工具是为了解决数据分析任务而创建的。
Pandas 纳入了大量库和一些标准的数据模型，提供了高效地操作大型数据集所需的工具。最具有统计意味的工具包，某些方面优于R软件。数据结构有一维的Series，二维的DataFrame(类似于Excel或者SQL中的表，如果深入学习，会发现Pandas和SQL相似的地方很多，例如merge函数)，三维的Panel（Pan（el) + da(ta) + s，知道名字的由来了吧）。学习Pandas你要掌握的是：汇总和计算描述统计，处理缺失数据 ，层次化索引清理、转换、合并、重塑、GroupBy技术日期和时间数据类型及工具（日期处理方便地飞起）
> 快速入门：[10 Minutes to pandas](https://link.zhihu.com/?target=http%3A//pandas.pydata.org/pandas-docs/stable/10min.html)

### Matplotlib: Python中最著名的绘图系统，
很多其他的绘图例如seaborn（针对pandas绘图而来）也是由其封装而成。创世人John Hunter于2012年离世。这个绘图系统操作起来很复杂，和R的ggplot,lattice绘图相比显得望而却步，这也是为什么我个人不丢弃R的原因，虽然调用```plt.style.use("ggplot")```绘制的图形可以大致按照ggplot的颜色显示，但是还是感觉很鸡肋。但是matplotlib的复杂给其带来了很强的定制性。其具有面向对象的方式及Pyplot的经典高层封装。
需要掌握的是：
- 散点图，折线图，条形图，直方图，饼状图，箱形图的绘制。
- 绘图的三大系统：pyplot，pylab(不推荐)，面向对象
- 坐标轴的调整，添加文字注释，区域填充，及特殊图形patches的使用
- 金融的同学注意的是：可以直接调用Yahoo财经数据绘图（真。。。）
> Pyplot快速入门：[Pyplot tutorial](https://link.zhihu.com/?target=http%3A//matplotlib.org/users/pyplot_tutorial.html)

### Scipy：方便、易于使用、专为科学和工程设计的Python工具包.
它包括统计,优化,整合,线性代数模块,傅里叶变换,信号和图像处理,常微分方程求解器等等。基本可以代替Matlab，但是使用的话和数据处理的关系不大，数学系，或者工程系相对用的多一些。（略）近期发现有个statsmodel可以补充scipy.stats，时间序列支持完美

### Scikit-learn：关注机器学习的同学可以关注一下，很火的开源机器学习工具，
这个方面很多例如去年年末Google开源的TensorFlow，或者Theano，caffe(贾扬清)，Keras等等，这是另外方面的问题。
> 主页：[An introduction to machine learning with scikit-learn](https://link.zhihu.com/?target=http%3A//scikit-learn.org/stable/tutorial/basic/tutorial.html)

### 图书：
- Pandas的创始者：[利用Python进行数据分析](https%3A//book.douban.com/subject/25779298/)   (豆瓣)​book.douban.com/subject/25779298/（力荐）
- 提升自己：[机器学习实战](https%3A//book.douban.com/subject/24703171/)  (豆瓣)​book.douban.com/subject/24703171/



# Python 生态体系
这 4 个库在 Python 生态体系中的地位也不一样，相对来说 Numpy 最简单，处于最底层。国外有大神用一张图总结过 Python 生态体系中各个工具的层次：<img src="https://pica.zhimg.com/50/v2-297731bd359ebc14978967a92f1716cb_720w.jpg?source=1940ef5c" data-caption="" data-size="normal" data-rawwidth="882" data-rawheight="660" class="origin_image zh-lightbox-thumb" width="882" data-original="https://pica.zhimg.com/v2-297731bd359ebc14978967a92f1716cb_r.jpg?source=1940ef5c"/>
- 所以着手学这几个库的时候，可以先从 Numpy 学起，然后逐步掌握 SciPy，Pandas 和 Matplotlib。
