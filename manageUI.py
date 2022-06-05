import datetime
import random
import asyncio
import instabotApi
from instabotApi import InstClient


async def start_parse(ui):
    proxy_array = make_proxy_list(ui.fileWithProxy)
    instabotApi.InstClient.proxies = proxy_array
    accounts_log_pass = make_acc_with_log_pass(ui.fileWithAccountsForParse)
    accounts_to_parse = make_acc_to_parse(ui.fileToParse)
    # f = open(datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S"), "w+")
    tasks = []
    for acc in accounts_log_pass:
        print(acc[0] + " " + acc[1])
        tasks.append(asyncio.create_task(start_one_client(acc[0], acc[1])))
    results = []
    # for task in tasks:
    #     res = await task
    #     print(res)
    #     if res:
    #         results.append(res)
    #
    # print(str(len(results)) + " yoooo")


async def get_clients():
    return 1


def make_proxy_list(path):
    f = open(path, "r")
    data = f.read()
    array = data.split("\n")
    return array


def make_acc_to_parse(path):
    f = open(path, "r")
    data = f.read()
    array = data.split("\n")
    return array


def make_acc_with_log_pass(path):
    f = open(path, "r")
    data = f.read()
    data = data.split("\n")
    array = []
    for each in data:
        if each == "": continue
        a = each.split(":")
        array.append(a)

    return array


def write_data(data, file):
    return 1


async def start_one_client(username, password):
    try:
        cl = InstClient(username, password)
        print("WOW")
        return cl
    except Exception as e:
        print(e)
        print("NOT WOW")
        return False


def parse_user(username, client):
    return 1
