#!/usb/bin/python
## -*- coding: utf-8 -*-
import os, sys
#import logging, logging.config, logging.handlers
#import configparser
import subprocess
from subprocess import check_output
from  ldap3 import Server, Connection, NTLM, SUBTREE
from ldap3.core.exceptions import LDAPException, LDAPBindError, LDAPSocketOpenError

import zmprov
from config import Config

import logger_setup



'''
 процедура возвращающая словарь со списком листов рассылки и адресов чденов группы
 словарь имеет вид:
	ключь - адрес списка рассылки: [ список адресов почты членов шруппы ] 
'''
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




if __name__ == '__main__':
	# создаем логи
	logger = logger_setup.setup_custom_logger(__name__)
	# загружаем переменные из файла конфигурации
	conf = Config()
	
	ad_group_dict = get_ad_grouplist()
	# список групп рассылки из AD
	ad_address_list = [k for k in ad_group_dict.keys()]
	
	zm_exec= zmprov.ZimbraClient(conf.zmprov)
	
	
	# вызываем внешнюю комманду для получения списков рассылки zimbra
	#out = check_output([conf.zmprov, 'gadl'])
	
	# список групп рассылки из zimbra
	zimbra_address_list = zm_exec.getAlldistributionLists()
	
	
	print (zimbra_address_list)
	# списки которые в ad более не присутствуют. Удалить из zimbra
	addres_list_for_del = list(set(zimbra_address_list) - set(ad_address_list))
	# список который в zimbra не существует. Требуется добавить. 
	addres_list_for_add = list(set(ad_address_list) - set(zimbra_address_list))
	
	print (addres_list_for_del)
	print (addres_list_for_add)
	logger.info('Очитска zimbra от удаленных каталогов')
	for address_for_del in addres_list_for_del:
		logger.info('Удаляется список рассылки: %s ', address_for_del)
		if zm_exec.deleteDistributionList(address_for_del):
			logger.info('Выполненно успешно')
		
	for ad_addres_item in ad_address_list:
		if not ad_addres_item in zimbra_address_list:
			logger.info('Список рассылки %s не найден', ad_addres_item)
			logger.info('выполняем добавление')
			
			
			#out = check_output([conf.zmprov, 'cdl', ad_addres_item])
			#print(str(out, 'utf-8').splitlines())
		
	
	
	print (ad_group_dict)
	
	
	

	
	
	
