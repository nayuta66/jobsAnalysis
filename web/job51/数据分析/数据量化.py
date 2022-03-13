import pandas
import re
import mysql.connector


def analysis():
    data = pandas.read_excel(r'C://Users//rbwu//Desktop//毕设//jobdata_clean.xls', sheet_name='jobdata_clean',
                             keep_default_na=False)
    for index, row in data.iterrows():
        if row['edu'] == '博士':
            data.at[index, 'edu'] = '4' + 'e'
        elif row['edu'] == '硕士':
            data.at[index, 'edu'] = '3' + 'e'
        elif row['edu'] == '本科':
            data.at[index, 'edu'] = '2' + 'e'
        elif row['edu'] == '大专':
            data.at[index, 'edu'] = '1' + 'e'
        else:
            data.at[index, 'edu'] = '0' + 'e'
        #  提取工作经验
        num = 0
        s = 0
        for e in row['work_time']:
            if e.isdigit():
                num += 1
                s += int(e)
        if num >= 1:
            if s / num < 1:
                data.at[index, 'work_time'] = '10' + 'y'
            else:
                data.at[index, 'work_time'] = str(s / num) + 'y'
        elif num == 0:
            data.at[index, 'work_time'] = '0' + 'y'

        # 提取薪资
        try:
            if not row['salary']:
                data.at[index, 'salary'] = '0' + 'k'
            else:
                if '年' in row['salary']:
                    if '万' in row['salary']:
                        obj = re.match(r"(.*)-(.*)['万','千']/", row['salary'])
                        x = float(obj.group(1))
                        y = float(obj.group(2))
                        salary = (x + y) / 2 / 12 * 10
                        data.at[index, 'salary'] = str(salary) + 'k'
                    elif '千' in row['salary']:
                        obj = re.match(r"(.*)-(.*)['万','千']/", row['salary'])
                        x = float(obj.group(1))
                        y = float(obj.group(2))
                        salary = ((x + y) / 2) / 12
                        data.at[index, 'salary'] = str(salary) + 'k'
                elif '月' in row['salary']:
                    if '万' in row['salary']:
                        obj = re.match(r"(.*)-(.*)['万','千']/", row['salary'])
                        x = float(obj.group(1))
                        y = float(obj.group(2))
                        salary = ((x + y) / 2) * 10
                        data.at[index, 'salary'] = str(salary) + 'k'
                    elif '千' in row['salary']:
                        obj = re.match(r"(.*)-(.*)['万','千']/", row['salary'])
                        x = float(obj.group(1))
                        y = float(obj.group(2))
                        salary = ((x + y) / 2)
                        data.at[index, 'salary'] = str(salary) + 'k'
                else:
                    data.at[index, 'salary'] = '0' + 'k'
        except BaseException as e:
            data.at[index, 'salary'] = '0' + 'k'

    pandas.DataFrame(data).to_excel(r'C://Users//rbwu//Desktop//毕设//analysis.xls', sheet_name='Sheet1', index=False,
                                    header=True)


def sqlClean():
    # 打开数据库
    db = mysql.connector.connect(user='root', password='@Wrb2418217111')
    # 使用cursor方法获取操作游标
    cursor = db.cursor()
    # 使用execute方法执行SQl语句
    cursor.execute('use 51job_data')
    cursor.execute('select category, job_fun, num from job_num_data')
    d = cursor.fetchall()
    for item in d:
        category = item[0]
        job_fun = item[1]
        num = item[2]
        try:
            cursor.execute(
                'select count(*) from jobdata_clean where category="%s" and job_fun="%s"' % (category, job_fun))
            total = cursor.fetchone()
            total = total[0]
            limit = total - int(num / 2000 * total)
            sql = "DELETE FROM jobdata_clean WHERE category='%s' and job_fun='%s' ORDER BY id DESC LIMIT %d" % (
                category, job_fun, limit)
            cursor.execute(sql)
            db.commit()
            print(category, job_fun, limit)
        except BaseException as e:
            print(e)
            print(limit)
    # 关闭数据库
    db.close()


def createAprioridata():
    data = pandas.read_excel(r'C://Users//rbwu//Desktop//毕设//analysis.xls', sheet_name='Sheet1',
                             keep_default_na=False)
    num = 0
    avg_salary = 0
    avg_edu = 0
    avg_work = 0
    for index, row in data.iterrows():
        num += 1
        row['edu'] = int(row['edu'][:-1])

        avg_salary += float(row['salary'][:-1])
        avg_edu += row['edu']
        avg_work += float(row['work_time'][:-1])

        if row['edu'] >= 2:
            data.at[index, 'edu'] = '学历偏高'
        else:
            data.at[index, 'edu'] = '学历偏低'

        row['work_time'] = float(row['work_time'][:-1])
        if row['work_time'] >= 3:
            data.at[index, 'work_time'] = '工作经验大于3'
        else:
            data.at[index, 'work_time'] = '工作经验小于3'

        row['salary'] = float(row['salary'][:-1])
        if row['salary'] == 0:
            data.at[index, 'salary'] = 's0'
        elif row['salary'] < 6:
            data.at[index, 'salary'] = '工资小于6k'
        else:
            data.at[index, 'salary'] = '工资大于6k'

    pandas.DataFrame(data).to_excel(r'C://Users//rbwu//Desktop//毕设//apriori.xls', sheet_name='Sheet1', index=False,
                                    header=True)


def statistics():
    data = pandas.read_excel(r'C://Users//rbwu//Desktop//毕设//analysis.xls', sheet_name='Sheet1',
                             keep_default_na=False)
    # 打开数据库
    db = mysql.connector.connect(user='root', password='@Wrb2418217111')
    # 使用cursor方法获取操作游标
    cursor = db.cursor()

    cursor.execute('use 51job_data')
    cursor.execute(
        'create table statistics(id int not null auto_increment , category varchar(8), job_fun int, \
        work_place varchar(128), work_time float, edu int,salary float ,\
        primary key (id))engine=InnoDB default charset=utf8')

    cursor.execute('use 51job_data')
    for index, row in data.iterrows():
        row['work_place'] = row['work_place'][0:2]
        row['edu'] = int(row['edu'][:-1])
        row['work_time'] = float(row['work_time'][:-1])
        row['salary'] = float(row['salary'][:-1])

        sql = "insert into statistics(category,job_fun,work_place,work_time,edu,salary)\
                               values('%s','%s','%s','%s','%s','%s')" % (
            row['category'], row['job_fun'], row['work_place'], row['work_time'], row['edu'], row['salary']
        )
        cursor.execute(sql)
    db.commit()
    # 关闭数据库连接
    db.close()


if __name__ == '__main__':
    # sqlClean()
    # analysis()
    createAprioridata()
    # statistics()
