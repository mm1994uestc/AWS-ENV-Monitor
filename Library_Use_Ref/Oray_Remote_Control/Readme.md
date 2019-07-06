# How to Control the raspberry remotely?
### Step1:我们使用Oray的花生壳服务，首先在下面的网站下载树莓派对应的花生壳软件:
[Oray软件下载](https://hsk.oray.com/download)
### Step2:使用如下的命令安装下载完成的花生壳软件:
`sudo dpkg -i phddns_3.0.3_systemd.deb`
这里大家根据自己的软件版本对指令进行修改即可
### Step3:安装完成之后我们就能够得到如下的结果，我们将设备的SN码和默认的密码保存下来：
![Install success](https://github.com/mm1994uestc/AWS-ENV-Monitor/blob/master/Library_Use_Ref/Oray_Remote_Control/Install_success.png)
### Step4:接下来注册一个Oray网站的账号，登陆创建控制台添加内网映射设备：
添加的域名是Oray自动分配给你的，之后远程访问的IP地址基于这个域名，如果是远程ssh到主机请选用通用应用，外网端口可以选择动态端口，这样就是免费的，你也可以购买固定端口，接下来就是内网主机选择，我们通过路由器查看树莓派IP地址，将地址填入Oray服务即可，端口号选择22
### Step5:在树莓派端启动Oray花生壳软件：
`sudo service phddns start`
### Step6:如果还需要将树莓派做为网页服务器，我们还可以将设备的80端口映射出来，映射的方法与之前相同！
