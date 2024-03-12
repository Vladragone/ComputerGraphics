from random import uniform

with open("data.txt", "w") as file:
    for _ in range(100):
        x = uniform(-100, 100)
        y = uniform(-100, 100)
        file.write(str(round(x, 3)) + " " + str(round(y, 3)) + "\n")
