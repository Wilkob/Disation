import pygame
import random
import os
import math

RAWRES = 0
EQUIP = 1
CIVPOP = 2
TROOPPOP = 3
screenH = 800
screenW = 1200
WIN = pygame.display.set_mode((screenW, screenH))
FPS = 60
tickdone = 0
movevalue = 10
SHIP_HIEGHT = 25
SHIP_WIDTH = 25
SHIP_IMAGE0 = pygame.image.load(os.path.join('Assets', 'Ship0.png'))
SHIP_IMAGE1 = pygame.image.load(os.path.join('Assets', 'Ship1.png'))
SHIP0 = pygame.transform.scale(SHIP_IMAGE0, (SHIP_HIEGHT, SHIP_WIDTH))
SHIP1 = pygame.transform.scale(SHIP_IMAGE1, (SHIP_HIEGHT, SHIP_WIDTH))
BACKGROUD_IMAGE = pygame.image.load(os.path.join('Assets', 'blue.png'))
BACKGROUD = pygame.transform.scale(BACKGROUD_IMAGE, (screenW, screenW))
PLANET_HIEGHT = 100
PLANET_WIDTH = 100
PLANET_IMAGE0 = pygame.image.load(os.path.join('Assets', 'planet0.png'))
PLANET_IMAGE1 = pygame.image.load(os.path.join('Assets', 'planet1.png'))
PLANET_IMAGED = pygame.image.load(os.path.join('Assets', 'planetD.png'))
PLANET0 = pygame.transform.scale(PLANET_IMAGE0, (PLANET_HIEGHT, PLANET_WIDTH))
PLANET1 = pygame.transform.scale(PLANET_IMAGE1, (PLANET_HIEGHT, PLANET_WIDTH))
PLANETD = pygame.transform.scale(PLANET_IMAGED, (PLANET_HIEGHT, PLANET_WIDTH))
pygame.font.init()
STAT_FONT = pygame.font.SysFont("comicsans", 50)

ships = []
planets = []
STARTplanets = []
maxcargo = 50
Fitness = 0


class Ship:
    def __init__(self, x, y, Goalx, Goaly, goods):
        self.GameRec = pygame.Rect(x, y, SHIP_HIEGHT, SHIP_WIDTH)
        self.Goalx = Goalx
        self.Goaly = Goaly
        self.goods = goods

    def tracking(self):  # moves the ship closer to the target planet and iif its been reached delivers the cargo
        closeX = math.isclose(self.GameRec.x, self.Goalx, abs_tol=movevalue)
        closeY = math.isclose(self.GameRec.y, self.Goaly, abs_tol=movevalue)
        if self.GameRec.x == self.Goalx and self.GameRec.y == self.Goaly:
            planet = planetcontact(self.GameRec)
            planet.ingoods(self.goods)
            ships.remove(self)
        else:
            if self.GameRec.x < self.Goalx:
                if closeX == True:
                    self.GameRec.x += 1
                else:
                    self.GameRec.x += movevalue
            if self.GameRec.x > self.Goalx:
                if closeX == True:
                    self.GameRec.x -= 1
                else:
                    self.GameRec.x -= movevalue
            if self.GameRec.y < self.Goaly:
                if closeY == True:
                    self.GameRec.y += 1
                else:
                    self.GameRec.y += movevalue
            if self.GameRec.y > self.Goaly:
                if closeY == True:
                    self.GameRec.y -= 1
                else:
                    self.GameRec.y -= movevalue

    def outputall(self):
        print(
            "\nX:", self.GameRec.x,
            "\nY:", self.GameRec.y,
            "\nGoal X:", self.Goalx,
            "\nGoal Y:", self.Goaly,
            "\nCargo Type: ", end="")
        if self.goods.things == CIVPOP:
            print("civ pop")
        if self.goods.things == TROOPPOP:
            print("troop pop")
        if self.goods.things == RAWRES:
            print("raw resources")
        if self.goods.things == EQUIP:
            print("equipment")
        print("Cargo Amount:", self.goods.amount)


