import requests
import datetime
import random
from hidden import dj_url


class Student:
    def __init__(self, username, user_first_name, user_id):
        self.username = username
        self.user_first_name = user_first_name
        self.user_id = user_id
        self.tests = {}
        self.tests_for_grade = []
        self.current_test = None

    def get_tests(self):
        response = requests.get(dj_url + '/testing/')
        data = response.json()
        for i in data:
            if in_future(i["test_opening_date"], i["test_closing_date"]) or i['all_time_opened']:
                self.tests[i['test_name']] = {}
                self.tests[i['test_name']]['multis'] = i['multis']
                self.tests[i['test_name']]['matches'] = i['matches']
                self.tests[i['test_name']]['tf_tasks'] = i['tf_tasks']
                self.tests_for_grade = [i["test_name"], 0]

    def get_user_id_or_create(self):
        response = requests.get(dj_url+'/studs/student/')
        data = response.json()
        for usr in data:
            if usr['telegram_id'] == str(self.user_id):
                self.id = usr['id']
                self.json_tests = usr['tests']

                return None

        submit_data = {
            "name": self.user_first_name,
            "telegram_username" : self.username,
            "telegram_id": self.user_id,
            "tests": []
        }
        requests.post(dj_url+'/studs/student/', json=submit_data)
        response = requests.get(dj_url+'/studs/student/')
        data = response.json()
        for usr in data:
            if usr['telegram_id'] == str(self.user_id):
                self.id = usr['id']
                self.json_tests = usr['tests']

    def update_grade(self, point):
        self.tests_for_grade[1] += int(point)

    def submit_test(self):
        self.get_user_id_or_create()
        print(self.tests_for_grade)
        self.json_tests.append({
            "test_name" : self.tests_for_grade[0],
            "points_for_test" : self.tests_for_grade[1]
        })

        submit_data = {
            "name":self.user_first_name,
            "telegram_username": self.username,
            "telegram_id": self.user_id,
            "tests": self.json_tests}
        requests.put(dj_url+'/studs/student/{}/'.format(self.id), json=submit_data)
        self.tests_for_grade = []

    def __str__(self):
        return self.user_first_name


def in_future(opening_date, closing_date):
    opening_date, closing_date = convert_date(opening_date), convert_date(closing_date)
    opening_date, closing_date = datetime.datetime(*opening_date), datetime.datetime(*closing_date)
    return opening_date <= datetime.datetime.now() and closing_date > datetime.datetime.now()


def convert_date(str_date):
    str_date = str_date.replace('-', ' ').replace('T', ' ').replace('+', ' ').split()
    year, month, day, time, plus = str_date
    time = time.split(':')
    date = [year, month, day, time[0], time[1], time[2]]
    date = [int(i) for i in date]
    return date


def convert_task(type, task):
    choices_points = []
    task_text = ''
    if type == 'multis':
        task_text += task['question'] + '\n\n'
        for i, j in enumerate(task['multis_choices']):
            task_text += '{}) {}\n'.format(chr(97 + i), j['choice_text'])
            choices_points.append((chr(97+i), j['points']))
    elif type == 'tf_tasks':
        task_text = task['statement']
        if task['True?']:
            choices_points.append(('True', 1))
            choices_points.append(('False', 0))
        else:
            choices_points.append(('True', 0))
            choices_points.append(('False', 1))
    elif type == 'matches':
        right_choice = ''
        task_text1 = ''
        opt_dict = {}
        choice_combinations = []
        for i in task['match_options']:
            opt_dict[i['question_text']] = i['choice']
        choices = list(opt_dict.values())
        questions = list(opt_dict.keys())
        random.shuffle(questions)
        for i, j in enumerate(questions):
            task_text += '{}) {}\n'.format(i+1, j)
            right_choice += chr(choices.index(opt_dict[j])+97)
            task_text1 += '{}) {}\n'.format(chr(i+97), choices[i])
        task_text += '\n' + task_text1
        choices_points.append((right_choice, 1))
        choice_combinations.append(right_choice)
        choice = list(right_choice)
        print(choice)
        for i in range(3):
            while True:
                random.shuffle(choice)
                if ''.join(choice) not in choice_combinations:
                    break
            print(choice)
            text_choice = ''.join(choice)
            choice_combinations.append(text_choice)
            choices_points.append((text_choice, 0))
        random.shuffle(choices_points)

    return task_text, choices_points







