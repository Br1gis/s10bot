import telebot
from telebot import types
import bs4
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3



client = telebot.TeleBot("5057236580:AAFMFIUGavEp9j42Y-8YoWlLISUAkD4uEW4")




admins = ['The_Brigis','kharitinov']

rep_cd = []

db = sqlite3.connect('userbase.db', check_same_thread = False)
sql = db.cursor()


def main_menu(message):
	reply_markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
	school_adress = types.KeyboardButton(text = "Адрес школы")
	school_contact = types.KeyboardButton(text = "Как связаться")
	school_register = types.KeyboardButton(text = "Как поступить")
	school_quess = types.KeyboardButton(text = "Частые вопросы")
	school_question = types.KeyboardButton(text = "Вопрос директору")
	school_subs = types.KeyboardButton(text = "Подписаться")
	reply_markup.add(school_adress, school_contact, school_register, school_quess, school_question, school_subs)
	client.send_message(message.chat.id, 'Приветствую!', reply_markup = reply_markup)


def rass_news(message):
	textik = message.text 
	c = sqlite3.connect("userbase.db")
	cur = c.cursor()

	cur.execute("SELECT user_id FROM users")
	rows = cur.fetchall()
	for row in range(len(rows)):
		if rows[row][0] is None:
			continue
		else:
			for i in sql.execute(f"SELECT subnews FROM users WHERE user_id = {message.from_user.id}"):
				if i[0] == 0:
					continue
				else:
					time.sleep(1)
					client.send_message(rows[row][0], f'{textik}')
					print(rows[row][0])
	client.send_message(message.chat.id, '✅ Рассылка завершена!')
	admin_panel(message)


def rass_route(message):
	textik = message.text 
	c = sqlite3.connect("userbase.db")
	cur = c.cursor()

	cur.execute("SELECT user_id FROM users")
	rows = cur.fetchall()
	for row in range(len(rows)):
		if rows[row][0] is None:
			continue
		else:
			for i in sql.execute(f"SELECT subup FROM users WHERE user_id = {message.from_user.id}"):
				if i[0] == 0:
					continue
				else:
					time.sleep(1)
					client.send_message(rows[row][0], f'{textik}')
					print(rows[row][0])
	client.send_message(message.chat.id, '✅ Рассылка завершена!')
	admin_panel(message)




def reg(message):
	db = sqlite3.connect('userbase.db')
	sql = db.cursor()
	name = message.from_user.first_name
	user_id = message.from_user.id
	sql.execute(f"SELECT name FROM users WHERE user_id = {user_id}")
	if sql.fetchone() is None:
		user_id = message.from_user.id
		name = message.from_user.first_name
		sql.execute(f"INSERT INTO users VALUES (?, ?, ?, ?)", (name, user_id, 0, 0))
		db.commit()
		client.send_message(message.chat.id, 'Отлично! Вы зарегистрированы!')
		main_menu(message)
	else:
		main_menu(message)


def admin_panel(message):
	if not message.from_user.username in admins:
		client.send_message(message.chat.id, 'Вы не являетесь администратором!')
	else:
		adm_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		item_rassylka = types.KeyboardButton(text = "Начать рассылку")
		item_back = types.KeyboardButton(text = "Выйти из панели")
		adm_reply.add(item_rassylka, item_back)
		client.send_message(message.chat.id, 'Админ-панель', reply_markup = adm_reply)


def goemail(message):
	emailanswer = message.text
	try:
		#msg = MIMEMultipart()
		#msg.attach(MIMEText(textmailik, 'plain'))

		server = smtplib.SMTP('smtp.mail.ru: 25')
		server.starttls()
		server.login("oksry01@mail.ru", "G3x5Dis0WVjPq41zsD7L")
		server.sendmail("oksry01@mail.ru","bchol@yandex.ru",f"Новое сообщение от пользователя бота Школа 10!\nИмя: {names}\nТекст вопроса: {textmailik}\nНомер телефона для связи: {emailanswer}".encode('utf-8'))
		client.send_message(message.chat.id, 'Ваш вопрос был успешно отправлен на рассмотрение! Ожидайте ответа на указанный номер телефона')
	except Exception as e:
		client.send_message(message.chat.id, 'Что-то пошло не так! Попробуйте снова.')
		print(e)


