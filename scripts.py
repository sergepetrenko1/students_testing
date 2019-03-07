import urllib.request, json
import random
import pprint

URL = 'http://10.10.225.169:8000/testing/'


def get_test_by_key(value, key='test_name'):
    try:
        # Get json data from server
        with urllib.request.urlopen(URL) as url:
            data = json.loads(url.read().decode())
        # Get test needed from data
        for test in data:
            if test[key] == value:
                return test
        return -1
    except Exception as err:
        print(err)
        return -1


def get_random_sequence_of_question(test):
    all_questions = test['matches'] + test['multis'] + \
        test['tf_tasks'] + test['word_boxes']
    random.shuffle(all_questions)
    return all_questions


def get_test_temp(value, key='test_name'):
    with open('testing data.json') as f:
        data = f.read()
        data = json.loads(data)
        print(data)
    for test in data:
        if test[key] == value:
            return test
    return -1


def convert_questions(questions, type):
    res = dict()
    # Numerate empty spaces for future data
    for question, question_num in enumerate(questions):
        converted_question = dict()
        converted_question['text'] = question['task_name']
        converted_question['options' ] = question[type]


def save_json():
    with open('testing data.json', 'w') as f:
        with urllib.request.urlopen(URL) as url:
            data = json.loads(url.read().decode())
            json.dump(data, f)
            pprint.pprint(data)


if __name__ == '__main__':

    save_json()
    # current_test = get_test_temp('New New Test')
    # print(current_test)
    # current_questions = get_random_sequence_of_question(current_test)
    # print(current_questions)