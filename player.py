import cocos
from cocos.director import director
import pyglet


class KeyControl(cocos.layer.Layer):
	'''KeyControl was used to listen to the key event
	every time the Key was pressed or release,
	The key will insert at the beginning of the list(duplicate was noallowed)
	'''
	is_event_handler = True #:enable pyglet's events

	def __init__(self):
		super(KeyControl, self).__init__()
		#The list used to hold the key event
		self.currentKeyPressed = []

	def on_key_press(self, key, modifiers):
		key = pyglet.window.key.symbol_string(key)
		#if the key was not in the currentKeyPressed
		if key not in self.currentKeyPressed:
			#insert at the beginning of the list
			self.currentKeyPressed.insert(0,key)

	def on_key_release(self, key, modifiers):
		key = pyglet.window.key.symbol_string(key)
		if key in self.currentKeyPressed:
			self.currentKeyPressed.remove(key)

		
class Player():
	# keyLayout referred to the Players keyBoard layout for the game
	def __init__(self, keyLayout):
		self.keyLayout = keyLayout
		self.currentKey = ""

	def get_cmd(self, currentKeyPressed):
		self.currentKey = ""
		for key in currentKeyPressed:
			if key in self.keyLayout:
				self.currentKey = key
				break
		return self.currentKey
#Test
# ===========================================
class World(cocos.layer.Layer):
	def __init__(self):

		super(World, self).__init__()
		#use the text to debug the players input
		text = "Current: "
		for i in xrange(0, len(players)):
			text += "Player" + str(i+1) + " " + players[i].currentKey + " "

		self.info = cocos.text.Label(text, x = 100,  y=280)
		self.add(self.info)
		self.schedule(self.update)

	def update(self,dt):
		for player in players:
			player.get_cmd(keyControl.currentKeyPressed)
		text = "Current: "
		for i in xrange(0, len(players)):
			text += "Player" + str(i+1) + " " + players[i].currentKey + " "
		self.info.element.text = text

director.init(resizable=True)
player1 = Player(('A','W','S','D' ))
player2 = Player(('UP','DOWN','LEFT','RIGHT' ))
players = [player1, player2]
keyControl = KeyControl()
world = World()


if __name__ == "__main__":
	while True:
		director.run( cocos.scene.Scene(keyControl,world ) )


