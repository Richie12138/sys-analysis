import cocos
from cocos.director import director
import pyglet

# macros to indicate directions
MOVE[K_UP, K_DOWN, K_LEFT, K_RIGHT] = [1, 2, 3, 4]

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
	# keyLayout referred to the player's keyboard layout
	def __init__(self, keyLayout):
    """
    Initialize the player, including his keyboard layout
    Parameters:
    @keyLayout: a list of keys for up, down, left, right,
                respectively.
    """

		self.keyLayout = keyLayout
		self.currentMove = None

	def get_cmd(self, currentKeyPressed):
    """
    Return the command issued by the player.
    All possible return values are defined in
    the MOVE macro.
    Parameters:
    @currentKeyPressed: a list of key pressed
    """

		for key in currentKeyPressed:
            for i in range(len(keyLayout)):
                if keyLayout[i] == key:
                    self.currentMove = MOVE[i]
				break
		return self.currentMove
