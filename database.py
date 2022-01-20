import pandas as pd 
import datetime 
import time 
import pytz 
import numpy 
import json 
import mysql.connector

# ADMIN DATA


admin = {
    'user_name': 'IngenHouzs',
    'password':'ILoveIndonesia'
}

def connect_db(machine): 
    global local_item_list
    global dropbox_items 
    global dtbs 
    global dtbs_cursor  
    global dtbs_cursor_codelistings
    global transaction_code_listings 
    global marker 
    global clientside_dtbs
    global clientdtbs_cursor
    dtbs = mysql.connector.connect(
        host = machine,
        user = 'root',
        password ='KonohaGakure123',
        database = 'database transaction general'
    )  
    clientside_dtbs = mysql.connector.connect(
        host = machine,
        user = 'root',
        password ='KonohaGakure123',
        database = 'client details database'
    )  
    dtbs_cursor = dtbs.cursor()  
    dtbs_cursor.execute('SELECT * FROM `item list`') 
    local_item_list = list(zip(*dtbs_cursor.fetchall()))   
    marker = machine 
    clientdtbs_cursor = clientside_dtbs.cursor()

connect_db('127.0.0.1')

dropbox_items = [(items + '-' + str(local_item_list[1][local_item_list[0].index(items)]))for items in local_item_list[0]] 

