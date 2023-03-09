import asyncio # Импортируем асинхронность

from sys import platform # Импортируем опредление платформы
from random import randint # Импортируем рандом
from json import loads # Импортируем модуль для работы с JSON
from typing import Coroutine # ДЛЯ АННОТАЦИИ
from aiohttp.web import Application, RouteTableDef, Response, Request, run_app # Импортируем кучу всего из aiohttp.web

subapp = Application()
routes = RouteTableDef()

if platform == 'win32':
	try: asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
	except: pass

async def add_func(nickname:str) -> None:
	pass
	# В этой функции мы на основе никнейма ищем telegram id игрока и пишем ему что он вошёл на сервер

async def remove_func(nickname:str) -> None:
	pass
	# В этой функции мы на основе никнейма ищем telegram id игрока и пишем ему что он вышел с сервера

class Back:
	
	def __init__(self,
		add_function:Coroutine=add_func,
		remove_function:Coroutine=remove_func,
		host:str='127.0.0.1',
		port:int=randint(1000, 9999),
		subapp_host:str='service',
		app:Application=Application(),
		loop:asyncio.AbstractEventLoop=asyncio.get_event_loop()
	):
		self.add_function = add_function
		self.remove_function = remove_function
		self.app = app
		self.host = host
		self.port = port
		self.subapp_host = subapp_host
		self.loop = loop
	
	@routes.get('/server/add?{data}')
	async def server_get_add(self, request:Request):
		try: data = loads(str(request.url()).split('?')[1])
		except: return Response(status=503)

		self.add_function(data)

		return Response(body=1)

	@routes.get('/server/remove?{data}')
	async def server_get_remove(self, request:Request):
		try: data = loads(str(request.url()).split('?')[1])
		except: return Response(status=503)

		self.remove_function(data)

		return Response(body=1)

	async def _preset_application(self) -> None:
		subapp.add_routes(routes)
		self.app.add_subapp(self.subapp_host, subapp)

	async def run_server(self, loop:asyncio.AbstractEventLoop=None) -> None:
		await self._preset_application()

		run_app(
			self.app,
			host=self.host,
			port=self.port,
			loop=(loop if loop is not None else self.loop)
		)