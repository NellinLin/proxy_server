# proxy_server
Задание: https://park.mail.ru/blog/topic/view/15225/

## Установка и запуск
```
git clone https://github.com/NellinLin/proxy_server.git

cd proxy_server

docker build -t proxyserv . && docker run -p 6080:6080 proxyserv
```
Необходимо прописать порт прокси сервера в настройках браузера.

Например:
![Иллюстрация к проекту](https://github.com/NellinLin/proxy_server/blob/master/images/settings.jpg)

## Автор
[Шишова Анастасия](https://github.com/NellinLin)
