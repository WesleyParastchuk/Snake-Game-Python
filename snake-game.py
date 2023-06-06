from tkinter import *
import random
import time


class Food:
    COLOR = "red"

    def __init__(self):
        self.foodPosition = []
        self.foodPart = 0
        self.createFood()

    def foodClean(self):
        if bool(self.foodPosition):
            self.foodPosition.clear()
        if bool(self.foodPart):
            tela.Bg_canva.delete(self.foodPart)
            self.foodPart = 0

    def createFood(self):
        x = random.randint(0, Game.BLOCKS-1)
        y = random.randint(0, Game.BLOCKS-1)
        if self.validPosition([x, y]):
            self.foodPosition.append(x)
            self.foodPosition.append(y)
            self.showFoodPart([x, y])
            return
        return self.createFood()

    def showFoodPart(self, pos):
        x0 = pos[0] * Game.BLOCKSIZE
        x1 = (pos[0] + 1) * Game.BLOCKSIZE
        y0 = pos[1] * Game.BLOCKSIZE
        y1 = (pos[1] + 1) * Game.BLOCKSIZE
        self.foodPart = tela.Bg_canva.create_rectangle(x0, y0, x1, y1, fill=self.COLOR)

    def validPosition(self, pos):
        for i in range(len(cobra.snakePositions)):
            if (
                cobra.snakePositions[i][0] == pos[0]
                and cobra.snakePositions[i][1] == pos[1]
            ):
                return False
        return True


class Snake:
    INITIALSIZE = 4
    COLOR = "green"
    HEADCOLOR = "darkgreen"

    def __init__(self):
        self.size = self.INITIALSIZE
        self.snakePositions = []
        self.snakeParts = []
        self.createSnake()

    def createSnake(self):
        x = y = Game.BLOCKS // 2
        for tam in range(self.INITIALSIZE):
            self.snakePositions.append([x - tam, y])
            self.showSnakePart(self.snakePositions[tam])

    def showSnakePart(self, pos):
        x0 = pos[0] * Game.BLOCKSIZE
        x1 = (pos[0] + 1) * Game.BLOCKSIZE
        y0 = pos[1] * Game.BLOCKSIZE
        y1 = (pos[1] + 1) * Game.BLOCKSIZE
        self.snakeParts.append(
            tela.Bg_canva.create_rectangle(
                x0,
                y0,
                x1,
                y1,
                fill=Snake.HEADCOLOR if (len(self.snakeParts) == 0) else Snake.COLOR,
            )
        )

    def move(self, direction):
        newX = self.snakePositions[0][0]
        newY = self.snakePositions[0][1]
        if(direction == "Up"):
            newY -= 1
        elif(direction == "Down"):
            newY += 1
        elif(direction == "Right"):
            newX += 1
        elif(direction == "Left"):
            newX -= 1
        self.snakePositions.insert(0, [newX, newY])
        for i in range(len(self.snakeParts)):
            x = (
                self.snakePositions[i][0] - self.snakePositions[i + 1][0]
            ) * Game.BLOCKSIZE
            y = (
                self.snakePositions[i][1] - self.snakePositions[i + 1][1]
            ) * Game.BLOCKSIZE
            tela.Bg_canva.move(self.snakeParts[i], x, y)
        if(self.snakePositions[0] == comida.foodPosition):
            comida.foodClean()
            comida.createFood()
            tela.addPoint()
            self.showSnakePart(self.snakePositions[len(self.snakePositions)-1])
        else:
            self.snakePositions.pop()

    def validateMove(self):
        x = self.snakePositions[0][0]
        y = self.snakePositions[0][1]
        if((x < 0 or x > Game.BLOCKS-1) or (y < 0 or y > Game.BLOCKS-1)):
            return False
        for i in range(1, len(self.snakePositions)):
            if(x == self.snakePositions[i][0] and y == self.snakePositions[i][1]):
                return False
        return True

class Game:
    BGCOLOR = "black"
    BDCOLOR = "gray"
    GAMESIZE = 640
    BLOCKSIZE = 20
    BORDERSIZE = 10
    BLOCKS = GAMESIZE // BLOCKSIZE
    SPEED = 100
    POINTSIZE = 50

    def __init__(self):
        self.points = 0
        self.direction = "Right"
        self.createScreen()
        self.createButtons()

    def createScreen(self):
        self.size = Game.GAMESIZE
        self.screen = Tk()
        self.screen.title("Snake Game")
        self.screen.geometry(str(self.size+Game.BORDERSIZE) + "x" + str(self.size+Game.BORDERSIZE+Game.POINTSIZE))
        self.screen.resizable(False, False)
        self.screen.config(bg=Game.BDCOLOR)
        self.Bg_canva = Canvas(
            master=self.screen,
            height=self.size,
            width=self.size,
            bg=Game.BGCOLOR,
            highlightthickness=0,
        )
        self.Bg_canva.pack(pady=Game.BORDERSIZE//2)

    def createButtons(self):
        self.screen.bind("<w>", lambda event: self.setDirection("Up"))
        self.screen.bind("<s>", lambda event: self.setDirection("Down"))
        self.screen.bind("<a>", lambda event: self.setDirection("Left"))
        self.screen.bind("<d>", lambda event: self.setDirection("Right"))
        self.screen.bind("<Up>", lambda event: self.setDirection("Up"))
        self.screen.bind("<Down>", lambda event: self.setDirection("Down"))
        self.screen.bind("<Right>", lambda event: self.setDirection("Right"))
        self.screen.bind("<Left>", lambda event: self.setDirection("Left"))

    def validDirection(self, newDirection):
        if self.direction == newDirection:
            return False
        if(self.direction == "Up"):
            return not (newDirection == "Down")
        elif(self.direction == "Down"):
            return not (newDirection == "Up")
        elif(self.direction == "Left"):
            return not (newDirection == "Right")
        elif(self.direction == "Right"):
            return not (newDirection == "Left")
        return False

    def setDirection(self, newDirection):
        if self.validDirection(newDirection):
            self.direction = newDirection

    def gameOver(self):
        return cobra.validateMove()

    def moveLoop(self):
        if(self.gameOver()):
            cobra.move(self.direction)
            tela.screen.after(Game.SPEED, self.moveLoop)

    def iniciateGame(self):
        self.moveLoop()

    def addPoint(self):
        self.points += 1
        print(self.points)

    def keepInGame(self):
        self.screen.mainloop()

    def play():
        global tela, cobra, comida
        tela = Game()
        cobra = Snake()
        comida = Food()
        tela.iniciateGame()
        tela.keepInGame()

if __name__ == "__main__":
    Game.play()