import random
def generate(num):
    file = open(str("dataset_" + str(num) + ".txt"), "w+")
    i = 0
    while i < num:
        val = random.randint(0, 1000000)
        file.writelines(str(val) + "\n")
        i += 1

generate(500)
generate(5000)
generate(50000)