import os
from setuptools import setup

def read(fname): #TODO around readme
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "randvkmessage",
    version = "0.1",
    author = "Sergey Romanov",
    author_email = "rsergom@yandex.ru",
    description = ("Random messages from walls vk users"),
    license = "BSD",
    keywords = "vk messages",
    url = "need url",
    packages=['randvkmessage', 'test'],
    long_description=read('README.rst'),
    classifiers=[
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)