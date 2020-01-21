from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api import VkUpload
import random
import requests
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import vk_api
import json
import pygame
import re
import datetime
print ('-' * 40)


# Настройки
session = requests.Session()
token =  '44a9cbb38e0f07020e625ba2615257624c6fbb07455396fa0c6acea1d6e3136c2596655e0451e47ef97c0'
vk_session = vk_api.VkApi(token=token)
longpoll = VkLongPoll (vk_session) # Отслеживает активность с группой через сервера
vk = vk_session.get_api()
upload = vk_api.VkUpload(vk_session)
bad_words = []
help_command = ['/помощь','/help', '!помощь', '/помощь', '!help', 'помощь']


                                       # Клавиатура

empty = {"buttons":[],"one_time":True}

                                        # Казино
keyboard_casino = {"one_time": False,"buttons": [
    [{
      "action": {
        "type": "text",
        "label": "Начать игру"
      },
      "color": "positive"
    }]
]}

casino_play = {'one_time': False, 'buttons': [
    [{
       "action": {
         "type": "text",
         "label": "2x2",
         "payload": "{\"button\": \"1\"}"

       },
       "color": "primary"
     },
     {
       "action": {
        "type": "text",
        "label": "3x3",
        "payload": "{\"button\": \"2\"}"

       },
       "color": "positive"
     },
     {
       "action": {
        "type": "text",
        "label": "zero (поставить на ноль)",
        "payload": "{\"button\": \"3\"}"
       },
       "color": "secondary"
     }],
     [{
       "action": {
         "type": "text",
         "label": "Закончить",
         "payload": "{\"button\": \"4\"}"
       },
       "color": "negative"
     }]
]}

_3x3_ = {'one_time': False, 'buttons': [
    [{
       "action": {
         "type": "text",
         "label": "Первая 12",
         "payload": "{\"button\": \"1\"}"

       },
       "color": "primary"
     },
     {
       "action": {
        "type": "text",
        "label": "Вторая 12",
        "payload": "{\"button\": \"2\"}"

       },
       "color": "primary"
     },
     {
       "action": {
        "type": "text",
        "label": "Третья 12",
        "payload": "{\"button\": \"3\"}"
       },
       "color": "primary"}]
]}
_2x2_ = {'one_time': False, 'buttons': [
    [{
       "action": {
         "type": "text",
         "label": "Красный",
         "payload": "{\"button\": \"1\"}"

       },
       "color": "negative"
     },
     {
       "action": {
        "type": "text",
        "label": "Черный",
        "payload": "{\"button\": \"2\"}"

       },
       "color": "secondary"
     }],
     [{
       "action": {
        "type": "text",
        "label": "Закончить",
        "payload": "{\"button\": \"3\"}"
       },
       "color": "negative"}]
]}




