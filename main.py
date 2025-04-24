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
            if queryer.ls.__len__() == 0:
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
    # grab normally
    def th(lds):
        tool.grabber.loop_rob(cookie, lds, 3) # mode
    for i in range(loads.__len__()):
        threading.Thread(target=th, args=(loads,)).start()

if __name__ == "__main__":
    #! Please check again the cookie and mode
    cookie = "PHPSESSID=ST-3166783-5rd0EWOZrKPJ49z9WD0WxcPjKhsauthserver2"
    search_ls = [
        "软陶",
        "宇宙的奥秘",
        "职场心理学",
        "民间剪纸",
        "三维建模",
        "AIGC 艺术鉴赏",
        "象棋"
    ]
    main()
