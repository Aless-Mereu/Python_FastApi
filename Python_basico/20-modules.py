import maths_util
from my_package import messages

results = maths_util.additions(5, 3)
print(f"The result of the addition is: {results}")

greeting = messages.greet("Alice")
farewell = messages.bye("Alice")
print(greeting)
print(farewell)