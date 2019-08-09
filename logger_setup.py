#!/usb/bin/python
## -*- coding: utf-8 -*-
import os, sys
import logging, logging.config, logging.handlers
from config import Config
import __main__

conf = Config()

def setup_custom_logger(name):

	if not os.path.exists(conf.log_path) or not os.path.isdir(conf.log_path):
		print ('не существует каталог для лог файлов. Проверьте файл конфигурации')
		sys.exit(1)
	if not os.access(conf.log_path, os.W_OK):
		print ('каталог для лог файл недоступен для записи. Проверьте права пользователя ')
		print ('от имени которого запускается скрипт на возможность записи в указанный каталог ')
		sys.exit(1)


	"""
	Based on http://docs.python.org/howto/logging.html#configuring-logging
	"""
	filename = os.path.join(conf.log_path, os.path.splitext(__main__.__file__)[0] + '.log')

	if conf.log_level.upper() == 'DEBUG':
		formater = "%(asctime)s - %(levelname)-8s - [%(filename)s:%(lineno)s - %(funcName)20s() ] - %(message)s"
	else:
		formater = "%(asctime)s - %(levelname)-8s - %(message)s"

	dictLogConfig = {
		"version":1,
		"handlers":{
			"console":{
				"class":"logging.StreamHandler",
				"level":"DEBUG",
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
			name:{
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
	logger = logging.getLogger(name)
	return logger
	
