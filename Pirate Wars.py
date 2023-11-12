from cmu_graphics import *

# Pirate Wars:

# Developers: Kush Patel, Joel Weber and Eric Kloostra
# Date: May 30,2022
# Course: ICS4U
# Purpose: To create a game where two users control their ships and try to
#          knock down their opponent and collect their coins

# *Use key 'g' to skip through stages*

# Note (Nov 12, 2023): When moving file to Github, controls stopped working. Users were able to control ships perfectly fine in CMU's sandbox.
    
# app.background = rgb(0,0,255)
import math
app.ships = []
app.background = gradient('deepSkyBlue','dodgerBlue','deepSkyBlue',start='top')
app.steps = 0

#***************************** GAME STATE *******************************

# Class that manages the how the game runs. It act as as the terminal to control all the other classes.
class GameState(object):
    #Set variables to the way that the game will start
    def __init__(self):
        self.mode = 'MENU'
        self.stage = -2
        self.pirate_music1 = Sound('https://audio-previews.elements.envatousercontent.com/files/299425627/preview.mp3?response-content-disposition=attachment%3B+filename%3D%22BQPA6ZN-pirates.mp3%22')
        self.pirate_music2 = Sound('https://audio-previews.elements.envatousercontent.com/files/311786163/preview.mp3?response-content-disposition=attachment%3B+filename%3D%228J852HD-pirates.mp3%22')
        self.cannon_sound = Sound('https://audio-previews.elements.envatousercontent.com/files/175653570/preview.mp3?response-content-disposition=attachment%3B+filename%3D%22WQN3B5E-cannon-tower-attack.mp3%22')
        self.here_there_be_pirates = Sound('https://audio-previews.elements.envatousercontent.com/files/294114887/preview.mp3?response-content-disposition=attachment%3B+filename%3D%22PQ8R9BU-pirate-dialogue-here-there-be-pirates.mp3%22')
        self.stageDrawing = Group()
        self.trees = Group()
        self.drawStartScreen()
        self.onStartSelect = True
        self.onCreditsSelect = False
        self.drawControls()
        self.drawCredits()
        self.controlDisplay.visible = False
        self.creditsDisplay.visible = False
        self.steps = 0
        self.stageCoins = 3
        self.droppedCoins = []

        
    #Moves on to the actual game(stage 1) and creates ships/players
    def startGame(self):
        self.startScreen.visible = False
        self.controlDisplay.visible = False
        self.creditsDisplay.visible = False
        self.mode = 'PLAYING STAGE'
        self.stage = 1
        ship1 = Ship(1,300,300)
        ship2 = Ship(2,100,300)
        app.ships.append(ship1)
        app.ships.append(ship2)
        self.goldCount()
        self.drawStage(self.stage)
    
    #Changes mode and displays credits which leads to the gam
    def displayCredits(self):
        self.startScreen.visible = False
        self.mode = 'VIEWING CREDITS'
        self.stage = -2
        self.creditsDisplay.visible = True
        self.controlDisplay.visible = False
        
    #Displays controls which leads to the game
    def displayControls(self):
        self.startScreen.visible = False
        self.mode = 'VIEWING CONTROLS'
        self.stage = -1
        self.controlDisplay.visible = True
        self.creditsDisplay.visible = False
        self.here_there_be_pirates.play()

    #Gets the next stage number, draws its respective screen, and updates mode
    def nextStage(self):
        if self.mode != 'GAME COMPLETE':
            self.stage += 1
            self.drawStage(self.stage)
        if self.stage == -1:
            self.mode = 'VIEWING CONTROLS'
        elif self.stage > 0:
            self.mode = 'PLAYING STAGE'
        elif self.stage == 4:
            self.mode = 'GAME COMPLETE'
        app.ships[0].coinCount = self.stageCoins
        app.ships[1].coinCount = self.stageCoins
        self.p2coinNum.value = self.stageCoins
        self.p1coinNum.value = self.stageCoins
      
    #Handles bg music
    def music(self):
        if self.mode == 'MENU':
            self.pirate_music1.play()
        if self.mode != 'MENU':
            self.pirate_music1.pause()
        if self.mode == 'PLAYING STAGE':
            self.pirate_music2.play()
    
    #Moves ships to location in paramaters
    def resetShips(self,coordList):
        count = 0
        for ship in app.ships:
            ship.spawnX = coordList[count][0]
            ship.spawnY = coordList[count][1]
            ship.spawnAng = coordList[count][2]
            ship.coinCount = self.stageCoins
            ship.respawn()
            count += 1

    #*************************** HANDLE/INPUT FUNCTIONS ****************************

    #Allows user to choose between start and credits option
    def menuSelect(self,key):
        if key == 'up':
            self.onStartSelect = True
            self.onCreditsSelect = False
        if key == 'down':
            self.onCreditsSelect = True
            self.onStartSelect = False
        if key == 'enter':
            if self.onStartSelect:
                self.displayControls()
            elif self.onCreditsSelect:
                self.displayCredits()
            self.onStartSelect = False
            self.onCreditsSelect = False
    
    #Allows user to navigate through controls or credits page
    def pageSwitch(self,key):
        if key == 'space':
            self.startGame()
            self.controlDisplay.visible = False
        if key == 'backspace':
            self.mode = 'MENU'
            self.drawStartScreen()
            self.steps = 0
            self.onStartSelect = True
    
    # Controls animations, music, coins, and win count
    def handleOnStep(self):
        self.animatePrompt()
        if self.onStartSelect == True:
            self.animateStartSelect()
        if self.onCreditsSelect == True:
            self.animateCreditsSelect()
        self.steps += 1
        self.music()
        if len(app.ships) != 0:
            if app.ships[0].coinCount == self.stageCoins*2:
                self.nextStage()
                app.ships[0].wins += 1
                print(app.ships[0].wins)            
            elif app.ships[1].coinCount == self.stageCoins*2:
                self.nextStage()
                app.ships[1].wins += 1
        if self.stage == 3:
            game.kraken1.handleOnStep()
            game.kraken2.handleOnStep()
            game.kraken3.handleOnStep()
    
    
    def handleKeyInput(self,key):
        if self.mode == 'MENU':
            self.menuSelect(key)
        if self.mode == 'VIEWING CONTROLS' or self.mode == 'VIEWING CREDITS':
            self.pageSwitch(key)

    #****************************** DRAWING FUNCTIONS ******************************
    #Draws the credits screen
    def drawCredits(self):
        self.creditsDisplay = Group(
            Image('https://as2.ftcdn.net/v2/jpg/02/31/49/37/1000_F_231493739_o25eZhn8MMZPUGt08zLSw2lAMd3DBFXq.jpg',-200,-60),
            Label('PIRATE WARS CREATED BY...',200,80,size=24,font='monospace',bold=True),
            Label('Joel Weber',200,140,size=26,font='cinzel'),
            Label('Kush Patel',200,220,size=26,font='cinzel'),
            Label('Eric Kloostra',200,300,size=26,font='cinzel'),
            Label('press SPACE',340,378,fill='snow'),
            Label('to start game',340,390,fill='snow'),
            Label('press BACKSPACE',65,378,fill='snow'),
            Label('to return to menu',60,390,fill='snow')
            )

    #Draws the controls screen
    def drawControls(self):
        self.controlDisplay = Group(
            #Background image
            Image('https://media.istockphoto.com/photos/pirates-map-background-picture-id539349004?k=20&m=539349004&s=612x612&w=0&h=DzFMSzxL_WlRB7hYHZ4bT3_JNhdhA2AWsQTmE_mPxHI=',0,0),
            
            #Labels giving directions
            Label('ARR ME MATIES!',200,50,size=25,bold=True,font='cinzel'),
            Label('A BATTLE HAS ARISEN!',200,100,size=15),
            Label('YOU MUST GET THE MOST GOLD',200,125,size=15),
            Label('BY ANY MEANS POSSIBLE!',200,145,size=15),
            
            #Tells the players how to move and shoot
            Label('Player 1',100,180,size=12),
            Label('Use the WASD keys to move,',100,200,size=12),
            Label('V to shoot',100,220,size=12),
            Label('Player 2',300,180,size=12),
            Label('Use the arrow keys to move,',300,200,size=12),
            Label('/ to shoot',300,220,size=12),
            
            #Makes keys for showing how to move
            Rect(80,242,40,40,fill=gradient('dimGray','lightGray','snow',start='bottom-left'),border='black'),
            Rect(42,280,40,40,fill=gradient('dimGray','lightGray','snow',start='bottom-left'),border='black'),
            Rect(80,280,40,40,fill=gradient('dimGray','lightGray','snow',start='bottom-left'),border='black'),
            Rect(118,280,40,40,fill=gradient('dimGray','lightGray','snow',start='bottom-left'),border='black'),
            Rect(80,325,40,40,fill=gradient('dimGray','lightGray','snow',start='bottom-left'),border='black'),
            Rect(280,242,40,40,fill=gradient('dimGray','lightGray','snow',start='bottom-left'),border='black'),
            Rect(242,280,40,40,fill=gradient('dimGray','lightGray','snow',start='bottom-left'),border='black'),
            Rect(280,280,40,40,fill=gradient('dimGray','lightGray','snow',start='bottom-left'),border='black'),
            Rect(318,280,40,40,fill=gradient('dimGray','lightGray','snow',start='bottom-left'),border='black'),
            Rect(280,325,40,40,fill=gradient('dimGray','lightGray','snow',start='bottom-left'),border='black'),
            Label('W',100,262,size=15),
            Label('A',62,300,size=15),
            Label('S',100,300,size=15),
            Label('D',138,300,size=15),
            Label('V',100,345,size=15),
            Label('^',300,265,size=17),
            Label('<',262,300,size=15),
            Label('v',300,300,size=15),
            Label('>',338,300,size=15),
            Label('/',300,345,size=15),
            
            #Tells the player how to navigate through to the game and back to the menu
            Label('press SPACE',340,378),
            Label('to continue',340,390),
            Label('press BACKSPACE',65,378),
            Label('to return',60,390)
            )

    #Draws the starting menu
    def drawStartScreen(self):
        self.startScreen = Group(
            Image('https://www.twoanimators.com/2A_Blog/images/Colgate_Pirate_Ship/2A_ShipPaint_Colgate_LG.jpg',-280,-100),
            Label('PIRATE WARS', 150, 40, fill='black', font = 'cinzel', size=38, bold=True),
            Label('START', 20, 90, fill='white', font = 'orbitron', align = 'left', size=24, bold=True),
            Label('CREDITS', 20, 120, fill='white', font = 'orbitron', align = 'left', size=24, bold=True),
            Label('Press ENTER to Continue',20,150,font='orbitron',align = 'left', size=10)
        )
        
        #Draws triangles that blink beside "START"
        self.startSelector = Group(
            RegularPolygon(self.startScreen.children[2].left-10,90,5,3,rotateAngle=90),
            RegularPolygon(self.startScreen.children[2].right+10,90,5,3,rotateAngle=270)
            )
        self.startScreen.add(self.startSelector)
        self.startSelector.visible = False
        
        #Draws triangles that blink beside "CREDITS"
        self.creditsSelector = Group(
            RegularPolygon(self.startScreen.children[3].left-10,120,5,3,rotateAngle=90),
            RegularPolygon(self.startScreen.children[3].right+10,120,5,3,rotateAngle=270))
        self.startScreen.add(self.creditsSelector)
        self.creditsSelector.visible = False
        
        #Label that says "Press enter to continue"
        self.prompt = self.startScreen.children[4]

    #Blinks triangles beside "START"
    def animateStartSelect(self):
        self.creditsSelector.visible = False
        if self.steps < 15:
            self.startSelector.visible = True
        if self.steps > 15:
            self.startSelector.visible = False
        if self.steps > 30:
            self.steps = 0
    
    #Blinks triangles beside "CREDITS"
    def animateCreditsSelect(self):
        self.startSelector.visible = False
        if self.steps < 15:
            self.creditsSelector.visible = True
        if self.steps > 15:
            self.creditsSelector.visible = False
        if self.steps > 30:
            self.steps = 0
            
    #Draws attention to the continue prompt
    def animatePrompt(self):
        if self.steps <= 15:
            self.prompt.centerY -= 0.1
        elif self.steps <= 30:
            self.prompt.centerY += 0.1
        elif self.steps > 30:
            self.steps = 0

    #Draws borders that can be hit tested with the ships
    def drawBoundaries(self):
        self.stageDrawing.add(
            Line(0,0,400,0),
            Line(400,0,400,400),
            Line(400,400,0,400),
            Line(0,400,0,0)
            )
    
    #Draws gold count and its icon for both players
    def goldCount(self):
        self.p2coin = Group(
            Oval(40,33,20,10,fill='goldenRod',border='black',borderWidth=1.5),
            Oval(40,30,20,10,fill='gold',border='black',borderWidth=1.5),
            Oval(38,27,20,10,fill='goldenRod',border='black',borderWidth=1.5),
            Oval(38,24,20,10,fill='gold',border='black',borderWidth=1.5),
            Oval(40,21,20,10,fill='goldenRod',border='black',borderWidth=1.5),
            Oval(40,18,20,10,fill='gold',border='black',borderWidth=1.5),
            Rect(5,18,20,15,fill = gradient(app.ships[1].colorScheme[2][0],app.ships[1].colorScheme[2][1],app.ships[1].colorScheme[2][0],start = 'left'),border='black')
            )
        self.p1coin = Group(
            Oval(360,33,20,10,fill='goldenRod',border='black',borderWidth=1.5),
            Oval(360,30,20,10,fill='gold',border='black',borderWidth=1.5),
            Oval(362,27,20,10,fill='goldenRod',border='black',borderWidth=1.5),
            Oval(362,24,20,10,fill='gold',border='black',borderWidth=1.5),
            Oval(360,21,20,10,fill='goldenRod',border='black',borderWidth=1.5),
            Oval(360,18,20,10,fill='gold',border='black',borderWidth=1.5),
            Rect(375,18,20,15,fill = gradient(app.ships[0].colorScheme[1][0],app.ships[0].colorScheme[1][1],app.ships[0].colorScheme[1][0],start = 'left'),border='black')
            )
        self.p2coinNum = Label(self.stageCoins,60,25,size=18)
        self.p1coinNum = Label(self.stageCoins,340,25,size=20)
        self.adjustGoldVisibility(False)
    
    #Makes gold counter either visible or invisible
    def adjustGoldVisibility(self,visible):
        self.p1coinNum.visible = visible
        self.p2coinNum.visible = visible
        self.p1coin.visible = visible
        self.p2coin.visible = visible
    
    #Draws the first stage
    def drawStage1(self):
        self.stageDrawing.add(
            Rect(180,238,40,164,fill='peru',border='saddleBrown'),
            Rect(120,200,160,40,fill='peru',border='saddleBrown'),
            Label('Shoot the ship and collect the loot',200,25,size=13,font='orbitron')
            )
        for dockY in range(200,240,10):
            self.stageDrawing.add(Line(120,dockY,280,dockY,fill='saddleBrown',lineWidth=1))
        for dockY2 in range(240,400,10):
            self.stageDrawing.add(Line(180,dockY2,220,dockY2,fill='saddleBrown',lineWidth=1))
        self.stageCoins = 3
    
    #Draws the second stage
    def drawStage2(self):
        # Makes a list that stores the island coordinates
        islandCoords = [[130,150],[270,300]]
        # Has 2 values that get randomly selected to determine the direction from the center that the trees get placed in
        posCoeff = [-1,1]
        # Generates 2 islands
        for islands in range(2):
            # Sets the coordinates to a smaller variable for better readability
            x = islandCoords[islands][0]
            y = islandCoords[islands][1]
            # The length that the tree trunk will cover
            segNum = randrange(50,75)
            self.stageDrawing.add(
                Oval(x,y,140,50,fill = 'tan'),
                Label('Use the islands for cover mate!',200,25,size=13,font='orbitron')
                )
            # Creates the 2-4 trees on each island
            for trees in range(randrange(2,5)):
                # Set the start x and y positions for each segment of the tree trunk
                xS = (x)+((13*trees)*posCoeff[randrange(0,2)])
                yS = y + randrange(-10,11)
                # Creates 5 - 7 segments for the palm tree trunk
                for segs in range(0,segNum,10):
                    xS += randrange(-2,3)
                    self.trees.add(Polygon(xS,yS-segs,xS+20,yS-segs,xS+15,yS-(segs+10),xS+5,yS-(segs+10),fill = gradient('sienna','saddleBrown')))
                    # Identify the final segment coordinates on which the tree leaves can be drawn
                    if segs+10 >= segNum:
                        lX = xS+10
                        lY = yS-(segs+5)
                # Draw the tree leaves
                for leaves in range(randrange(4,7)):
                    self.trees.add(Star(lX,lY,randrange(20,45),randrange(4,7),fill = gradient('oliveDrab','limeGreen')))
            self.trees.toFront()
        self.stageCoins = 4    
    
    #Draws the third atage
    def drawStage3(self):
        game.steps = 0
        self.kraken1 = Kraken(120,120)
        self.kraken2 = Kraken(280,180)
        self.kraken3 = Kraken(200,320)
        self.stageDrawing.add(
            Label('Beware the KRAKENS, or else...',200,25,size=12,font='orbitron'),
            self.kraken1.drawing,
            self.kraken2.drawing,
            self.kraken3.drawing
            )
        self.stageCoins = 5    

    #Draws the game end screen and displays winner
    def drawGameEnd(self):
        
        self.adjustGoldVisibility(False)

        
        for ship in app.ships:
            ship.drawing.visible=False
        
        bg = Image('https://yppedia.puzzlepirates.com/images/c/c3/Portrait_expansive_cove.png',-75,0)
        bg.width = 475
        bg.height = 400
        
        pirate = Image('https://piratewins.io/images/standingpirate.png',-60,125)
        pirate.width = 450
        pirate.height = 275
        
        if app.ships[0].wins > app.ships[1].wins:
            c1,c2 = app.ships[0].colorScheme[1]
            winInd = Label("Player 1 Wins!",200,45,size=20,font='cinzel',bold=True,fill=c1)
        else:
            c1,c2 = app.ships[1].colorScheme[2]
            winInd = Label("Player 2 Wins!",200,45,size=20,font='cinzel',bold=True,fill=c1)
        self.stageDrawing.add(
            bg,
            pirate,
            winInd,
            Label("Congrats sailor, you made off with all the other ship's treasure",200,85,size=10,font='cinzel',bold=True),
            Line(140,68,195,68),
            Label('X',200,68,size=12,bold=True),
            Line(205,68,260,68)
            )
        
    #Changes the screen to match the new stage
    def drawStage(self,stageNum):
        self.stageDrawing.clear()
        self.trees.clear()
        self.drawBoundaries()
            
        if stageNum == 1:
            print('Stage 1')
            shipCoords = [[320,320,0],[80,320,0]]
            self.resetShips(shipCoords)
            self.drawStage1()
            self.adjustGoldVisibility(True)
            
        elif stageNum == 2:
            print('Stage 2')
            shipCoords = [[375,300,0],[25,100,180]]
            self.resetShips(shipCoords)
            self.drawStage2()
            self.adjustGoldVisibility(True)
            
        elif stageNum == 3:
            print('Stage 3')
            shipCoords = [[320,320,0],[80,320,0]]
            self.resetShips(shipCoords)
            self.drawStage3()
            self.adjustGoldVisibility(True)
        
        elif stageNum == 4:
            print('Game End')
            self.drawGameEnd()
            for ships in app.ships:
                ships.bars.clear()
        
        else:
            print('Invalid Stage Code')

