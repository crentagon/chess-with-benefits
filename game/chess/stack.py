
class Stack:

	def __init__(self):
		self.container = [] 

	def is_empty(self):
		return self.size() == 0 

	def push(self, item):
		self.container.append(item) 

	def pop(self):
		return self.container.pop() 

	def sort(self):
		self.container.sort()

	def search_and_pop(self, fullmove_clock):
		i = 0
		for element in self.container:
			if element[1] == fullmove_clock:
				self.container.pop(i)
				break
			i += 1

	def print_stack(self):
		print ">>> Start print"
		for element in self.container:
			print ">>>>>>", element
		print ">>> End print"

	def size(self):
		return len(self.container)
