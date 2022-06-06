import asyncio
import random
from instagrapi import Client
from instabotApi import InstClient

def get_json():
    return 1


def get_smth():
    f = open("test.txt", "r")
    data = f.read().split("||:|")
    ig_www_claim = data[1].strip()
    data = data[0].split("||")
    (login, password) = data[0].split(":")
    data = data[1].split("|")
    data1= data[0].split(";")
    data2 = data[1].split(";")
    dsuserid= data2[3].split("=")[1]
    sessionid = data2[len(data2)-1].split("=")[1]
    cl = Client()

    cl.login_by_sessionid(sessionid)
    cl.user_id
    print(data)


if __name__ == '__main__':
    get_smth()