class Commands():
	def __init__(self, response, peer_id,  user_id, chat_id = '', message_id = ""):
		self.response = response 
		self.peer_id =peer_id
		self.user_id = user_id
		if chat_id:
			self.chat_id = chat_id
		if message_id:
			self.message_id = message_id

			                                   # Казино
	def casino(self):
		send(id_type = 'peer_id', id = (self.peer_id), message = 
			('Мини-игра включена'), keyboard = json.dumps(keyboard_casino))
		words_casino = self.response.split(' ')



		                                       # Узнает информацию
	def info_chat(self):		
		info = requests.get('http://api.vk.com/method/' + 'messages.getConversationMembers',
			{
			'v' : 5.92,
			'access_token': '44a9cbb38e0f07020e625ba2615257624c6fbb07455396fa0c6acea1d6e3136c2596655e0451e47ef97c0',
			'peer_id': self.peer_id,
			'fields': "last_seen"
			})
		return info.text


		                                        # Создает картинку
	def create_image(self, text_of_user):
		try:
			words_01 = ''
			for word_01 in text_of_user:
				if words_01 == '':
					words_01 += word_01
				else:
					words_01 += ' ' + word_01
			pygame.init()
			screen = pygame.display.set_mode((1080, 480))
			bg = pygame.image.load("Images/Шизойд.bmp")
			screen.blit(bg, (0,0))
			text_of_user = re.split(r';', words_01)
			if len(text_of_user) == 2:
				info = get_info(user_ids = self.user_id, name_case = 'Gen')
				profile = info[0]
				text_of_disness = text_of_user[0]
				text_of_recom = text_of_user[1]
			elif len(text_of_user) >=3:	
				info_text = text_of_user[0].replace('https://vk.com/id', "").replace(';','')
				info_text = get_info(user_ids = info_text, name_case = 'Gen')
				profile = info_text[0]	
				text_of_disness = text_of_user[1]
				text_of_recom = text_of_user[2]
			a = ''	
			a = a + profile['first_name'] + ' ' + profile['last_name']
			text = pygame.font.SysFont('arial', 36)
			text_01_1 = ('Медицинская история больного ' + a)
			text_01 = text.render(text_01_1, 0, (0,0,0))
			text_02_1 = ('Болезнь пациента: ' + str(text_of_disness.lstrip()))
			text_02 = text.render(text_02_1, 0, (0,0,0))
			text_03_1 = ('Рекомендации: ' + str(text_of_recom.lstrip()))
			text_03 = text.render(text_03_1, 0, (0,0,0))
			name = ('Удостоверение_больного.jpg')
			print ('picture ' + name + ' has been saved!')
			print ('-' * 40)	
			screen.blit(text_01, (240, 100))
			screen.blit(text_02, (260, 150))
			screen.blit(text_03, (280, 200))
			pygame.display.update()
			pygame.display.flip()
			pygame.image.save(screen, name)
			a = vk_session.method('photos.getMessagesUploadServer')
			b = requests.post(a['upload_url'], 
				files={'photo': open(name, 'rb')}).json()
			c = vk_session.method('photos.saveMessagesPhoto', {'photo': b['photo'], 'server': b['server'], 'hash': b['hash']})[0]
			d = 'photo{}_{}'.format(c['owner_id'], c['id'])
			send(id_type = 'peer_id', id = (self.peer_id), message = ('Вот ваша медицинская история:')
				, attachment = d)
		except UnicodeError:
			send(id_type = 'peer_id', id = (self.peer_id), message = 
				('Вот скажи мне, ты мудак??? Мало того, что ты шизойд долбанный, так ты еще ебанный насос. Ну давай разберем тобою написанное: ' + 
					str(text_of_user) + ' Складывается впечатление что ты реально контуженный , обиженный жизнью имбицил )) Ты, рэмбо комнатный, я уже тебя вычислил ' +
					"Твой айпи уже вычислено, и за тобой уже напрвалено команда санитаров. Тебя уже ждет мягкая комната со смерительной рубашкой))))"))
		except UnboundLocalError:
			send(id_type = 'peer_id', id = (self.peer_id), message = 
				('Шизойдина, ты забыл что-то написать!'))				
		except KeyError:
			send(id_type = 'peer_id', id = (self.peer_id), message = 'Неккоректный id')


		                                        # Поиск команд
	def search(self):
		self.flag_for_censored = True
		commands = Commands((self.response), (self.peer_id), (self.user_id))
		words = self.response
		words = words.split(' ')
		if words[0] == '/инфо':
			info = commands.info_chat()
			info = json.loads(info)	
			info = info['response']
			profiles = info['profiles']
			profile_list = ''
			for profile in profiles:
				a = (str(profile['first_name']) + ' ' + str(profile["last_name"]))
				profile_list = str(profile_list + str("\n\t" + a))
			send(id_type = 'peer_id', id = (self.peer_id), message = ('Участников в беседе: ' + str(profile_list)))
		if words[0] == '/справка':
				words[0], *text_of_user = words
				commands.create_image(text_of_user)
		if words[0] in help_command:
			a = 'Список комманд бота:\n1. /инфо - возвращает информцию об участниках\n2. /вклцензура - включает цензуру'
			b = "\n3. /выклцензура - выключает функцию '/вклцензура'\n4. /справка - создает справку пользователя.\nПример: /справка *id пользоватлея*(если опустить, то возьмет Ваш id); *болезнь*; *рекомендации*"
			с = "\n5. /казино - включает мини-игру"
			send(id_type = 'peer_id', id = (self.peer_id), message = (a + ' ' + b + " " + с))
		if words[0] == '/казино':
			commands.casino()


                                                # Возвращает id
