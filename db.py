# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 05:47:43 2022

@author: andya
"""

import sqlite3
import os

here = os.path.abspath(os.path.dirname(__file__))
SCHEMA_FILE = os.path.join(here, "schema.sql")

def get_schema():
    with open(SCHEMA_FILE) as f:
        return f.read()

def get_connection(file_name):
    if not os.path.exists(file_name):
        with sqlite3.connect(file_name) as conn:
            cur = conn.cursor()
            cur.executescript(get_schema())

    return sqlite3.connect(file_name)