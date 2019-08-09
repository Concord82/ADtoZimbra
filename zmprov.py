#!/usb/bin/python
## -*- coding: utf-8 -*-

import os, sys
import subprocess
from subprocess import check_output
import logging
import __main__

class ZimbraClient():
	zmprov = ''
	# Инициализация класса. 
	# При создании указывается путь до утилиты zmprov
	def __init__(self, zmprov_path):
		
		self.logger = logging.getLogger(__main__.__name__)
		
		if os.path.exists(zmprov_path) and os.path.isfile(zmprov_path):
			self.zmprov = zmprov_path
		else:
			self.logger.error ('Указанный путь %s до утилиты zmprov неверен')
			self.logger.error ('проверьте правильность расположения утилиты для дальнейшей работы')
			sys.exit(1)
	
	def zmprov_exec(self, *kwargs):
		out = check_output([self.zmprov, *kwargs])
		return str(out, 'utf-8').splitlines()
	
	
	
	# Получить список доменов обслуживаемых zimbra
	def getalldomain(self):
		out = check_output([self.zmprov, 'gad'])
		return str(out, 'utf-8').splitlines()
	
	#############################################
	# работа со списками рассылки
	#############################################
	# получить адреса списков рассылки
	def getAlldistributionLists(self):
		self.logger.info('Выполняем получение адресов списков рассылки')
		out = check_output([self.zmprov, 'gadl'])
		return str(out, 'utf-8').splitlines()
	
	# создать список рассылки
	def createDistributionList(self, address):
		domain = address.split('@')[1]
		# получаем список доменов zimbra
		domainlist = self.getalldomain()
		# если домен рассылки входит в число доменов обслуживаемых zimbra
		# выполняем добавление списка 
		if domain in domainlist:
			try:
				out = check_output([self.zmprov, 'cdl', address])
				return str(out, 'utf-8').splitlines()
			except subprocess.CalledProcessError as e:
				self.logger.warning('при вызове zmprov произошла ошибка')
				self.logger.warning(e)
		else:
			self.logger.warning('Домен %s не обслуживается данным сервером', domain)
		return False
			
	# список членов заданного спска рассылки
	def getDistributionListmembership (self, DistributionList):
		# получаем список адресо рассылок
		AlldistributionLists = self.getAlldistributionLists()
		# проверяем наличие заданного адреса в списке
		if DistributionList in AlldistributionLists:
			# выполняем запрос в zimbra
			out = check_output([self.zmprov, 'gdlm', DistributionList])
			# из полученного вывода комманды извлекаем только адреса
			# членов данной рассылки
			out = str(out, 'utf-8').splitlines()
			out = out[out.index('members')+1:]
			return out
		# если адрес не присутствует в списке рассылки, выводим ошибку
		else:
			self.logger.warning('Список %s не найден на сервере zimbra', DistributionList)
			return False
	
	# добавление членов в группу подписки
	def addDistributionListMember (self,  DistributionList, members):
		append_member = []
		# в однорй комманде можно добавлять не более 100 адресов.
		# для верности разбиваем список заданных адресов на части по 50
		for i in range(0, len(members), 50):
			append_member = members[i:i+50]
			try:
				out = check_output([self.zmprov, 'adlm', DistributionList] + append_member)
			except subprocess.CalledProcessError as e:
				self.logger.exception('при вызове zmprov произошла ошибка')
				self.logger.warning(e)
				return False
		return True
		
	# удаление членов из группы подписки
	def removeDistributionListMember (self,  DistributionList, members):
		append_member = []
		# в одной комманде можно удалить не более 100 адресов.
		# для верности разбиваем список заданных адресов на части по 50
		for i in range(0, len(members), 50):
			append_member = members[i:i+50]
			try:
				out = check_output([self.zmprov, 'rdlm', DistributionList] + append_member)
			except subprocess.CalledProcessError as e:
				self.logger.exception('при вызове zmprov произошла ошибка')
				self.logger.warning(e)
				return False
		return True
		
			
	def deleteDistributionList(self, DistributionList):
		try:
			out = check_output([self.zmprov, 'ddl', DistributionList])
			return True
		except subprocess.CalledProcessError as e:
			self.logger.exception('при вызове zmprov произошла ошибка')
			self.logger.warning(e)
			return False
		
	
if __name__ == '__main__':
	zmprov = ZimbraClient('/opt/zimbra/bin/zmprov')
	
	out = zmprov.getalldomain()
	print (out)
	
	out = zmprov.getAlldistributionLists()
	print (out)
	print ('\n\n\n')
	#zmprov.deleteDistributionList('test@cons.ru')
	
	
	#zmprov.addDistributionListMember('cons-talks@zimbra-mailserver.internal.cons.tsk.ru', ['taa@cons.tsk.ru'])
	

	out = zmprov.getDistributionListmembership('cons-talks@zimbra-mailserver.internal.cons.tsk.ru')
	if not out == False:
		print (out)
		
		
	
	
