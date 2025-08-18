# import cmd_habit_tracker.wrapper_functions as wf
from cmd_habit_tracker import cli

def main():
    # initialize stuff
    cli.initialize()
    #wf.reset()

    # print a welcome message
    cli.welcome()

    cli.quick_test() # for experimenting purposes

    # the main program
    cli.refresh()
    cli.automatic_track()
    
    while True:
        cli.execute_command(cli.get_command())

if __name__ == "__main__":
    main()


