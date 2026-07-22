from cmu_graphics import *
from cmu_cpcs_utils import rounded
import random
import math

def onAppStart(app):
    app.grading = False
    app.gradingShape = None
    
    #starting menu
    app.menu = True
    app.skinsMenu = False
    app.startButtonHighlighted = False
    app.menuButtonHighlighted = False
    app.skinsButtonHighlighted = False
    app.currentSkin = None
    # image from https://classroomclipart.com/image/vector-clipart/red-white-blue-top-hat-clipart-32783.htm
    app.topHatURL = 'cmu://1166267/46628903/red-white-blue-top-hat-clipart-32783-removebg-preview+(1).png'
    # image from https://similarpng.com/gold-crown-on-transparent-background-png/
    app.crownURL = 'cmu://1166267/46622841/Gold-crown-on-transparent-background-PNG-removebg-preview.png'
    # image from https://www.gettyimages.com/detail/illustration/sombrero-mexican-hat-icon-vector-royalty-free-illustration/1336555405
    app.sombreroURL = 'cmu://1166267/46629184/gettyimages-1336555405-612x612-removebg-preview.png'
    
    #player position (dot)
    app.playerX = app.width / 2
    app.playerY = app.height - 70
    
    #other starting logistics
    app.r = 10.5
    app.colors = ['crimson', 'mediumSpringGreen', 'mediumPurple', 'lightSkyBlue']
    app.playerFillIndex = random.randrange(len(app.colors))
    app.playerFill = app.colors[app.playerFillIndex]
    app.vertAcceleration = 1.2
    app.vertSpeed = 0
    app.score = 0
    app.bestScore = 0
    app.scoreRecorded = False
    
    #for when we are about to start the game but space hasn't been clicked yet
    app.starting = False
    app.gameOver = True
    app.takingSteps = False
    
    #initial obstacles
    app.obstacles = []
    generateRandomObstacle(app, 100)
    

def drawBlackBackground(app):
    drawRect(0, 0, app.width, app.height)

def redrawAll(app):
    if app.grading:
        drawGrading(app)
    elif app.skinsMenu:
        drawSkinsMenu(app)
    elif app.menu:
        drawMenuScreen(app)
    elif app.starting:
        drawStartingScreen(app)
    elif app.gameOver:
        drawGameOver(app)
    else:
        drawGame(app)

def drawGrading(app):
    drawBlackBackground(app)
    drawLabel('Grading Shortcuts', app.width / 2, 30, size = 30, bold = True, fill = 'pink')
    options = ['Ring', 'Square', 'Line', 'Plus Signs', 'Skins']
    optionsKey = ['R', 'Q', 'L', 'P', 'S']
    for i in range(len(options)):
        cx, cy = app.width / 2, 80 + (i * 60)
        drawRect(cx - 75, cy - 25, 150, 50, fill = 'grey')
        drawLabel(options[i], cx, cy - 10, size = 20, fill = 'white', bold = True)
        drawLabel(f'Click {optionsKey[i]} key', cx, cy + 10, fill = 'white', bold = True)
    drawLabel("Press 'M' to return to menu", app.width / 2, app.height - 30, fill = 'white', size = 20, bold = True)

def drawSkinsMenu(app):
    drawBlackBackground(app)
    drawLabel('Choose A Skin!', app.width / 2, 60, size = 40, bold = True, fill = 'pink')
    skinOptions = [None, 'topHat', 'crown', 'sombrero']
    numOfSkins = len(skinOptions)
    for i in range(numOfSkins):
        currSkin = skinOptions[i]
        div = app.width // (numOfSkins + 1)
        cx = div * (i + 1)
        cy = app.height / 2
        if app.currentSkin == currSkin:
            drawCircle(cx, cy, app.r + 30, fill = 'pink', opacity = 40)
        drawBallPreview(app, cx, cy, currSkin)
    drawGoBackToMenu(app)

def drawBallPreview(app, cx, cy, currSkin):
    drawCircle(cx, cy, app.r, fill = 'pink')
    if currSkin == 'topHat':
        drawTopHat(app, cx, cy)
    elif currSkin == 'sombrero':
        drawSombrero(app, cx, cy)
    elif currSkin == 'crown':
        drawCrown(app, cx, cy)

