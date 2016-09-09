import log
import device
import api
import resource.task.auto_combat as autoCombat

def main():
    autoCombat.setup()
    while True:
        try:
            autoCombat.do()
        except RuntimeError:
            api.touchAt((250, 250))

main()
