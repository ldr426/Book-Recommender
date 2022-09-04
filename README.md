# Book-Recommend
Book recommender web project based on collaborative filtering algorithm

协同过滤图书推荐系统运行说明

## 1.	Environment Configuration / 环境配置
-	Python 3.6
-	Anaconda. Reference：https://www.cnblogs.com/yuxuefeng/articles/9235431.html
-	Flask
-	Mysql 5.7
-	Pymysql
-	Yaml

## 2.	Development Tools / 开发工具
PyCharm 2020.2.1 x64

## 3.	run configuration / 运行配置
1.	Create a new database in mysql, and import the data into the database from book.sql in the decompressed folder

      在mysql中新建book数据库，将解压缩后文件夹下的 book.sql将数据导入数据据

2.	Open the project with pycharm, the configuration file of the database is web/config.yml, change the database password to your own password
      
      用pycharm打开项目，数据库的配置文件为web/config.yml，将其中的数据库密码改为你自己的密码
  
3.	Select the running environment of python, and pip install the relevant dependencies in the first step of the environment configuration
      
      选择python的运行环境，pip安装第一步环境配置中的相关依赖包
  
4.	Finally, open the app.py file, pull the file to the end, and click the small green arrow to run
      
      最后，打开app.py文件，把文件拉到最后，点击绿色小箭头，即可运行

<div align="center"><img src="https://user-images.githubusercontent.com/56751303/187025937-09289d04-f0fb-429e-9383-f6aa48b12280.png"></div>
 
5.	There are two different types of users in the system. One is a normal user and the other is an administrator user. The username of an ordinary user is the UserID field of the user table in the database, and the password is the Location field. The administrator username and password are both admin.
      
      系统中有两种不同类型的用户。一种是普通用户，一种是管理员用户。普通用户的用户名为数据库中user表的UserID字段，密码为Location字段。管理员用户名、密码均为admin
