from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

class Chatter():
	def __init__(self):
		self.chatbot = ChatBot("myBot")
		self.chatbot.set_trainer(ChatterBotCorpusTrainer)
		 
		# 使用中文语料库训练它
		self.chatbot.train("chatterbot.corpus.chinese")

	def getContent(self, content):
		if content == '你不懂':
			response = '不怪你'
		else:
			response = self.chatbot.get_response(content).text
		
		return {'type':'text', 'content':response}
