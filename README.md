# air-quality-predict
## 项目简介
+ 点击[项目地址](www.byesyoucan.xin)查看效果；
+ 本项目使用go语言编写后台，python语言编写爬虫和机器学习模块， 
    使用go语言调用python接口实现混合编程。
## 功能简介
+ 从[空气质量研究](https://www.aqistudy.cn/historydata/monthdata.php?city=%E5%8D%97%E6%98%8C) 
    这个网站上获取南昌AQI数据，然后存入postgresql数据库中；
+ 训练KNN，GBDT，BP神经网络这三种机器学习模型
+ 展示过去7天的和未来7天的数据；
+ 查询历史AQI