def drawTopHat(app, cx, cy):
    drawImage(app.topHatURL, cx, cy - 8, align = 'bottom', width = 37, height = 37)

def drawCrown(app, cx, cy):
    drawImage(app.crownURL, cx, cy + 2, align = 'bottom', width = 37, height = 45)

def drawSombrero(app, cx, cy):
    drawImage(app.sombreroURL, cx, cy - 20, align = 'center', width = 70, height = 90)
    
def drawMenuScreen(app):
    drawBlackBackground(app)
    drawLabel('Color Switch', app.width / 2, 70, size = 50, fill = 'pink', bold = True)
    drawPlayingAgainButton(app)
    drawGoToSkinsButton(app)
    drawLabel("Press 'G' to go to grading shortcuts", app.width / 2, app.height - 25, fill = 'white', size = 20, bold = True)
    
def drawGoToSkinsButton(app):
    length, height, left, top = returningToMenuAndSkinsRectDims(app)
    centerX, centerY = drawingMenuAndSkinsRectAndReturnCenters(app, left, top, length, height)
    drawLabel('Skins', centerX, centerY, fill = 'pink', size = 35, bold = True)
    if app.skinsButtonHighlighted:
        drawRect(left, top, length, height, fill = 'hotPink', opacity = 40)
    
def drawPlayingAgainButton(app):
    centerX, centerY, r = app.width / 2, app.height / 2, 50
    drawCircle(centerX, centerY, r, fill='grey')
    drawPolygon(centerX - 0.5 * r, centerY - 0.75 * r, centerX + 0.75 * r, centerY, centerX - 0.5 * r, centerY + 0.75 * r, fill = 'pink')
    if app.startButtonHighlighted:
        drawCircle(centerX, centerY, r, fill='hotPink', opacity = 40)

def mouseIntersectsWithRectButton(length, height, left, top, mouseX, mouseY, app):
    return ((mouseX <= left + length) and (mouseX >= left)
        and (mouseY <= top + height) and (mouseY >= top))
        
def onMouseMove(app, mouseX, mouseY):
    if app.menu or app.gameOver:
        if not app.menu:
            length, height, left, top = returningToMenuAndSkinsRectDims(app)
            if mouseIntersectsWithRectButton(length, height, left, top, mouseX, mouseY, app):
                app.menuButtonHighlighted = True
            else:
                app.menuButtonHighlighted = False
                
        else: # implying on app.menu True
            length, height, left, top = returningToMenuAndSkinsRectDims(app)
            if mouseIntersectsWithRectButton(length, height, left, top, mouseX, mouseY, app):
                app.skinsButtonHighlighted = True
            else:
                app.skinsButtonHighlighted = False
        #this logic applies on both screens        
        if distance(mouseX, mouseY, app.width / 2, app.height / 2) <= 50:
            app.startButtonHighlighted = True
        else:
            app.startButtonHighlighted = False
    
    if app.skinsMenu:
        length, height, left, top = returningToMenuAndSkinsRectDims(app)
        if mouseIntersectsWithRectButton(length, height, left, top, mouseX, mouseY, app):
            app.menuButtonHighlighted = True
        else:
            app.menuButtonHighlighted = False

