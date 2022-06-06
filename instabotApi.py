import random
import string

from instagrapi import Client

from requests.exceptions import ProxyError
from urllib3.exceptions import HTTPError

from instagrapi import Client
from instagrapi.exceptions import (
    ClientConnectionError,
    ClientForbiddenError,
    ClientLoginRequired,
    ClientThrottledError,
    GenericRequestError,
    PleaseWaitFewMinutes,
    RateLimitError,
    SentryBlock,
)


class InstClient:
    """instApi one client"""
    proxies = None
    cl = None
    user_id = None

    def __init__(self, login, password):
        self.cl = Client(proxy=self.next_proxy())
        try:
            self.cl.login(login, password)
        except (ProxyError, HTTPError, GenericRequestError, ClientConnectionError):
            # Network level
            self.cl.set_proxy(self.next_proxy())
        except (SentryBlock, RateLimitError, ClientThrottledError):
            # Instagram limit level
            self.cl.set_proxy(self.next_proxy())
        except (ClientLoginRequired, PleaseWaitFewMinutes, ClientForbiddenError):
            #print("logical error")
             # Logical level
            self.cl.set_proxy(self.next_proxy())

        self.user_id = self.cl.user_id  # user_id_from_username(login)

    def next_proxy(self):
        return random.choices(self.proxies)[0]

    def get_follows(self, user_id):
        user_id = user_id or self.user_id
        data = self.cl.user_following_v1(user_id)
        array = []
        for each in data:  # TODO return user_id instead of username
            array.append(each.username)
        return array

    def get_bio(self, user_id=None):  # TODO
        user_id = user_id or self.user_id
        #data = self.cl.user_info_gql(user_id)
        data = self.cl.user_info_by_username_v1(user_id)
        #data = self.cl.user_info(user_id).dict()
        array = []
        for each in data:
            if each != "":
                array.append(each)
        return array

    def get_posts(self, user_id):  # TODO
        user_id = user_id or self.user_id
        data = self.cl.user_medias_gql(user_id)

        return data

    def get_followers(self, user_id):
        user_id = user_id or self.user_id
        data = self.cl.user_followers_gql(user_id)
        array = []
        for each in data:  # TODO return user_id instead of username
            array.append(each.username)
        return array

    def get_user_id(self, username):
        if username is None:
            return None
        return self.cl.user_id_from_username(username)
