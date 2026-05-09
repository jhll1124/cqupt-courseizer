import requests
import logging
import time


class Queryer:
    def __init__(self):
        self.ls = []
        self.ld = []

    def request(self, query_str, cookie):
        """发送HTTP请求获取课程数据"""
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                url = f"http://xk1.cqupt.edu.cn/json-data-yxk.php?type={query_str}"
                
                headers = {
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                    "Cache-Control": "max-age=0",
                    "Connection": "keep-alive",
                    "Cookie": cookie,
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36 Edg/101.0.1210.39"
                }

                logging.info(f"请求: {query_str}")
                response = requests.get(url, headers=headers, timeout=3)
                
                if response.status_code != 200:
                    logging.warning(f"HTTP {response.status_code}")
                    retry_count += 1
                    if retry_count < max_retries:
                        time.sleep(0.5)
                        continue
                    return None
                
                if not response.text or len(response.text) < 10:
                    logging.warning(f"响应内容异常")
                    retry_count += 1
                    if retry_count < max_retries:
                        time.sleep(0.5)
                        continue
                    return None
                
                try:
                    return response.json()
                except ValueError as e:
                    logging.warning(f"JSON解析失败: {e}")
                    retry_count += 1
                    if retry_count < max_retries:
                        time.sleep(0.5)
                        continue
                    return None
                    
            except requests.exceptions.Timeout:
                logging.warning(f"请求超时 ({query_str})")
                retry_count += 1
                if retry_count < max_retries:
                    time.sleep(0.5)
                    continue
                return None
                
            except requests.exceptions.ConnectionError:
                logging.warning(f"连接失败 ({query_str})")
                retry_count += 1
                if retry_count < max_retries:
                    time.sleep(0.5)
                    continue
                return None
                
            except requests.exceptions.RequestException as e:
                logging.warning(f"请求异常: {e}")
                retry_count += 1
                if retry_count < max_retries:
                    time.sleep(0.5)
                    continue
                return None
        
        return None

    def all_renwen(self, cookie):
        """查询人文社会科学课程"""
        body_data = self.request("jctsRw", cookie)
        if body_data:
            try:
                class_info = ClassInfos.from_dict(body_data)
                for item in class_info.data:
                    load = self.create_load_string(item)
                    self.write2ls(load)
                logging.info(f"人文课程: {len(class_info.data)} 门")
            except (KeyError, TypeError) as e:
                logging.error(f"解析失败: {e}")

    def all_ziran(self, cookie):
        """查询自然科学与技术课程"""
        body_data = self.request("jctsZr", cookie)
        if body_data:
            try:
                class_info = ClassInfos.from_dict(body_data)
                for item in class_info.data:
                    load = self.create_load_string(item)
                    self.write2ls(load)
                logging.info(f"自然课程: {len(class_info.data)} 门")
            except (KeyError, TypeError) as e:
                logging.error(f"解析失败: {e}")

    def all_banji(self, cookie):
        """查询班级课程"""
        body_data = self.request("bj", cookie)
        if body_data:
            try:
                class_info = ClassInfos.from_dict(body_data)
                for item in class_info.data:
                    load = self.create_load_string(item)
                    self.write2ls(load)
                logging.info(f"班级课程: {len(class_info.data)} 门")
            except (KeyError, TypeError) as e:
                logging.error(f"解析失败: {e}")

    def create_load_string(self, item):
        load_string = f"xnxq={item.xnxq}&jxb={item.jxb}&kchb={item.kcbh}&kcmc={item.kcmc}&xf={item.xf}&teaname={item.tea_name}&rslimit={item.rs_limit}&kclb={item.kclb}&kchtye={item.kch_type}&memo={item.memo}"
        return load_string

    def write2file(self, file_path, content):
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(content + "\n")

    def write2ls(self, content):
        """将课程信息添加到列表"""
        self.ls.append(content)
    
    def ls2ld(self, search_keywords):
        """根据关键词筛选课程"""
        for keyword in search_keywords:
            for course in self.ls:
                if keyword in course and course not in self.ld:
                    self.ld.append(course)

class ClassInfos:
    """课程信息集合类"""
    def __init__(self, code, info, data):
        self.code = code
        self.info = info
        self.data = data

    @classmethod
    def from_dict(cls, data):
        data_items = [ClassInfoItem.from_dict(item) for item in data['data']]
        return cls(code=data['code'], info=data['info'], data=data_items)


class ClassInfoItem:
    """单个课程信息类"""
    def __init__(self, xnxq, jxb, kcbh, kcmc, xf, tea_name, rs_limit, kclb, kch_type, memo):
        self.xnxq = xnxq
        self.jxb = jxb
        self.kcbh = kcbh
        self.kcmc = kcmc
        self.xf = xf
        self.tea_name = tea_name
        self.rs_limit = rs_limit
        self.kclb = kclb
        self.kch_type = kch_type
        self.memo = memo

    @classmethod
    def from_dict(cls, item):
        return cls(
            xnxq=item['xnxq'],
            jxb=item['jxb'],
            kcbh=item['kcbh'],
            kcmc=item['kcmc'],
            xf=item['xf'],
            tea_name=item['teaName'],
            rs_limit=item['rsLimit'],
            kclb=item['kclb'],
            kch_type=item['kchType'],
            memo=item['memo']
        )