def distance(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        
def onMousePress(app, mouseX, mouseY):
    if app.menu or app.gameOver:
        length, height, left, top = returningToMenuAndSkinsRectDims(app)
        if not app.menu:
            if mouseIntersectsWithRectButton(length, height, left, top, mouseX, mouseY, app):
                app.menu = True
                app.skinsMenu = False
                app.gameOver = False
        else:
            if mouseIntersectsWithRectButton(length, height, left, top, mouseX, mouseY, app):
                app.skinsMenu = True
                app.menu = False
                app.gameOver = False
            gradingLeft = left - length - 10
            if mouseIntersectsWithRectButton(length, height, gradingLeft, top, mouseX, mouseY, app):
                app.grading = True
                app.menu = False
        #this logic applies to both screens    
        if distance(mouseX, mouseY, app.width / 2, app.height / 2) <= 50:
            resetGame(app)
    elif app.skinsMenu:
        skinsMenuButtons(app, mouseX, mouseY)

def gradingButtons(app, key):
    options = ['ring', 'square', 'wrapAroundLine','plusSigns', 'skins']
    selectedShape = None
    if key == 'r':
        selectedShape = 'ring'
    elif key == 'q':
        selectedShape = 'square'
    elif key == 'l':
        selectedShape = 'wrapAroundLine'  
    elif key == 'p':
        selectedShape = 'plusSigns'
    elif key == 's': #selected shape will be None here
        app.skinsMenu = True
        app.grading = False
                
    if selectedShape != None: #starting the game
                app.grading = False
                app.starting = True
                app.gameOver = False
                app.playerY = app.height - 70
                app.scoreRecorded = False
                app.vertSpeed = 0
                app.score = 0
                app.obstacles = []
                app.gradingShape = selectedShape
                generateRandomObstacle(app, 100)

def skinsMenuButtons(app, mouseX, mouseY):
    length, height, left, top = returningToMenuAndSkinsRectDims(app)
    if mouseIntersectsWithRectButton(length, height, left, top, mouseX, mouseY, app):
        app.skinsMenu = False
        app.menu = True
        app.gameOver = False
    skinOptions = [None, 'topHat', 'crown', 'sombrero']
    numOfSkins = len(skinOptions)
    for i in range(numOfSkins):
        currSkin = skinOptions[i]
        div = app.width // (numOfSkins + 1)
        cx = div * (i + 1)
        cy = app.height / 2
        if distance(mouseX, mouseY, cx, cy) <= 35:
            app.currentSkin = currSkin
    
def drawStartingScreen(app):
    drawBlackBackground(app)
    drawPlayer(app, app.width / 2, app.playerY)
    drawLabel('Press the space bar to start', app.width / 2, app.height - 30, fill = 'white', size = 25, bold = True)
    for obs in app.obstacles:
        obs.draw(app)
    
def generateRandomObstacle(app, cy):
    offset = 0
    lenOfObs = len(app.obstacles)
    if lenOfObs != 0:
        for i in range(lenOfObs - 1, -1, -1):
            obs = app.obstacles[i]
            if obs.shape != 'checkpoint' and obs.cy >= app.height + 62:
                app.obstacles.pop(i)
            if obs.cy >= app.height * (2/3): 
                app.scoreRecorded = False
                
    if app.starting:
        obs1 = Obstacle('ring', app.width / 2, cy, None)
        obs2 = Obstacle('square', app.width / 2, cy, None)
        obs3 = Obstacle('wrapAroundLine', app.width / 2, cy, None)
        obs4 = Obstacle('plusSigns', app.width / 2, cy, None)
        offsetsList = [0 for i in range(4)]
    else:
        offset1, offset2, offset3, offset4 = 62, 35, 80, 100 #based on shape dimensions
        offsetsList = [offset1, offset2, offset3, offset4]
        obs1 = Obstacle('ring', app.width / 2, cy - offset1, None) # needs offset to start off screen
        obs2 = Obstacle('square', app.width / 2, cy - offset2, None)
        obs3 = Obstacle('wrapAroundLine', app.width / 2, cy - offset3, None)
        obs4 = Obstacle('plusSigns', app.width / 2, cy - offset4, None)
        
    obsList = [obs1, obs2, obs3, obs4]
    if app.gradingShape != None:
        if app.gradingShape == 'ring':
            index = 0
        elif app.gradingShape == 'square':
            index = 1
        elif app.gradingShape == 'wrapAroundLine':
            index = 2
        elif app.gradingShape == 'plusSigns':
            index = 3
    else:
        index = random.randrange(len(obsList))
        
    newObs = obsList[index]
    app.obstacles.append(newObs)
    generatePointStar(app, cy, offsetsList[index])

def spawnCheckPoint(app):
    checkPtObs = Obstacle('checkpoint', app.width // 2, 0, None)
    app.obstacles.append(checkPtObs)

def resetGame(app):
    app.gradingShape = None
    app.menu = False
    app.starting = True
    app.gameOver = False
    if app.score > app.bestScore:
        app.bestScore = app.score
    app.playerY = app.height - 70
    app.vertSpeed = 0
    app.score = 0
    app.scoreRecorded = False
    app.obstacles = []
    generateRandomObstacle(app, 100)

class Obstacle:
    def __init__(self, shape, cx, cy, shapeColor):
        self.shape = shape
        self.cx = cx
        self.cy = cy
        self.changingFactor = 0 #angle, horizontal displacement, etc
        self.spawnedNext = False
        self.shapeColor = shapeColor
        self.colors = ['crimson', 'mediumSpringGreen', 'mediumPurple', 'lightSkyBlue']
        self.otherPlusColors = ['mediumPurple', 'mediumSpringGreen', 'crimson', 'lightSkyBlue']
        #red and purple do not line up in normal color list order due to reversed rotation 
    
    def rotateObsAngle(self): #for rotation/horizontal shifting
        self.changingFactor += 3
    
    def draw(self, app):
        if self.shape == 'ring':
            self.drawRing()
            
        elif self.shape == 'square':
            self.drawSquare()
            
        elif self.shape == 'plusSigns':
            self.drawPlusSigns(app)
            
        elif self.shape == 'wrapAroundLine':
            self.drawWrapAroundLine(app)
            
        elif self.shape == 'checkpoint':
            self.drawCheckpoint()
        
        elif self.shape == 'pointStar':
            drawStar(app.width / 2, self.cy, 30, 5, fill = self.shapeColor,
                    opacity = 70, border = self.shapeColor, rotateAngle = self.changingFactor)

    def getRadiusEndpoint(cx, cy, r, theta):
        return (cx + r*math.cos(math.radians(theta)),
                cy - r*math.sin(math.radians(theta)))
                
    def drawRing(self):
        for i in range(4):
            startingAngle = self.changingFactor + 90 * i
            drawArc(self.cx, self.cy, 124, 124, startingAngle, 90, fill = self.colors[i], borderWidth = 15)
            drawCircle(self.cx, self.cy, 45)
    
    def drawSquare(self):
        points = []
        for i in range(4):
            theta1 = self.changingFactor + 90 * i
            theta2 = self.changingFactor + 90 * (i+1)
            #drawCircle(self.cx, self.cy, 45, fill='red', opacity = 40)
            #debugging circle to find dimensions inside the circle
            x1, y1 = Obstacle.getRadiusEndpoint(self.cx, self.cy, 70, theta1)
            x2, y2 = Obstacle.getRadiusEndpoint(self.cx, self.cy, 70, theta2)
            drawLine(x1, y1, x2, y2, fill=self.colors[i], lineWidth = 15)
    
    def drawWrapAroundLine(self, app):
        lineLength = app.width // 4
        for i in range(4):
            starting = lineLength * i
            movingStart = (starting + self.changingFactor)
            movingStartMod = movingStart % app.width
            ending = lineLength * (i+1)
            movingEnd = (ending + self.changingFactor)
            movingEndMod = movingEnd % app.width
            if movingStartMod < movingEndMod: # since we are moding them
                drawLine(movingStartMod, self.cy, movingEndMod, self.cy, fill=self.colors[i], lineWidth = 20)
            else: # overflow
                drawLine(movingStartMod, self.cy, app.width, self.cy, fill=self.colors[i], lineWidth = 20)
                drawLine(0, self.cy, movingEndMod, self.cy, fill=self.colors[i], lineWidth = 20)
    
    def drawCheckpoint(self):
        for i in range(4):
            startingAngle = 90 * i
            drawArc(self.cx, self.cy, 36, 36, startingAngle, 90, fill = self.colors[i], borderWidth = 15)
    
    def drawPlusSigns(self, app):
        lineLengths = 50
        remainingSpace = app.width - 2 * lineLengths
        left = remainingSpace / 2
        right = left + 2 * lineLengths #dividing up space evenly to they intersect at the same position
        # when they meet in the middle
        
        for i in range(4):
            thetaRight = self.changingFactor + 90 * i
            thetaLeft = -self.changingFactor + 90 * i
            xRight, yRight = Obstacle.getRadiusEndpoint(right, self.cy, lineLengths, thetaRight)
            xLeft, yLeft = Obstacle.getRadiusEndpoint(left, self.cy, lineLengths, thetaLeft)
            drawLine(xRight, yRight, right, self.cy, fill = self.colors[i], lineWidth = 15)
            drawLine(xLeft, yLeft, left, self.cy, fill = self.otherPlusColors[i], lineWidth = 15)
        
def wrapAroundLineCollision(app, obs):
    belowLine = obs.cy + app.r
    aboveLine = obs.cy - app.r
    if (belowLine >= app.playerY - app.r) and (app.playerY + app.r >= aboveLine):
        wrapAroundCollisionHelper(app, obs)

def wrapAroundCollisionHelper(app, obs):
    lineLength = app.width // 4
    matchFound = False
    for i in range(4):
        starting = lineLength * i
        movingStart = (starting + obs.changingFactor)
        movingStartMod = movingStart % app.width
        ending = lineLength * (i+1)
        movingEnd = (ending + obs.changingFactor)
        movingEndMod = movingEnd % app.width
        
        if movingStartMod <= app.width //2 <= movingEndMod:
            if obs.colors[i] == app.playerFill:
                matchFound = True
        
    if not matchFound:
        app.gameOver = True

def squareCollision(app, obs):    
    insideSquare = 50 - app.r
    outsideSquare = 70 + app.r
    if insideSquare <= distance(app.playerX, app.playerY, obs.cx, obs.cy) <= outsideSquare:
        spinningAngleCollisionHelper(app, obs)

def spinningAngleCollisionHelper(app, obs):
    # Gemini gave me a general idea on how to approach
    # the logic for this function (but not written by it)
    if app.playerY > obs.cy:
        hitAngle = 270
    else:
        hitAngle = 90
        
    matchFound = False
    for i in range(4):
        start = (obs.changingFactor + 90 * i) % 360
        end = (obs.changingFactor + 90 * (i+1)) % 360
        if start <= hitAngle <= end:
            if app.playerFill == obs.colors[i]:
                matchFound = True
    if not matchFound:
        app.gameOver = True
                
def ringCollision(app, obs):
    insideRing = 45 - app.r
    outsideRing = 62 + app.r
    if insideRing <= distance(app.playerX, app.playerY, obs.cx, obs.cy) <= outsideRing:
        spinningAngleCollisionHelper(app, obs)

def onStep(app):
    if not app.takingSteps: # app.takingSteps True for debugging purposes
        takeStep(app)
        
def spawnNewObs(app, obs):
    if not obs.shape == 'checkpoint' and not obs.shape == 'pointStar' and not obs.spawnedNext:
        spawnCheckPoint(app)
    elif obs.shape == 'checkpoint' and not obs.spawnedNext:
        generateRandomObstacle(app, 0)
    obs.spawnedNext = True

def generatePointStar(app, cy, offset):
    starObs = Obstacle('pointStar', app.width // 2, cy - offset, 'yellow')
    app.obstacles.append(starObs)

def checkForShapeCollisions(app, obs):
    if obs.shape == 'ring':
        ringCollision(app, obs)
    if obs.shape == 'square':
        squareCollision(app, obs)
    if obs.shape == 'wrapAroundLine':
        wrapAroundLineCollision(app, obs)
    if obs.shape == 'pointStar':
        pointStarCollision(app, obs)
    if obs.shape == 'plusSigns':
        plusSignsCollision(app, obs)

def plusSignsCollision(app, obs):
    #only checking right side since colliding
    #with one side gaurentees it will collide with other side
    top = obs.cy + 50
    bottom = obs.cy - 50
    if bottom <= app.playerY <= top:
        plusSignsCollisionHelper(app, obs)

def plusSignsCollisionHelper(app, obs):
    # if ball within 10 degrees of flat arms
    matchFound = False
    for i in range(4):
        armAngle = (obs.changingFactor + 90 * i) % 360
        if abs(180 - armAngle) <= 10:
            if obs.colors[i] != app.playerFill:
                app.gameOver = True

def pointStarCollision(app, obs):
    bottom = obs.cy + 15 + app.r
    top = obs.cy - 15 - app.r
    if top <= app.playerY <= bottom and not app.scoreRecorded:
        app.score += 1
        obs.shapeColor = 'darkGray'
        app.scoreRecorded = True
  
def takeStep(app):
    if not app.menu and not app.gameOver and not app.starting:
        for obs in app.obstacles:
            obs.rotateObsAngle()
            if obs.cy >= (2/5) * app.height and obs.shape != 'pointStar':
                spawnNewObs(app, obs)
            if obs.shape == 'checkpoint':
                assignRandomColorToPlayer(app, obs)
            else:
                checkForShapeCollisions(app, obs)
                
        if not app.takingSteps:
            app.vertSpeed += app.vertAcceleration
        app.playerY += app.vertSpeed
        
    if outOfBounds(app):
        app.gameOver = True
        
    if needToShift(app):
        shiftGameUp(app)

def outOfBounds(app):
    return app.playerY + app.r >= app.height

def needToShift(app):
    return app.playerY <= app.height / 2

def shiftGameUp(app):
    app.playerY += app.vertSpeed
    shift = app.height / 2 - app.playerY
    for obs in app.obstacles:
        obs.cy += shift / 2
    app.playerY = app.height / 2

def assignRandomColorToPlayer(app, obs):
    if distance(app.playerX, app.playerY, obs.cx, obs.cy) <= 18:
        originalColor = app.playerFillIndex
        newColor = originalColor
        while newColor == originalColor:
            newColor = random.randrange(len(app.colors))
        app.playerFillIndex = newColor
        app.playerFill = app.colors[app.playerFillIndex]
        if obs in app.obstacles:
            app.obstacles.remove(obs)
        app.checkPointSpawned = False

def onKeyPress(app, key):
    key = key.lower()
    if key == 'space':
        if app.starting:
            app.starting = False
            app.gameOver = False
            app.playerY = app.height - 70
            app.vertSpeed = -10.5
        elif app.gameOver:
            resetGame(app)
        else:
            app.vertSpeed = -10.5
    # for debugging purposes
    # if key == 'b':
    #     takeStep(app)
    # if key == 't':
    #     app.takingSteps = not app.takingSteps
    elif key == 'g':
        app.grading = True
        app.menu = False
        app.gameOver = False
        app.starting = False
    elif key == 'm':
        app.grading = False
        app.menu = True
    elif app.grading:
        gradingButtons(app, key)
        
def drawGame(app):
    drawBlackBackground(app)
    for obs in app.obstacles:
        obs.draw(app)
    drawLabel(app.score, app.width - 30, 30, fill = 'pink', size = 25, bold = True)
    drawPlayer(app, app.width / 2, app.playerY)

def drawPlayer(app, cx, cy):
    drawCircle(cx, cy, app.r, fill = app.playerFill)
    if app.currentSkin == 'topHat':
        drawTopHat(app, cx, cy)
    elif app.currentSkin == 'sombrero':
        drawSombrero(app, cx, cy)
    elif app.currentSkin == 'crown':
        drawCrown(app, cx, cy)

def drawGameOver(app):
    drawBlackBackground(app)
    drawPlayingAgainButton(app)
    if app.score > app.bestScore:
        drawLabel(f'New Personal Record!!', app.width / 2, 40, size = 26, fill = 'pink', bold = True)
        drawLabel(f'Your Score Was {app.score}', app.width / 2, 90, size = 26, fill = 'pink', bold = True)
    else:
        drawLabel(f'Your Score Was: {app.score}', app.width / 2, 40, size = 26, fill = 'pink', bold = True)
        drawLabel(f'Best Score: {app.bestScore}', app.width / 2, 90, size = 26, fill = 'pink', bold = True)
    drawGoBackToMenu(app)
    drawLabel("Press 'g' to go to grading shortcuts", app.width / 2, app.height - 25, fill = 'white', size = 20, bold = True)

def drawGoBackToMenu(app):
    length, height, left, top = returningToMenuAndSkinsRectDims(app)
    centerX, centerY = drawingMenuAndSkinsRectAndReturnCenters(app, left, top, length, height)
    drawLabel('Return to', centerX, centerY - 15, fill = 'pink', size = 25, bold = True)
    drawLabel('Main Menu', centerX, centerY + 15, fill = 'pink', size = 25, bold = True)
    if app.menuButtonHighlighted:
        drawRect(left, top, length, height, fill = 'hotPink', opacity = 40)

def returningToMenuAndSkinsRectDims(app):
    length = 150
    height = 75
    left = app.width - length - 25
    top = app.height - height - 50
    return length, height, left, top

def drawingMenuAndSkinsRectAndReturnCenters(app, left, top, length, height):
    drawRect(left, top, length, height, fill = 'grey')
    centerX = left + length // 2
    centerY = top + height // 2
    return centerX, centerY
    
def main():
    runApp()

main()