class planet:

    def __init__(self, x, y, Name):
        self.name = Name
        self.GameRec = pygame.Rect(x, y, PLANET_HIEGHT, PLANET_WIDTH)
        self.civpop = 100
        self.trooppop = int(self.civpop * 0.8)
        self.rawresoures = 500
        self.equipment = 500
        self.rate = random.randint(10, 20) / 10

        self.Type = random.randint(0, 1)
        if self.Type == RAWRES:
            self.popraw = 0.5
            self.popequip = 0
        else:
            self.popequip = 0.5
            self.popraw = 0

        self.TroopsSupplied = 1

    def XY(self):
        return self.GameRec.x, self.GameRec.y

    def outputall(self):
        print("\nName:",
              self.name,
              "\nX:", self.GameRec.x,
              "\nY:", self.GameRec.y,
              "\ncivpop:", self.civpop,
              "\ntrooppop:", self.trooppop,
              "\nrawresoures:", self.rawresoures,
              "\nequipment:", self.equipment,
              "\nrate:", self.rate,
              "\npopraw:", self.popraw,
              "\npopequip:", self.popequip,
              "\n%TroopsSupplied:", self.TroopsSupplied
              )

    def ingoods(self, goods):  # changes the internal levels when ships arrive
        if goods.things == CIVPOP:
            self.civpop += goods.amount
        if goods.things == TROOPPOP:
            self.trooppop += goods.amount
        if goods.things == RAWRES:
            self.rawresoures += goods.amount
        if goods.things == EQUIP:
            self.equipment += goods.amount

    def outgoods(self, things, amount):  # removes resources when ships are sent
        if things == CIVPOP and self.civpop >= amount:
            self.civpop -= amount
            OUT = goods(things, amount)
        elif things == CIVPOP and self.civpop > 0:
            allin = self.civpop
            self.civpop = 0
            OUT = goods(things, allin)

        if things == TROOPPOP and self.civptrooppopop >= amount:
            self.trooppop -= amount
            OUT = goods(things, amount)
        elif things == TROOPPOP and self.trooppop > 0:
            allin = self.trooppop
            self.trooppop = 0
            OUT = goods(things, allin)

        if things == RAWRES and self.rawresoures >= amount:
            self.rawresoures -= amount
            OUT = goods(things, amount)
        elif things == RAWRES and self.rawresoures > 0:
            allin = self.rawresoures
            self.rawresoures = 0
            OUT = goods(things, allin)

        if things == EQUIP:
            self.equipment -= amount
            OUT = goods(things, amount)
        elif things == EQUIP and self.equipment > 0:
            allin = self.equipment
            self.equipment = 0
            OUT = goods(things, allin)
        return OUT

    def checkout(self, things):  # checks if resources can be sent
        OUT = False
        if things == CIVPOP and self.civpop > 0:
            OUT = True
        if things == TROOPPOP and self.civptrooppopop > 0:
            OUT = True
        if things == RAWRES and self.rawresoures > 0:
            OUT = True
        if things == EQUIP and self.equipment > 0:
            OUT = True
        return OUT

    def tick(self):  # changes the planets internal levels
        global Fitness
        if self.civpop != 0:
            producede = (self.civpop * self.popequip) * self.rate
            producedraw = (self.civpop * self.popraw) * self.rate
            self.rawresoures = (self.rawresoures + producedraw)
            if self.rawresoures < producede:
                producede = self.rawresoures - producede
                if producede <= 0:
                    producede = 0

                self.rawresoures = 0

            else:
                self.rawresoures = self.rawresoures - producede

            self.equipment = (self.equipment + producede)
            try:
                self.TroopsSupplied = int(self.equipment / self.trooppop * 100)
                Fitness += 0.5
            except:
                self.TroopsSupplied = 0

            if self.TroopsSupplied >= 100:
                self.TroopsSupplied = 100
                Fitness += 0.5 * (self.civpop / 10)

            self.equipment = (self.equipment - self.trooppop)
            if self.equipment <= 0:
                self.equipment = 0

            if self.TroopsSupplied <= 0:
                self.civpop = int(self.civpop * 0.95)
                self.trooppop = int(self.civpop * 0.8)
                Fitness -= 0.5
            elif self.TroopsSupplied <= 10:
                self.civpop = int(self.civpop * 0.99)
                self.trooppop = int(self.civpop * 0.8)
                Fitness -= 0.1
            if self.civpop == 0:
                Fitness -= 20
                self.trooppop = 0
                self.rawresoures = 0
                self.equipment = 0

    def givepersupply(self):
        return self.TroopsSupplied

    def givepop(self):
        return self.civpop


class goods:
    def __init__(self, things, amount):  # creates object to store the reaources for transpoort
        self.things = things
        self.amount = amount


def SendingResoures(SendingPlanet, RecivingPlanet, Type, amount):
    if amount > maxcargo:
        a = maxcargo
    else:
        a = amount
    c = SendingPlanet.checkout(Type)
    if c == True and SendingPlanet != RecivingPlanet:
        spawnship(*SendingPlanet.XY(), *RecivingPlanet.XY(), SendingPlanet.outgoods(Type, a))


