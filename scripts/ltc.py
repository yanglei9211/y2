from locust import HttpUser, task, HttpLocust, TaskSet, between
import os

class Pstart(HttpUser):
    min_wait = 100
    max_wait = 500

    host = 'http://127.0.0.1:8888'

    def on_start(self):
        print("start")

    @task(1)
    def check_sub_post_go(self):
        header = {"Content-Type": "application/json"}
        data = {}
        # self.client.post('/api/y2/test/sub?x=100000&y=7', data=data, headers=header)
        self.client.post('/sub?x=100000&y=7', data=data, headers=header)

    @task(1)
    def check_sub_post_fast(self):
        header = {"Content-Type": "application/json"}
        data = {}
        self.client.post('/api/y2/test/sub?x=100000&y=7', data=data, headers=header)
        # self.client.post('/sub?x=100000&y=7', data=data, headers=header)

    @task(1)
    def check_sub_post_tor(self):
        header = {"Content-Type": "application/json"}
        data = {}
        # self.client.post('/api/y2/test/sub?x=100000&y=7', data=data, headers=header)
        self.client.post('/sub?x=100000&y=7', data=data, headers=header)


def excute_sc():
    os.system(
        "locust -f ltc.py --headless -u 10 -t 10s "
        "--loglevel=INFO "
        "--logfile=test.log --host=http://127.0.0.1:8888")
