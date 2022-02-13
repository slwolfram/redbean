import pytest
import sqlite3
import os
import psutil
import time
import requests
import logging
from update_redbean import recurse_filetree


redbean_fp = 'redbean.zip'
suppress_logs = False
port = 5000
kill_after = False
url = f'http://localhost:{port}'


@pytest.fixture(scope='session', autouse=True)
def redbean():

    global url
    # pid = None
    log_cmd = 'i>/dev/null 2>' if suppress_logs else ''
    # os.system(f"cp {redbean_fp} redbean_test.zip")
    # os.system(f"mv .init.lua .tmp.init.lua")
    # os.system(f"unzip redbean_test.zip .init.lua -d ./ {log_cmd}")
    # with open('.init.lua', 'r') as f:
    #     init_lua = f.read()
    # init_lua = init_lua.replace('db = sqlite3.open_memory(',
    #                             'db = sqlite3.open(\'redbean.test.db\')\n-- db = sqlite.open_memory(')
    # init_lua = init_lua.replace('db = sqlite3.open(',
    #                             'db = sqlite3.open_memory()\n-- sqlite3.open(')
    # with open('.init.lua', 'w') as f:
    #     f.write(init_lua)
    # os.system(f"zip redbean_test.zip .init.lua {log_cmd}")
    start_cmd = f'./redbean.zip -p {port} {log_cmd} &'
    # pid = None
    try:
        recurse_filetree('./')
        os.system(start_cmd)
        time.sleep(3)
    #     res = requests.get(url + '/api/boards.lua')
    #     logging.info(u'Started redbean.\n{url}')
    #     for proc in psutil.process_iter():
    #         if 'redbean.zip' in proc.name():
    #             pid = proc.pid
    #             print(pid)

    #     print(res.content)
    #     json = res.json()
    #     print(res.json())
    #     assert len(json) == 0
    except:
        logging.exception("""\nUnable to start redbean. 
        Probably that it is b/c it's already running, so we will continue running the tests.\n""")
    #     pass
    ## end setup

    ## truncate tables
    # os.system('touch redbean.test.db')
    # cnxn = sqlite3.connect('redbean.test.db')
    # cur = cnxn.cursor()
        # create tables if they don't already exist
    # cur.execute('''
    # CREATE TABLE IF NOT EXISTS boards (
    #   id INTEGER PRIMARY KEY,
    #   name TEXT,
    #   description TEXT,
    #   created_user TEXT,
    #   created_dttm TEXT,
    #   updated_user TEXT,
    #   updated_dttm TEXT,
    #   delete_flg TEXT
    # )
    # ''')
        # truncate
    # cur.execute('''
    # DELETE FROM boards
    # ''')
    # cur.close()
    # cnxn.commit()
    # cnxn.close()
    ## end truncate tables


    yield url


    # tear down
    # if kill_after and pid:
    #     try:
    #        os.system(f'kill -9 {pid}')
    #    except:
    #        logging.exception('kill failed\n')
    # os.system('rm redbean_test.zip .init.lua')
    # os.system('mv .tmp.init.lua .init.lua')


def test_create_board_1(redbean):
    res = requests.post(redbean + '/api/boards.lua', data=dict(
        name='b1',
        description='d1',
        user='user'
    ))
    assert res.content == b'1'


def test_create_board_2(redbean):
    res = requests.post(redbean + '/api/boards.lua', data=dict(
        name='b2',
        description='d2',
        user='user'
    ))
    assert res.content == b'2'


def test_get_boards(redbean):
    res = requests.get(redbean + '/api/boards.lua')
    print(res.json())
    json = res.json()
    assert len(json) == 2

    
def test_get_board(redbean):
    res = requests.get(redbean + '/api/boards.lua?id=1')
    print(res.json())
    json = res.json()
    assert 'id' in json and 'name' in json and json['id']==1


def test_update_board(redbean):
    res = requests.put(redbean + '/api/boards.lua?id=1', data=dict(
        name = 'b2-update',
        description = 'd2-update',
        user = 'user-update'
    ))
    res = requests.get(redbean + '/api/boards.lua?id=1')
    json = res.json()
    print(json)
    assert json['name']=='b2-update'\
           and json['description']=='d2-update'\
           and json['updated_user']=='user-update'\
           and json['id']==1


    
def test_create_topic_1(redbean):
    res = requests.post(redbean + '/api/topics.lua', data=dict(
        name='t1',
        description='td1',
        user='user',
        board_id=1
    ))
    assert res.content == b'1'