def get_info(user_ids, name_case = '' , fields = ''):
	# http://api.vk.com/method/users.get?
	answer = requests.get('http://api.vk.com/method/' + 'users.get',
		{
		'v' : 5.92,
		'access_token': '44a9cbb38e0f07020e625ba2615257624c6fbb07455396fa0c6acea1d6e3136c2596655e0451e47ef97c0',
		'user_ids': user_ids,
		'name_case': name_case,
		'fields': fields
		})
	answer = answer.text
	# Обращаемся по имени
	# https://api.vk.com/method/users.get?user_id=210700286&v=5.52
	answer = json.loads(answer)
	info = answer['response']
	return info


def match(color, color_match, peer_id):
	if color == color_match[0]:
		send(id_type = 'peer_id',
			id = peer_id,
			message = 'Выиграш. Цвет ячейки совпал',
			keyboard = json.dumps(empty))
	else:
		if color_match[0] == 2:
			send(id_type = 'peer_id',
				id = peer_id,
				message = 'Проигрыш. Выпал ноль',
				attachment = 'doc27549026_530435226',
				keyboard = json.dumps(empty))
		else:
			send(id_type = 'peer_id',
				id = peer_id,
				message = 'Проигрыш. Цвет не тот',
				attachment = 'doc27549026_530435226',
				keyboard = json.dumps(empty))


	                                            # Сообщение с ЛС
def from_user_mess(response, id_type, user_id):
	person = get_info(event.user_id)
	person = person[0]
	if response == 'привет':
		person = get_info(user_id)
		person = person[0]
		print ('Пришло сообщение: '+ "'" +str(response) + "'" +' oт ' + (str(person['first_name']) + ' ' + str(person['last_name'])))
		print ('-' * 40)
		send(id_type = id_type, id = user_id ,message = ('Привет, ' + str(person['first_name'] + ' ' + str(person['last_name']))))
	elif response in bad_words:
		print ('Пришло сообщение: '+ "'" +str(response) + "'" +' oт ' + (str(person['first_name']) + ' ' + str(person['last_name'])))
		print ('-' * 40)
		send(id_type = id_type, id = user_id ,message = 'Не матерись',
			attachment = 'photo-190440655_457239019')


		                               # Отправка сообщения в беседу
def from_chat_mess(response, id_type,chat_id, user_id, peer_id, message_id):
	person = get_info(event.user_id)
	if response == 'привет':
		person = get_info(user_id)
		person = person[0]
		send(id_type = id_type, id = chat_id ,message = ('Привет, ' + str(person['first_name'] + ' ' + str(person['last_name']))))	

                    
                                                # Удаляет сообщение
def delete(message_id):
	vk_session.method('messages.delete',{
		'message_id': message_id,
		'delete_for_all': 1
		})


		                             # Краткий вызов функции отправки
def send(id_type, id, message = "", attachment= "", reply_to = '', keyboard = ''):
    vk_session.method('messages.send',{
    	id_type: id,
    	'message': message,
    	'random_id': random.randint(111111,9999999),
    	"attachment": attachment,
    	'reply_to': reply_to,
    	'keyboard': keyboard
    	})


