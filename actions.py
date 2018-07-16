from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet

class ActionNavigate(Action):
	temp = {"homepage": "https://itsm.towngas.com/"}
	def name(self):
		return 'action_navigate'
		
	def run(self, dispatcher, tracker, domain):
		
		func = tracker.get_slot('function')
		url = self.temp[func]

		# loc = tracker.get_slot('location')
		# current = client.getCurrentWeather(q=loc)
		
		# country = current['location']['country']
		# city = current['location']['name']
		# condition = current['current']['condition']['text']
		# temperature_c = current['current']['temp_c']
		# humidity = current['current']['humidity']
		# wind_mph = current['current']['wind_mph']

		response = """I think you are looking for this!\n {}""".format(url)
						
		dispatcher.utter_message(response)
		return [SlotSet('function',url)]