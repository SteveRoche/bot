import os, sys
import random
import json
import requests
from time import sleep
from flask import Flask, request, abort

memes = [item for item in os.listdir(os.path.join(os.getcwd(), 'memes')) if item != 'file_data.json']

with open('TOKEN', 'r') as f:
	API_TOKEN = f.read()

class Bot:
	def __init__(self, token, offset=0):
		self.url = 'https://api.telegram.org/bot{token}/'.format(token=token)
		self.offset = offset

	def getMe(self):
		return requests.get(''.join([self.url, 'getMe'])).json()

	def getUpdates(self):
		return requests.get(''.join([self.url, 'getUpdates']), params={'offset': self.offset}).json()

	def sendMessage(self, chatId, text):
		requests.get(self.__buildCommand('sendMessage'), params={
			'chat_id': chatId,
			'text': text,
		})

	def sendPhoto(self, chatId):
		requests.post(
			self.__buildCommand('sendPhoto'), 
			files={ 'photo': open('memes/{filename}'.format(filename=random.choice(memes)), 'rb')},
			data={ 'chat_id': chatId }
		)

	def __buildCommand(self, command):
		return ''.join([self.url, command])

bot = Bot(API_TOKEN)

while True:
	results = bot.getUpdates()['result']
	for result in results:
		update_id = result['update_id']
		chat_id = result['message']['chat']['id']
		if bot.offset <= update_id:
			bot.offset = update_id + 1

			if result['message']['text'] == '/memeplz':
				bot.sendPhoto(chat_id)
			else:
				bot.sendMessage(chat_id, 'Ask for a meme')
	sleep(2)