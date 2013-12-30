# The Adventures of Bob the Turtle (Turtle Bob)
#
# This is the main module for this application.
#

#Import the time module so that we can delay for times and such
import time
#Import the atexit module so we can have a graceful and consisten exit 
# from the program
import atexit
#Import terminalsize.py so we can get the size of the console
import terminalsize

def main():
    print("Let the adventure begin!")
    getgoing()
    print("And so we continue!")
    renderscreen()

#This function will be used to display the gameplay screen and will adapt to
# changes in screen size
#Testing functionality right now
def renderscreen():
    #Set some of our variables
    #These will end up being passed as arguments to the renderscreen function
    title = "Introduction"
    bodytext = "As we begin our adventure, the narrator, in a calm and soothing voice, explains some details about our adventurer."
    
    #Get the screen attributes
    (width, height) = terminalsize.get_terminal_size()
    #Calculate the indent for the bodytext
    bodyindent = int(width * 0.1)
    #Calculate the indent of the title
    titleindent = int((width - len(title))/2)
    #Calculate the width of the bodytext lines
    bodywidth = int(0.8 * width)
    #Calculate the indent for the "Press a Key" message
    contindent = int((width - len("Press a Key"))/2)

    #This will print '=' across the width of the screen to make a top border
    for i in range(width-1):
        print("=", end="")
    print("=") #The last '=' and a newline
    #This will print spaces until when the title should begin
    for i in range(titleindent):
        print(" ", end="")
    #Print the title, which includes a newline, along with another blank line
    print(title)
    print("")

    #This will print out the bodytext line by line, stopping if it would run past
    # the end of the terminal
    place = 0
    k = 3
    while place < len(bodytext):
        for i in range(bodyindent):
            print(" ", end="")
        for i in range(bodywidth):
            if place + i > len(bodytext) - 1:
                print(" ", end="")
                break #Leaves the smallest enclosing for/while statement
            print(bodytext[place + i], end="")
        place += int(0.8 * width)
        for i in range(bodyindent - 1):
            print(" ", end="")
        print(" ")
        if k >= height - 2:
            print("")
            for i in range(contindent):
                print(" ", end="")
            input("Press a key") #Also has a newline
        k += 1
    print("")

    

    

#This function will be used to clean up after our program and give a farewell
# message 
def goodbye():
    time.sleep(1)
    print("Fair travels!")
    time.sleep(1)

#This allows the user to exit the program in a civil manner
#Note: If the input is 'y', then we just pass through this function
def getgoing():
    strt = input("Ready to get going? (y/n) ")
    if strt == "n":
        exit()
    elif strt != "y":
        print("I didn't understand what you said!")
        time.sleep(1)
        getgoing()

#Register the functions that we want to run when the program is closed
#Note: this must be done after the function has been defined, so we have
# it at the end
atexit.register(goodbye)

#Begin the adventure!
main()