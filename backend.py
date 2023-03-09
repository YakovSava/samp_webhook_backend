import asyncio  # Импортируем асинхронность

from sys import platform  # Импортируем опредление платформы
from json import loads  # Импортируем модуль для работы с JSON
from typing import Coroutine  # ДЛЯ АННОТАЦИИ
# Импортируем кучу всего из aiohttp.web
from aiohttp.web import Application, RouteTableDef, Response, Request, run_app

subapp = Application()  # Инциализируем суб-приложение
routes = RouteTableDef()  # Инициализируем роуты
bot = ... # Заглушка что бы IDLE не ругалась

if platform == 'win32':  # Если на виндовс...
    try:
        # Устанавливаем селекторную политику на виндовс
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except:
        pass  # Игнорируем ошибки


async def add_func(nickname: str) -> None:
    # В этой функции мы на основе никнейма ищем telegram id игрока и пишем ему что он вошёл на сервер
    json_data = { # Пример - заглушка
        'id': { # Тут должно быть id
            'nickname': 'MyNick', # Тут указан ник
            'password': 'qwerty12345' # тут указаны другие данные
        }
    }
    for telegram_id, telegram_data in list(json_data.items()): # Перебираем циклом распаковывая
        if telegram_data['nickname'] == nickname: # Если ник есть
            await bot.send_message( # Отправляем сообщение
                chat_id=telegram_id, # Указываем telegram_id
                message='Вы вошли на сервер!' # Отправляем сообщение
            )


async def remove_func(nickname: str) -> None:
    # В этой функции мы на основе никнейма ищем telegram id игрока и пишем ему что он вышел с сервера
    json_data = { # Пример - заглушка
        'id': { # Тут должно быть id
            'nickname': 'MyNick', # Тут указан ник
            'password': 'qwerty12345' # тут указаны другие данные
        }
    }
    for telegram_id, telegram_data in list(json_data.items()): # Перебираем циклом распаковывая
        if telegram_data['nickname'] == nickname: # Если ник есть
            await bot.send_message( # Отправляем сообщение
                chat_id=telegram_id, # Указываем telegram_id
                message='Вы вышли сервера!' # Отправляем сообщение
            )


class Back:  # Объявляем класс

    def __init__(self, # Функция инициализации
                add_function: Coroutine=add_func, # Указываем функцию входа на сервер
                remove_function: Coroutine=remove_func, # Указываем функцию выхода с сервера
                host: str='127.0.0.1', # Указываем хост
                port: int=80, # Указываем порт на который происходит запрос. Стандартный http порт - 80
                subapp_host: str='service', # Указываем хост суб-приложения. Вид ссылки должен быть такой: service.127.0.0.1:80 (:80 можно не указывать если порт 80 будет)
                app: Application=Application(), # Инициализация приложения
                loop: asyncio.AbstractEventLoop=asyncio.get_event_loop() # Указываем event loop
                ):
        self.add_function = add_function # Вписываем в переменную класса
        self.remove_function = remove_function # Вписываем в переменную класса
        self.app = app # Вписываем в переменную класса
        self.host = host # Вписываем в переменную класса
        self.port = port # Вписываем в переменную класса
        self.subapp_host = subapp_host # Вписываем в переменную класса
        self.loop = loop # Вписываем в переменную класса

    @routes.get('/server/add?{data}') # Указываем путь к входу
    async def server_get_add(self, request: Request):
        try:
            data = loads(str(request.url()).split('?')[1]) # Подгружаем данные
        except:
            return Response(status=503) # При ошибке отправляем ошибку

        self.add_function(data) # Активируем функцию

        return Response(body=1) # Без ошибки отправляем еденицу

    @routes.get('/server/remove?{data}') # Указываем путь к выходу
    async def server_get_remove(self, request: Request):
        try:
            data = loads(str(request.url()).split('?')[1]) # Подгружаем данные
        except:
            return Response(status=503) # При ошибке отправляем ошибку

        self.remove_function(data) # Активируем функцию

        return Response(body=1) # Без ошибки отправляем еденицу

    async def _preset_application(self) -> None:
        subapp.add_routes(routes) # Добавлем функции к субприложению
        self.app.add_subapp(self.subapp_host, subapp) # Добавляем субприложение к приложению по хосту субприложения

    async def run_server(self, loop: asyncio.AbstractEventLoop=None) -> None: # Можно указать асинхронный поток
        await self._preset_application() # Активируем пресет

        run_app( # Запускаем приложение
            self.app, # Приложение
            host=self.host, # Указываем хост
            port=self.port, # Указываем порт
            loop=(loop if loop is not None else self.loop) # Тенарный оператор)))
        )
