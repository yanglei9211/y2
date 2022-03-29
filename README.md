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
