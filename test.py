import randvkmessage
import unittest


class MainTest(unittest.TestCase):
	def test(self):
		#coming soon...
		pass


'''if __name__ == "__main__":
	print "RandomVKMessage %s" % __version__
	unittest.main()'''

ran = randvkmessage.RandomVKMessage(count="s7")
ran.start()