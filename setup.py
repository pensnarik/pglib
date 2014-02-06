#!/bin/env python3

import os

from distutils.core import setup

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()

def get_packages(dirs):
    packages = []
    for dir in dirs:
        for dirpath, dirnames, filenames in os.walk(dir):
            if '__init__.py' in filenames:
                packages.append(dirpath)
    return packages

setup(name = "pglib",
      description="PostgreSQL adapter for Python, based on psycopg2",
      license="""GPL""",
      version = "0.1",
      maintainer = "Andrey Zhidenkov",
      maintainer_email = "pensnarik@gmail.com",
      url = "http://unix-blog.com",
      scripts = [],
      packages = get_packages(['pglib']))
