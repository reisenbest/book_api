# book_api
REST API сервис для каталога книг. Тестовое задание
стек - джанго, докер, постгрес,
Инструкции к деплою:

1. скачать\склонировать репозиторий
2. запустить команду docker-compose up --build из директории где хранится Dockerfile
    установятся зависимости
    автоматически пройдут миграции
    создастся суперюзер
    запустится сервер
   
4. перейти на /api/swagger/ и авторизоваться (django-login) (пользователь уже создан при сборке)

логи для входа:
username = 'admin' email = 'admin@admin.com' password = 'admin'

или авторизоваться через админ панель

4. В сваггре представлены все эндпоинты - для парсинга json файла с книгами из задания:

А. - обратиться по эндпоинту в swagger-ui и передать полный url к файлу json (https://gitlab.grokhotov.ru/hr/python-test-vacancy/-/raw/master/books.json) 

Б. - В адресной строке передать /api/parsebooks/?url=https://gitlab.grokhotov.ru/hr/python-test-vacancy/-/raw/master/books.json/

Если докер запущен без флага -d - логи будут выводиться прямо в терминале, иначе нужно смотреть в самом докере, парсятся довольно долго данные
пару минут точно. По заданию не понял нужно уже с готовыми дать или нет.

Правила валидации для книги (что я принял за валидную книгу):

    "title": - должен быть, но может повторяться
    "isbn":  - должен быть - длина либо 10 либо 13 знаков - уникальный
    "pageCount" - может быть = 0 только если статус "MEAP", иначе больше 0 обязательно
    "publishedDate": - может отсуствовать только если статус "MEAP"
    "thumbnailUrl": может отсутсвовать - если отсутствует\недоступно - заполянется поле стоковой кратинкой 
    "shortDescription": может отсусттвовать
    "longDescription": может отсутствовать
    "authors": должен быть хотя бы один
    "categories": на 1 месте главная категория, далее категории на уровень ниже


 
