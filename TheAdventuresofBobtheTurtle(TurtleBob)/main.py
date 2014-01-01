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
#Import the random module so we can do things with randomness, like present
# the choices in a random order
import random
#Import the os module so we can do things like see file sizes
import os

def main():
    print("Let the adventure begin!")
    getgoing()
    print("And so we continue!")
    #Give the screen dimensions greater scope than the renderscreen function
    (widthpass, heightpass) = terminalsize.get_terminal_size()
    #The first screen
    (numofchoices, choicemap) = renderscreen("first", widthpass, heightpass)
    #The main game loop
    while True == True:
        #getchoice handles exiting the loop, so no external control is needed
        choice = getchoice(numofchoices)
        #Get the proper screen size
        (widthpass, heightpass) = terminalsize.get_terminal_size()
        #Will use the choice to render the appropriate screen, ultimately
        (numofchoices, choicemap) = renderscreen(choicemap[choice], widthpass, heightpass)


#This function will be used to display the gameplay screen and will adapt to
# changes in screen size
#Testing functionality right now
def renderscreen(adventure, width, height):
    #Open the appropriate file in the adventures folder
    adventurefile = open("adventures/" + adventure + ".txt", "r")
    #Figure out the size of the file and return the pointer to the beginning
    adventurefile.seek(0, os.SEEK_END)
    filesize = adventurefile.tell()
    adventurefile.seek(0, os.SEEK_SET)
    #Set some of our variables
    #These will end up being passed as arguments to the renderscreen function
    #Note: Need to trim the newlines from the ends of the lines
    title = adventurefile.readline()[:-1]
    bodytext = adventurefile.readline()[:-1]
    #The choices are presented in the form of a list of tuples of the form:
    #   ("Name of the adventure file", "Text of choice")
    choices = [adventurefile.readline().split(":", 1)]
    while adventurefile.tell() < filesize:
        choices.append(adventurefile.readline().split(":", 1))
    
    #Calculate the indent for the bodytext
    bodyindent = int(width * 0.1)
    #Calculate the indent of the title
    titleindent = int((width - len(title))/2)
    #Calculate the width of the bodytext lines
    bodywidth = int(0.8 * width)
    #Calculate the indent for the "Press Enter" message
    contindent = int((width - len("Press Enter"))/2)
    #Calculate the indent for the choices
    choiceindent = int(0.05 * width)
    #Calculate with width of the choice lines
    choicewidth = int(0.9 * width)

    #This will print '=' across the width of the screen to make a top border
    for i in range(width-2):
        print("=", end="")
    print("=") #The last '=' and a newline
    #This will print spaces until when the title should begin
    for i in range(titleindent):
        print(" ", end="")
    #Print the title, which includes a newline, along with another blank line
    print(title)
    print("")

    #This will print out the bodytext line by line, gracefully handling newlines,
    # stopping if it would run past the end of the terminal
    place = 0 #Spot in the currently rendered text
    screennum = 4 #The line in the window being rendered - used to determine if about
                  # to run off of the screen
    isnew = False
    while place < len(bodytext):
        for i in range(bodyindent):
            print(" ", end="")
        for i in range(bodywidth):
            #This first clause checks to see if the next character is a newline and
            # handles it appropriately
            if place + i + 1 < len(bodytext) and bodytext[place + i] == "\\" and bodytext[place + i + 1] == "n":
                print("")
                screennum += 1
                #Skip rendering the newline characters
                place += i + 2
                isnew = True
                break #Leaves the smallest enclosing for/while statement
            if place + i > len(bodytext) - 1:
                break
            print(bodytext[place + i], end="")
        if isnew == False and place < len(bodytext):
            place += int(0.8 * width)
            print("")
            screennum += 1
        #Note: Have already handled if isnew is True, so no additional steps need
        # to be taken
        isnew = False
    if screennum >= height - 2:
        print("")
        screennum+=1
        for i in range(contindent):
            print(" ", end="")
        input("Press Enter") #Also has a newline
        screennum += 1
        height += height
        renderscreen(adventure, width, height)
    print("")
    print("")
    screennum += 2

    #Render the choices, with one line of space in between them
    #Create a list of the choices, randomized
    randchoices = random.sample(list(zip(*choices))[1], len(choices))
    #Get rid of newlines at the end of the choices, if they are there
    for currentchoice in randchoices:
        if currentchoice[-1] == "\n":
            randchoices[randchoices.index(currentchoice)] = currentchoice[:-1]
    for currentchoice in randchoices:
        place = 0
        while place < len(currentchoice):
            for i in range(choiceindent - 3):
                print(" ", end="")
            if place == 0:
                print(str(randchoices.index(currentchoice) + 1) + ".", end="")
            else:
                print("  ", end="")
            print(" ", end="")
            for i in range(choicewidth):
                #This first clause checks to see if the next character is a newline and
                # handles it appropriately
                if place + i + 1 < len(currentchoice) and currentchoice[place + i] == "\\" and currentchoice[place + i + 1] == "n":
                    print("")
                    screennum += 1
                    #Skip rendering the newline character
                    place += i + 2
                    isnew = True
                    break #Leaves the smallest enclosing for/while statement
                if place + i > len(currentchoice) - 1:
                    break
                print(currentchoice[place + i], end="")
            if isnew == False:
                place += int(0.9 * width)
            #Note: Have already handled if isnew is True, so no additional
            # steps need to be taken
            isnew = False
            print("") #Line of space between options
            screennum += 1
            if screennum >= height - 2:
                print("")
                screennum += 1
                print(str(screennum) + "/" + str(height))
                for i in range(contindent):
                    print(" ", end="")
                input("Press Enter") #Also has a newline
                screennum += 1
                height += 6
                renderscreen(adventure, width, height)
    
    #Print blank lines until this rendering has taken up the rest of the window,
    # save a line for the input from the user        
    while screennum < height:
        print("")
        screennum += 1
    
    #Return the number of choices so getchoice() can check to see if one is valid
    # and return a dictionary that represents which choices map to which adventure
    # page
    choicemap = {}
    for i in range(len(randchoices)):
        for k in range(len(choices)):
            if choices[k][1] == randchoices[i] or choices[k][1] == randchoices[i] + "\n":
                choicemap[i+1] = choices[k][0]
    return (len(randchoices), choicemap)
                
#This function gets the choice from the user and renders the next screen as
# well as allowing a civil exit from the program
def getchoice(numofchoices):
    choice = input("Which choice would you like to make? ")
    if choice == "q" or choice == "quit" or choice == "exit":
        exit()
    if choice.isdigit() == False or int(choice) > numofchoices:
        print("That's not a valid option!")
        choice = getchoice(numofchoices)
    return int(choice)


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