def answer(message):
	global textmailik
	textmailik = message.text
	msg = client.send_message(message.chat.id, 'Отлично! Остался последний шаг. Напишите свой номер телефона для связи (пример - 89108872921):')
	client.register_next_step_handler(msg, goemail)


def report(message):
	reptext = message.text
	if not message.from_user.id in rep_cd:
		client.send_message(message.chat.id, 'Отлично! Ваш запрос был отправлен!')
		client.send_message(984674439, f'Новый баг-репорт от {message.from_user.username}:\n{reptext}')
		rep_cd.append(message.from_user.id)
		time.sleep(3600)
		print('ok')
		rep_cd.remove(message.from_user.id)
	if message.from_user.id in rep_cd:
		client.send_message(message.chat.id, 'Вы можете отправлять сообщения об ошибке только с перерывом в 1 час!')


def textmail(message):
	global names
	names = message.text
	if names == "-":
		client.send_message(message.chat.id, 'Отмена действия')
	else:
		msg = client.send_message(message.chat.id, 'Теперь напишите текст вопроса:')
		client.register_next_step_handler(msg, answer)


@client.message_handler(content_types = ['text'])
def get_text(message):
	if message.text == '/start':
		reg(message)
	if message.text == '/admin':
		admin_panel(message)
	if message.text == 'Адрес школы':
		client.send_message(message.chat.id, 'Наша школа находится по адресу:\nРоссийская Федерация, Нижегородская обл., г.Павлово ул. Суворова, 4')
	if message.text == 'Как связаться':
		client.send_message(message.chat.id, 'Контактные данные для связи:\nТелефон: +7 (83171) 2-08-70\nEmail: pav_s10@mail.ru\nСайт: http://s10pav.ru')
	if message.text == 'Как поступить':
		client.send_message(message.chat.id, 'Для поступления необходимо иметь при себе следующие документы:\n• Заявление (файл ниже)\n• Копия документа, удостоверяющего личность родителя (законного представителя) ребенка.\n• Копия свидетельства о рождении или документа, подтверждающего родство заявителя.\
			\n• Копия свидетельства о регистрации ребенка по месту жительства или свидетельства о регистрации ребенка по месту пребывания на закрепленной территории.\n• Копия документа, подтверждающего  установление опеки или попечительства (при необходимости).\
			\n• Копия документа, подтверждающего право заявителя на пребывание в Российской Федерации (для иностранных граждан).\n• Справка с места работы родителя(ей) (законного(ых) представителя(ей) ребенка (при наличии права внеочередного или первоочередного приема на обучение).\
			\n• Копия заключения психолого-медико-педагогической комиссии (при наличии).\n\nКсерокопии документов принимаются при наличии оригиналов!\nГрафик приема: понедельник-пятница с 13.00 до 16.00 час.')
		file = open("zaiavl-1-klass.docx", "rb")
		client.send_document(message.chat.id, file)
	if message.text == "Частые вопросы":
		client.send_message(message.chat.id, 'Ответы на часто-задаваемые вопросы:\n*Могут ли дети самостоятельно добираться домой из школы?* Да, по заявлению родителей.\n*Можно ли выбрать учителя?* Нет, учителей для классов назначает директор.\n*Можно ли выбрать меню в столовой?* Меню составлено с учетом САНПиН и утверждается директором.\n*Сколько дней может пропустить ребёнок без справки?* Три дня.\n*Может ли родитель присутствовать на уроке?* Может, по заявлению и согласованию с директором.', parse_mode = "Markdown")

	if message.text == 'Вопрос директору':
		msg = client.send_message(message.chat.id, 'Хорошо! Сначала рекомендуем ознакомиться с разделом: Частые вопросы. Если вашего вопроса там нет, то для начала напишите своё имя и фамилию (- для отмены действия):')
		client.register_next_step_handler(msg, textmail)
	if message.text == 'Подписаться':
		subs_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		item_news = types.KeyboardButton(text = "Новости школы")
		item_uproute = types.KeyboardButton(text = "Изменения в расписании")
		subs_reply.add(item_uproute, item_news)
		client.send_message(message.chat.id, 'Выберите, на что хотите подписаться (если вы уже были подписаны на этот раздел, то пройдет отписка):', reply_markup = types.ReplyKeyboardRemove())
		client.send_message(message.chat.id, 'Меню выбора:', reply_markup = subs_reply)
	if message.text == "Новости школы":
		db = sqlite3.connect('userbase.db', check_same_thread = False)
		sql = db.cursor()
		for r in sql.execute(f'SELECT subnews FROM users WHERE user_id = {message.chat.id}'):
			stat = r[0]
			if stat == 0:
				client.send_message(message.chat.id, "Вы успешно подписались на раздел!")
				main_menu(message)
				sql.execute(f'UPDATE users SET subnews = {stat + 1} WHERE user_id = {message.chat.id}')
				db.commit()
			if stat == 1:
				client.send_message(message.chat.id, "Вы успешно отписались от раздела!")
				main_menu(message)
				sql.execute(f'UPDATE users SET subnews = {stat - 1} WHERE user_id = {message.chat.id}')
				db.commit()
	if message.text == "Изменения в расписании":
		db = sqlite3.connect('userbase.db', check_same_thread = False)
		sql = db.cursor()
		for r in sql.execute(f'SELECT subup FROM users WHERE user_id = {message.chat.id}'):
			stat = r[0]
			if stat == 0:
				client.send_message(message.chat.id, "Вы успешно подписались на раздел!")
				main_menu(message)
				sql.execute(f'UPDATE users SET subup = {stat + 1} WHERE user_id = {message.chat.id}')
				db.commit()
			if stat == 1:
				client.send_message(message.chat.id, "Вы успешно отписались от раздела!")
				main_menu(message)
				sql.execute(f'UPDATE users SET subup = {stat - 1} WHERE user_id = {message.chat.id}')
				db.commit()
	if message.text == "Начать рассылку":
		ads_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		ad_news = types.KeyboardButton(text = "Новости")
		ad_route = types.KeyboardButton(text = "Изменения расписания")
		ads_reply.add(ad_news, ad_route)
		client.send_message(message.chat.id, 'Выберите тип рассылки (отменить для отмены действия):', reply_markup = ads_reply)
	if message.text == "отменить":
		if not message.from_user.username in admins:
			client.send_message(message.chat.id, 'Вы не являетесь администратором!')
		else:
			admin_panel(message)
	if message.text == 'Новости':
		msg = client.send_message(message.chat.id, 'Хорошо! Теперь напишите текст для рассылки:')
		client.register_next_step_handler(msg, rass_news)
	if message.text == 'Изменения расписания':
		msg = client.send_message(message.chat.id, 'Хорошо! Теперь напишите текст для рассылки')
		client.register_next_step_handler(msg, rass_route)
	if message.text == "Выйти из панели":
		main_menu(message)
	if message.text == "Сообщить об ошибке":
		msg = client.send_message(message.chat.id, "Если вы столкнулись с проблемами в работе сервиса, подробно опишите их и ошибки будут устранены:")
		client.register_next_step_handler(msg, report)





if __name__ == '__main__': # чтобы код выполнялся только при запуске в виде сценария, а не при импорте модуля
    try:
    	print('start')
    	client.polling(none_stop=True)
    except Exception as e:
       print(e) # или import traceback; traceback.print_exc() для печати полной инфы
       time.sleep(15)