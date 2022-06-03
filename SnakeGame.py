#*******************************************************************
#Created By: Meet Patel
#Version 2.1
#Title: Snake game
#Discription: A snake game for my CS30 final project. It has music and soundeffects too. The goal is to eat the apple and get as long as possible.
#Submitted to: Sheena Williams
#*******************************************************************

#----------------------Importing important libraries----------------------------

import pygame #Pygame will allow us to add graphics and sound
from random import randint #Randint will allow us to generate a random number
import time #Time library will let us keep track of time and allow us to delay the game

#------------------------Declaring pygame window variables-----------------------
grid_size = 20 #The size of each box in the screen
window_width = 900
window_height = 700

#Having a variable to store the file name of the highscore.txt file
highscore_file = "highscore.txt"


#------------------------Initiating pygame graphics and sound effects-------------------

#Intiating the pygame library
pygame.init()

#Making the screen 900 wide and 700 high
screen=pygame.display.set_mode((window_width,window_height))

#Setting the title of the game to display on the pygame window
pygame.display.set_caption("Snake Game")

#Intitating the pygame sound effects sub-library
pygame.mixer.init()

#Declaring soundeffects with the according audio file stored along with the program
eat = pygame.mixer.Sound("generate.wav")
end= pygame.mixer.Sound("end.wav")
key = pygame.mixer.Sound("keypress.mp3")

#Loading the background music
pygame.mixer.music.load('music.mp3')

#Loading our title screen image and resizing it
title_img = pygame.image.load("snake.jpeg")
title_img = pygame.transform.scale(title_img,(window_width,window_height))#Scaling it to fit the entire screen

#Loading our end screen image and resizing it too
end_img = pygame.image.load("endscreen.jpg")
end_img = pygame.transform.scale(end_img,(window_width,window_height))

appleIMG=pygame.image.load("apple.png") #Loading in the apple image

#Setting the volume to 20% so backgrund music is not so distracting
pygame.mixer.music.set_volume(0.2)

#--------------------------------Making the snake class--------------------------------------
class Snake():

    #Intiating nessecary variables for the snake objects
    #Passing in the speed and starting cordinates of the snake
    def __init__(self,speed,x,y):
            
        self.snake_list = [] #This list will be used to store each body part (cordinates) of the snake
        self.snakeX = x #the x coordinate of the snake head
        self.snakeY = y #the y coordinate of the snake head
        self.speed = speed # Setting the speed or refresh rate of the snake
        self.length = 0 #Used to keep track of the length of the snake

        #Used to determine which direction the snake will change in and how much
        self.X_change = 0 
        self.Y_change = 0
        
    #Displays the snake list
    def display_snake(self):
        #Iterating through the 2D list for every set of coordinates in the sanke list
        for coords in self.snake_list: #Here coords is a list with the x and y coordinate like this --> [x,y]
            #Drawing a green square at the coordinates and making sure it is the size of the grid
            pygame.draw.rect(screen,(0,255,0),[coords[0],coords[1],grid_size,grid_size])


#--------------------------------The class for the game components------------------------------------
class Snake_Game():

    #Having score variables to keep track of the score
    def __init__(self):
        self.score = 0
        self.highscore = 0

    #---------------------------------------Title screen---------------------------------------------------

    #The title screen function is used to display the starting screen
    def title_screen(self):

            #Playing out background music and passing in -1 to make it loop forever until stopped
            #pygame.mixer.music.play(-1)
            
            #Using a while loop to update screen according to User input
            while True:

                #Sets the background as our title_image and places it at (0,0) cordinate
                screen.blit(title_img,(0,0))

                #Importing the highscore and updating our highscore attribute accordingly
                self.highscore = self.import_hightscore()

                #Dispalying text at according coordinates and with suitable font sizes
                #The message_display function takes in the string to be displayes then the font size followed by the x and y coordinate
                self.message_display("Welcome to Snake Game",40,450,300)
                self.message_display(f"Current Highscore: {self.highscore}",20,450,330) #Using sting formatting to display the highscore variable 
                self.message_display("Use arrow keys to move snake",25,450,370)
                self.message_display("Do not exit boundary or crash inself",25,450,400)
                self.message_display("Objective is to eat the apples and get a highscore",25,450,430)
                self.message_display("Press S to start or Q to quit",35,450,480)

                #Getting user input
                for event in pygame.event.get():
                    #If red x button on top right is pressed then it ends title screen
                    #Note the if statments are structured as recomended by pygame documentation
                    if event.type==pygame.QUIT:
                        return #Breaks the function

                    #If a keyboard input was given
                    if event.type==pygame.KEYDOWN:
                        #Play the keyboard sound effect
                        pygame.mixer.Sound.play(key)
                        #If the s key was pressed return True so the main funtion continues calling the other functions
                        if event.key==pygame.K_s:
                            return True
                        #If q was pressed end title screen
                        if event.key==pygame.K_q:
                            return  #Breaks the function
                #Updating the new changes to the screen
                pygame.display.update()

