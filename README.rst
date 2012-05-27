Randvkmessage
********

A python console tools for getting random messages from wall vk.com users
Created by Sergey Romanov <rsergom@yandex.ru>

Installation
************
>>> python setup.py install

Basic Usage
************
>>> import randvkmessage
>>> message = randvkmessage.RandomVKMessage()
>>> message.start()

Optional Usage
************
>>> import randvkmessage
>>> message = randvkmessage.RandomVKMessage(login="vklogin",password="vkpassword",decode='cp1251',wait=4,count=10)
>>> message.start()
