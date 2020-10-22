# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 12:03:54 2020

@author: szc
"""

from selenium import webdriver
import time
import os

def get_file_num(files):
    num = 0
    for file_name in files:
        if file_name.endswith('tar.gz'):
            num += 1
    return num


driver = webdriver.Chrome(executable_path="E:\\anaconda3\\envs\\tf2\\chromedriver.exe")
# driver = webdriver.Chrome()
driver.get('https://osdds.nsoas.org.cn/#/')

'''user_name = 'ziye1417'
passward = 'lbl970126'''

####这是后半段

hrefs = driver.find_elements_by_xpath("//*[@href]")
data_refs = []
for href in hrefs:
    if href.text == '数据下载':
        # print(href)
        data_refs.append(href)

chrome_dir = "C:\\Users\\h_459\\Downloads"
num_file = get_file_num(os.listdir(chrome_dir)) + 1
for data_ref in data_refs[num_file-1:]:
    data_ref.click()
    while True:
        files = os.listdir(chrome_dir)
        current_file_num = get_file_num(files)
        if current_file_num == num_file:
            break
        time.sleep(8)
    num_file += 1
    print(num_file)