#----------------------------------------------Main game loop---------------------------------------------------------

    #The loop where the game is actually played
    def main_loop(self):
        
        #Declaring a snake object with speed 0.075 and having its starting point around the center of the screen
        snake = Snake(0.075,440,340) 

        #Declaring an apple object
        apple = Apple()
        #Generating an apple for the first time
        apple.generate_apple()

        #Using a while loop and a run variable to control the loop and end it when needed.
        #this is because breaking the loop in the middle wont update the screen at the end
        run = True
        while run:
            
            #Getting user input
            for event in pygame.event.get(): #Note same if statment structure as in pygame documentation
                #If red button is pressed stop the while loop
                if event.type==pygame.QUIT:
                    run = False

                #Matching the input of key strokes to the movement of the snake by incresing or decreasing the x and y cordinates by the grid size
                if event.type==pygame.KEYDOWN:
                    #if left key is pressed make snake coordinates change in negative x direction
                    if event.key==pygame.K_LEFT:
                        snake.X_change=-grid_size
                        #Setting y = 0 so Snake moves in only one directiona at a time other wise it would move diagonal which we don't want
                        snake.Y_change=0
                    #Same logic as above
                    if event.key==pygame.K_RIGHT:
                        snake.X_change=grid_size
                        snake.Y_change=0
                    if event.key==pygame.K_UP:
                        snake.Y_change=-grid_size
                        snake.X_change=0
                    if event.key==pygame.K_DOWN:
                        snake.Y_change=grid_size
                        snake.X_change=0

            #Executing the desired move according to x change and y change which is dependent on keybaord input
            snake.snakeX+=snake.X_change #Changes snake x coordianteds to move the snake
            snake.snakeY+=snake.Y_change #Changes snake y coordianteds to move the snake

            #The key part of the code is here. Snake_Head is just a temporrary list which will have the x and y cords of the snake head.
            snake_Head=[]
            #Adding the snake head coordinates to the snake head list
            snake_Head.append(snake.snakeX)
            snake_Head.append(snake.snakeY)

            #Adding the cordinates of the snake head in the snake list. This is a very crutial part of the code.
            #This way we are able to refer back where the snake head used to be and display the snake accordingly
            snake.snake_list.append(snake_Head)

            #Fills the screen with black colour
            screen.fill((0,0,0))

            #Prints the snake parts on the screen 
            snake.display_snake()

            #Displaying the score with font size 20 and at coordinate 20 by 20
            self.message_display(f"{self.score}",20,20,20)

            #Making sure the snake list is not longer than snake length
            #Bassically we do not need snake coordiantes more than its length it would be ineffecient
            if len(snake.snake_list)>snake.length:
                #Getting rid of unncesary coordintes
                snake.snake_list.pop(0) #Gets rid of the first list element which is the last snake body coordinates

            #Runs with the values of the snake list backwards
            for x in snake.snake_list[:-1]:
            #Bassically checks if snake crashed in to itself.
                if x==snake_Head: #If the snake head goes back to where it jsut was
                    run=False #End game

                    
            #Checks if snake has not gone outside of screen if so then game ends. 
            #Using flexible logics by taking use of vaiables
            #Note snake head is a list with x and y coordiantes like this --> [x,y] so snake_Head[0] is the x coordinate and snake_Head[1] would be y
            if snake_Head[0]>(window_width-grid_size) or snake_Head[0]<0 or snake_Head[1]>(window_height-grid_size) or snake_Head[1]<0:
                run=False

            #Checks if snake eats the apple or not. If it does then it adds a snake body part and increases the snake length and generate a new apple             
            if apple.appleX==snake_Head[0] and apple.appleY==snake_Head[1]: #If apple coordinates macth with snake head coordinates
                self.score+=1 #Increase score
                pygame.mixer.Sound.play(eat) #Play eat sound effect
                snake.length+=1 #Increase length of snake
                apple.generate_apple() #Generate new apple

            #Basically speeds up the snakes speed as it gets bigger and bigger to make the game faster and harder
                if snake.length==20:
                    snake.speed=0.065
                if snake.length==50:
                    snake.speed=0.055
            
            #Displaying the apple
            apple.display_apple()

            #This is where the snake speed comes in use. 
            #the snake speed is the refresh rate so we slow down the while loop iteration by pasuing the code for a certaing time
            time.sleep(snake.speed)

            #Display updates
            pygame.display.update()
        
        #When game ends
        pygame.mixer.music.stop() #Stop music
        pygame.mixer.Sound.play(end) #Play game end sound effect

        #If the socre is greater than the highscore than update the highscore
        if self.score>self.highscore:
            self.export_highscore(self.score) #Exporting our score 
            self.highscore = self.score #Updating our local highscore variable to the current score
        
        #Having a little break between the main loop and the end screen to make it a smooth transition
        time.sleep(2)
        
