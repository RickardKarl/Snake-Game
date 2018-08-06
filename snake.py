import turtle
import random
import time


"""Comments from the author:

This game is somewhat sloppily made.
I created it as a demonstration for kids during a programming camp,
which is why I specifically used Turtle for the game's graphics.
I wouldn't recommend using that package to others.
    
    Enjoy!
    // Rickard Karlsson
"""

class snake(turtle.Turtle):

    #################
    ## CLASS VARIABLES
    #################

    stepsize = 20 # Changes the stepsize of the snake, recommended with 10-20
    size_screen = 200 # Changes screensize
    color_of_snake = "red"
    background_color = "white"
    border_color = "black"
    width_snake = stepsize # Recommended to be same as stepsize
    hard_mode = False # If True then you can go through the wall

    ##############
    ## CONSTRUCTOR
    ##############

    def __init__(self):

        self.score = 0 # Score counter

        ## Initializes the snake using the super class turtle
        super().__init__()
        turtle.title("Snake")
        turtle.setup(2*snake.size_screen+4*snake.stepsize, 2*snake.size_screen+4*snake.stepsize)

        ## Controls appearance of snake
        self.hideturtle()
        self.speed(0)
        self.color(snake.color_of_snake)
        self.penup()
        self.shape("square")
        self.width(snake.width_snake)
        self.shapesize(snake.width_snake*0.04,snake.width_snake*0.04) # Shouldn't be adjusted

        ## Instance variables for the snake
        self.snake_stamp = []   # Saves stamp-id which are the marks the snake is putting down when moving around
        self.snake_stamp.append(self.stamp()) # First stamp
        self.snake_length = 3   # Starting length of snake
        self.route = []         # Saves current positons in x,y coordinates for the snake. Will be saved in Vec2D-type
        self.wanted_direction = "left" # Starting direction
        self.current_direction = "left"

        ## painter is another turtle instance which is used to paint the surroundings
        self.painter = turtle.Turtle()
        self.painter.hideturtle()
        self.painter.color(snake.border_color)
        self.painter.width(snake.width_snake)
        self.painter.penup()
        self.painter.speed(0)
        self.painter.goto(snake.size_screen,snake.size_screen)

        ## apple is another turle instance to place apple in by usings stamps, same way as the snake
        self.apple = turtle.Turtle()
        self.apple.speed(0)
        self.apple.hideturtle()
        self.apple.shape("turtle")
        self.apple.shapesize(snake.width_snake * 0.04, snake.width_snake * 0.04)
        self.apple.penup()
        self.apple.color("green")

        ## Instance variables for apple
        self.apple_stamp = []   # Saves the stamp-id for the apple position
        self.apple_x = []       # apple's x-coordinate
        self.apple_y = []       # apple's y-coordinate

        ## Creates border for the game
        self.makeBorder()

    ####################
    ## INSTANCE METHODS
    ####################

    # Creates the border around the game
    # Returns nothing
    def makeBorder(self):
        self.painter.goto(snake.size_screen,snake.size_screen)
        self.painter.pendown()
        self.painter.setheading(270)
        for i in range(4):
            self.painter.forward(snake.size_screen*2)
            self.painter.right(90)
        self.painter.penup()
        self.painter.goto(0,0)

    # Fills the board when the game end and write score
    # Returns nothing
    def end_game(self):
        self.painter.goto(snake.size_screen, snake.size_screen)
        self.painter.pendown()
        self.painter.setheading(270)
        for i in range(int(snake.size_screen/snake.stepsize)):
            self.painter.forward(snake.size_screen * 2)
            self.painter.right(90)
            self.painter.forward(snake.stepsize)
            self.painter.right(90)
            self.painter.forward(snake.size_screen * 2)
            self.painter.left(90)
            self.painter.forward(snake.stepsize)
            self.painter.left(90)
        self.painter.penup()
        self.painter.goto(0, 0)
        self.painter.color("white")
        self.painter.write("Total score: " + str(self.score), align="center", font=("Arial", int(snake.size_screen/10), "bold"))

    ##
    # Methods that moves the snake in four different direction
    # It uses a wanted direction and current moving direction so that you can't turn in the opposite direction

    def goleft(self):
        if self.current_direction != "right":
            self.wanted_direction = "left"

    def goright(self):
        if self.current_direction != "left":
            self.wanted_direction = "right"

    def goup(self):
        if self.current_direction != "down":
            self.wanted_direction = "up"

    def godown(self):
        if self.current_direction != "up":
            self.wanted_direction = "down"
    ##
    ##
    ##

    # Clears the stamp corresponding to the stamp-id with certain index in variable snake_stamp
    # Input is index
    # Returns nothing
    def erase_stamp(self,index):
        self.clearstamp(self.snake_stamp[index])

    # Erases the tail of snake, will always make sure the snake is the correct length
    # Returns nothing
    def erase_tail(self):
        while len(self.snake_stamp)>self.snake_length:
            self.erase_stamp(0)
            self.snake_stamp.remove(self.snake_stamp[0])
            self.route.remove(self.route[0])

    # Checks whether a position given in x- and y-coordinates are laying at the current position of the snake
    # Inputs the x- and y-coordinates
    # Returns True if the given coordinates are not in snakes position, else False
    def legit_route(self,x,y):
        if snake.hard_mode is True and not self.check_if_inside_border():
            return False
        given_position = turtle.Vec2D(x, y)
        for position in self.route[0:len(self.route)-1]:
            if given_position == position:
                return False
        else:
            return True

    # Places an apple in a random spot which the snake isn't positioned at
    # Returns nothing
    def place_apple(self):
        self.apple.clearstamp(self.apple_stamp)
        while True:
            random_x = random.randint(-snake.size_screen+snake.stepsize,snake.size_screen-snake.stepsize)
            random_y = random.randint(-snake.size_screen+snake.stepsize,snake.size_screen-snake.stepsize)
            if random_x % snake.stepsize != 0:
                random_x = random_x - random_x % snake.stepsize
            if random_y % snake.stepsize != 0:
                random_y = random_y - random_y % snake.stepsize
            if self.legit_route(random_x,random_y):
                break
        self.apple.goto(random_x, random_y)

        self.apple_stamp = self.apple.stamp()
        self.apple_x = self.apple.xcor()
        self.apple_y = self.apple.ycor()

    # Checks whether the snake has moved to a position where the apple is placed
    # Returns True if it has caught the apple, False otherwise
    def check_if_apple(self):
        apple_position = turtle.Vec2D(self.apple_x,self.apple_y)
        if self.position() == apple_position:
            self.snake_length += 1
            self.score += 1
            self.apple.clearstamp(self.apple_stamp)
            self.place_apple()
            return True
        else:
            return False

    def check_if_inside_border(self):
        if abs(self.xcor()) >= snake.size_screen or abs(self.ycor()) >= snake.size_screen:
            return False
        else:
            return True

    # This method moves the snake across the board when he goes through one of the walls
    # Returns True if he has been teleported across the board, otherwise False
    def teleport_across_border(self):
        if self.hard_mode is not True:
            if self.xcor() >= snake.size_screen:
                self.goto(-snake.size_screen+snake.stepsize,self.ycor())
                self.snake_stamp.append(self.stamp())
                return True
            elif self.xcor() <= -snake.size_screen:
                self.goto(snake.size_screen-snake.stepsize,self.ycor())
                self.snake_stamp.append(self.stamp())
                return True
            elif self.ycor() >= snake.size_screen:
                self.goto(self.xcor(), -snake.size_screen+snake.stepsize)
                self.snake_stamp.append(self.stamp())
                return True
            elif self.ycor() <= -snake.size_screen:
                self.goto(self.xcor(), snake.size_screen-snake.stepsize)
                self.snake_stamp.append(self.stamp())
                return True
            else:
                return False

    # This is a sequence to be looped using the other instance methods, it is executed every time the snake moves
    # NOTE: Important to check_if_apple before erasing tail
    def run_event(self):
        if not self.teleport_across_border():
            self.snake_stamp.append(self.stamp())
        self.check_if_apple()
        self.erase_tail()
        self.route.append(turtle.Vec2D(self.xcor(), self.ycor()))

    # This is the method that actually moves the snake, it calls run_event after each movement
    # Returns nothing
    def go_in_direction(self):
        if self.wanted_direction == "up":
            self.goto(self.xcor(), self.ycor() + snake.stepsize)
            self.current_direction = "up"
        elif self.wanted_direction == "down":
            self.goto(self.xcor(), self.ycor() - snake.stepsize)
            self.current_direction = "down"
        elif self.wanted_direction == "left":
            self.goto(self.xcor() - snake.stepsize, self.ycor())
            self.current_direction = "left"
        elif self.wanted_direction == "right":
            self.goto(self.xcor() + snake.stepsize, self.ycor())
            self.current_direction = "right"

        self.run_event()

    # This is a time-based loop that updates the game
    # It uses recursion and calls itself after 1 ms
    # (pretty stupid I know, but this is the best way I found using turtle)
    # Returns nothing, but can end the game
    def timer_event(self):
        if self.legit_route(self.xcor(), self.ycor()):
            self.go_in_direction()
            time.sleep(0.1)
            turtle.ontimer(self.timer_event, 1)
        else:
            self.end_game()

    # Method that starts the game
    # To be used once
    def start_game(self):
        self.place_apple()
        self.timer_event()
        turtle.onkey(t.goup, "w")
        turtle.onkey(t.goright, "d")
        turtle.onkey(t.goleft, "a")
        turtle.onkey(t.godown, "s")
        turtle.listen()


t = snake()
t.start_game()
turtle.done()
