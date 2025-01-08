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
    print("\033[31m[Tip] Please check again the cookie, \
search_ls and connection to the host. \
Because of the multi-threading, \
the program cannot be stopped unless forcefully terminated.\033[0m")
    logging.basicConfig(level=logging.INFO)
    tool = miHomo()

    queryer = tool.queryer
    # query for loop
    while True:
        queryer.all_renwen(cookie)
        if queryer.ls.__len__() == 0:
            logging.error("No courses found")
            time.sleep(0.5)
            continue
        queryer.all_ziran(cookie)
        break
    queryer.ls2ld(search_ls)
    loads = queryer.ld

    logging.info("Courses found")
    print(loads)
    # grab normally
    def th(lds):
        tool.grabber.loop_rob(cookie, lds)
    for i in range(loads.__len__()):
        threading.Thread(target=th, args=(loads[i],)).start()

if __name__ == "__main__":
    # Please enter your cookie here
    cookie = "PHPSESSID=ST-911652-ithrpm06JjhZEQN5hIQ6Vo-Uyzgauthserver2"
    search_ls = [
        "宇宙的奥秘",
        "中国民间剪纸艺术",
        "职场心理学",
        "高等数学"
    ]
    main()