while True:
	for event in longpoll.listen():
		if event.type == VkEventType.MESSAGE_NEW:
			if event.to_me:
				response = event.text.lower()


				                               # Сообщение от пользователя
				if event.from_user:
					commands = Commands(response = response, peer_id = event.peer_id, user_id = event.user_id)
					commands.search()
					from_user_mess(response, 'user_id', event.user_id)  


                                                         # Казино 
					if response == 'закончить':
						send(id_type = 'peer_id', 
							id = (event.peer_id), 
							message = ('Мини-игра окончена'), 
							keyboard = json.dumps(empty))            
					if response == 'начать игру':
						send(id_type = 'peer_id', 
							id = (event.peer_id), 
							message = ('Что выбираем?'), 
							keyboard = json.dumps(casino_play),
							attachment = 'photo-190440655_457239091')

                                                            # 2х2
					if response == '2x2':							
						send(id_type = 'peer_id', id = (event.peer_id), message = 
							('На что ставите?'), keyboard = json.dumps(_2x2_),
							attachment = 'photo-190440655_457239092')
						color_casino = [0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,2]
						random.shuffle(color_casino)
					if response == 'черный':
						color = 1
						match(color, color_casino, event.peer_id)	
					if response == 'красный':						
						color = 0
						match(color, color_casino, event.peer_id)	

					                          # 3x3						                                   
					if response == '3x3':
						send(id_type = 'peer_id', id = (event.peer_id), message = # первая 12
							('На что ставите?'), keyboard = json.dumps(_3x3_), 
							attachment = 'photo-190440655_457239092')
					if response == 'первая 12': 
						option_casino = [i for i in range(1,13)]
						option = [i for i in range(1,37)]
						send(id_type = 'peer_id', 
							id = (event.peer_id),
							message = 'Ставка принята',
							attachment = 'doc227973627_528053399')
						for b in range (1,4):
							random.shuffle(option)
							send(id_type = 'peer_id', 
								id = (event.peer_id),
								message = (option[0]))
						if option[0] in option_casino:
							send(id_type = 'peer_id', 
								id = (event.peer_id),
								message = ("Вам выпало: " + str(option[0]) 
									+ '. Выиграш!'),
								keyboard = json.dumps(empty))	
						else:
							send(id_type = 'peer_id', 
								id = (event.peer_id),
								message = ("Вам выпало: " + str(option[0]) 
									+ '. Вы проиграли...'),
								keyboard = json.dumps(empty))																			
					if response == 'вторая 12':	 # вторая 12
						option_casino = [i for i in range(13,25)]
						option = [i for i in range(1,37)]
						send(id_type = 'peer_id', 
							id = (event.peer_id),
							message = 'Ставка принята',
							attachment = 'doc227973627_528053399')
						for b in range (1,4):
							random.shuffle(option)
							send(id_type = 'peer_id', 
								id = (event.peer_id),
								message = (option[0]))							
						if option[0] in option_casino:
							send(id_type = 'peer_id', 
								id = (event.peer_id),
								message = ("Вам выпало: " + str(option[0]) 
									+ '. Выиграш!'),
								keyboard = json.dumps(empty))	
						else:
							send(id_type = 'peer_id', 
								id = (event.peer_id),
								message = ("Вам выпало: " + str(option[0]) 
									+ '. Вы проиграли...'),
								keyboard = json.dumps(empty))								
					if (response == 'третья 12'):	   # третья 12
						option_casino = [i for i in range(25,37)]
						option = [i for i in range(1,37)]
						send(id_type = 'peer_id', 
							id = (event.peer_id),
							message = 'Ставка принята',
							attachment = 'doc227973627_528053399')
						for b in range (1,4):
							random.shuffle(option)
							send(id_type = 'peer_id', 
								id = (event.peer_id),
								message = (option[0]))
						if option[0] in option_casino:
							send(id_type = 'peer_id', 
								id = (event.peer_id),
								message = ("Вам выпало: " + str(option[0]) 
									+ '. Выиграш!'),
								keyboard = json.dumps(empty))	
						else:
							send(id_type = 'peer_id', 
								id = (event.peer_id),
								message = ("Вам выпало: " + str(option[0]) 
									+ '. Вы проиграли...'),
								keyboard = json.dumps(empty))											


                                                                # Сообщение из беседы
				elif event.from_chat:
					print (response)
					commands = Commands(response = response, peer_id = event.peer_id, 
						user_id = event.user_id, chat_id = event.chat_id , message_id = event.message_id)
					commands.search()
					from_chat_mess(response,'chat_id' ,event.chat_id, event.user_id, event.peer_id , event.message_id)

                                                        # Функции бота
					if response == '/вклцензура':
						bad_words = ['сука','блин','блять','блядь','ахуеть','ёпта','епта','бля','ебать','хуй']
						send(id_type = 'peer_id', 
							id = event.peer_id, 
							message = ('Фильтрация слов включена'), 
							reply_to = event.message_id)
					elif response == '/выклцензура':
						bad_words = []
						send(id_type = 'peer_id', 
							id = event.peer_id, 
							message = ('Фильтрация слов отключена'), 
							reply_to = event.message_id)	
					if response in bad_words:
						try:
							delete(event.message_id)
						except vk_api.exceptions.ApiError: 
							send(id_type = 'peer_id', id = event.peer_id, message = ('Нельзя удалить сообщение'))	

                                                       # Казино
					if response == '[club190440655|@club190440655] закончить' or (response == '[club190440655|санитар-бот] закончить'):
						if event.user_id == current_id:
							send(id_type = 'peer_id', 
								id = (event.peer_id), 
								message = ('Мини-игра окончена'), 
								keyboard = json.dumps(empty)) 
						else:
							delete(event.message_id)
					if response == '[club190440655|@club190440655] начать игру'  or (response == '[club190440655|санитар-бот] начать игру'):
						current_id = event.user_id
						print (current_id)
						send(id_type = 'peer_id', 
							id = (event.peer_id), 
							message = ('Что выбираем?'), 
							keyboard = json.dumps(casino_play),
							attachment = 'photo-190440655_457239091')
       
                                                            # 2х2
					if response == '[club190440655|@club190440655] 2x2'  or (response == '[club190440655|санитар-бот] 2x2'):							
						if event.user_id == current_id: 
							print (event.user_id)	
							print (current_id)						
							send(id_type = 'peer_id', id = (event.peer_id), message = 
								('На что ставите?'), keyboard = json.dumps(_2x2_),
								attachment = 'photo-190440655_457239092')
							color_casino = [0,1,0,1,0,1,0,1,2]
							random.shuffle(color_casino)
						else:
							print (event.user_id)	
							print (current_id)	
							delete(event.message_id)
					if response == '[club190440655|@club190440655] черный'  or (response == '[club190440655|санитар-бот] черный'):
						if event.user_id == current_id: 
							color = 1
							match(color, color_casino, event.peer_id)
						else:
							delete(event.message_id)	
					if response == '[club190440655|@club190440655] красный'  or (response == '[club190440655|санитар-бот] красный'):
						if event.user_id == current_id: 						
							color = 0
							match(color, color_casino, event.peer_id)
						else:
							delete(event.message_id)	

                                                            # 3x3
					if response == '[club190440655|@club190440655] 3x3' or (response == '[club190440655|санитар-бот] 3x3'):
						if event.user_id == current_id: 
							send(id_type = 'peer_id', id = (event.peer_id), message = 
								('На что ставите?'), keyboard = json.dumps(_3x3_), 
								attachment = 'photo-190440655_457239092')
						else:	
							delete(event.message_id)
					if response == '[club190440655|@club190440655] первая 12' or (response == '[club190440655|санитар-бот] первая 12'):	
						if event.user_id == current_id: 
							option_casino = [i for i in range(1,13)]
							option = [i for i in range(1,37)]
							send(id_type = 'peer_id', 
								id = (event.peer_id),
								message = 'Ставка принята',
								attachment = 'doc227973627_528053399')
							for b in range (1,4):
								random.shuffle(option)
								send(id_type = 'peer_id', 
									id = (event.peer_id),
									message = (option[0]))
							if option[0] in option_casino:
								send(id_type = 'peer_id', 
									id = (event.peer_id),
									message = ("Вам выпало: " + str(option[0]) 
										+ '. Выиграш!'),
									keyboard = json.dumps(empty))	
							else:
								send(id_type = 'peer_id', 
									id = (event.peer_id),
									message = ("Вам выпало: " + str(option[0]) 
										+ '. Вы проиграли...'),
									keyboard = json.dumps(empty))				
						else:	
							delete(event.message_id)
					if response == '[club190440655|@club190440655] вторая 12' or (response == '[club190440655|санитар-бот] вторая 12'):	
						if event.user_id == current_id: 
							option_casino = [i for i in range(13,25)]
							option = [i for i in range(1,37)]
							send(id_type = 'peer_id', 
								id = (event.peer_id),
								message = 'Ставка принята',
								attachment = 'doc227973627_528053399')
							for b in range (1,4):
								random.shuffle(option)
								send(id_type = 'peer_id', 
									id = (event.peer_id),
									message = (option[0]))
							if option[0] in option_casino:
								send(id_type = 'peer_id', 
									id = (event.peer_id),
									message = ("Вам выпало: " + str(option[0]) 
										+ '. Выиграш!'),
									keyboard = json.dumps(empty))
							else:
								send(id_type = 'peer_id', 
									id = (event.peer_id),
									message = ("Вам выпало: " + str(option[0]) 
										+ '. Вы проиграли...'),
									keyboard = json.dumps(empty))			
						else:	
							delete(event.message_id)	
					if response == '[club190440655|@club190440655] третья 12' or (response == '[club190440655|санитар-бот] третья 12'):	
						if event.user_id == current_id: 
							option_casino = [i for i in range(25,37)]
							option = [i for i in range(1,37)]
							send(id_type = 'peer_id', 
								id = (event.peer_id),
								message = 'Ставка принята',
								attachment = 'doc227973627_528053399')
							for b in range (1,4):
								random.shuffle(option)
								send(id_type = 'peer_id', 
									id = (event.peer_id),
									message = (option[0]))
							if option[0] in option_casino:
								send(id_type = 'peer_id', 
									id = (event.peer_id),
									message = ("Вам выпало: " + str(option[0]) 
										+ '. Выиграш!'),
									keyboard = json.dumps(empty))	
							else:
								send(id_type = 'peer_id', 
									id = (event.peer_id),
									message = ("Вам выпало: " + str(option[0]) 
										+ '. Вы проиграли...'),
									keyboard = json.dumps(empty))		
						elif event.user_id != current_id:
							delete(event.message_id)

                                         # Сталкер-бот

