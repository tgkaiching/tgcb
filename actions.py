from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet

from jsonFormatter import readFromJSON, JSON_toTree
from anytree import AnyNode, RenderTree, search

class ActionNavigate(Action):
	FILENAME = 'ITSM_training.json'
	ITSM_tree = None

	def __init__(self):
		json_data = readFromJSON(self.FILENAME)
		self.ITSM_tree = JSON_toTree(json_data)

	def name(self):
		return 'action_navigate'
		
	def run(self, dispatcher, tracker, domain):	
		func = tracker.get_slot('function')
		result_list = search.findall(self.ITSM_tree, lambda node: (func) in node.id)
		length = len(result_list)
		temp = ""
		if(length > 1):	
			for x in range(0, length):
				result = result_list[x]
				temp += str(x+1) + ". " + result.id + ": "
				temp += result.url
				if(x != length - 1):
					temp += "\n"
			response = """Are you looking for...\n{}""".format(temp)		
		elif (length == 1):
			url = result_list[0].url
			title = result_list[0].id
			response = """I think you are looking for this!\n{}\n{}""".format(title, url)
		else:
			temp = search.find(self.ITSM_tree, lambda node: ("homepage") == node.id)
			url = temp.url
			response = "Sorry! {} is not found! Please checkout our homepage {}".format(func, url)
		# print(response)
						
		dispatcher.utter_message(response)
		return [SlotSet('function',None)]