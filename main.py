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
            queryer.all_renwen(cookie)
            if len(queryer.ls) == 0:
                logging.error("No courses found")
                time.sleep(0.5)
                continue
            queryer.all_ziran(cookie)
            break
        except:
            logging.error("Request Error")
            time.sleep(0.5)
            continue
    queryer.ls2ld(search_ls)
    loads = queryer.ld

    logging.info("Courses found")
    print(loads)
    # grab launch!
    def th(lds, i, mode):
        tool.grabber.loop_rob(cookie, lds, i, mode)
    for i in range(len(loads)):
        threading.Thread(target=th, args=(loads[i], i+1, mode)).start()

if __name__ == "__main__":
    #! Please check again the cookie and mode
    # mode\n1 - speed, 2 - slow, 3 - 捡漏, else - sep=mode
    cookie = "PHPSESSID=ST-3172428-4CJV3uA51x9vwCZvtJ3Hb-2erm4authserver2"
    mode = 3
    search_ls = [
        "软陶",
        "宇宙的奥秘",
        "民间剪纸",
        "三维建模",
        "AIGC 艺术鉴赏",
        "象棋"
    ]
    main()
