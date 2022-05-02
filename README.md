配置文件样例:  
[default]  

send_error_msg=0    # err日志是否机器人输出

msg_robot=   

[mongodb]  

mongodb_url=mongodb://

replica_set = 

w_value = 1

wtimeout = 5000


[mq]  

mq_host = amqp://

log_mq_name = 



依赖:

pip3 install -r requirements.txt


运行:

python3 main.py --port=xxx, --debug=0/1



目录结构:

/

--controller: 控制器,业务路由

--bl: 业务逻辑处理

--model: 模块

----db_model: db封装

----http_model: 外部服务封装

--script: 脚本

--util: 工具类

----auth.py 权限相关

----errors.py 异常处理

----escape.py 格式编码

----logger.py 日志模块

----mq.py 消息队列

--app_define.py  全局常量定义

--setting.py 配置

--main.py 入口文件




