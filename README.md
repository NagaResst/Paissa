[![Auto Check and Update Patch Data](https://github.com/NagaResst/Paissa/actions/workflows/auto-update.yaml/badge.svg)](https://github.com/NagaResst/Paissa/actions/workflows/auto-update.yaml) [![Push to OSS](https://github.com/NagaResst/Paissa/actions/workflows/push-data.yaml/badge.svg)](https://github.com/NagaResst/Paissa/actions/workflows/push-data.yaml)
# **开发环境**:  
python 3.10  
qt designer  

# **依赖**:  
pyqt5
requests 


# **Windows端运行方法**：  
使用了[PyStand](https://github.com/skywind3000/PyStand )的启动器，将```Paissa.py```重命名为```Paissa.int```后，运行Paissa.exe启动。

# **版本数据更新**：
需要在 [ffxiv-datamining-cn](https://github.com/thewakingsands/ffxiv-datamining-cn) 下载从新版本游戏中解包出来的物品列表```item.csv```放入Data文件夹内，并替换同名文件。
直接用python运行```Data/format_item.py```就会生成新数据文件```item.Pdt```。  
```item.csv```只作为物品索引，其他所有数据都来源于 [garlandtools.cn](https://garlandtools.cn/) 。大家都是用爱发电，请只在需要的时候进行数据文件的更新，避免给其他开发者带来困扰。  

**推荐**[点击这里](http://43.142.142.18/item.Pdt)下载我自己维护的数据文件。
> Pdt只是简单粗暴的json文件，第一个键值对说明了这份数据对应游戏版本。



# **使用说明**：

## 1. 市场价格查询的界面加入了与销量有关的简评：

关系如下：

| 这个东西很难卖出去 | 真的很难卖，不建议下场搅浑水 |  
| 大家都在买HQ，几乎不买NQ | HQ还挺好卖的，NQ就寄了。 |  
| 大家只买HQ，并且不太好卖 | 字面意思 |  
| 这个东西很受欢迎 | 销量很高，需要一天补几次货 |  
| 这个东西一定卖得出去 |销 量一般或者比较好 |  
| 看不出来销量好不好，感觉不太行 | 本质上是查询数据失败，不过可能真的卖不动 |  

>※ 如果出现了HQ和NQ的走货量指数，可以根据走货量指数评估，走货量指数不代表单位时间内绝对的销售数量，但是有一定关系。
  一般超过12的东西就很好卖了，快销品普遍在13以上。但是具体卖不卖的动，还得看你所在的服务器的脚本哥让不让你卖。

## 2. 成本计算界面加入了利润空间做参考：  
   需要注意的是，根据上文提及的走货量指数，如果超过75%的人选择了买HQ，那么利润按照HQ的商品价格去计算，否则按照NQ的商品价格计算。  
   估算利润 = 7天市场平均售价 * 单次产出数量 - 直接材料成本 (选择直接材料成本是因为这是你最后一步的加工，如果这一步加工不赚钱，不如出售原材料)  
   在料理，或则爆发药的计算时，兼容了生产数量的计算。但是单个物品的成本，依旧按照单次生产进行计算，因为你无法用3分之1的成本来制作这些东西。  
## 3. 直接材料成本 和 原始材料成本 ，最大的参考意义是告诉你：  
  直接板子买半成品，还是自己搓，请根据成本树中的结果酌情选择，而不是一味的只参考某一个值。  
   如果不差钱，建议直接板子买，别搓，因为这是获得道具的最快方法。
## 4. 在菜单栏的其他中，可以选择是否使用静态资源加速查询  
   在启用静态资源加速的情况下，只有查询物品价格的时候才会使用网络。  
   如果游戏版本更新，可以单独更新静态资源的数据文件，或者关闭静态资源加速，使用在线资源查询。  
   (未来可能推出差异文件更新进行版本的迭代。)

# **关于二开**：  
用 qt designer 直接打开```.ui```文件可以对界面设计进行可视化的编程。需要使用pyuic转化成```.py```文件。  
```.ui```文件和对应的```.py```文件中只包含界面显示相关的代码，界面上行为的代码都在```Window.py```中，后台数据查询的功能都封装在```Queryer.py```中。