# n = 1
# e = ' не в сети до '
# while 1:
# 	online_of_user = get_info(user_ids = 390964742, fields = 'last_seen, online')
# 	online_of_user = online_of_user[0]
# 	activity_username = online_of_user['first_name']  + ' ' + online_of_user['last_name']
# 	activity_online = online_of_user['online']
# 	activity_last_seen_01 = online_of_user['last_seen']
# 	activity_last_seen = datetime.datetime.fromtimestamp(activity_last_seen_01['time'])	
# 	activity_platform = activity_last_seen_01['platform']
# 	if activity_platform == 1:
# 		activity_platform = ' с мобильного сайте.'
# 	elif activity_platform == 2:
# 		activity_platform = ' с айфона.'
# 	elif activity_platform == 3:
# 		activity_platform = ' с айпада.'
# 	elif activity_platform == 4:
# 		activity_platform = ' с андройда.'
# 	elif activity_platform == 5:
# 		activity_platform = ' с виндовс фона.'
# 	elif activity_platform == 6:
# 		activity_platform = ' с виндовс 10.'
# 	elif activity_platform == 7:
# 		activity_platform = ' с компьютера.'
# 	if activity_online != n:
# 		print ('!!!!!! Пользователь ' + activity_username + e + str(activity_last_seen) + str(activity_platform))
# 		if n == 0:
# 			n += 1
# 			e = ' не в сети до '
# 		elif n == 1:
# 			e = ' в сети с '
# 			n -= 1
# 	else:
# 		continue
# v = 1
# q = ' не в сети до '
# while 1:
# 	online_of_user_01 = get_info(user_ids = 306520119, fields = 'last_seen, online')
# 	online_of_user_01 = online_of_user_01[0]
# 	activity_username_01 = online_of_user_01['first_name']  + ' ' + online_of_user_01['last_name']
# 	activity_online_01 = online_of_user_01['online']
# 	activity_last_seen_01_01 = online_of_user_01['last_seen']
# 	activity_last_seen_01_1 = datetime.datetime.fromtimestamp(activity_last_seen_01_01['time'])		
# 	if activity_platform_01 == 1:
# 		activity_platform_01 = ' с мобильного сайте.'
# 	elif activity_platform_01 == 2:
# 		activity_platform_01 = ' с айфона.'
# 	elif activity_platform_01 == 3:
# 		activity_platform_01 = ' с айпада.'
# 	elif activity_platform_01 == 4:
# 		activity_platform_01 = ' с андройда.'
# 	elif activity_platform_01 == 5:
# 		activity_platform_01 = ' с виндовс фона.'
# 	elif activity_platform_01 == 6:
# 		activity_platform_01 = ' с виндовс 10.'
# 	elif activity_platform_01 == 7:
# 		activity_platform_01 = ' с компьютера.'
# 	if activity_online_01 != v:
# 		print ('Пользователь ' + activity_username + e + str(activity_last_seen_01_1) + str(activity_platform_01))
# 		if v == 0:
# 			v += 1
# 			q = ' не в сети до '
# 		elif n == 1:
# 			q = ' в сети с '
# 			v -= 1
# 	else:
# 		continue
# w = 1
# t = ' не в сети до '
# while 1:	
# 	online_of_user_02 = get_info(user_ids = 234364920, fields = 'last_seen, online')
# 	online_of_user_02 = online_of_user_02[0]
# 	activity_username_02 = online_of_user_02['first_name']  + ' ' + online_of_user_02['last_name']
# 	activity_online_02 = online_of_user_02['online']
# 	activity_last_seen_01_02 = online_of_user_02['last_seen']
# 	activity_last_seen_02 = datetime.datetime.fromtimestamp(activity_last_seen_01_02['time'])		
# 	if activity_platform_02 == 1:
# 		activity_platform_02 = ' с мобильного сайте.'
# 	elif activity_platform_02 == 2:
# 		activity_platform_02 = ' с айфона.'
# 	elif activity_platform_02 == 3:
# 		activity_platform_02 = ' с айпада.'
# 	elif activity_platform_02 == 4:
# 		activity_platform_02 = ' с андройда.'
# 	elif activity_platform_02 == 5:
# 		activity_platform_02 = ' с виндовс фона.'
# 	elif activity_platform_02 == 6:
# 		activity_platform_02 = ' с виндовс 10.'
# 	elif activity_platform_02 == 7:
# 		activity_platform_02 = ' с компьютера.'
# 	if activity_online_02 != w:
# 		print ('Пользователь ' + activity_username + e + str(activity_last_seen_02) + str(activity_platform_02))
# 		if w == 0:
# 			w += 1
# 			t = ' не в сети до '
# 		elif w == 1:
# 			t = ' в сети с '
# 			w -= 1
# 	else:
# 		continue
# i = 1
# p = ' не в сети до '
# while 1:
# 	online_of_user_03 = get_info(user_ids = 419843014, fields = 'last_seen, online')
# 	online_of_user_03 = online_of_user_03[0]
# 	activity_username_03 = online_of_user_03['first_name']  + ' ' + online_of_user_03['last_name']
# 	activity_online_03 = online_of_user_03['online']
# 	activity_last_seen_01_03 = online_of_user_03['last_seen']
# 	activity_last_seen_03 = datetime.datetime.fromtimestamp(activity_last_seen_01_03['time'])		
# 	if activity_platform_03 == 1:
# 		activity_platform_03 = ' с мобильного сайте.'
# 	elif activity_platform_03 == 2:
# 		activity_platfor_03 = ' с айфона.'
# 	elif activity_platform_03 == 3:
# 		activity_platform_03 = ' с айпада.'
# 	elif activity_platform_03 == 4:
# 		activity_platform_03 = ' с андройда.'
# 	elif activity_platform_03 == 5:
# 		activity_platform_03 = ' с виндовс фона.'
# 	elif activity_platform_03 == 6:
# 		activity_platform_03 = ' с виндовс 10.'
# 	elif activity_platform_03 == 7:
# 		activity_platform_03 = ' с компьютера.'
# 	if activity_online_03 != i:
# 		print ('Пользователь ' + activity_username + e + str(activity_last_seen) + str(activity_platform))
# 		if i == 0:
# 			i += 1
# 			p = ' не в сети до '
# 		elif i == 1:
# 			p = ' в сети с '
# 			i -= 1
# 	else:
# 		continue