# Generic ship objects that have identical mechanics and only different asetics and key inputs
class Ship(object):
    
    #The intialization function uses the parameter playerNum to identify the ship, and cx and cy for ship placement and controls.
    def __init__(self,playerNum,cx,cy):
        # Set the cx and cy to the default respawn point
        self.spawnX = cx
        self.spawnY = cy
        self.spawnAng = 0
        self.draw(playerNum,cx,cy)
        self.getControls(playerNum,1)
        self.shipBullets = []
        self.otherShip = None
        self.frictionCoeff = 0.15
        self.momentum = 0
        self.playerNum = playerNum
        self.ammo = 3
        self.ammoMax = 3
        self.steps = 0
        self.coinCount = 3
        self.abandonShip = Sound('https://audio-previews.elements.envatousercontent.com/files/203774877/preview.mp3?response-content-disposition=attachment%3B+filename%3D%224JF2KR9-cartoon-pirate-voice-pack.mp3%22')
        self.asCounter = 1
        self.asAudio = 2
        self.invincible = False
        self.wins = 0
    
    #Retrieves the controls for the corresponding ship
    def getControls(self,playerNum,sF):
        if (playerNum == 1):
            self.ctrls = {
                'up': [2*sF,'move'],
                'down': [-2*sF,'move'],
                'left': [-7*sF,'rotate'],
                'right': [7*sF,'rotate'],
                '/': [10,'shoot']
            }
        else: 
            self.ctrls = {
                'w': [2*sF,'move'],
                's': [-2*sF,'move'],
                'a': [-7*sF,'rotate'],
                'd': [7*sF,'rotate'],
                'v': [10,'shoot']
            }
        
    #Gives colours for the ship sail
    def getColors(self):
        self.colorScheme = {
            1 : ['red','black'],
            2 : ['orange','whiteSmoke']
        }
    
    #Draws the ships
    def draw(self,playerNum,cx,cy):
        #Gets colors for ship depending on player
        self.getColors()
        c1,c2 = self.colorScheme[playerNum]
        
        sD=2.5
        self.drawing = Group(
            Polygon(66/sD,134/sD,57/sD,56/sD,80/sD,23/sD,103/sD,56/sD,94/sD,134/sD,fill='saddleBrown'),
            Polygon(68/sD,132/sD,59/sD,56/sD,80/sD,25/sD,101/sD,56/sD,92/sD,132/sD,fill='sandyBrown'),
            Polygon(72/sD,128/sD,64/sD,56/sD,80/sD,32/sD,96/sD,56/sD,88/sD,128/sD,fill='saddleBrown'),
            Polygon(74/sD,126/sD,66/sD,56/sD,80/sD,34/sD,94/sD,56/sD,86/sD,126/sD,fill='chocolate'),
            Rect(75/sD,110/sD,10/sD,5/sD,fill='saddleBrown'),
            
            #BIG SAIL
            Arc(80/sD,80/sD,80/sD,32/sD,270,180,fill=c1),
            
            Arc(60/sD,80/sD,38/sD,25/sD,306,36,fill=c2),
            Polygon(53/sD,80/sD,60/sD,80/sD,54/sD,69/sD,45/sD,73/sD,fill=c2),
            
            Arc(100/sD,80/sD,38/sD,25/sD,18,36,fill=c2),
            Polygon(107/sD,80/sD,100/sD,80/sD,106/sD,69/sD,115/sD,73/sD,fill=c2),
            
            Arc(75/sD,80/sD,55/sD,32/sD,332,22,fill=c2),
            Polygon(77/sD,80/sD,68/sD,80/sD,62/sD,66/sD,72/sD,64/sD,fill=c2),
            
            Arc(85/sD,80/sD,55/sD,32/sD,4,22,fill=c2),
            Polygon(83/sD,80/sD,92/sD,80/sD,97/sD,66/sD,87/sD,64/sD,fill=c2),
            
            Rect(40/sD,80/sD,80/sD,4/sD,fill='saddleBrown'),
            
            Line(77/sD,110/sD,44/sD,84/sD,fill='white'),
            Line(77/sD,110/sD,54/sD,84/sD,fill='white'),
            Line(83/sD,110/sD,116/sD,84/sD,fill='white'),
            Line(83/sD,110/sD,106/sD,84/sD,fill='white'),
            Line(44/sD,84/sD,44/sD,80/sD,fill='white',lineWidth=2),
            Line(54/sD,84/sD,54/sD,80/sD,fill='white',lineWidth=2),
            Line(116/sD,84/sD,116/sD,80/sD,fill='white',lineWidth=2),
            Line(106/sD,84/sD,106/sD,80/sD,fill='white',lineWidth=2),
            Line(77/sD,110/sD,77/sD,115/sD,fill='white',lineWidth= 2),
            Line(83/sD,110/sD,83/sD,115/sD,fill='white',lineWidth= 2),
            
            #Cannon
            Arc(80/sD,40/sD,8/sD,6/sD,90,180),
            Polygon(76/sD,40/sD,84/sD,40/sD,82/sD,30/sD,78/sD,30/sD),
            Polygon(82/sD,30/sD,78/sD,30/sD,76/sD,28/sD,84/sD,28/sD)
            )
            
        self.drawing.centerX = cx
        self.drawing.centerY = cy
        
        self.bar(sD)
    
    #Draws the bars that show player amunition    
    def bar(self,sD):    
        self.bars = Group(
            Rect(self.drawing.centerX-40/sD,self.drawing.centerY-150/sD,20/sD,10/sD),
            Rect(self.drawing.centerX-10/sD,self.drawing.centerY-150/sD,20/sD,10/sD),
            Rect(self.drawing.centerX+20/sD,self.drawing.centerY-150/sD,20/sD,10/sD),  
            )
    
    #Calculates vectors for ship movement
    def getMotionVectors(self,vel,angle):
        self.dy = vel*math.cos((angle*math.pi)/180)
        self.dx = vel*math.sin((angle*math.pi)/180)
        self.move()
    
    #Moves the ship
    def move(self):
        try:
            self.drawing.centerX += self.dx
            self.bars.centerX += self.dx
            self.drawing.centerY -= self.dy
            self.bars.centerY -= self.dy
            self.bounced = False
            assertEqual(self.drawing.hitsShape(game.stageDrawing),False)
        except:
            self.bounce()
        if self.drawing.hitsShape(self.otherShip.drawing) == True:
            if self.bounced == False:
                self.checkShipCollision('move')
            else:
                self.bounce()
    
    #Causes the ship to bounce when there is a collision with the wall
    def bounce(self):
        self.drawing.centerX -= self.dx
        self.drawing.centerY += self.dy
        self.bars.centerX -= self.dx
        self.bars.centerY += self.dy
        self.momentum *= -0.75
        self.bounced = True
    
    #Check if a bullet hits the ship
    def checkHits(self):
        for buls in self.shipBullets:
            if buls.drawing.hitsShape(self.otherShip.drawing) == True and self.otherShip.invincible == False:
                buls.removeBullet()
                self.fallenCoin()
                self.otherShip.respawn()
                self.abandonShip.play(restart=True)
                self.asAudio = 1
      
    #Check if there is a collision with another ship and causes them to bounce
    def checkShipCollision(self,function):
        if self.otherShip.momentum > 0.5: 
            oX,oY = getPointInDir(self.otherShip.drawing.centerX,self.otherShip.drawing.centerY,self.otherShip.drawing.rotateAngle,17)
        elif self.otherShip.momentum < -0.5: 
            oX,oY = getPointInDir(self.otherShip.drawing.centerX,self.otherShip.drawing.centerY,self.otherShip.drawing.rotateAngle+180,17)
        else: 
            return
        if self.drawing.hits(oX,oY) == True and (self.otherShip.momentum > 0.5 or self.otherShip.momentum < -0.5) and function == 'move':
            dx = self.dx
            dy = self.dy
            Odx = self.otherShip.dx
            Ody = self.otherShip.dy
            self.getMotionVectors(self.otherShip.momentum,self.otherShip.drawing.rotateAngle)
            self.dx += dx
            self.dy += dy
            self.otherShip.getMotionVectors(-1*self.otherShip.momentum,self.otherShip.drawing.rotateAngle)
            self.otherShip.dx += Odx
            self.otherShip.dy += Ody
        elif self.drawing.hits(oX,oY) == True and function == 'move': 
            self.otherShip.momentum = 0
    
    #Draws coin on the ground where a player was shot
    def fallenCoin(self):
        self.otherShip.coinCount -=1
        groundCoins = Group(
            Oval(self.otherShip.drawing.centerX,self.otherShip.drawing.centerY,12,16,fill=gradient(rgb(240,140,0),'yellow',rgb(240,140,0),start='top'),border='black',borderWidth=1),
            Label('$',self.otherShip.drawing.centerX,self.otherShip.drawing.centerY,size=10)
            )
        game.droppedCoins.append(groundCoins)
        if self.playerNum == 1:
            game.p2coinNum.value = self.otherShip.coinCount
        else:
            game.p1coinNum.value = self.otherShip.coinCount
    
    #Checks if the ship touches a coin and adjusts coin count accordingly
    def checkPickUpCoins(self):
        for cns in game.droppedCoins:
            if self.drawing.hitsShape(cns) == True:
                self.coinCount += 1
                if self.playerNum == 1:
                    game.p1coinNum.value = self.coinCount
                else:
                    game.p2coinNum.value = self.coinCount
                game.droppedCoins.remove(cns)
                cns.clear()
        
    #Turns the ship
    def turn(self):
        try:
            self.drawing.rotateAngle += self.dAngle
            assertEqual(self.drawing.hitsShape(game.stageDrawing),False)
        except:
            self.drawing.rotateAngle -= 1.5*self.dAngle
        self.checkShipCollision('turn') 
    
    #Processes the keys that are inputed
    def handleKeyInput(self,key,pressed):
        self.command = self.ctrls[key]
        if 'move' in self.command[1] and pressed == False:
            self.vel = self.command[0]
            if self.vel != 0:
                self.momentum = self.vel
                self.getMotionVectors(self.vel,self.drawing.rotateAngle)
        if 'rotate' in self.command[1] and pressed == False:
            self.dAngle = self.command[0]
            self.turn()
        if 'shoot' in self.command[1] and self.ammo > 0 and pressed == True:
            self.shoot()
    
    #Shoots the cannon on the ship
    def shoot(self):
        bombProb = randrange(0,5)
        bulletX,bulletY = getPointInDir(self.drawing.centerX,self.drawing.centerY,self.drawing.rotateAngle,15)
        if bombProb == 0:
            shot = Bomb(bulletX,bulletY,self.drawing.rotateAngle,self.command[0])
        else:
            shot = Bullets(bulletX,bulletY,self.drawing.rotateAngle,self.command[0])
        self.shipBullets.append(shot)
        self.ammo -=1
        self.steps = 0
        game.cannon_sound.pause()
        game.cannon_sound.play(restart=True)
    
    #Reloads the amunition on the ship after a number of steps
    def reloadAmmo(self):
        if self.ammo < self.ammoMax and self.steps%30 == 0:
            self.ammo += 1
            self.steps = 0
    
    #Calculates momentum of the ship
    def momentumMotion(self):
        if self.momentum > 0.25:
            self.momentum -= self.frictionCoeff
        elif self.momentum < -0.25:
            self.momentum += self.frictionCoeff
        else:
            self.momentum = 0
        self.getMotionVectors(self.momentum,self.drawing.rotateAngle)
    
    #Used to control other ships functions and variables
    def identifyOtherShip(self):
        for ship in app.ships:
            if self != ship:
                self.otherShip = ship
    
    #Shows how much ammo is left
    def adjustAmmo(self):
        barNum = 0
        for bars in self.bars:
            barNum += 1
            if (self.ammo == 2 and barNum > 2) or (self.ammo == 1 and barNum > 1) or (self.ammo == 0 and barNum > 0):
                bars.opacity = 25
            else:
                bars.opacity = 75
    
    #Respawns the ship
    def respawn(self):
        self.drawing.centerX = self.spawnX
        self.bars.centerX = self.spawnX
        self.drawing.centerY = self.spawnY
        self.bars.centerY = self.spawnY-40
        self.drawing.rotateAngle = self.spawnAng
        self.invincible = True
        self.drawing.opacity = 40
    
    #Makes the ship temporarily invinsible for a set period of time after respawning
    def adjInvinsibility(self):
        self.drawing.opacity += 1
        if self.drawing.opacity == 100:
            self.invincible = False
    
    #Runs functions that need to occur every step
    def handleOnStep(self):
        if self.otherShip == None:
            self.identifyOtherShip()
        self.momentumMotion()
        self.steps += 1
        self.reloadAmmo()
        self.adjustAmmo()
        if self.asAudio == 1:
            self.asCounter += 1
        if self.asCounter % 40 == 0:
            self.abandonShip.pause()
            self.asAudio = 2
        if self.drawing.opacity < 100:
            self.adjInvinsibility()
        self.checkPickUpCoins()

