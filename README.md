# Детектор стандарта ERC20

## Запуск проекта
***
1. Склонируйте удаленный репозиторий
```bash
$ git clone https://github.com/YourBobi/detector_erc20.git
```
2. Создайте два .env файла и заполните их:
- первый в корневой директории для docker
```
DB_PORT="5432"
DB_NAME="detector_db"
DB_USER="postgres"
DB_PASSWORD="postgres"
DB_HOST="localhost"
```
- второй в директории /detector для настройки проекта
```
DB_NAME="detector_db"
DB_USER="postgres"
DB_PASSWORD="postgres"
DB_HOST="localhost"
DB_PORT="5432"

REDIS_URL="redis://redis:6379/0"
```

3. Убедитесь что на устройстве установлен докер, после чего соберите образ
```bash
$ docker-compose build
$ docker-compose up
```
4. Создайте таблицы в базе данных и заполните данными следующими командами:
```bash
$ docker-compose run --rm web-app sh -c "python manage.py migrate"
$ docker-compose run --rm web-app sh -c "python manage.py fill_contracts"
```

## Описание проекта (простым языком)
***
Для создания детектора был написан базовый класс ContractComparer, в котором описаны методы:
- __use_correct_solidity_version - устанавливает корректную для контракта версию solidity для последующего парсинга кода
- __get_slither - создает файл для исходно кода контракта и через класс Slither разбивает код solidity на сигнатуры 
- __set_functions - записывает и оставляет функции которые определяют стандарт контракта
- compare_signature - сравнивает сигнатуру контракта и возвращает True если контракт подходит под описание.

Запуск детектора происходит периодической задачей через celery, которая описана в файле erc20.tasks.check_and_update_erc20_contracts. 
Лучший результат которого удалось достигнуть в рамках одного контейнера 2000000 контрактов в неделю.

***
Основные файлы, где происходит весь сахар:
- erc20/models - описание моделей в бд
- erc20/comparer - проверка стандарта erc20
- erc20/tasks - описание периодической задачи на проверку erc20
- core/tocken_standarts/base_comparer - базовый класс для сравнения 
- core/tocken_standarts/signatures - описание сигнатур функций контракта