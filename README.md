# Qmobi_test_task
test task for the interview


==========Инструкция по запуску.==========

Для запуска приложения необходимо запустить скрипт run_app.sh:
$./run_app.sh  # Пример запуска приложения из корневой папки проекта.

Для запуска тестов необходимо ввести следующую команду:
$python3 ./tests/TestDoGetAndPostMethods.py

==========Описание проекта.==========
В файле app.py реализован класс CurrencyConverterHTTPServer, являющийся наследником класса
BaseHTTPRequestHandler.
В классе CurrencyConverterHTTPServer содержатся следующие методы:
- set_response - осуществляет установку соединения;
- get_currency_rate - осуществляет поиск на сайте http://www.cbr.ru/currency_base/daily/ 
  курса валюты, заданной в запросе;
- get_query_params - осуществляет извлечение данных (наименование валюты и количество валюты 
  для перевода) из запросов GET и POST;
- get_response - осуществляет формирование ответа для пользователя;
- do_GET - реализация запроса GET;
- do_POST - реализация запроса POST.
 
