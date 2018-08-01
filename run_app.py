from rasa_core.channels import HttpInputChannel
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_slack_connector import SlackInput


nlu_interpreter = RasaNLUInterpreter('./models/nlu/default/tgcbnlu')
agent = Agent.load('./models/dialogue', interpreter = nlu_interpreter)

input_channel = SlackInput('xoxp-409107014070-407546356660-409119760486-77861617fa60210fc5c1331cc4243e11', #app verification token
							'xoxb-409107014070-407666773299-2FhaFYnN8ibOzW6eWwFhzCql', # bot verification token
							'zhEsoPSnm7cjwnKA7IODChY6', # slack verification token
							True)

agent.handle_channel(HttpInputChannel(5004, '/', input_channel))