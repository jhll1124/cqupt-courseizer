import logging
import threading
import time
import sys
import queryer
import grabber
from config_loader import ConfigLoader


class miHomo:
    def __init__(self):
        self.queryer = queryer.Queryer()
        self.grabber = grabber.Grabber()

    def new(self):
        return self

def main():
    """主函数：加载配置并启动抢课"""
    # 加载配置文件
    config_loader = ConfigLoader("config.yml")
    config = config_loader.load()
    
    # 从配置文件获取参数
    cookie = config_loader.get_cookie()
    mode = config_loader.get_mode()
    search_ls = config_loader.get_courses()
    
    # 设置日志级别 - 强制输出到stdout
    logging.basicConfig(
        level=config_loader.get_log_level(),
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True
    )
    
    # 立即刷新输出
    sys.stdout.flush()
    
    logging.info(f"已加载配置文件: config.yml")
    logging.info(f"抢课模式: {mode}")
    logging.info(f"目标课程数量: {len(search_ls)}")
    sys.stdout.flush()
    
    tool = miHomo()

    queryer = tool.queryer
    # query for loop - 持续查询直到获取到课程数据
    while True:
        try:
            logging.info("开始查询人文课程...")
            queryer.all_renwen(cookie)
                
            logging.info("开始查询自然课程...")
            queryer.all_ziran(cookie)
                
            logging.info("开始查询班级课程...")
            queryer.all_banji(cookie)
            
            if len(queryer.ls) == 0:
                logging.warning("未查询到任何课程，请检查Cookie是否有效，0.5秒后重试...")
                sys.stdout.flush()
                time.sleep(0.5)
                continue
            
            break
            
        except requests.exceptions.RequestException as e:
            logging.warning(f"网络请求失败: {e}，0.5秒后重试...")
            sys.stdout.flush()
            time.sleep(0.5)
            continue
                
        except Exception as e:
            logging.warning(f"查询过程发生错误: {e}，0.5秒后重试...")
            sys.stdout.flush()
            time.sleep(0.5)
            continue
    
    logging.info(f"查询到课程总数: {len(queryer.ls)}")
    queryer.ls2ld(search_ls)
    loads = queryer.ld

    if len(loads) == 0:
        logging.error(f"没有找到包含关键词 {search_ls} 的课程，请检查关键词是否正确")
        logging.error("程序退出")
        sys.stdout.flush()
        sys.exit(1)

    logging.info(f"找到匹配课程数量: {len(loads)}")
    for i, load in enumerate(loads):
        logging.info(f"课程 {i+1}: {load}")
    
    sys.stdout.flush()
    
    # 启动多线程抢课
    logging.info("=" * 50)
    logging.info("开始抢课，多线程运行中...")
    logging.info("提示：由于多线程运行，程序只能通过强制终止来停止")
    logging.info("=" * 50)
    sys.stdout.flush()
    
    def thread_worker(course_data, course_idx, grab_mode):
        """线程工作函数"""
        tool.grabber.loop_rob(cookie, course_data, course_idx, grab_mode)
    
    # 为每门课程启动线程
    for i in range(len(loads)):
        threading.Thread(
            target=thread_worker, 
            args=(loads[i], i+1, mode),
            daemon=True
        ).start()
    
    # 主线程保持运行
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("\n程序被用户中断")
        sys.stdout.flush()
        sys.exit(0)

if __name__ == "__main__":
    main()
