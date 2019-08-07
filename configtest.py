#!/usb/bin/python
## -*- coding: utf-8 -*-
import os, sys
import logging, logging.config, logging.handlers
#import configparser
import subprocess
from subprocess import check_output
from  ldap3 import Server, Connection, NTLM, SUBTREE
from ldap3.core.exceptions import LDAPException, LDAPBindError, LDAPSocketOpenError

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

class Config:
	ad_server = ''
	ad_port = ''
	ad_tls = False
	ad_user = ''
	ad_password = ''
	ad_search_base = ''
	zmprov = ''
	log_path = ''
	log_level = ''
	
	def __init__(self):
		config_file = self.file_path('conf')
		print (config_file)
		config = configparser.ConfigParser()
		if not os.path.exists(config_file):
			if not os.path.exists(os.path.splitext(config_file)[0]+'.tmp'):
				self.createConfig(config_file)
				print ('Ошибка! Не найден файл конфигурации.')
				print ('в рабочем каталоге создан шаблон файла конфигурации')
				print ('внесите в него параметры для вашей системы и замените его расширение на расширение conf')
			sys.exit(1)
			
		config = configparser.ConfigParser()
		config.read(config_file)
		
		self.ad_server = config.get("AD", "server")
		self.ad_port = config.getint("AD", "port")
		self.tls = config.getboolean ("AD", "use_tls")	
		self.ad_user = config.get('AD', 'user')
		self.ad_password = config.get('AD', 'password')
		self.ad_search_base = config.get('AD', 'search_base')
		
		self.zmprov = config.get("MAIN", "zmprov")
		self.log_path = config.get('MAIN', 'logdir')
		self.log_level = config.get('MAIN', 'loglevel')
		
	def file_path(self, extension):
		script_dir = os.path.abspath(os.path.dirname('__file__'))
		config_file = os.path.splitext(__file__)[0] + '.' + extension
		return os.path.join(script_dir, config_file)
		
	
		
	def createConfig(self, path):
		"""
		Create a config file
		"""
		config = configparser.ConfigParser()
		
		config.add_section("AD")
		config.set("AD", "server", "user_name_in_AD")
		config.set("AD", "port", "389")
		config.set ("AD", "use_tls", "yes")
		config.set("AD", "user", "user_name_in_AD")
		config.set("AD", "password", "password")
		config.set("AD", "search_base", "OU=internet,OU=Resources_and_Services,DC=cons,DC=tsk,DC=ru")
		
		config.add_section("MAIN")
		config.set("MAIN", "zmprov", "/opt/zimbra/bin/zmprov")
		config.set("MAIN", "logdir", "/home/lviv/project")
		config.set("MAIN", "loglevel", "loglevel")
		
		
		with open(os.path.splitext(path)[0] + '.tmp', "w") as config_file:
			config.write(config_file)


# процедура возвращающая словарь со списком листов рассылки и адресов чденов группы
# словарь имеет вид:
#	ключь - адрес списка рассылки: [ список адресов почты членов шруппы ] 
def get_ad_grouplist():
	server = Server(conf.ad_server, conf.ad_port, conf.ad_tls)
	try:
		connection = Connection(server, user=conf.ad_user, password=conf.ad_password, authentication=NTLM, auto_bind=True)
	except LDAPSocketOpenError as err:
		logger.critical('Ошибка соединения с сервером. Проверьте адрес сервера в файле конфигурации.')
		logger.critical(err)
		sys.exit(1)
	except LDAPBindError as err:
		logger.critical('Ошибка соединения с сервером. Неверный логин или пароль.')
		logger.critical(err)
		sys.exit(1)
	
	connection.search(search_base=conf.ad_search_base, 
	search_filter='(objectClass=group)', search_scope=SUBTREE, attributes = ['cn', 'distinguishedName', 'mail','member'])
	# создаем словарь для наполнения его элементами
	ad_group_dict = {}
	# перебираем полученные группы из заданного OU
	for entries in connection.entries:
		# список адресов электронной почты членов группы
		# создаем или обнуляем при следующей итерации цикла
		member_email = []
		# перебираем членов группы в цикле
		for member in entries.member.values:
			# ищем адрес почты члена группы
			connection.search(
				search_base='OU=CONSULTANT,dc=cons,dc=tsk,dc=ru',
				search_filter=f'(distinguishedName={member})',
				attributes = ['mail']
			)
			# вносим полученный адрес в созданный временный список
			member_email.append(connection.entries[0].mail.values)
		# после перебора добавляем к словарю значение
		# ключь адрес почты группы
		# значение временный список
		ad_group_dict[entries.mail.value] = member_email

	return ad_group_dict


