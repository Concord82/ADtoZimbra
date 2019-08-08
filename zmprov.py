#!/usb/bin/python
## -*- coding: utf-8 -*-

import os, sys
import subprocess
from subprocess import check_output
import logging

class ZimbraClient():
	zmprov = ''
	# Инициализация класса. 
	# При создании указывается путь до утилиты zmprov
	def __init__(self, zmprov_path):
		self.logger = logging.getLogger(__name__)
		
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
		AlldistributionLists = self.getAlldistributionLists()
		if DistributionList in AlldistributionLists:
			out = check_output([self.zmprov, 'gdlm', DistributionList])
			out = str(out, 'utf-8').splitlines()
			out = out[out.index('members')+1:]
			return out
		else:
			self.logger.warning('Список %s не найден на сервере zimbra', DistributionList)
			return False
		
		
		
		
		
	
if __name__ == '__main__':
	zmprov = ZimbraClient('/opt/zimbra/bin/zmprov')
	
	
	
	out = zmprov.getDistributionListmembership('cons-talks2@zimbra-mailserver.internal.cons.tsk.ru')
	if not out == False:
		print (out)
	
	
