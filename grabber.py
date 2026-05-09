import time
import logging
import requests
import threading
import sys


class Grabber:
    def __init__(self):
        self.lock = threading.Lock()
        self.success_flags = {}  # 记录每门课程是否抢课成功

    def single_rob(self, cookie, load):
        """单次抢课请求"""
        url = "http://xk1.cqupt.edu.cn/post.php"
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": cookie,
            "Origin": "http://xk1.cqupt.edu.cn",
            "Referer": "http://xk1.cqupt.edu.cn/yxk.php",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
            "X-Requested-With": "XMLHttpRequest"
        }
        
        try:
            response = requests.post(url, data=load, headers=headers, timeout=5)
            
            if response.status_code != 200:
                logging.warning(f"HTTP {response.status_code}")
                return "网络错误"
            
            try:
                response_data = response.json()
                res = Response.from_dict(response_data)
                return res.info
            except ValueError:
                logging.warning("响应解析失败")
                return "响应格式错误"
                
        except requests.exceptions.Timeout:
            return "请求超时"
        except requests.exceptions.ConnectionError:
            return "连接失败"
        except requests.exceptions.RequestException:
            return "请求异常"
        except Exception as e:
            logging.error(f"未知错误: {e}")
            return "未知错误"

    def loop_rob(self, cookie, load, idx, mode=1):
        """循环抢课
        mode: 1-快速(0.25s), 2-慢速(5s), 3-捡漏(100s), 其他-自定义间隔(秒)
        """
        attempt = 1
        interval = 0.25
        
        if mode == 2:
            interval = 5
        elif mode == 3:
            interval = 100
        elif mode != 1:
            interval = mode
        
        # 初始化该课程的成功标志
        with self.lock:
            if idx not in self.success_flags:
                self.success_flags[idx] = False
            
        logging.info(f"课程 {idx} 开始抢课，间隔: {interval}秒")
        sys.stdout.flush()
        
        while True:
            # 检查是否已经抢到
            with self.lock:
                if self.success_flags[idx]:
                    logging.info(f"课程 {idx} 已被其他线程抢到，本线程退出")
                    sys.stdout.flush()
                    return
            
            info = self.single_rob(cookie, load)
            
            if info == "ok":
                with self.lock:
                    if not self.success_flags[idx]:
                        self.success_flags[idx] = True
                        logging.info(f"[成功] 课程 {idx} 抢课成功！")
                        sys.stdout.flush()
                return
            else:
                logging.debug(f"课程 {idx} 第 {attempt} 次尝试: {info}")
                
            time.sleep(interval)
            attempt += 1

    def high_concurrency_single_rob(self, cookie, load, idx):
        """高并发单次抢课"""
        # 初始化该课程的成功标志
        with self.lock:
            if idx not in self.success_flags:
                self.success_flags[idx] = False
                
        logging.info(f"线程 {idx + 1} 已启动")
        sys.stdout.flush()
        
        while True:
            # 检查是否已经抢到
            with self.lock:
                if self.success_flags[idx]:
                    logging.info(f"课程 {idx + 1} 已被其他线程抢到，本线程退出")
                    sys.stdout.flush()
                    return
                    
            info = self.single_rob(cookie, load)
            
            if info == "ok":
                with self.lock:
                    if not self.success_flags[idx]:
                        self.success_flags[idx] = True
                        logging.info(f"[成功] 课程 {idx + 1} 抢课成功！")
                        sys.stdout.flush()
                return
            else:
                logging.debug(f"课程 {idx + 1}: {info}")
                
            time.sleep(0.25)

    def loop_rob_with_high_concurrency(self, cookie, loads):
        """高并发循环抢课"""
        threads = []
        for idx, load in enumerate(loads):
            thread = threading.Thread(target=self.high_concurrency_single_rob, args=(cookie, load, idx))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        success_count = sum(1 for flag in self.success_flags.values() if flag)
        logging.info(f"[完成] 共成功抢到 {success_count} 门课程")
        sys.stdout.flush()


class Response:
    """抢课响应数据类"""
    def __init__(self, code, info):
        self.code = code
        self.info = info

    @classmethod
    def from_dict(cls, data):
        return cls(code=data.get("code"), info=data.get("info"))