def create_logger():
	"""
	Based on http://docs.python.org/howto/logging.html#configuring-logging
	"""
	filename = os.path.join(conf.log_path, os.path.splitext(__file__)[0] + '.log')
	
	if conf.log_level.upper() == 'DEBUG':
		formater = "%(asctime)s - %(levelname)-8s - [%(filename)s:%(lineno)s - %(funcName)20s() ] - %(message)s"
	else:
		formater = "%(asctime)s - %(levelname)-8s - %(message)s"
	
	dictLogConfig = {
		"version":1,
		"handlers":{
			"console":{
				"class":"logging.StreamHandler",
				"level":"INFO",
				"formatter":"myFormatter",			
			},
			"file":{
				"class":"logging.handlers.RotatingFileHandler",
				"formatter":"myFormatter",
				"filename":filename,    
				"maxBytes":64*1024,
				"backupCount":10,
			}
		},
		"loggers":{
			"exampleApp":{
				"handlers":['console', 'file'],
				"level":conf.log_level.upper(),
			}
		},
		"formatters":{
			"myFormatter":{
				"format":formater,
				"datefmt":"%d-%b-%Y %H:%M:%S",
			}
		}
	}
    
	logging.config.dictConfig(dictLogConfig)
	logger = logging.getLogger("exampleApp")
	return logger


if __name__ == '__main__':
	conf = Config()
	
	
	if not os.path.exists(conf.log_path) or not os.path.isdir(conf.log_path):
		print ('не существует каталог для лог файлов. Проверьте файл конфигурации')
		sys.exit(1)
	if not os.access(conf.log_path, os.W_OK):
		print ('каталог для лог файл недоступен для записи. Проверьте права пользователя ')
		print ('от имени которого запускается скрипт на возможность записи в указанный каталог ')
		sys.exit(1)
	
	logger = create_logger()

	ad_group_dict = get_ad_grouplist()
	# список групп рассылки из AD
	ad_address_list = [k for k in ad_group_dict.keys()]
	
	
	# вызываем внешнюю комманду для получения списков рассылки zimbra
	out = check_output([conf.zmprov, 'gadl'])
	
	# список групп рассылки из zimbra
	zimbra_address_list = str(out, 'utf-8').splitlines()
	
	
	
	# списки которые в ad более не присутствуют. Удалить из zimbra
	addres_list_for_del = list(set(zimbra_address_list) - set(ad_address_list))
	# список который в zimbra не существует. Требуется добавить. 
	addres_list_for_add = list(set(ad_address_list) - set(zimbra_address_list))
	
	print (addres_list_for_del)
	print (addres_list_for_add)
	logger.info('Очитска zimbra от удаленных каталогов')
	for address_for_del in addres_list_for_del:
		logger.info('Удаляется список рассылки: %s ', address_for_del)
		proc = subprocess.Popen([conf.zmprov, 'ddl', address_for_del], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		stdout = proc.communicate()[0]
		if stdout == b'':
			logger.info('Выполненно успешно')
		
	for ad_addres_item in ad_address_list:
		if not ad_addres_item in zimbra_address_list:
			logger.info('Список рассылки %s не найден', ad_addres_item)
			logger.info('выполняем добавление')
			out = check_output([conf.zmprov, ])
	
	
	print (ad_group_dict)
	
	
	

	
	
	
