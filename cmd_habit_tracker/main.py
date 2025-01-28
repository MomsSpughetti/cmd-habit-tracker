import cmd_habit_tracker.wrapper_functions as wf

def main():
    # initialize stuff
    wf.initialize()
    #wf.reset()

    # print a welcome message
    wf.welcome()

    wf.quick_test() # for experimenting purposes

    # the main program
    wf.refresh()
    wf.automatic_track()
    
    while True:
        wf.execute_command(wf.get_command())

if __name__ == "__main__":
    main()


