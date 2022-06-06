import datetime
import math
import random
import asyncio
from threading import Thread
import instabotApi
from instabotApi import InstClient
import json


async def start_parse(ui):
    proxy_array = make_proxy_list(ui.fileWithProxy)
    instabotApi.InstClient.proxies = proxy_array
    accounts_log_pass = make_acc_with_log_pass(ui.fileWithAccountsForParse)
    accounts_to_parse = make_acc_to_parse(ui.fileToParse)

    f = open(datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S"), "w+")

    clients = get_clients(accounts_log_pass)

    results = []  # TODO проблема в том что мы сделали аккаунты с полем False но хуй знает как это запускать чтобы если акк сдох то задача отошла другому
    is_there_not_checked_acc = True  # наверное через while True и заново раздавать задачи, при этом удаляя из списка уже готовые
    try:
        while is_there_not_checked_acc:
            threads = [None] * len(clients)
            ui.change_accounts_to_parse_left(len(accounts_to_parse))
            ui.change_accounts_alive_left(len(clients))
            if len(clients) == 0 :
                ui.no_alive_acc_error()
                for res in results:
                    for e in res:
                        f.write(e + ";")
                    f.write("\n")
                f.close()
                return
            number_of_accs_for_one_user = math.floor(len(accounts_to_parse) / len(clients))

            for i in range(len(clients)):
                print(str(len(clients)) + "len clients")
                if i == len(clients) - 1:
                    print("here line 27")
                    threads[i] = Thread(target=parse_users, args=(
                        clients[i], accounts_to_parse, number_of_accs_for_one_user * i, len(accounts_to_parse) - 1, results))
                    threads[i].start()
                else:
                    threads[i] = Thread(target=parse_users, args=(
                        clients[i], accounts_to_parse, number_of_accs_for_one_user * i,
                        number_of_accs_for_one_user * i + number_of_accs_for_one_user, results))
                    threads[i].start()
            for i in range(len(threads)):
                threads[i].join()
            print("here line 34")
            is_there_not_checked_acc = False
            for acc in accounts_to_parse:
                if acc[1] or acc[2] > 2:
                    accounts_to_parse.remove(acc)
                if acc[2]>2:
                    ui.change_bad_acc()
            if len(accounts_to_parse) > 0:
                print("here line 40")
                is_there_not_checked_acc = True
            else:
                break

        for res in results:
            for e in res:
                f.write(e + ";")
            f.write("\n")

        f.close()
        print("EVERYTHING DONE")
    except Exception as g:
        ui.throw_exception(g)
        for res in results:
            for e in res:
                f.write(e + ";")
            f.write("\n")
        f.close()

def get_clients(accounts_log_pass):
    threads = [None] * len(accounts_log_pass)
    results = [None] * len(accounts_log_pass)
    for i in range(len(threads)):
        threads[i] = Thread(target=start_one_client,
                            args=(accounts_log_pass[i][0], accounts_log_pass[i][1], results, i))
        threads[i].start()

    for i in range(len(threads)):
        threads[i].join()
    clients = []
    for each in results:
        if each is None or each.user_id is None:
            print("none sorry")
        else:
            clients.append(each)
            print(each.user_id)
    return clients


def make_proxy_list(path):
    f = open(path, "r")
    data = f.read()
    array = data.split("\n")
    return array


def make_acc_to_parse(path):
    f = open(path, "r")
    data = f.read()
    array = data.split("\n")
    arr = []
    for each in array:
        if each == "": continue
        arr.append([each, False, 0])
    return arr


def make_acc_with_log_pass(path):
    f = open(path, "r")
    data = f.read()
    data = data.split("\n")
    array = []
    for each in data:
        if each == "": continue
        each = each.split("||")[0]
        a = each.split(":")
        array.append(a)

    return array


def write_data(data, file):
    return 1


def start_one_client(username, password, result, index):
    try:
        cl = InstClient(username, password)
        print("wow")
        print(cl.cl.settings)
        result[index] = cl
        # return cl
    except Exception as e:
        print("not wow")
        # return False


def parse_users(client, accounts, index_from, index_to, results):
    print(f'index from {index_from} : index to {index_to}')

    for i in range(index_from, index_to + 1):
        print(accounts[i][0])
        if accounts[i][1]:
            accounts.remove(accounts[i])
            continue
        data = parse_one_user(client, accounts[i][0])
        if not data:

            accounts[i] = [accounts[i][0], False, accounts[i][2] + 1]
            continue
        else:
            accounts[i] = [accounts[i][0], True, 0]
            results.append(data)


def parse_one_user(client: InstClient, user: str):

    try:
        data = []
        print('user : ' + user)
        userid = client.get_user_id(user.strip())
        print(user + "userid")
        bio = client.get_bio(userid)
        print(bio)
        follows = client.get_follows(userid)
        print(follows)
        followers = client.get_followers(userid)
        print(followers)
        posts = client.get_posts(userid)
        print(posts)
        data.append(bio)
        data.append(follows)
        data.append(followers)
        data.append(posts)
        return data
    except Exception as e:

        print(e)
        return False
