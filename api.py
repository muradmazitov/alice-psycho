#TaTaPiH
# coding: utf-8
from __future__ import unicode_literals
import random
import json
import logging
from flask import Flask, request
app = Flask(__name__)


logging.basicConfig(level=logging.DEBUG)

sessionStorage = {}

@app.route("/", methods=['POST'])

def main():
    logging.info('Request: %r', request.json)

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )

#Вопросы
Count = 21
Quest = [['Я не испытываю печали', 'Я подавлен и печален', 'Я страдаю от тоски и подавленности', 'Я настолько несчастен, что я больше не могу этого выносить'], ['Будущее не подавляет и не пугает меня', 'Будущее меня пугает', 'Я чувствую, что будущее совсем ничего не может мне предложить', 'Я чувствую, что будущее безнадежно, и не могу поверить, что что-то изменится в лучшую сторону'], ['Я не чувствую себя неудачником', 'Я чувствую, что неудачлив больше, чем другие', 'В прошлом я вижу лишь серию неудач', 'Я ощущаю себя полным неудачником'], ['Я не испытываю безразличия', 'Вещи и события не радуют меня, как раньше', 'Мне кажется, что я вообще ни от чего не получаю удовлетворения', 'Я ничего не хочу и всем недоволен'], ['Я не чувствую никакой вины за собой', 'Я чувствую себя плохим и никчемным человеком', 'Я чувствую себя плохим и никчемным практически всегда', 'Я чувствую себя очень плохим и ненужным'], ['Я не думаю, что меня накажут', 'Я чувствую, что со мной может случиться что-то плохое', 'Я верю, что меня судьба меня накажет', 'Я знаю, что я совершал такие поступки, за которые меня следует наказать'], ['Я не разочарован в себе', 'Я разочарован в себе', 'Я зол на себя', 'Я ненавижу себя'], ['Я не считаю себя хуже других', 'Я критикую свои слабости', 'Я виню себя за ошибки', 'Я виню себя за все, что идет не так'], ['Я не думаю о том, чтобы нанести себе вред', 'Я иногда думаю покончить с собой, но я не буду этого делать', 'Я реально думаю о самоубийстве', 'Я убью себя, как только представится возможность'], ['Я плачу не чаще обычного', 'Сейчас я плачу чаще, чем обычно', 'Я все время плачу', 'Я не могу заплакать, даже когда я хочу'], ['Я не более раздражен, чем обычно', 'Я раздражаюсь легче, чем обычно', 'Я все время раздражен', 'Меня уже не задевают те вещи, которые раньше раздражали'], ['Люди интересны мне по-прежнему', 'Другие люди интересуют меня меньше прежнего', 'Я почти утратил интерес и чувства к другим людям', 'Я полностью утратил интерес к людям и не обращаю на них внимания'], ['Я способен принимать решения, как и прежде', 'Я стараюсь избегать принятия решений', 'Мне очень трудно принимать решения', 'Я больше вообще не могу принимать решения'], ['По-моему, мой внешний вид не изменился', 'Я обеспокоен тем, что выгляжу постаревшим и непривлекательным', 'По-моему, мой внешний вид полностью изменился и я не выгляжу больше привлекательным', 'Я чувствую себя страшным и отталкивающим'], ['Моя работоспособность сохранилась на прежнем уровне', 'Начало работы требует от меня дополнительных усилий', 'Чтобы что-то сделать вовремя, мне нужно буквально заставлять себя', 'Я совсем не могу работать'], ['Я сплю так же хорошо, как обычно', 'По утрам я чувствую себя более усталым, чем раньше', 'Я просыпаюсь на 2-3 часа раньше обычного и больше не могу уснуть', 'Я просыпаюсь раньше обычного каждое утро и не могу проспать подряд более 5 часов'], ['Я устаю не больше обычного', 'Я устаю быстрее, чем раньше', 'Я устаю буквально на пустом месте', 'Я настолько устал, что не могу ничего делать'], ['Мой аппетит такой же, как и прежде', 'Мой аппетит слабее, чем прежде', 'Мой аппетит сильно ухудшился', 'У меня вообще нет аппетита'], ['Мой вес в последнее время сохранился на прежнем уровне', 'Я похудел больше, чем на 3 кг', 'Я похудел больше, чем на 5 кг', 'Я похудел больше, чем на 8 кг'], ['Я думаю о своем здоровье не чаще, чем обычно', 'Я все чаще замечаю разные боли и недомогания, расстройства желудка и запоры', 'Я настолько внимательно слежу за тем, что чувствую и как я себя чувствую, что не могу думать ни о чем другом', 'Я полностью погружен в мысли о своем здоровье и ощущениях'], ['Мой интерес к половой жизни не изменился', 'Мой интерес к половой жизни снизился', 'Мой интерес к половой жизни значительно снизился', 'Я полность потерял интерес к половой жизни']]

