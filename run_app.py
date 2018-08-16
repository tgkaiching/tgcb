from rasa_core.channels import HttpInputChannel
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_slack_connector import SlackInput


nlu_interpreter = RasaNLUInterpreter('./models/nlu/default/tgcbnlu')
agent = Agent.load('./models/dialogue', interpreter = nlu_interpreter)

input_channel = SlackInput('xoxp-409107014070-407546356660-408021814001-b52a02b7c37b9a796f12d4b2ab9a2a05', #app verification token
							'xoxb-409107014070-407666773299-4CqKEYtfAjzZSJMnBCithjVL', # bot verification token
							'QfDLRRuYLCC4uKRjrGcTTYXc', # slack verification token
							True)

agent.handle_channel(HttpInputChannel(5004, '/', input_channel))