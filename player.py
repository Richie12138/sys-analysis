# macros to indicate directions
MOVE = [UP, DOWN, LEFT, RIGHT] = [0, 1, 2, 3] 

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

	def update(self, currentKeyPressed):
		"""
        Update the player's command.
        @currentKeyPressed: a list of key pressed
        """

		self.currentMove = None
		for key in currentKeyPressed:
			if key in self.keyLayout:
					self.currentMove = MOVE[self.keyLayout.index(key)]
					break

# Test
# ========================================
# 
# 	def test(self, screen, id, xy, fontr):
# 		"""Test"""
# 		move = {UP: "up",
# 				DOWN:"down",
# 				LEFT: "left",
# 				RIGHT: "right"
# 			}
# 
# 		if self.currentMove != None:
# 			action = move[self.currentMove]
# 		else:
# 			action = "None"
# 
# 		info = "Player" + str(id) + " " +  action ;
# 		screen.blit(fontr.render("%s:" %(info),True,(0,0,0)),tuple(xy))
# 
