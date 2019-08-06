#!/usb/bin/python
## -*- coding: utf-8 -*-

import os, sys
import logging, logging.config
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
	log_path = ''
	log_level = ''
	
	def __init__(self):
		config_file = self.file_path('conf')
		config = configparser.ConfigParser()
		if not os.path.exists(config_file):
			if not os.path.exists(os.path.splitext(config_file)[0]+'.tmp'):
				self.createConfig(config_file)
				print 'Ошибка! Не найден файл конфигурации.'
				print 'в рабочем каталоге создан шаблон файла конфигурации'
				print 'внесите в него параметры для вашей системы и замените его расширение на расширение conf'
			sys.exit(1)
			
		config = configparser.ConfigParser()
		config.read(config_file)
		
		self.ad_server = config.get("AD", "server")
		self.ad_port = config.getint("AD", "port")
		self.tls = config.getboolean ("AD", "use_tls")	
		self.ad_user = config.get('AD', 'user')
		self.ad_password = config.get('AD', 'password')
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
		config.add_section("MAIN")
		config.set("MAIN", "logdir", "/home/lviv/project")
		config.set("MAIN", "loglevel", "loglevel")
		
		with open(os.path.splitext(path)[0] + '.tmp', "w") as config_file:
			config.write(config_file)

def main():
    """
    Based on http://docs.python.org/howto/logging.html#configuring-logging
    """
    
    dictLogConfig = {
        "version":1,
        "handlers":{
            "fileHandler":{
                "class":"logging.FileHandler",
                "formatter":"myFormatter",
                "filename":"config2.log"
            }
        },
        "loggers":{
            "exampleApp":{
                "handlers":["fileHandler"],
                "level":conf.log_level.upper(),
            }
        },
        "formatters":{
            "myFormatter":{
                "format":"%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
        }
    }
    
    logging.config.dictConfig(dictLogConfig)
    logger = logging.getLogger("exampleApp")
    return logger
    
def test_log():
    logger.info("Program started")
    logger.info("Done!")


if __name__ == '__main__':
	conf = Config()
	logger = main()
	print conf.ad_user
	logger.info('asdasdasdasdad')
	test_log()
	
	
