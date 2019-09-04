# Create a new user for mysql
## Create New User
##### Step1. Login in the mysql without passwd. `sudo mysql -uroot`
##### Setp2. Use the mysql database to setup the new User.
```
use mysql;
select user,host,plugin from user;
create user 'pi'@'localhost' identified by 'mysql';
create user 'pi'@'%' identified by 'mysql';
update user set plugin='unix_socket' where user='pi';
select user,host,plugin from user;
flush privileges;
```  
![Create](https://cl.ly/2284db1ff20d/sreateuser.png)
##### Step3. Setting the privilige of the new user.
```
grant all privileges on * to pi@'localhost' identified by 'mysql';
grant all privileges on * to pi@'%' identified by 'mysql';
flush privileges;
```  

1.**PrivilegesCode表示授予的权限类型，常用的有以下几种类型：**
* all privileges：所有权限。
* select：读取权限。
* delete：删除权限。
* update：更新权限。
* create：创建权限。
* drop：删除数据库、数据表权限。

2.**DbName.tableName表示授予权限的具体库或表，常用的有以下几种选项：**
* .：授予该数据库服务器所有数据库的权限。
* dbName.*：授予dbName数据库所有表的权限。
* dbName.dbTable：授予数据库dbName中dbTable表的权限。

3.**Username@host表示授予的用户以及允许该用户登录的IP地址。其中Host有以下几种类型：**

* localhost：只允许该用户在本地登录，不能远程登录。
* %：允许在除本机之外的任何一台机器远程登录。
* 192.168.52.32：具体的IP表示只允许该用户从特定IP登录。
* password指定该用户登录时的页面。
* flush privileges表示刷新权限变更。

##### Step4. Check the privilige of the user. `show grants for 'pi';`  
![Privilige](https://cl.ly/5cfaca2e3ba9/privilige.png)
## Delet a User  
drop user命令会删除用户以及对应的权限，执行命令后你会发现mysql.user表和mysql.db表的相应记录都消失了。 `drop user 'pi'@'%';`
## Refernece
[MySQL用户管理：添加用户、授权、删除用户](https://www.cnblogs.com/chanshuyi/p/mysql_user_mng.html)
[MySQL AddUser](https://www.cnblogs.com/pejsidney/p/8945934.html)
[MySQL Login Error](http://www.mamicode.com/info-detail-2491371.html)