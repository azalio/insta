#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from pymongo import MongoClient
from bson import ObjectId


def get_urls(account):
    data = {}
    url = 'http://instagram.com/{0}/media'.format(account)
    media = requests.get(url).json()
    for item in media["items"]:
        data[item['created_time']] = item['images']['standard_resolution']['url']
    return data


def mongo_connect():
    client = MongoClient('localhost', 27017)
    db = client['instagramm']
    collection = db['media']
    return client, db, collection


def check_id(id, collection):
    if collection.find({"_id": id}).count() == 1:
        return False
    else:
        return True


def main():
    accounts = ['nakedfeed']

    client, db, collection = mongo_connect()

    for account in accounts:
        data = get_urls(account)
        for date in data:
            id = ObjectId(str(data[date][-1:-13:-1]))
            if check_id(id, collection):
                post = {"_id": id,
                        "author": account,
                        "date": date,
                        "url": data[date]}
                collection.insert_one(post)


if __name__ == '__main__':
    main()
