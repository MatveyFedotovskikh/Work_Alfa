import json


def lessons_no_info_url(lessons):
    list_in_list_error = [

    ]
    for lesson in lessons:
        no_lesson_number = False
        no_course_lesson = False
        no_comment       = False
        no_url           = False
        error = ''
        if lesson['attendance'] == True:
            if lesson['tip_lesson'] != 'Пробный':
                if lesson['lesson_number'] == '':
                    no_lesson_number = True    
            else:
                if lesson["comment"] == '':
                    no_comment = True
                    
            if lesson['record_lesson_link'] == '': 
                no_url = True

            if no_lesson_number:
                error+='Нет номера урока'
            if no_course_lesson:
                if error!='':
                    error+=', '
                error+='Не написан курс'
            if no_comment:
                if error!='':
                    error+=', '
                error+='Не написан коммент'
            if no_url:
                if error!='':
                    error+=', '
                error+='нет ссылки на запись'
                
            if error!='':
                list_in_list_error.append({lesson["link_student_for_mentors"]:{"link_student_for_teacher":lesson["link_student_for_teacher"],"date":lesson["date"],"time":lesson["datetime"],"error":error}})
                    
                
    return list_in_list_error

def main():
    list_error = {}
    with open('max_feb.json', encoding='utf-8') as fh:
        data = json.load(fh)
    for i in data:
        intermediate_list_in_list_error = lessons_no_info_url(data[i])
        if intermediate_list_in_list_error != []:
            list_error[i] = intermediate_list_in_list_error
            
    with open('max_feb_erorr.json', 'w', encoding='utf-8') as f:
        json.dump(list_error, f, ensure_ascii=False, indent=4)

main()



