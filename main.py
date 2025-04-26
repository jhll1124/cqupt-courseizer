import logging
import threading
import time
import queryer
import grabber


class miHomo:
    def __init__(self):
        self.queryer = queryer.Queryer()
        self.grabber = grabber.Grabber()

    def new(self):
        return self

def main():
    '''[Tip] Please check again the cookie, \
search_ls and connection to the host. \
Because of the multi-threading, \
the program cannot be stopped unless forcefully terminated.'''
    logging.basicConfig(level=logging.INFO)
    tool = miHomo()

    queryer = tool.queryer
    # query for loop  
    while True:
        try:
            logging.info("开始查询人文课程...")
            queryer.all_renwen(cookie)
            if queryer.ls.__len__() == 0:
                logging.error("未找到人文课程，请检查Cookie和网络连接")
                time.sleep(0.5)
                continue
                
            logging.info("开始查询自然课程...")
            queryer.all_ziran(cookie)
            if queryer.ls.__len__() == 0:
                logging.error("未找到自然课程，请检查Cookie和网络连接")
                time.sleep(0.5)
                continue
                
            logging.info("开始查询班级课程...")
            queryer.all_banji(cookie)
            if queryer.ls.__len__() == 0:
                logging.error("未找到班级课程，请检查Cookie和网络连接")
                time.sleep(0.5)
                continue
                
            break
        except:
            logging.error("Request Error")
            time.sleep(0.5)
            continue
    
    logging.info(f"查询到课程总数: {len(queryer.ls)}")
    queryer.ls2ld(search_ls)
    loads = queryer.ld

    if len(loads) == 0:
        logging.error(f"没有找到包含关键词 {search_ls} 的课程，请检查关键词是否正确")
        return

    logging.info(f"找到匹配课程数量: {len(loads)}")
    for i, load in enumerate(loads):
        logging.info(f"课程 {i+1}: {load}")
    
    
    # grab launch!
    def th(lds, i, mode):
        tool.grabber.loop_rob(cookie, lds, i, mode)
    for i in range(len(loads)):
        threading.Thread(target=th, args=(loads[i], i+1, mode)).start()

if __name__ == "__main__":
    #! 请检查cookie是否有效，cookie通常会在一段时间后过期
    # 格式应该为: PHPSESSID=xxxxx
    cookie = "PHPSESSID=ST-3465842-xaFBpis9iKxSP-TYZzxHeMB-dSgauthserver1"
    mode = 1
    # 设置要搜索的课程关键词
    search_ls = [
        "知识产权保护",
        "汇编语言程序设计",
        "张杰",
        "形势与政策"
    ]
    
    main()
