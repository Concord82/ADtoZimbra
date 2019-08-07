# ADtoZimbra
## Подготовка системы
Я устанавливал zimbra на дистрибутив Linux Centos. Посмотреть версию можно командой:

`rpm -q centos-release`

В centos установлен python 2ой версии. Для работы скрипта требуется Python версии 3. 
Для того что бы не засорять систему пакетами будем использовать virtualenv. Для начала
требуется включить репозитории epel-release. Выполняем комманду:

`yum install epel-release`

Устанавливаем git, Python 3ей версии и необходимые компоненты

`yum install -y git python36 python36-devel python36-setuptools`

Устанавливаем pip

`easy_install-3.6 pip3`

Через pip ставим virtualenv для управления виртуальными окружениями. 

`pip3 install --upgrade virtualenv`

## Создание виртуального окружения и загрузка репозитория со скриптом.

