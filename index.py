from zombie import Zombie
from google import Google

from taskmaster import TaskMaster

t = TaskMaster()

forwardToEmail = ""
signUpPassword = ""


while True:
    try:
        zombie = Zombie(t.getActiveProxy())
        google = Google(zombie)
        email = google.signup(t.getActivePhone(),signUpPassword)
        google.forwardToEmail(forwardToEmail)
    except KeyboardInterrupt:
        zombie.kill()
        selection = ""
        while selection != "y" and selection != "n":
            selection = input("rotate profile? Y/N \n>> ").lower()
        if selection == "y":
            t.rotateActiveBrowserProfile()
    finally:
        zombie.kill()
