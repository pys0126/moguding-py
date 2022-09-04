# 蘑菇丁/工学云自动打卡脚本
## 基础用法
完善代码第`146`行往后的信息，即可：

![image](https://user-images.githubusercontent.com/47041406/182870150-0e8c5c48-6229-4025-be22-bcbe8a1a45f3.png)

## 高级用法（自定义代理）
重写代码第`12`行的`get_proxy()`函数，如果你使用的代理池是[ProxyPool](https://github.com/jhao104/proxy_pool)且搭建在本地，那无需更改。

![image](https://user-images.githubusercontent.com/47041406/182870718-6fe931b7-f33a-4871-b127-71cea98b8afb.png)

## 如何解放双手，自动执行
- 方式一：
使用你的Linux服务器，执行`crontab -e`命令，并添加一下代码：
``` shell
#上班
00 上班时间 * * * python3 脚本存放路径 >> 日志存放路径
#下班
00 下班时间 * * * python3 脚本存放路径 >> 日志存放路径
```
![image](https://user-images.githubusercontent.com/47041406/182873546-f23ab078-3343-4b02-84bf-84278831f26c.png)