# Class that draws bullet and has the methods for moving clearing. 
class Bullets(object):
    # Defines the bullet variables with the parameters that it is called with 
    def __init__(self,bcx,bcy,bDir,vel):
        self.draw(bcx,bcy)
        self.vel = vel
        self.bDir = bDir
        self.steps = 0
        self.exploStep = None
        self.move()
        
    # Makes a cannon ball
    def draw(self,bcx,bcy):
        self.drawing = Group(Circle(bcx,bcy,3,fill=rgb(20,20,20)))

    #Moves/shoots the bullets
    def move(self):
        if self.drawing.hitsShape(game.stageDrawing) == False:
            dy = self.vel*math.cos((self.bDir*math.pi)/180)
            dx = self.vel*math.sin((self.bDir*math.pi)/180)
            self.drawing.centerX += dx
            self.drawing.centerY -= dy
            for ship in app.ships:
                ship.checkHits()
                
        else:
            self.removeBullet()
    
    #Removes the bullets from ammo count
    def removeBullet(self):
        for ship in app.ships:
                if self in ship.shipBullets: 
                    ship.shipBullets.remove(self)
                    self.drawing.clear()
    
    #Calls the functions that need to be called every step
    def handleOnStep(self):
        self.move()

class Bomb(Bullets):
    
    #Moves the bomb
    def move(self):
        for dots in self.drawing:
            if self.exploStep == None:
               super().move() 
            elif dots.radius > 10: 
                dots.radius -= 3
            else:
                super().removeBullet()
    
    #Removes the bullets from ammo count
    def removeBullet(self):
        if self.exploStep == None:
            self.exploStep = self.steps
            danger = Circle(self.drawing.centerX,self.drawing.centerY,60,fill=gradient('red','orange'))
            self.drawing.clear()
            self.drawing = Group(danger)
    
    #Calls the functions that need to be called every step
    def handleOnStep(self):
        super().handleOnStep()
        self.steps += 1

