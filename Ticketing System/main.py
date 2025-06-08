def MainMenu():
  print("\n\tWelcome to CC03 Cinema\nPlease Choose an Operation Below\n\n\t"
        "1. Book a movie ticket\n\t2. Available Movies(Test)\n\t3. Search(Test)\n\t4. EXIT")
MainMenu()
choose = int(input("\nChoose >> "))

while True:

  match choose:

    case 1:

      print("Command")
      from Ticketsystem import *

    case 2:

      print('Mario Movie\nJohn Wick\nFast and Furious\nSpiderman: Into Spiderverse\nMission Impossible: Dead Reckoning\nHarry Potter\nMario Movie\nDBZ: Movie')

    case 3:
      print("\nSearch")

    case 4:
      print("Thank You,\nGoodbye!")
      exit()

    case default:
      print("\nInvalid Selection, Please Try again!\n ")
      MainMenu()
      choose = int(input("\nChoose >> "))