#generate Quest
'''f = open('suggestions_for_ans.txt', 'r')
for i in range(Count):
    n = 4
    temp = []
    while n != 0:
        s = f.readline().strip();
        if (s == ''):
            continue
        n -= 1
        temp.append(s)
    Quest.append(temp)
f.close()
print(Quest)
'''

def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']: 
        sessionStorage[user_id] = { 'suggests' : [ 'Да, хочу', 'Нет, не хочу'] , 'state' : 1 }
        res['response']['text'] = "Тест на определение уровня депрессии. Вы уверены что хотите продолжить и пройти этот тест?"
        
        res['response']['buttons'] = getSuggests(user_id)
        return
    
    
    if sessionStorage[user_id]['state'] == 1:
        if req['request']['command'].lower() in [
            'да',
            'да, хочу',
            'уверен',
            'ага',
            'агась',
        ]:
            res['response']['text'] = 'Хорошо, вас ждёт 21 вопрос. В каждом вопросе будет 4 варианта ответа, сначала прочитайте все варианты.\nВыберите одну альтернативу, которая наилучшим образом характеризует ваше состояние в данный момент.\nНачнем.'
            sessionStorage[user_id]['state'] = 2
            sessionStorage[user_id]['number'] = 0
            sessionStorage[user_id]['total'] = 0            
            sessionStorage[user_id]['suggests'] = Quest[0]
            res['response']['buttons'] = getSuggests(user_id)
            return
        else:
            res['response']['text'] = 'Навык выключен.'
            res['response']['end_session'] = True
            return
        
    qid = sessionStorage[user_id]['number']
    
    if req['request']['command'] in Quest[qid]:
        sessionStorage[user_id]['total'] += Quest[qid].index(req['request']['command']) 
        qid += 1
        
        if qid == 21:
            total = sessionStorage[user_id]['total'] 
            if 0 <= total <= 12:
                res['response']['text'] = 'По результатам теста могу сделать вывод, что у вас не наблюдается признаков депрессии.'
            elif 13 <= total <= 18:
                res['response']['text'] = 'По результатам теста могу сделать вывод, что у вас наблюдается легкая стадия депрессии.\nДля того чтобы избавиться от навязчивого состояния вам нужны: правильный режим сна, здоровая пища и регулярная физическая активность.'
            elif 19 <= total <= 29:
                res['response']['text'] = 'По результатам теста могу сделать вывод, что у вас наблюдается умеренная стадия депрессии. Рекомендую вам озаботиться своим здоровьем, ваше эмоциональное состояние может повлиять на ваше физическое состояние.\nПостарайтесть чаще делать физические упражнения, правильно питаться и восстановить свой режим. Также советую избегать конфликтных ситуаций.\nЕсли вам не помогают вышепересчисленные меры, обратитесь к психотерапевту'
            else:
                res['response']['text'] = 'По результатам теста могу сделать вывод, что у вас наблюдается тяжелая депрессия. Ваше состояние очень тяжелое, рекомендую обратиться к психотерапевту.\n8 (800) 100-49-94. Кризисная линия доверия. Круглосуточно.'
                res['response']['end_session'] = True
            return 
            
        
        sessionStorage[user_id]['number'] = qid
        sessionStorage[user_id]['suggests'] = Quest[qid]
        res['response']['text'] = 'Вопрос номер ' + str(qid + 1)
        res['response']['buttons'] = getSuggests(user_id)
        return
    else:
        res['response']['text'] = 'Пожалуйста выберите вариант ответа из предложенных.'
        res['response']['buttons'] = getSuggests(user_id)
        return

def getSuggests(session_id):
    session = sessionStorage[session_id]
    suggests = [
            {'title': suggest, 'hide': True}
            for suggest in session['suggests']
        ]
    random.shuffle(suggests)
    return suggests