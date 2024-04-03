import Controller

while True:
    try:
        print("starting new game")
        c = Controller.Controller()
        c.start()
        c = 5
    except Exception as e:
        print(e)
        break