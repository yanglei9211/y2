配置文件样例:  
[default]  
send_error_msg=0    # err日志是否机器人输出
msg_robot=migrate_school_paper   

[mongodb]  
mongodb_url=mongodb://klx_developer:klx_developer@10.198.16.22:33012,10.198.16.23:33012/admin
replica_set = 33012
w_value = 1
wtimeout = 5000

[mq]  
mq_host = amqp://guest:o2o@10.198.22.193
log_mq_name = mq_key_wx_message


依赖:
pip3 install -r requirements.txt

运行:
python3 main.py --port=xxx, --debug=0/1