class Kraken(object):
    #Initializes variables for the KRAKEN
    def __init__(self,cx,cy):
        self.cx = cx
        self.cy = cy
        self.movementRadius = 25
        self.draw()
    
    #Draws the KRAKEN
    def draw(self):
        self.drawing = Group(
            
            #Head
            Arc(200,200,30,60,270,180),
            
            #Left tentacles
            Arc(168,200,17,30,270,90),
            Arc(180,200,16,24,270,75),
            
            #Right tentacles
            Arc(220,200,16,24,15,75),
            Arc(232,200,16,30,0,90),
            
            #Eyes
            Arc(194,195,8,6,110,180,fill='red'),
            Arc(206,195,8,6,70,180,fill='red'),
            
            #Waves
            Arc(200,200,80,60,90,180,fill='lightSkyBlue'),
            Arc(200,200,70,50,90,180,fill='deepSkyBlue'),
            Arc(200,200,60,40,90,180,fill='lightSkyBlue'),
            Arc(200,200,50,30,90,180,fill='deepSkyBlue'),
            Arc(200,200,40,20,90,180,fill='lightSkyBlue'),
            Arc(200,200,30,10,90,180,fill='deepSkyBlue')
            )
        
        #Makes a zone that the KRAKEN is able to move within
        # self.movementZone = Circle(self.cx,self.cy,self.movementRadius,fill='white',visible=False)
        
        #Places the KRAKEN at designated areas
        self.drawing.centerX = self.cx
        self.drawing.centerY = self.cy

    #Makes the krakens swim
    def swim(self):
        #Gets the random movements 
        self.dx = randrange(-2,3)
        self.dy = randrange(-2,3)
        
        #If the KRAKEN can't move to the area originally designated, this flips its movement to the other direction
        if (self.cx-self.movementRadius > self.drawing.centerX+self.dx) or (self.drawing.centerX+self.dx > self.cx+self.movementRadius):
            self.dx *= -1
        if (self.cy-self.movementRadius > self.drawing.centerY+self.dy) or (self.drawing.centerY+self.dy > self.cy+self.movementRadius):
            self.dy *= -1
        # I removed this Kraken containment method to fix the glitching on the final stage. The .contains method must iterate through all
        # the poins in a drawing which in turn uses lots of processing power.
        # if self.movementZone.contains(self.drawing.centerX+self.dx,self.drawing.centerY+self.dy) == False:
        #     self.dx *= -1
        #     self.dy *= -1
        
        #Moves the Kraken
        self.drawing.centerX += self.dx
        self.drawing.centerY += self.dy
            
    #Checks if the KRAKEN hits a ship
    def checkHits(self):
        for ships in app.ships:
            if self.drawing.hitsShape(ships.drawing) == True:
                ships.otherShip.fallenCoin()
                ships.respawn()

                
    #Calls the functions that need to be called every step
    def handleOnStep(self):
        self.checkHits()
        self.swim()

#Intakes the keys that are being held
def onKeyHold(keys):
    for key in keys:
        for ship in app.ships:
            if (key in ship.ctrls):
                ship.handleKeyInput(key,False)
    game.handleKeyInput(key)

#Intakes the keys that are being pressed
def onKeyPress(keys):
    for key in keys:
      for ship in app.ships:
          if (key in ship.ctrls):
            ship.handleKeyInput(key,True)
    if keys == 'g':
        game.nextStage()
    
#Runs certian functions every step
def onStep():
    for ship in app.ships:
        ship.handleOnStep()
        for bulls in ship.shipBullets:
            bulls.handleOnStep()
    game.handleOnStep()

    
#Instantiate the game
game = GameState()



cmu_graphics.run()