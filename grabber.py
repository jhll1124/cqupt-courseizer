import time
import logging
import requests
import threading


class Grabber:
    def __init__(self):
        self.lock = threading.Lock()

    def single_rob(self, cookie, load):
        url = "http://xk2.cqupt.edu.cn/post.php"
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": cookie,
            "Origin": "http://xk2.cqupt.edu.cn",
            "Referer": "http://xk2.cqupt.edu.cn/yxk.php",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
            "X-Requested-With": "XMLHttpRequest"
        }
        
        data = load
        response = requests.post(url, data=data, headers=headers)
        
        if response.status_code != 200:
            logging.error(f"Bad StatusCode: {response.status_code}, body: {response.text}")
            return "Error"
        
        response_data = response.json()
        res = Response.from_dict(response_data)
        
        return res.info

    def single_rob_with_info(self, cookie, load):
        logging.info(self.single_rob(cookie, load))

    def loop_rob(self, cookie, load, idx, mode=1):
        '''mode\n1 - speed, 2 - slow, 3 - 捡漏, else - sep=mode'''
        attempt = 1
        sep = 0.25
        if mode == 2:
            sep = 5
        elif mode == 3:
            sep = 100
        elif mode != 1:
            sep = mode
        logging.info(f"Course {idx} started")
        while True:
            info = self.single_rob(cookie, load)
            if info == "ok":
                logging.info(f"\033[31mCourse {idx} 抢课成功\033[0m")
                return
            else:
                logging.info(f"Attempt {idx}-{attempt}: {info}")
            time.sleep(sep)
            attempt += 1

    def high_concurrency_single_rob(self, cookie, load, idx):
        logging.info(f"Thread {idx + 1} started")
        while True:
            info = self.single_rob(cookie, load)
            if info == "ok":
                logging.info(info)
                return
            else:
                logging.info(f"Course {idx + 1}: {info}")
            time.sleep(0.25)

    def loop_rob_with_high_concurrency(self, cookie, loads):
        threads = []
        for idx, load in enumerate(loads):
            thread = threading.Thread(target=self.high_concurrency_single_rob, args=(cookie, load, idx))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        logging.info("\033[31m抢课成功\033[0m")

class Response:
    def __init__(self, code, info):
        self.code = code
        self.info = info

    @classmethod
    def from_dict(cls, data):
        return cls(code=data.get("code"), info=data.get("info"))
