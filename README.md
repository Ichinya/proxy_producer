# Proxy Producer
[![Docker](https://github.com/Ichinya/proxy_producer/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/Ichinya/proxy_producer/actions/workflows/docker-publish.yml)

Импортирует списки прокси и отправляет на проверку в MQ

## Настройки
Для работы нужно использовать переменные окружения. Использовать можно переименованием файла `.env.example` в `.env` или передать переменные окружения при создании докера

## Точки входа
Берет из базы прокси и отправляет в MQ на проверку
```shell
python send_to_mq.py
```

Запуск слушателя очереди проверенных прокси для записи в базу
```shell
python main.py
```

Парсинг источников с прокси. Собирает примерно 20к-25к прокси за 2 минуты с более 50 сайтов.
```shell
python update_list_proxy
```

## Требования
Работает с PostgreSQL, RabbitMQ и [Proxy Checker](https://github.com/Ichinya/proxy_cheker)

## Принцип работы
Создает таблицы в PostgreSQL, где хранятся списки прокси и результат их проверок.

Для запуска крона нужно запустить `cron.sh`. Если используете Docker-Compose, то смотрите запуск в репозитории [proxy-checker-docker](https://github.com/Ichinya/proxy-checker-docker)