def ending(run1, T, gen=None, Ai=None):  # making sure all planets have pop in them and if not close the program
    global Fitness
    totalpop = 0
    for i in planets:
        totalpop += i.givepop()
    if totalpop > 0 and run1 == True and T <= 20000:  #
        run = True
    else:
        print("Sim over", "Total pop = ", totalpop, "Tick Complete = ", T, "Fitness =", Fitness)
        if gen is None:
            out = str(str(totalpop) + ";" + str(T) + ";" + str(Fitness) + "\n")
            file = "Trained output 105C.txt"
        else:
            out = str(str(Ai) + ";" + str(totalpop) + ";" + str(T) + ";" + str(Fitness)+ "\n" )
            file = str("Learning " + str(gen) + "output 105C.txt")

        #tofile(file,out)
        run = False

    return (run)


def tofile(file, data):
    file = open(file, "a")
    file.write(data)
    file.close()


def tick():  # has all the planet update there interal levels
    global tickdone, planets
    if tickdone == 10:
        tickdone = 0
        for i in planets:
            i.tick()
    else:
        tickdone += 1
    shipsmove()


def draw_win(gen=None, Ai=None):
    WIN.blit(BACKGROUD, (0, 0))
    for i in planets:
        if i.givepop() == 0:
            WIN.blit(PLANETD, (i.GameRec.x, i.GameRec.y))
        elif i.Type == 0:
            WIN.blit(PLANET0, (i.GameRec.x, i.GameRec.y))
        else:
            WIN.blit(PLANET1, (i.GameRec.x, i.GameRec.y))
    for i in ships:
        if i.goods.things == 0:
            WIN.blit(SHIP0, (i.GameRec.x, i.GameRec.y))
        else:
            WIN.blit(SHIP1, (i.GameRec.x, i.GameRec.y))

    if gen is not None:
        score_label = STAT_FONT.render("Gen: " + str(gen), 1, (255, 255, 255))
        WIN.blit(score_label, (10, 10))
    if Ai is not None:
        score_label = STAT_FONT.render("Ai: " + str(Ai), 1, (255, 255, 255))
        WIN.blit(score_label, (10, 50))

    pygame.display.update()  # updates the window to new changes


def spawnship(x, y, gx, gy, cargo):  # creates a new ship with a start goal and cargo
    Recship = Ship(x, y, gx, gy, cargo)
    ships.append(Recship)


def shipsmove():  # moves all ships
    for i in ships:
        i.tracking()


def planetcontact(rect):  # checks if an object is in contact with planet
    for i in planets:
        if rect.colliderect(i.GameRec) == True:
            return i
    return 0


def clicked(pos):  # checks if something has been clicked
    for i in planets:
        if i.GameRec.collidepoint(pos) == True:
            i.outputall()
    for i in ships:
        if i.GameRec.collidepoint(pos) == True:
            i.outputall()


def popgalaxy(size):#this function creates all the planets based on the number it is given
    for i in range(size):
        contact = True
        while contact == True:
            recpalanet = planet(random.randint(0, (screenW - PLANET_WIDTH)),
                               random.randint(0, (screenH - PLANET_HIEGHT)), i)

            if planetcontact(recpalanet.GameRec) == 0:  # if the planet is inside another planet find a new postions
                planets.append(recpalanet)
                contact = False
            else:
                recpalanet.GameRec.x = random.randint(0, (screenW - PLANET_WIDTH))
                recpalanet.GameRec.y = random.randint(0, (screenH - PLANET_HIEGHT))


def AI(net):
    for i in planets:
        RAWS = []
        EQP = []
        pop = []
        type = []
        rate = []
        for x in planets:
            RAWS.append(x.rawresoures)
            EQP.append(x.equipment)
            pop.append(x.givepop())
            type.append(x.Type)
            rate.append(x.rate)
        output = net.activate((*RAWS, *EQP, *pop, *type, *rate))
        for out in range(10):
            if output[out] > 0.5:
                if output[10] > 0.5:
                    SendingResoures(i, planets[out], RAWRES, maxcargo)
                if output[11] > 0.5:
                    SendingResoures(i, planets[out], EQUIP, maxcargo)


def cleanup():
    global planets, ships
    ships = []
    planets = []
    draw_win()


def Run(net, a=None, g=None):
    global planets, Fitness
    print("Sim Starting")
    popgalaxy(10)
    run = True
    pygame.display.set_caption("Visual Map Gen: " + str(g) + "AI: " + str(a))
    clock = pygame.time.Clock()
    T = 0
    Fitness = 0
    while run:
        clock.tick(FPS)
        T += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # allows to quit via the X button
                run = False
                break
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                clicked(pos)

        tick()
        AI(net)
        draw_win(g, a)

        run = ending(run, T, g, a)

    cleanup()
    return Fitness


