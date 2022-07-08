from selenium import webdriver
import time
import os
import csv

driver = webdriver.Chrome()
driver.get('https://www.bilibili.com/video/BV1d5411L7JD?from=search&seid=17529924982249509511&spm_id_from=333.337.0.0')
time.sleep(100)
# def slide():
for i in range(10):
    js="var q=document.documentElement.scrollTop=100000"
    driver.execute_script(js)
    time.sleep(1)

def get_title():
    tizhu_name = driver.find_elements_by_xpath('//div[@class="con "]/div/a[1]')
    tizhu_time = driver.find_elements_by_xpath('//*[@id="comment"]/div/div[2]/div/div[4]/div/div[2]/div[2]/span[1]')
    tizhu_repeat = driver.find_elements_by_xpath('//*[@id="comment"]/div/div[2]/div/div[4]/div/div[2]/p')
    for i in range(11):
        try:
            element1 = driver.find_element_by_link_text('点击查看')
            driver.execute_script("arguments[0].click();", element1)
        except Exception:
            element1 = driver.find_element_by_link_text('点击查看')
            driver.execute_script("arguments[0].click();", element1)
    list1 = []
    for j in range(len(tizhu_name)):
        dict = {}
        dict['网名'] = tizhu_name[j].text
        dict['评论'] = tizhu_repeat[j].text
        dict['时间'] = tizhu_time[j].text
        list1.append(dict)
    return list1
def get_reply():
    huitie_name = driver.find_elements_by_xpath('//*[@id="comment"]/div/div[2]/div/div[4]/div/div[2]/div[3]/div/div[1]/div/a[1]')
    huitie_time = driver.find_elements_by_xpath('//*[@id="comment"]/div/div[2]/div/div[4]/div/div[2]/div[3]/div/div[2]/span[1]')
    huitie_repeat = driver.find_elements_by_xpath('//*[@id="comment"]/div/div[2]/div/div[4]/div/div[2]/div[3]/div/div[1]/div/span[@class="text-con"]')
    list2 = []
    for n in range(len(huitie_name)):
        dict = {}
        dict['网名'] = huitie_name[n].text
        dict['评论'] = huitie_repeat[n].text
        dict['时间'] = huitie_time[n].text
        list2.append(dict)
    return list2

def save(list1,list2):
    for i in list2:
        list1.append(i)
    with open(os.path.join('B站评论'+'.csv'),'w',encoding='GB18030') as f:
        writer = csv.DictWriter(f,fieldnames=['网名','评论','时间'])
        writer.writeheader()
        writer.writerows(list1)

if __name__ == '__main__':
    # slide()
    list1 = get_title()
    list2 = get_reply()
    save(list1,list2)

