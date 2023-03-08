import asyncio

from sys import platform
from random import randint
from json import loads 
from typing import Coroutine
from aiohttp.web import Application, RouteTableDef, Response, Request

subapp = Application()
routes = RouteTableDef()

if platform == 'win32':
	try: asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
	except: pass

class NoneFunction: pass

class Back:
	
	def __init__(self, function:Coroutine=NoneFunction, host:str='127.0.0.1', port:int=randint(1000, 9999), subapp_host:str='service'):
		self.function = function
		self.app = Application()
	
	@routes.get('/server/add?{data}')
	async def server_get_add(self, request:Request):
		try: data = loads(str(request.path).split('?')[1])
		except: return Response(status=503)

		self.function(data)

		return Response(body=1)

	@routes.post('/server/add')
	async def server_post_add(self,request:Request):
		pass