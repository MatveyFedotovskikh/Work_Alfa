import functools
import time
from typing import KeysView
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime
import password 
import json
import requests
class Selenium_test():
    def __init__(self):
        options = webdriver.ChromeOptions()
        # user-agent
        options.add_argument('user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0')
        options.add_argument('log-level=INT')
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(
            executable_path=password.path_sel,
            options=options
        )
        self.date_now = 3 #datetime.datetime.now().month
        self.data = {}
        self.run = True
        self.error = 0
    def time_of_function(function):
        @functools.wraps(function)
        def _wrapped(*args):
            start_time = time.perf_counter()
            res = function(*args)
            runtime = time.perf_counter() - start_time
            print(f"{function.__name__} took {runtime:.4f} secs")
            return res
        return _wrapped
    
    def start(self):
        self.driver.get("https://rtschool.s20.online/company/1/lesson/index")
        time.sleep(1)
        email_input = self.driver.find_element(by=By.ID, value="loginform-username")
        email_input.clear()
        email_input.send_keys(password.login_alfa)
        time.sleep(0.2)
        password_input = self.driver.find_element(by=By.ID, value="loginform-password")
        password_input.clear()
        password_input.send_keys(password.passowrd_alfa)
        time.sleep(0.2)
        password_input.send_keys(Keys.ENTER)
        time.sleep(1) 
        self.driver.find_element(by=By.XPATH, value='//*[@id="w1"]/div[1]/span/span[2]/a').click()
        time.sleep(1)
        self.driver.find_element(by=By.XPATH, value='//*[@id="w1"]/div[1]/span/span[2]/ul/li[5]/a').click()
        time.sleep(1)
        self.driver.execute_script("document.body.style.zoom='50%'")       

    def replace_link(self,link):
        link_result = link.split("&")[0]
        return link_result
    
    def count_students(self,number):
        element = self.driver.find_element(by=By.XPATH, value=f'//*[@id="w1-container"]/table/tbody/tr[{number}]/td[6]')
        time.sleep(2)
        list_a = element.find_elements(by=By.TAG_NAME, value='a')
        if len(list_a) <= 3:
            return len(list_a) - 1
        else:
            return len(list_a) - 2
        
    def ind_group(self,i):
        link_client = self.driver.find_element(by=By.XPATH, value=f'//*[@id="w1-container"]/table/tbody/tr[{i}]/td[6]/a[2]').get_attribute("title")
        cancellations_type = [0,0,0,0,0]
        count_paid_students = 0
        if link_client[:12] == 'Отсутствовал':
            if link_client[14:17] == '✅ Ф':
                cancellations_type[0]+=1
            if link_client[14:17] == '✅ 1':
                count_paid_students += 1
                cancellations_type[1]+=1
            if link_client[14:17] == '✅ О':
                cancellations_type[2]+=1
            if link_client[14:17] == '❌ О':
                count_paid_students += 1
                cancellations_type[3]+=1
            if link_client[14:17] == '⛔ Н':
                cancellations_type[4]+=1
            return (False, cancellations_type, count_paid_students)
        else:
            count_paid_students = 1
            return (True, cancellations_type, count_paid_students)                                                    
    
    def group(self,i):
        count_group=self.count_students(i)
        a = False
        cancellations_type = [0,0,0,0,0]
        count_paid_students = 0
        for number_student_in_group in range(2,count_group+2):
            link_client = self.driver.find_element(by=By.XPATH, value=f'//*[@id="w1-container"]/table/tbody/tr[{i}]/td[6]/a[{number_student_in_group}]').get_attribute("title")
            
            if link_client[:12] == 'Отсутствовал':
                if link_client[14:17] == '✅ Ф':
                    cancellations_type[0]+=1
                if link_client[14:17] == '✅ 1':
                    count_paid_students += 1
                    cancellations_type[1]+=1
                if link_client[14:17] == '✅ О':
                    cancellations_type[2]+=1
                if link_client[14:17] == '❌ О':
                    count_paid_students += 1
                    cancellations_type[3]+=1
                if link_client[14:17] == '⛔ Н':
                    cancellations_type[4]+=1
            else:
                a = True
        count_paid_students += count_group-sum(cancellations_type)
        return (a, cancellations_type, count_paid_students)
        

    def ind(self,i):                                                     
        link_client = self.driver.find_element(by=By.XPATH, value=f'//*[@id="w1-container"]/table/tbody/tr[{i}]/td[6]/a').get_attribute("title")
        cancellations_type = [0,0,0,0,0]
        count_paid_students = 0
        if link_client[:12] == 'Отсутствовал':
            if link_client[14:17] == '✅ Ф':
                cancellations_type[0]+=1
            if link_client[14:17] == '✅ 1':
                count_paid_students += 1
                cancellations_type[1]+=1
            if link_client[14:17] == '✅ О':
                cancellations_type[2]+=1
            if link_client[14:17] == '❌ О':
                count_paid_students += 1
                cancellations_type[3]+=1
            if link_client[14:17] == '⛔ Н':
                cancellations_type[4]+=1
            return (False, cancellations_type, count_paid_students)
        else:
            count_paid_students = 1
            return (True, cancellations_type, count_paid_students) 
        

    def PY(self,i):
        link_client = self.driver.find_element(by=By.XPATH, value=f'//*[@id="w1-container"]/table/tbody/tr[{i}]/td[6]/a').get_attribute("title")
        
        cancellations_type = [0,0,0,0,0]
        count_paid_students = 0
        if link_client[:12] == 'Отсутствовал':
            if link_client[14:17] == '✅ Ф':
                cancellations_type[0]+=1
            if link_client[14:17] == '✅ 1':
                count_paid_students += 1
                cancellations_type[1]+=1
            if link_client[14:17] == '✅ О':
                cancellations_type[2]+=1
            if link_client[14:17] == '❌ О':
                count_paid_students += 1
                cancellations_type[3]+=1
            if link_client[14:17] == '⛔ Н':
                cancellations_type[4]+=1
            return (False, cancellations_type, count_paid_students)
        else:
            count_paid_students = 1
            return (True, cancellations_type, count_paid_students) 
        
    

    def value_check(self,value,i):
        if value == 'Индивидуальный':
            return ('Индивидуальный',self.ind(i))
        elif value == 'Групповой':

            link_client = self.driver.find_element(by=By.XPATH, value=f'//*[@id="w1-container"]/table/tbody/tr[{i}]/td[8]').text

            if link_client[:3] == 'IND':
                return ('Индивидуально Групповой',self.ind_group(i))
            else:
                return ('Групповой',self.group(i))

        elif value == 'Пробный':
            return ('Пробный',self.PY(i))
        
    def teacher_correct(self,teacher):
        P = teacher.find("П -")
        if P==-1:
            M1 = teacher.find("M1")
            if M1 == -1:
                M1 = teacher.find("М1")
            M2 = teacher.find("M2")
            if M2 == -1:
                M2 = teacher.find("М2")
            M3 = teacher.find("M3")
            if M3 == -1:
                M3 = teacher.find("М3")
            s = []
            if M1>M2:
                s.append(M1)
            if M3>M2:
                s.append(M3)

            if s==[]:
                teacher = teacher[M2:]
            elif s==[-1,-1]:
                teacher = teacher[M2:]
            else:
                teacher = teacher[M2:min(s)]
            if teacher[-1] == ',':
                teacher=teacher[:-1]
            if teacher[-2] == ',':
                teacher=teacher[:-2]
        else:
            M1 = teacher.find("M1")
            if M1 == -1:
                M1 = teacher.find("М1")
            M2 = teacher.find("M2")
            if M2 == -1:
                M2 = teacher.find("М2")
            M3 = teacher.find("M3")
            if M3 == -1:
                M3 = teacher.find("М3")
            s = []
            if M1>P:
                s.append(M1)
            if M2>P:
                s.append(M2)
            if M3>P:
                s.append(M3)

            if s==[]:
                teacher = teacher[P:]
            elif s==[-1,-1,-1]:
                teacher = teacher[P:]
            else:
                teacher = teacher[P:min(s)]
            if teacher[-1] == ',':
                teacher=teacher[:-1]
            if teacher[-2] == ',':
                teacher=teacher[:-2]
    
        return teacher
    def sale_PY(self,number):
        button = self.driver.find_element(by=By.XPATH, value=f'//*[@id="w1-container"]/table/tbody/tr[{number}]/td[6]/a')
        self.driver.execute_script('arguments[0].click()', button)
        pay_info = self.driver.find_element(by=By.XPATH, value=f'//*[@id="customer-pjax"]/div[2]/div[2]/div/div/div[2]/div[2]/a').text
        self.driver.execute_script("window.history.go(-1)")
        time.sleep(0.5)
        self.driver.execute_script("document.body.style.zoom='50%'")   
        if pay_info[0] == '0':
            return False
        else:
            return True
    def steal_data_one_lesson(self,number):
        date = self.driver.find_element(by=By.XPATH, value=f'//*[@id="w1-container"]/table/tbody/tr[{number}]/td[4]').text
        if datetime.datetime.strptime(date, "%d.%m.%Y").date().month == self.date_now:
            date_time = self.driver.find_element(by=By.XPATH, value=f'//*[@id="w1-container"]/table/tbody/tr[{number}]/td[5]').text
            link_student_for_mentors = self.replace_link(self.driver.find_element(by=By.XPATH, value=f'//*[@id="w1-container"]/table/tbody/tr[{number}]/td[6]/a').get_attribute('href'))
            link_student_for_teacher = link_student_for_mentors.replace('company','teacher')
            tip_lesson_false = self.driver.find_element(by=By.XPATH, value=f'//*[@id="w1-container"]/table/tbody/tr[{number}]/td[6]/i[2]').get_attribute("title")
            tip_lesson_and_attendance = self.value_check(tip_lesson_false,number)
            tip_lesson = tip_lesson_and_attendance[0]
            attendance = tip_lesson_and_attendance[1][0]
            cancellations_type = tip_lesson_and_attendance[1][1]
            teacher = self.driver.find_element(by=By.XPATH, value=f'//*[@id="w1-container"]/table/tbody/tr[{number}]/td[7]').text
            sale_PY = False
            if tip_lesson == 'Пробный':
                teacher = self.teacher_correct(teacher)
                sale_PY = self.sale_PY(number)
            subject = self.driver.find_element(by=By.XPATH, value=f'//*[@id="w1-container"]/table/tbody/tr[{number}]/td[8]').text
            status = self.driver.find_element(by=By.XPATH, value=f'//*[@id="w1-container"]/table/tbody/tr[{number}]/td[9]').text
            comment = self.driver.find_element(by=By.CSS_SELECTOR, value=f'#w1-container > table > tbody > tr:nth-child({number}) > td:nth-child(10)').get_attribute("innerHTML")
            if comment == '' or ("Опыт" in comment):
                comment = self.driver.find_element(by=By.CSS_SELECTOR, value=f'#w1-container > table > tbody > tr:nth-child({number}) > td:nth-child(14)').get_attribute("innerHTML") #comment_old
                if tip_lesson == 'Пробный' and comment == '':
                    comment = self.driver.find_element(by=By.CSS_SELECTOR, value=f'#w1-container > table > tbody > tr:nth-child({number}) > td:nth-child(2)').get_attribute("innerHTML") #homework
                    if 'span' in comment:
                        comment = ''
            lesson_number = self.driver.find_element(by=By.CSS_SELECTOR, value=f'#w1-container > table > tbody > tr:nth-child({number}) > td:nth-child(12)').get_attribute("innerHTML")
            try:
                record_lesson_link = self.driver.find_element(by=By.XPATH, value=f'//*[@id="w1-container"]/table/tbody/tr[{number}]/td[13]/a')
                record_lesson_link = 'Запись есть'
            except:
                record_lesson_link = ''
            reason_cancellation = self.driver.find_element(by=By.CSS_SELECTOR, value=f'#w1-container > table > tbody > tr:nth-child({number}) > td:nth-child(16)').get_attribute("innerHTML")
            course_lesson = self.driver.find_element(by=By.CSS_SELECTOR, value=f'#w1-container > table > tbody > tr:nth-child({number}) > td:nth-child(3)').get_attribute("innerHTML")
            lesson_duration = int(self.driver.find_element(by=By.XPATH,value = f'//*[@id="w1-container"]/table/tbody/tr[{number}]/td[6]').text[:2])
            lesson_language = self.driver.find_element(by=By.CSS_SELECTOR, value=f'#w1-container > table > tbody > tr:nth-child({number}) > td:nth-child(15)').get_attribute("innerHTML") 
            count_paid_students = tip_lesson_and_attendance[1][2]
            force_Majeure = cancellations_type[0]
            first_pass = cancellations_type[1]
            cancellation_more_eight = cancellations_type[2]
            cancellation_less_eight = cancellations_type[3]
            no_money = cancellations_type[4]
            self.data_append(
                            date,
                            date_time, 
                            link_student_for_mentors, 
                            link_student_for_teacher, 
                            teacher, 
                            subject, 
                            status, 
                            comment, 
                            lesson_number, 
                            record_lesson_link, 
                            reason_cancellation, 
                            tip_lesson, 
                            attendance, 
                            course_lesson,
                            lesson_duration,
                            lesson_language,
                            count_paid_students,
                            force_Majeure,
                            first_pass,
                            cancellation_more_eight,
                            cancellation_less_eight,
                            no_money,
                            sale_PY
                        ) 
        elif datetime.datetime.strptime(date, "%d.%m.%Y").date().month == 2:
            self.run = False

        
        
    @time_of_function
    def steal_data_one_page_lessons(self):
        while self.run:
            try:
                for i in range(1,500):
                    print(i)
                    if i == 80:
                        print(0)
                    self.steal_data_one_lesson(i)
                    self.driver.execute_script(f"window.scrollBy({i*10-10},10)","")
                    if self.run == False:
                        break
                self.driver.get(self.driver.find_element(by=By.XPATH, value=f'//*[@id="w1"]/div[5]/ul/li[12]/a').get_attribute('href'))
                time.sleep(2)
                self.driver.execute_script("document.body.style.zoom='50%'")
            except Exception as ex:
                print(ex)
                break
        with open("max_feb_4.json", "w", encoding='utf-8') as outfile:
            json.dump(self.data, outfile, ensure_ascii=False,indent=2)
        
    
    def data_append(
                    self,
                    date,
                    date_time,
                    link_student_for_mentors,
                    link_student_for_teacher,
                    teacher,
                    subject,
                    status,
                    comment,
                    lesson_number,
                    record_lesson_link,
                    reason_cancellation,
                    tip_lesson,
                    attendance,
                    course_lesson,
                    lesson_duration,
                    lesson_language,
                    count_paid_students,
                    force_Majeure,
                    first_pass,
                    cancellation_more_eight,
                    cancellation_less_eight,
                    no_money,
                    sale_PY
                ): 
        try: 
            self.data[teacher].append({
                'teacher':teacher,
                'date': date,
                'datetime': date_time,
                'link_student_for_mentors': link_student_for_mentors,
                'link_student_for_teacher': link_student_for_teacher,
                'subject':subject,
                'status':status,
                'comment':comment,
                'lesson_number':lesson_number,
                'record_lesson_link':record_lesson_link,
                'reason_cancellation':reason_cancellation,
                'tip_lesson': tip_lesson,
                'attendance': attendance,
                'course_lesson': course_lesson,
                'lesson_duration': lesson_duration,
                'language':lesson_language,
                'count_paid_students' : count_paid_students,
                'force_Majeure': force_Majeure,
                'first_pass': first_pass,
                'cancellation_more_eight': cancellation_more_eight,
                'cancellation_less_eight': cancellation_less_eight,
                'no_money' : no_money,
                'sale_PY': sale_PY
            })
        except:
            self.data[teacher] = [
                {
                'teacher':teacher,
                'date': date,
                'datetime': date_time,
                'link_student_for_mentors': link_student_for_mentors,
                'link_student_for_teacher': link_student_for_teacher,
                'subject':subject,
                'status':status,
                'comment':comment,
                'lesson_number':lesson_number,
                'record_lesson_link':record_lesson_link,
                'reason_cancellation':reason_cancellation,
                'tip_lesson': tip_lesson,
                'attendance': attendance,
                'course_lesson': course_lesson,
                'lesson_duration': lesson_duration,
                'language':lesson_language,
                'count_paid_students' : count_paid_students,
                'force_Majeure': force_Majeure,
                'first_pass': first_pass,
                'cancellation_more_eight': cancellation_more_eight,
                'cancellation_less_eight': cancellation_less_eight,
                'no_money' : no_money,
                'sale_PY': sale_PY
                }
            ]

def main():
    selenium = Selenium_test()
    selenium.start()
    selenium.steal_data_one_page_lessons()

main()