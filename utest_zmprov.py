#!/usb/bin/python
## -*- coding: utf-8 -*-
import unittest
from zmprov import ZimbraClient


class ZimbraClientTest(unittest.TestCase):
	
	@classmethod
	def setUpClass(cls):
		"""Set up for class"""
		print("setUpClass")
		print("==========")
		
	@classmethod
	def tearDownClass(cls):
		"""Tear down for class"""
		print("==========")
		print("tearDownClass")
		
	def setUp(self):
		"""Set up for test"""
		self.zm_exec= ZimbraClient('/opt/zimbra/bin/zmprov')
		print("\nSet up for [%s]"% self.shortDescription())
		
	def tearDown(self):
		"""Tear down for test"""
		print("Tear down for [%s]"% self.shortDescription())
		print("")
		
	def test_01_getalldomain(self):
		''' Список доменов обслуживаемых Zimbra'''
		print("id: " + self.id())
		getalldomain = self.zm_exec.getalldomain()
		self.assertEqual(
			getalldomain, 
			['zimbra-mailserver.internal.cons.tsk.ru', 'test.cons.tsk.ru']
		)
		
	def test_02_getAlldistributionLists(self):
		''' Список листов рассылки на сервере'''
		print("id: " + self.id())
		AllDistribList = self.zm_exec.getAlldistributionLists()
		print (AllDistribList)
		self.assertIn(
			'cons-talks@zimbra-mailserver.internal.cons.tsk.ru', 
			AllDistribList
		)
		
	def test_03_createDistributionList(self):
		''' Создаем список рассылки'''
		print("id: " + self.id())
		self.assertNotEqual(
			self.zm_exec.createDistributionList('test2@test.cons.tsk.ru'), 
			False
		)
		
	def test_04_createDistributionList(self):
		''' Создаем список рассылки повторно для проверки обработчика ошибок'''
		print("id: " + self.id())
		self.assertFalse(
			self.zm_exec.createDistributionList('test2@test.cons.tsk.ru')
		)
		
	def test_05_addDistributionListMember(self):
		'''добавляем 10 членов в список рассылки '''
		print("id: " + self.id())
		user_list = []
		for i in range(10):
			user_list.append('user'+str(i)+'@test.cons.tsk.ru')
		self.assertTrue( 
			self.zm_exec.addDistributionListMember(
				'cons-talks@zimbra-mailserver.internal.cons.tsk.ru', 
				user_list
			)
		)
			
	def test_06_getDistributionListmembership(self):
		'''получаем членов списка рассылки '''
		print("id: " + self.id())
		DistributionListmembership = self.zm_exec.getDistributionListmembership(
			'cons-talks@zimbra-mailserver.internal.cons.tsk.ru'
		)
		flagg = True
		for i in range(10):
			if not 'user'+str(i)+'@test.cons.tsk.ru' in DistributionListmembership:
				flagg = False
				break
		self.assertTrue(flagg)
		
	def test_07_getDistributionListmembership(self):
		'''получаем членов несуществующего списка рассылки '''
		print("id: " + self.id())
		self.assertFalse( 
			self.zm_exec.getDistributionListmembership(
				'cons-talks434@zimbra-mailserver.internal.cons.tsk.ru'
			)
		)
		
	def test_08_removeDistributionListMember(self):
		'''удаляем 10 членов из списка рассылки '''
		print("id: " + self.id())
		user_list = []
		for i in range(10):
			user_list.append('user'+str(i)+'@test.cons.tsk.ru')
		self.assertTrue( 
			self.zm_exec.removeDistributionListMember(
				'cons-talks@zimbra-mailserver.internal.cons.tsk.ru', 
				user_list
			)
		)
		
	def test_09_addDistributionListMember(self):
		'''добавляем 100 членов в список рассылки '''
		print("id: " + self.id())
		user_list = []
		for i in range(100):
			user_list.append('user'+str(i)+'@test.cons.tsk.ru')
		self.assertTrue( 
			self.zm_exec.addDistributionListMember(
				'cons-talks@zimbra-mailserver.internal.cons.tsk.ru', 
				user_list
			)
		)
		
	def test_10_removeDistributionListMember(self):
		'''удаляем 100 членов из списка рассылки '''
		print("id: " + self.id())
		user_list = []
		for i in range(10):
			user_list.append('user'+str(i)+'@test.cons.tsk.ru')
		self.assertTrue( 
			self.zm_exec.removeDistributionListMember(
				'cons-talks@zimbra-mailserver.internal.cons.tsk.ru', 
				user_list
			)
		)
		
	def test_11_addDistributionListMember(self):
		'''добавляем члена в несуществующий список рассылки '''
		print("id: " + self.id())
		self.assertFalse( 
			self.zm_exec.addDistributionListMember(
				'cons-talks23@zimbra-mailserver.internal.cons.tsk.ru', 
				['test_user@ya.ru']
			) 
		)
			
	def test_12_removeDistributionListMember(self):
		'''удаляем члена из несуществующего списка рассылки '''
		print("id: " + self.id())
		self.assertFalse( 
			self.zm_exec.removeDistributionListMember(
				'cons-talks223@zimbra-mailserver.internal.cons.tsk.ru', 
				['user@mail.ru']
			) 
		)
		
	def test_13_deleteDistributionList(self):
		''' Удаляем список рассылки'''
		print("id: " + self.id())
		self.assertTrue(
			self.zm_exec.deleteDistributionList(
				'test2@test.cons.tsk.ru'
			)
		)
		
	def test_14_deleteDistributionList(self):
		''' Удаляем список рассылки повторно'''
		print("id: " + self.id())
		self.assertFalse(
			self.zm_exec.deleteDistributionList(
				'test2@test.cons.tsk.ru'
			)
		)
		
if __name__ == '__main__':
   unittest.main()