#---------------------------------------------End screen--------------------------------------------

    #The end screen function
    def end_screen(self):
            
            #Using another while loop to control the end screen
            while True:
                
                #Setting the background as our end image stored as a photo
                screen.blit(end_img,(0,0))

                #Displaying the score and highscore
                self.message_display(f" Your score: {self.score}          Highscore: {self.highscore}",20,450,354) #Again using string formating
                self.message_display("Press R to replay or Q to quit",35,450,480)

                #Getting user input same method as before
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        return 
                    if event.type==pygame.KEYDOWN:
                        #Playing keyboard sound effect
                        pygame.mixer.Sound.play(key)
                        #If user wants to repaly then return True so the main function can recall itself
                        if event.key==pygame.K_r:
                            return True
                        if event.key==pygame.K_q:
                            return 
                #Updating the pygame screen
                pygame.display.update()

    #Using a function to declare a text object which will later be used to create text objects
    def text_objects(self,text, font): #Note this coding method is the same as shown in the pygame documentation
        #Returning a text surface object
        textSurface = font.render(text, True, (255,255,255))
        return textSurface, textSurface.get_rect()

    #Dispalying a message on the pygame screen according to coordinate
    def message_display(self,text,size,x,y):
        #Declaring text font
        largeText = pygame.font.Font('freesansbold.ttf',size)
        #Creating text object
        TextSurf, TextRect = self.text_objects(text, largeText)
        #Centering text at x and y coordinate
        TextRect.center = (x,y)
        #Displaying text on screen
        screen.blit(TextSurf, TextRect)

    #Writing the highscore to a file
    def export_highscore(self,score):
        #If the file exists then it overwrites it and if it does not exist then it makes a new file
        with open(highscore_file,"w") as f: #f stand for file and f is a file object which we can call methods on such as open or write
            #Converting the score to a string and writing it to the file
            f.write(str(score))
            #Closing the API
            f.close()

    #Reading in the highscore from a file
    def import_hightscore(self):
        #Opening the highscore file and reading the high score
        with open(highscore_file,"r") as f: #f stand for file and f is a file object which we can call methods on such as open or read
            highscore = f.read()
            #Closing the API
            f.close()
        #If there is no highscore then it is 0
        if highscore == "":
            highscore = 0

        #Return the integer version of the highscore
        return int(highscore)

#------------------------------------------Apple class--------------------------------------------------

class Apple():
    
    #Having apple coordiantes as attributes
    def __init__(self):

        self.appleX = 0
        self.appleY = 0
    
    #Function to display the apple
    def display_apple(self):
        #Displaying the apple image at the apple's coordiantes
        screen.blit(appleIMG,(self.appleX,self.appleY))
        #Updating the pygame screen to show the new apple
        pygame.display.update()

    #Generating random coordinates for the apple
    def generate_apple(self):
        #Using a very complex logic to effeciently generate apple coordinates
        #Bassically i generate a number that will be later multiplied by 20 to get the coordinates according to the gird size
        self.appleX = randint(0,(window_width-grid_size)/grid_size)*grid_size
        self.appleY = randint(0,(window_height-grid_size)/grid_size)*grid_size

#----------------------------------Main function-------------------------------

#The main function used to call the different screen functions to control the flow of the game
def main(playing_again):

    #Making an object for our game
    game = Snake_Game()

    #If the player plays again there is no reason to show the title screen
    if not playing_again:
    #If user selects start in the title screen then continue further
        good_to_go = game.title_screen() #Returns a boolean value where if the player quits then it will be False 
    else:
        #If the the player is playing again continue further
        good_to_go = True
        #Starting the music again
        #pygame.mixer.music.play(-1)
        
    if good_to_go: #If the user does not quit the game and wants to play further

        #Calling the main loop
        game.main_loop()
        
        #If player wants to play again during the end screen then play agin will be True or else False
        play_again = game.end_screen()
        if play_again: #If the player does want to play again
            main(True) #Calling the main loop again which restarts the game and passing True to not dispaly Title screen
            #This is called recursion
            
#Calling our main loop for the first time to start the game once and showing the title screen
main(False)