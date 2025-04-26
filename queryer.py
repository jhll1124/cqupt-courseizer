import requests
import logging
import time


class Queryer:
    def __init__(self):
        self.ls = []
        self.ld = []

    def request(self, query_str, cookie):
        # 添加错误处理和重试机制
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                url = f"http://xk2.cqupt.edu.cn/json-data-yxk.php?type={query_str}"
                # url = f"https://jhll.fun:4430/file/json-data-yxk_jcts{query_str}.json"
                
                headers = {
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                    "Cache-Control": "max-age=0",
                    "Connection": "keep-alive",
                    "Cookie": cookie,
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36 Edg/101.0.1210.39"
                }

                logging.info(f"尝试请求: {url}")
                response = requests.get(url, headers=headers, timeout=10)  # 添加超时设置
                
                if response.status_code != 200:
                    logging.error(f"Bad StatusCode: {response.status_code}, body: {response.text}")
                    retry_count += 1
                    if retry_count < max_retries:
                        logging.info(f"重试请求 ({retry_count}/{max_retries})...")
                        time.sleep(1)  # 等待1秒后重试
                        continue
                    return None
                
                # 检查响应内容是否为空或非预期内容
                if not response.text or len(response.text) < 10:
                    logging.error(f"响应内容异常: {response.text}")
                    retry_count += 1
                    if retry_count < max_retries:
                        logging.info(f"重试请求 ({retry_count}/{max_retries})...")
                        time.sleep(1)
                        continue
                    return None
                
                try:
                    return response.json()
                except Exception as e:
                    logging.error(f"JSON解析失败: {e}, 响应内容: {response.text}")
                    retry_count += 1
                    if retry_count < max_retries:
                        logging.info(f"重试请求 ({retry_count}/{max_retries})...")
                        time.sleep(1)
                        continue
                    return None
                    
            except requests.exceptions.RequestException as e:
                logging.error(f"请求异常: {e}")
                retry_count += 1
                if retry_count < max_retries:
                    logging.info(f"重试请求 ({retry_count}/{max_retries})...")
                    time.sleep(1)
                    continue
                return None
        
        return None

    def all_renwen(self, cookie):
        body_data = self.request("jctsRw", cookie)
        if body_data:
            class_info = ClassInfos.from_dict(body_data)
            for item in class_info.data:
                load = self.create_load_string(item)
                # self.write2file("./output_renwen.txt", load)
                self.write2ls(load)

    def all_ziran(self, cookie):
        body_data = self.request("jctsZr", cookie)
        if body_data:
            class_info = ClassInfos.from_dict(body_data)
            for item in class_info.data:
                load = self.create_load_string(item)
                # self.write2file("./output_ziran.txt", load)
                self.write2ls(load)

    def all_banji(self, cookie):
        body_data = self.request("Bj", cookie)
        if body_data:
            class_info = ClassInfos.from_dict(body_data)
            for item in class_info.data:
                load = self.create_load_string(item)
                # self.write2file("./output_banji.txt", load)
                self.write2ls(load)

    def create_load_string(self, item):
        load_string = f"xnxq={item.xnxq}&jxb={item.jxb}&kchb={item.kcbh}&kcmc={item.kcmc}&xf={item.xf}&teaname={item.tea_name}&rslimit={item.rs_limit}&kclb={item.kclb}&kchtye={item.kch_type}&memo={item.memo}"
        return load_string

    def write2file(self, file_path, content):
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(content + "\n")

    def write2ls(self, content):
        self.ls.append(content)
    
    def ls2ld(self, search_str_ls):
        for j in range(search_str_ls.__len__()):
            for i in self.ls:
                if search_str_ls[j] in i:
                    self.ld.append(i)

class ClassInfos:
    def __init__(self, code, info, data):
        self.code = code
        self.info = info
        self.data = data  # List of ClassInfoItem objects

    @classmethod
    def from_dict(cls, data):
        # Parsing the data into a ClassInfos object
        data_items = [ClassInfoItem.from_dict(item) for item in data['data']]
        return cls(code=data['code'], info=data['info'], data=data_items)


class ClassInfoItem:
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
