PyMySQL
=======

 contents: Table of Contents
   local

This package contains a pure-Python MySQL client library. The goal of PyMySQL
is to be a drop-in replacement for MySQLdb and work on CPython, PyPy and IronPython.

NOTE: PyMySQL doesn't support low level APIs `_mysql` provides like `data_seek`,
`store_result`, and `use_result`. You should use high level APIs defined in `PEP 249`_.
But some APIs like `autocommit` and `ping` are supported because `PEP 249`_ doesn't cover
their usecase.

 `PEP 249`: https://www.python.org/dev/peps/pep-0249/

Requirements
-------------

* Python -- one of the following:

  - CPython_ >= 2.6 or >= 3.3
  - PyPy_ >= 4.0
  - IronPython_ 2.7

* MySQL Server -- one of the following:

  - MySQL_ >= 4.1  (tested with only 5.5~)
  - MariaDB_ >= 5.1

 CPython: http://www.python.org/  
 PyPy: http://pypy.org/  
 IronPython: http://ironpython.net/  
 MySQL: http://www.mysql.com/  
 MariaDB: https://mariadb.org/  


Installation On RaspberryPi
------------

The last stable release is available on PyPI and can be installed with ``pip``::

1. Install the MySQL
```
sudo apt-get update
sudo apt-get install mysql-server
sudo apt-get upgrade
```
2. Install the python-mysql interface
```
sudo pip install --upgrade pip
sudo pip install PyMySQL
```


Documentation
-------------

Documentation is available online: http://pymysql.readthedocs.io/

For support, please refer to the `StackOverflow
<http://stackoverflow.com/questions/tagged/pymysql>`_.

Example
-------

The following examples make use of a simple table

 code: sql
```
   CREATE TABLE `users` (
       `id` int(11) NOT NULL AUTO_INCREMENT,
       `email` varchar(255) COLLATE utf8_bin NOT NULL,
       `password` varchar(255) COLLATE utf8_bin NOT NULL,
       PRIMARY KEY (`id`)
   ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
   AUTO_INCREMENT=1 ;
```

 code: python

    import pymysql.cursors

    # Connect to the database
    connection = pymysql.connect(host='localhost',
                                 user='user',
                                 password='passwd',
                                 db='db',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
            cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()

        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
            cursor.execute(sql, ('webmaster@python.org',))
            result = cursor.fetchone()
            print(result)
    finally:
        connection.close()

This example will print:

 code: python

    {'password': 'very-secret', 'id': 1}

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
1.PrivilegesCode表示授予的权限类型，常用的有以下几种类型：
* all privileges：所有权限。
* select：读取权限。
* delete：删除权限。
* update：更新权限。
* create：创建权限。
* drop：删除数据库、数据表权限。

2.DbName.tableName表示授予权限的具体库或表，常用的有以下几种选项：
* .：授予该数据库服务器所有数据库的权限。
* dbName.*：授予dbName数据库所有表的权限。
* dbName.dbTable：授予数据库dbName中dbTable表的权限。

3.Username@host表示授予的用户以及允许该用户登录的IP地址。其中Host有以下几种类型：
* localhost：只允许该用户在本地登录，不能远程登录。
* %：允许在除本机之外的任何一台机器远程登录。
* 192.168.52.32：具体的IP表示只允许该用户从特定IP登录。
* password指定该用户登录时的页面。
* flush privileges表示刷新权限变更。
##### Step4. Check the privilige of the user. `show grants for 'pi';`  
![Privilige](https://cl.ly/5cfaca2e3ba9/privilige.png)
## Delet a User  
drop user命令会删除用户以及对应的权限，执行命令后你会发现mysql.user表和mysql.db表的相应记录都消失了。   
`drop user 'pi'@'%';`
## Refernece
[MySQL](https://github.com/mm1994uestc/PyMySQL)  
[MySQL用户管理：添加用户、授权、删除用户](https://www.cnblogs.com/chanshuyi/p/mysql_user_mng.html)  
[MySQL AddUser](https://www.cnblogs.com/pejsidney/p/8945934.html)  
[MySQL Login Error](http://www.mamicode.com/info-detail-2491371.html)   

Resources
---------

DB-API 2.0: http://www.python.org/dev/peps/pep-0249

MySQL Reference Manuals: http://dev.mysql.com/doc/

MySQL client/server protocol:
http://dev.mysql.com/doc/internals/en/client-server-protocol.html

PyMySQL mailing list: https://groups.google.com/forum/#!forum/pymysql-users

License
-------

PyMySQL is released under the MIT License. See LICENSE for more information.
