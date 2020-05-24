def task(car):
    for i in range(2):
        while not car.at_border():
            car.go()
        for i in range(2):
            car.left()
