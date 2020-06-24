def foo():
	return 123
class Test:
	wartosc = foo()

	def __init__(self):
		pass

	def test(self):
		print(Test.wartosc)

	def test2():
		print(Test.wartosc)

t = Test()
t.test()

Test.test2()