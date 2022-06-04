from instabotApi import InstClient
from UI import UI


def start(async_loop):
    ui = UI(async_loop)
    # cl = InstClient("legion0188", "tornadotop09")
    # userid = cl.get_user_id("lilknoppa")
    # print(userid)
    # print(cl.get_posts(userid))


if __name__ == '__main__':
    async_loop = asyncio.get_event_loop()
    start(async_loop)
