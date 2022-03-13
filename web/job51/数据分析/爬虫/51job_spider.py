#!/usr/bin/env python
# coding: utf-8

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from mylog import MyLog as mylog
from getcity import getCity
import json
import time
import urllib.request
from lxml import etree
import mysql.connector


class Item(object):
    job_name = None  # 岗位名
    company_name = None  # 公司名
    work_place = None  # 工作地点
    salary = None  # 薪资
    release_time = None  # 发布时间
    job_recruitment_details = None  # 招聘岗位详细
    job_number_details = None  # 招聘人数详细
    company_treatment_details = None  # 福利待遇详细
    practice_mode = None  # 联系方式


class GetJobInfo(object):
    """
    the all data from 51job.com
    所有数据来自前程无忧招聘网
    """

    def __init__(self):
        self.log = mylog()  # 实例化mylog类,用于记录日志
        self.startUrl = 'https://www.51job.com/'  # 爬取的目标网站
        self.browser = self.getBrowser()  # 设置chrome
        self.browser_input = self.userInput(self.browser)  # 模拟用户输入搜索
        self.getPageNext(self.browser_input)  # 找到下个页面
        self.category = None
        self.job = None

    def getBrowser(self):
        """
        设置selenium使用chrome的无头模式
        打开目标网站 https://www.51job.com/
        """
        try:
            # 创建chrome参数对象
            chrome_options = Options()
            # 把chrome设置成无界面模式,不论windows还是linux都可以，自动适配对应参数
            chrome_options.add_argument("headless")
            browser = webdriver.Chrome(options=chrome_options, executable_path=r'C:\Pycharm\chromedriver')
            # 利用selenium打开网站
            browser.get(self.startUrl)
            # 等待网站js代码加载完毕
            browser.implicitly_wait(20)
        except Exception as e:
            # 记录错误日志
            self.log.error('打开目标网站失败:{},错误代码:{}'.format(self.startUrl, e))
        else:
            # 记录成功日志
            self.log.info('打开目标网站成功:{}'.format(self.startUrl))
            # 返回实例化selenium对象
            return browser

    def getJob(self, tup, b):
        b = self.browser
        # 找到职能选择框,并模拟点击
        time.sleep(3)
        button = b.find_element_by_xpath('/html/body/div[2]/div[1]/div/div[1]/div[3]')
        button.click()

        # 选中职能弹出框
        b.current_window_handle
        # 侧边选择
        b.find_element_by_xpath('//*[@id="popop"]/div/div[2]/ul/li[%s]' % tup[0]).click()
        # 框内选择
        '//*[@id="popop"]/div/div[2]/div[1]/div[2]/div/table/tbody[1]/tr[2]/td/div/table/tbody/tr[1]/td/em'
        '//*[@id="popop"]/div/div[2]/div[1]/div[2]/div/table/tbody[1]/tr[2]/td/div/table/tbody/tr[1]/td/em'
        '//*[@id="popop"]/div/div[2]/div[1]/div[2]/div/table/tbody[2]/tr[2]/td/div/table/tbody/tr[1]/td/em'
        '//*[@id="popop"]/div/div[2]/div[1]/div[2]/div/table/tbody[3]/tr[2]/td/div/table/tbody/tr[1]/td/em'
        '//*[@id="popop"]/div/div[2]/div[1]/div[2]/div/table/tbody[3]/tr[2]/td/div/table/tbody/tr[1]/td/em'
        b.find_element_by_xpath(
            '//*[@id="popop"]/div/div[2]/div[1]/div[2]/div/table/tbody[%s]/tr[1]/td[%s]/em' % (tup[1], tup[2])).click()
        b.find_element_by_xpath(
            '//*[@id="popop"]/div/div[2]/div[1]/div[2]/div/table/tbody[%s]/tr[2]/td/div/table/tbody/tr[1]/td/em' % (
                tup[1],)).click()
        # 确定并搜索
        b.find_element_by_xpath('//*[@id="popop"]/div/div[3]/span').click()
        b.find_element_by_xpath('//*[@id="search_btn"]').click()
        time.sleep(3)

    def userInput(self, browser):
        """
        北京 上海 广州 深圳 武汉 西安 杭州
        南京  成都 重庆 东莞 大连 沈阳 苏州
        昆明 长沙 合肥 宁波 郑州 天津 青岛
        济南 哈尔滨 长春 福州
        只支持以上城市,输入其它则无效
        最多可选5个城市,每个城市用 , 隔开(英文逗号)
        """
        # 用户输入关键字搜索
        search_for_jobs = input("请输入职位搜索关键字:")
        # 用户输入城市
        print(self.userInput.__doc__)
        select_city = input("输入城市信息,最多可输入5个,多个城市以逗号隔开:")
        # 找到51job首页上关键字输入框
        textElement = browser.find_element_by_id('kwdselectid')
        # 模拟用户输入关键字
        textElement.send_keys(search_for_jobs)

        # 找到城市选择弹出框，模拟选择"北京,上海,广州,深圳,杭州"
        button = browser.find_element_by_xpath("//div[@class='ush top_wrap']\
        //div[@class='el on']/p[@class='addbut']//input[@id='jobarea']")

        # 打开城市对应编号文件
        with open("city.json", 'r', encoding='utf8') as f:
            city_number = f.read()
            # 使用json解析文件
            city_number = json.loads(city_number)

        new_list = []
        # 判断是否输入多值
        if len(select_city.split(',')) > 1:
            for i in select_city.split(','):
                if i in city_number.keys():
                    # 把城市替换成对应的城市编号
                    i = city_number.get(i)
                    new_list.append(i)
                    # 把用户输入的城市替换成城市编号
            select_city = ','.join(new_list)
        else:
            for i in select_city.split(','):
                i = city_number.get(i)
                new_list.append(i)
            select_city = ','.join(new_list)

        # 执行js代码
        browser.execute_script("arguments[0].value = '{}';".format(select_city), button)
        # 模拟点击搜索
        browser.find_element_by_xpath("//div[@class='ush top_wrap']/button").click()
        # 职能筛选
        self.category = input('行业：')
        self.job = input('职能：')
        alist = [(1, 1, 3), (1, 1, 1), (1, 1, 2), (1, 2, 2), (1, 2, 3), (1, 3, 1), (1, 4, 1), (1, 3, 3), (1, 5, 1),
                 (1, 5, 2), (1, 5, 3)]
        blist = [(2, 1, 1), (2, 1, 2), (2, 2, 1)]
        clist = [(3, 1, 1), (3, 1, 2), (3, 1, 3), (3, 2, 1)]
        dlist = [(4, 1, 1), (4, 1, 2), (4, 1, 3), (4, 2, 2), (4, 3, 1), (4, 4, 1), (4, 4, 2), (4, 4, 3), (4, 5, 1)]
        elist = [(5, 1, 1), (5, 1, 2), (5, 1, 3), (5, 2, 1), (5, 2, 2)]
        flist = [(6, 1, 1), (6, 1, 2), (6, 1, 3), (6, 2, 1), (6, 2, 2), (6, 2, 3), (6, 3, 1)]
        glist = [(7, 1, 1), (7, 1, 2), (7, 1, 3)]
        hlist = [(8, 1, 1), (8, 1, 2), (8, 1, 3), (8, 2, 1)]
        ilist = [(9, 1, 1), (9, 1, 2), (9, 1, 3)]
        jlist = [(10, 1, 1), (10, 1, 2), (10, 1, 3)]
        klist = [(11, 1, 1), (11, 1, 2), (11, 1, 3), (11, 2, 1), (11, 2, 2), (11, 2, 3), (11, 3, 1), (11, 3, 2)]

        if self.category == 'a':
            tup = alist[int(self.job) - 1]
        elif self.category == 'b':
            tup = blist[int(self.job) - 1]
        elif self.category == 'c':
            tup = clist[int(self.job) - 1]
        elif self.category == 'd':
            tup = dlist[int(self.job) - 1]
        elif self.category == 'e':
            tup = elist[int(self.job) - 1]
        elif self.category == 'f':
            tup = flist[int(self.job) - 1]
        elif self.category == 'g':
            tup = glist[int(self.job) - 1]
        elif self.category == 'h':
            tup = hlist[int(self.job) - 1]
        elif self.category == 'i':
            tup = ilist[int(self.job) - 1]
        elif self.category == 'j':
            tup = jlist[int(self.job) - 1]
        elif self.category == 'k':
            tup = klist[int(self.job) - 1]
        self.getJob(tup, browser)
        self.log.info("模拟搜索输入成功,获取目标爬取title信息:{}".format(browser.title))
        return browser

    def getPageNext(self, browser):
        # 找到总页数
        str_sumPage = browser.find_element_by_xpath(
            "/html/body/div[2]/div[3]/div/div[2]/div[4]/div[2]/div/div/div/span[1]").text
        sumpage = ''
        for i in str_sumPage:
            if i.isdigit():
                sumpage += i
        self.log.info("获取总页数:{}".format(sumpage))
        s = 1
        try:
            while s <= 12:
                urls = self.getUrl(self.browser)
                print("urls:{}".format(urls) + "\n")
                # 获取每个岗位的详情
                self.items = self.spider(urls)
                # 数据下载
                self.pipelines(self.items)
                # 清空urls列表,获取后面的url(去重,防止数据重复爬取)
                urls.clear()
                s += 1
                self.log.info('开始爬取第%d页' % s)
                # 找到下一页的按钮点击
                browser.find_element_by_class_name('next').click()
                # 等待加载js代码
                browser.implicitly_wait(20)
                time.sleep(1)
        except BaseException as e:
            print(e)

        self.log.info('获取所有岗位成功')
        browser.quit()

    def getUrl(self, browser):
        # 创建一个空列表,用来存放所有岗位详情的url
        urls = []
        # 获取所有岗位详情
        Elements = browser.find_elements_by_css_selector('div.e > a.el')
        for i in Elements:
            try:
                if i.get_attribute("href").split('/')[2] == 'jobs.51job.com':
                    urls.append(i.get_attribute("href"))
            except BaseException as e:
                print(e)
        return urls

    def spider(self, urls):
        # 数据过滤,爬取需要的数据,返回items列表
        items = []
        for url in urls:
            try:
                htmlcontent = self.getreponsecontent(url)
                html_xpath = etree.HTML(htmlcontent)
                item = Item()
                # 类别
                item.category = self.category
                # 职能
                item.job_fun = self.job
                # 岗位名
                item.job_name = html_xpath.xpath("normalize-space(//div[@class='cn']/h1/text())")
                # 公司名
                item.company_name = html_xpath.xpath("normalize-space(//div[@class='cn']\
                /p[@class='cname']/a/text())")

                # 工作地点
                item.work_place = html_xpath.xpath("normalize-space(//div[@class='cn']\
                //p[@class='msg ltype'])").split('|')[0].strip()
                # 工作经验
                if len(html_xpath.xpath("normalize-space(//div[@class='cn']//p[@class='msg ltype'])").split('|')) == 5:
                    item.work_time = html_xpath.xpath("normalize-space(//div[@class='cn']\
                    //p[@class='msg ltype'])").split('|')[1].strip()
                else:
                    item.work_time = ''
                # 学历要求
                try:
                    item.edu = html_xpath.xpath("normalize-space(//div[@class='cn']\
                    //p[@class='msg ltype'])").split("|")[2].strip()
                except BaseException as e:
                    print(e)
                    item.edu = ''

                # 招聘人数详细
                try:
                    item.job_number_details = html_xpath.xpath("normalize-space(//div[@class='cn']\
                    //p[@class='msg ltype'])").split("|")[3].strip()
                except BaseException as e:
                    print(e)
                    item.job_number_details = ''
                # 发布时间
                try:
                    item.release_time = html_xpath.xpath("normalize-space(//div[@class='cn']\
                                //p[@class='msg ltype'])").split('|')[4].strip()
                except BaseException as e:
                    print(e)
                    item.release_time = ''

                # 薪资
                item.salary = html_xpath.xpath("normalize-space(//div[@class='cn']/strong/text())").strip()
                # 招聘岗位详细
                job_recruitment_details_tmp = html_xpath.xpath("//div[@class='bmsg job_msg inbox']//text()")
                item.job_recruitment_details = ''
                ss = job_recruitment_details_tmp.index("职能类别：")
                ceshi = job_recruitment_details_tmp[:ss - 1]
                for i in ceshi:
                    item.job_recruitment_details = item.job_recruitment_details + i.strip() + '\n'

                # 福利待遇详细
                company_treatment_details_tmp = html_xpath.xpath("//div[@class='t1']//text()")
                item.company_treatment_details = ''
                for i in company_treatment_details_tmp:
                    item.company_treatment_details = item.company_treatment_details + ' ' + i.strip()
                # 联系方式
                practice_mode_tmp = html_xpath.xpath("//div[@class='bmsg inbox']/p//text()")
                item.practice_mode = ''
                for i in practice_mode_tmp:
                    item.practice_mode = item.practice_mode + ' ' + i.strip()
                items.append(item)
            except BaseException as e:
                print(e)
        return items

    def getreponsecontent(self, url):
        # 接收url,打开目标网站,返回html
        Headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
        try:
            request = urllib.request.Request(url, headers=Headers)
            response = urllib.request.urlopen(request)
            html = response.read().decode('gbk')
        except Exception as e:
            self.log.error(u'Python 返回 url:{} 数据失败\n错误代码:{}\n'.format(url, e))
        else:
            self.log.info(u'Python 返回 url:{} 数据成功\n'.format(url))
            time.sleep(1)  # 1秒返回一个结果  手动设置延迟防止被封
            return html

    def pipelines(self, items):  # 接收一个items列表, 将数据保存到数据库
        # 打开数据库
        db = mysql.connector.connect(user='root', password='@Wrb2418217111')
        # 使用cursor方法获取操作游标
        cursor = db.cursor()
        # 使用execute方法执行SQl语句
        cursor.execute('use information_schema')
        cursor.execute('select * from tables where table_name="jobdata"')
        # 可使用fetchone, fetchmany, fetchall等获取数据，每次查询都需要fetch一次结果
        if not cursor.fetchone():
            cursor.execute('use 51job_data')
            cursor.execute(
                'create table jobdata(id int not null auto_increment , category varchar(8), job_fun int(4), job_name varchar(128) not null, company_name varchar(128),\
                work_place varchar(128), work_time varchar(128), edu varchar (128),\
                job_num_details varchar (128),release_time varchar (128), salary varchar (128),\
                company_treatment_details varchar(128), practice_mode varchar(128),\
                primary key (id))engine=InnoDB default charset=utf8')
        cursor.execute('use 51job_data')
        for item in items:
            try:
                sql = "insert into jobdata(category,job_fun,job_name,company_name,work_place,work_time,edu,job_num_details,\
                        release_time,salary,company_treatment_details,practice_mode)\
                        values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                    item.category, item.job_fun, item.job_name, item.company_name, item.work_place, item.work_time,
                    item.edu,
                    item.job_number_details,
                    item.release_time,
                    item.salary,
                    item.company_treatment_details,
                    item.practice_mode)
                cursor.execute(sql)
            except BaseException as e:
                print(e)
        db.commit()
        # 关闭数据库连接
        db.close()


if __name__ == '__main__':
    if os.path.exists('city.json'):
        GetJobInfo()
    else:
        getCity()
        GetJobInfo()
