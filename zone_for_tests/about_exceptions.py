
class MyException(Exception):
    def __init__(self, message):
        super(MyException, self).__init__()
        self.message = message


try:
    raise MyException("Hi")
except MyException as err:
    print("No problem")
except Exception as err:
    print("Some problems")

# class MyError(Exception):
#     def __init__(self, text):
#         self.txt = text
#
#
# a = input("Input positive integer: ")
#
# try:
#     a = int(a)
#     if a < 0:
#         raise MyError("You give negative!")
# except ValueError:
#     print("Error type of value!")
# except MyError as mr:
#     print(mr)
# else:
#     print(a)