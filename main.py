import wrapper_functions as wf

if __name__ == "__main__":

    # initialize stuff
    wf.initialize()
    #wf.reset()

    # print a welcome message
    wf.welcome()

    # the main program
    while True:
        wf.execute_command(wf.get_command())



