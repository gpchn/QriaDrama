print("Hello world!")

def main(*args) -> None:
    print(args)

def callback(globals: dict) -> None:
    globals["load_game"]("LuckyLucky")