def test_create_topic_2(redbean):
    res = requests.post(redbean + '/api/topics.lua', data=dict(
        name='t2',
        description='td2',
        user='user',
        board_id=2
    ))
    assert res.content == b'2'


def test_get_topics(redbean):
    res = requests.get(redbean + '/api/topics.lua')
    print(res.json())
    json = res.json()
    assert len(json) == 2


def test_get_topics_by_board(redbean):
    res = requests.get(redbean + '/api/topics.lua?board_id=2')
    print(res.json())
    json = res.json()
    assert len(json) == 1
    assert json[0]['board_id']==2

    
def test_get_topic(redbean):
    res = requests.get(redbean + '/api/topics.lua?id=1')
    print(res.json())
    json = res.json()
    assert 'id' in json and 'name' in json and json['id']==1


def test_update_topic(redbean):
    res = requests.put(redbean + '/api/topics.lua?id=1', data=dict(
        name = 't2-update',
        description = 'td2-update',
        user = 'user-update',
        board_id = 3
    ))
    res = requests.get(redbean + '/api/topics.lua?id=1')
    json = res.json()
    print(json)
    assert json['name']=='t2-update'\
           and json['description']=='td2-update'\
           and json['updated_user']=='user-update'\
           and json['id']==1\
           and json['board_id']==3

    
def test_create_post_1(redbean):
    res = requests.post(redbean + '/api/posts.lua', data=dict(
        name='p1',
        description='pd1',
        user='user',
        topic_id=1,
        parent_post_id='null'
    ))
    assert res.content == b'1'


def test_create_post_2(redbean):
    res = requests.post(redbean + '/api/posts.lua', data=dict(
        name='p2',
        description='pd2',
        user='user',
        topic_id=2,
        parent_post_id=1
    ))
    assert res.content == b'2'


def test_get_posts(redbean):
    res = requests.get(redbean + '/api/posts.lua')
    print(res.json())
    json = res.json()
    assert len(json) == 2


def test_get_posts_by_topic(redbean):
    res = requests.get(redbean + '/api/posts.lua?topic_id=2')
    print(res.json())
    json = res.json()
    assert len(json) == 1
    assert json[0]['topic_id']==2

    
def test_get_post(redbean):
    res = requests.get(redbean + '/api/posts.lua?id=1')
    print(res.json())
    json = res.json()
    assert 'id' in json and 'name' in json and json['id']==1\
           and ('parent_post_id' not in json or json['parent_post_id']==None)


def test_update_post(redbean):
    res = requests.put(redbean + '/api/posts.lua?id=1', data=dict(
        name = 'p2-update',
        description = 'pd2-update',
        user = 'user-update',
        topic_id = 3,
        parent_post_id = 5
    ))
    res = requests.get(redbean + '/api/posts.lua?id=1')
    json = res.json()
    print(json)
    assert json['name']=='p2-update'\
           and json['description']=='pd2-update'\
           and json['updated_user']=='user-update'\
           and json['id']==1\
           and json['topic_id']==3\
           and json['parent_post_id']==5
    

def test_delete_post(redbean):
    res = requests.delete(redbean + '/api/posts.lua?id=1')
    res = requests.get(redbean + '/api/posts.lua')
    json = res.json()
    print(json)
    assert len(json)==1

    
def test_delete_posts(redbean):
    res = requests.delete(redbean + '/api/posts.lua')
    res = requests.get(redbean + '/api/posts.lua')
    json = res.json()
    assert len(json) == 0

    
def test_delete_topic(redbean):
    res = requests.delete(redbean + '/api/topics.lua?id=1')
    res = requests.get(redbean + '/api/topics.lua')
    json = res.json()
    print(json)
    assert len(json)==1

    
def test_delete_topics(redbean):
    res = requests.delete(redbean + '/api/topics.lua')
    res = requests.get(redbean + '/api/topics.lua')
    json = res.json()
    assert len(json) == 0


def test_delete_board(redbean):
    res = requests.delete(redbean + '/api/boards.lua?id=1')
    res = requests.get(redbean + '/api/boards.lua')
    json = res.json()
    print(json)
    assert len(json)==1

    
def test_delete_boards(redbean):
    res = requests.delete(redbean + '/api/boards.lua')
    res = requests.get(redbean + '/api/boards.lua')
    json = res.json()
    assert len(json) == 0
