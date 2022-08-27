# Book_Recommend
Book recommender web project based on collaborative filtering algorithm

协同过滤图书推荐系统运行说明

## 一、	环境配置
-	Python 3.6，可直接安装anaconda
可参考：https://www.cnblogs.com/yuxuefeng/articles/9235431.html
-	Flask
-	Mysql 5.7
-	Pymysql
-	Yaml

## 二、	开发工具
PyCharm 2020.2.1 x64

## 三、	运行配置
-	在mysql中新建book数据库，将解压缩后文件夹下的 book.sql将数据导入数据库
-	用pycharm打开项目，数据库的配置文件为web/config.yml，将其中的数据库密码改为你自己的密码
-	选择python的运行环境，pip安装第一步环境配置中的相关依赖包
-	最后，打开app.py文件，把文件拉到最后，点击绿色小箭头，即可运行
 ![image](https://user-images.githubusercontent.com/56751303/187025937-09289d04-f0fb-429e-9383-f6aa48b12280.png)

-	系统中有两种不同类型的用户。一种是普通用户，一种是管理员用户。普通用户的用户名为数据库中user表的UserID字段，密码为Location字段。管理员用户名、密码均为admin。
