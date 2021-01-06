"""
Subcontroller module for Froggit

This module contains the subcontroller to manage a single level in the Froggit game.
Instances of Level represent a single game, read from a JSON.  Whenever you load a new
level, you are expected to make a new instance of this class.

The subcontroller Level manages the frog and all of the obstacles. However, those are
all defined in models.py.  The only thing in this class is the level class and all of
the individual lanes.

This module should not contain any more classes than Levels. If you need a new class,
it should either go in the lanes.py module or the models.py module.

# YOUR NAME AND NETID HERE
# DATE COMPLETED HERE
"""
from game2d import *
from consts import *
from lanes  import *
from models import *

# PRIMARY RULE: Level can only access attributes in models.py or lanes.py using getters
# and setters. Level is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Level(object):
    """
    This class controls a single level of Froggit.

    This subcontroller has a reference to the frog and the individual lanes.  However,
    it does not directly store any information about the contents of a lane (e.g. the
    cars, logs, or other items in each lane). That information is stored inside of the
    individual lane objects.

    If you want to pause the game, tell this controller to draw, but do not update.  See
    subcontrollers.py from Lesson 27 for an example.  This class will be similar to that
    one in many ways.

    All attributes of this class are to be hidden.  No attribute should be accessed
    without going through a getter/setter first.  However, just because you have an
    attribute does not mean that you have to have a getter for it.  For example, the
    Froggit app probably never needs to access the attribute for the Frog object, so
    there is no need for a getter.

    The one thing you DO need a getter for is the width and height.  The width and height
    of a level is different than the default width and height and the window needs to
    resize to match.  That resizing is done in the Froggit app, and so it needs to access
    these values in the level.  The height value should include one extra grid square
    to suppose the number of lives meter.
    """

    # LIST ALL HIDDEN ATTRIBUTES HERE
    # Attribute _animator: A coroutine for performing an animation
    # Invariant: _animator is a generator-based coroutine (or None)

    # Attribute _animator1: A coroutine for performing an animation
    # Invariant: _animator1 is a generator-based coroutine (or None)

    # Attribute _lives: amount of lives the player has
    # Invariant: _lives is a integer

    # Attribute _label: a message that says "Lives"
    # Invariant: _label is a GLabel, or None if there is no title to display

    # Attribute _liveslist: list of frog head images
    # Invariant: _liveslist is a list

    # Attribute _hedgelist: list of hedge lanes
    # Invariant: _hedgelist is a list

    # Attribute _waterlist: list of water lanes
    # Invariant: _waterlist is a list

    # Attribute _roadlist: list of road lanes
    # Invariant: _roadlist is a list

    # Attribute _frog: the frog that they player moves
    # Invariant: _frog is a instance of Frog class

    # Attribute _hitboxdict: the hitbox of each object from objects.json
    # Invariant: _hitboxdict is a dictionary

    # Attribute _skull: the skull that appears when a frog dies
    # Invariant: _skull is a instance of Skull class

    # Attribute _jumpsound: the sound when a frog jumps
    # Invariant: _jumpsound is an instance of Sound

    # Attribute _diesound: the sound when a frog dies
    # Invariant: _diesound is an instance of Sound

    # Attribute _exitsound: the sound when a frog goes to an exit
    # Invariant: _exitsound is an instance of Sound

    def getLives(self):
        """
        Returns the number of lives
        """
        return self._lives

    def __init__(self, jsondict, hitboxdict):
        """
        Initializes a level with a json dictionary.

        Parameter jsondict: the json dictionary contains all information about
        a level
        Precondition: jsondict is a dictionary

        Parameter hitboxdict: the hitbox dictionary contains all information
        about an image hitbox
        Precondition: hitboxdict is a dictionary
        """
        self._initializerHelper(jsondict, hitboxdict)
        self._displayLives(jsondict)
        if self._liveslist == []:
            self._label.right = jsondict['size'][0]*GRID_SIZE
        else:
            self._label.right = self._liveslist[len(self._liveslist)-1].left
        laneCount = 0
        for lane in jsondict['lanes']:
            if lane['type'] == 'grass':
                laneobj = Grass(width = jsondict['size'][0]*GRID_SIZE, \
                                height = GRID_SIZE, lane = lane, hitbox = hitboxdict)
            if lane['type'] == 'road':
                laneobj = Road(width = jsondict['size'][0]*GRID_SIZE, \
                               height = GRID_SIZE, lane = lane, hitbox = hitboxdict)
                self._roadlist.append(laneobj)
            if lane['type'] == 'water':
                laneobj = Water(width = jsondict['size'][0]*GRID_SIZE,\
                                height = GRID_SIZE, lane = lane, hitbox = hitboxdict)
                self._waterlist.append(laneobj)
            if lane['type'] == 'hedge':
                laneobj = Hedge(width = jsondict['size'][0]*GRID_SIZE, \
                                height = GRID_SIZE, lane = lane, hitbox = hitboxdict)
                self._hedgelist.append(laneobj)
            laneobj.setLeft(0)
            laneobj.setBottom(laneCount*GRID_SIZE)
            laneCount = laneCount + 1
            self._laneslist.append(laneobj)
        self.createFrog(jsondict,hitboxdict)

    # UPDATE METHOD TO MOVE THE FROG AND UPDATE ALL OF THE LANES
    def update(self,dt,input, jsondict):
        """
        Returns: True if frog not dead or has won else False
        Updates the game objects each frame.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)

        Parameter input: The user input, used to control the frog and change state
        Precondition: input is an instance of GInput and is inherited from GameApp

        Parameter jsondict: the json dictionary contains all information about
        a level
        Precondition: jsondict is a dictionary
        """
        if not self._animator1 is None:
            try:
                self._animator1.send(dt)
            except:
                self._animator1 = None
                self._skull = None
                return False
        elif not self._animator is None:          # We have something to animate
            try:
                self._animator.send(dt)         # Tell it how far to animate
            except:
                self._animator = None
                if self._exitChecker() == False:
                    return False
                self._jumpsound.play()
        elif input.is_key_down('up'):
            if self._upCollide(dt,input, jsondict) == False:
                return False
        elif input.is_key_down('down'):
            self._downCollide(dt,input, jsondict)
        elif input.is_key_down('left'):
            self._leftCollide(dt,input, jsondict)
        elif input.is_key_down('right'):
            self._rightCollide(dt,input, jsondict)
        for lane in self._laneslist:
            lane.update(dt,jsondict)
        self._deathHelper(dt, jsondict)
        return True

    def draw(self, view):
        """
        Draws the game objects to the view.

        Every single thing you want to draw in this game is a GObject. To draw a
        GObject g, simply use the method g.draw(self.view). It is that easy!

        Many of the GObjects (such as the cars, logs, and exits) are attributes
        in either Level or Lane. In order to draw them, you either need to add
        getters for these attributes or you need to add a draw method to
        those two classes.  We suggest the latter.  See the example subcontroller.py
        from the lesson videos.
        """
        for lane in self._laneslist:
            lane.draw(view)

        for life in self._liveslist:
            life.draw(view)

        self._label.draw(view)

        if self._frog != None:
            self._frog.draw(view)
        if self._skull != None:
            self._skull.draw(view)

    def createFrog(self, jsondict, hitboxdict):
        """
        creates the frog at the start position

        Parameter jsondict: the json dictionary contains all information about
        a level
        Precondition: jsondict is a dictionary

        Parameter hitboxdict: the hitbox dictionary contains all information
        about an image hitbox
        Precondition: hitboxdict is a dictionary
        """
        x1 = (((jsondict['start'][0])))*GRID_SIZE + GRID_SIZE/2
        y1 = (((jsondict['start'][1]))) *GRID_SIZE +GRID_SIZE/2
        self._frog = Frog(x=x1,y=y1, \
                          source =  hitboxdict['sprites']['frog']['file'],\
                          format = hitboxdict['sprites']['frog']['format'] )
        self._frog.angle = FROG_NORTH
        self._frog.hitboxes = hitboxdict['sprites']['frog']['hitboxes']
        self._frog.frame = 0

    def isWin(self):
        """
        Returns: True if frog has won else False
        creates the frog at the start position
        """
        for x in self._hedgelist:
            if x.isLilypadfilled() == False:
                return False
        return True

    # ANY NECESSARY HELPERS (SHOULD BE HIDDEN)
    def _createSkull(self, x1, y1, jsondict, hitboxdict):
        """
        creates skull where frog died

        Parameter x1: the x position of the frog where it died
        Precondition: x1 is an integer

        Parameter y1: the y position of the frog where it died
        Precondition: y1 is an integer

        Parameter jsondict: the json dictionary contains all information about a level
        Precondition: jsondict is a dictionary

        Parameter hitboxdict: the hitbox dictionary contains all information
        about an image hitbox
        Precondition: hitboxdict is a dictionary
        """
        self._skull = Skull(x=x1,y=y1, \
                            source =  hitboxdict['sprites']['skulls']['file'], \
                            format = hitboxdict['sprites']['skulls']['format'] )
        self._skull.frame = 0

    def _displayLives(self,jsondict):
        """
        Displays the lives bar

        Parameter jsondict: the json dictionary contains all information about a level
        Precondition: jsondict is a dictionary
        """
        liveslist = []
        for life in range(self._lives):
            froglife =  GImage(top = jsondict['size'][1]*GRID_SIZE + GRID_SIZE,\
                               width = GRID_SIZE, height = GRID_SIZE, source = FROG_HEAD)
            if life == 0:
                froglife.right = jsondict['size'][0]*GRID_SIZE
            else:
                froglife.right = liveslist[life-1].left
            liveslist.append(froglife)

        self._liveslist = liveslist

    def _upCollide(self,dt,input, jsondict):
        """
        Returns: True if frog is not dead else False
        Makes frog go up if up arrow is pressed

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)

        Parameter input: The user input, used to control the frog and change state
        Precondition: input is an instance of GInput and is inherited from GameApp

        Parameter jsondict: the json dictionary contains all information about
        a level
        Precondition: jsondict is a dictionary
        """
        self._frog.angle = FROG_NORTH
        if self._frog.top <= (jsondict['size'][1] - 1)*GRID_SIZE:
            for x in self._hedgelist:
                self._frog.y = self._frog.y + GRID_SIZE
                if self._frog.collides(x.getTile()) == True:
                    y = x.hedgeobjects((self._frog.x,self._frog.y),True)
                    if y == 0:
                        self._frog.y = self._frog.y-GRID_SIZE
                        return True
                    else:
                        self._frog.y = self._frog.y-GRID_SIZE
                else:
                    self._frog.y = self._frog.y-GRID_SIZE

            inhedge = False
            y = 0
            for x in self._hedgelist:
                if self._frog.collides(x.getTile()) == True:
                    y = x.hedgeobjects((self._frog.x,self._frog.y),True)
                    inhedge = True
            if inhedge == False or y == 2:
                self._animator = self._frog.animate_slide('up', \
                                                jsondict['size'][0]*GRID_SIZE)
                next(self._animator)
        return True

    def _downCollide(self,dt,input, jsondict):
        """
        Returns: True if frog is not dead else False
        Makes frog go down if down arrow is pressed

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)

        Parameter input: The user input, used to control the frog and change state
        Precondition: input is an instance of GInput and is inherited from GameApp

        Parameter jsondict: the json dictionary contains all information about
        a level
        Precondition: jsondict is a dictionary
        """
        self._frog.angle = FROG_SOUTH
        if self._frog.bottom >= GRID_SIZE/2:
            for x in self._hedgelist:
                self._frog.y = self._frog.y - GRID_SIZE
                if self._frog.collides(x.getTile()) == True:
                    y = x.hedgeobjects((self._frog.x,self._frog.y),True)
                    self._frog.y = self._frog.y + GRID_SIZE
                    if y == 0 or y == 1:
                        return True
                else:
                    self._frog.y = self._frog.y + GRID_SIZE

            self._animator = self._frog.animate_slide('down', \
                                                jsondict['size'][0]*GRID_SIZE)
            next(self._animator)

    def _leftCollide(self,dt,input, jsondict):
        """
        Makes frog go left if left arrow is pressed

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)

        Parameter input: The user input, used to control the frog and change state
        Precondition: input is an instance of GInput and is inherited from GameApp

        Parameter jsondict: the json dictionary contains all information about
        a level
        Precondition: jsondict is a dictionary
        """
        self._frog.angle = FROG_WEST
        if self._frog.left >= GRID_SIZE/2:
            inhedge = False
            for x in self._hedgelist:
                if self._frog.collides(x.getTile()) == True:
                    inhedge = True
            if inhedge == False:
                self._animator = self._frog.animate_slide('left', \
                                                jsondict['size'][0]*GRID_SIZE)
                next(self._animator)

    def _rightCollide(self,dt,input, jsondict):
        """
        Makes frog go right if right arrow is pressed

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)

        Parameter input: The user input, used to control the frog and change state
        Precondition: input is an instance of GInput and is inherited from GameApp

        Parameter jsondict: the json dictionary contains all information about
        a level
        Precondition: jsondict is a dictionary
        """
        self._frog.angle = FROG_EAST
        if self._frog.right <= (jsondict['size'][0]*GRID_SIZE - GRID_SIZE/2):
            inhedge = False
            for x in self._hedgelist:
                if self._frog.collides(x.getTile()) == True:
                    inhedge = True
            if inhedge == False:
                self._animator = self._frog.animate_slide('right', \
                                                jsondict['size'][0]*GRID_SIZE)
                next(self._animator)

    def _logRide(self,dt, jsondict):
        """
        Returns: True if frog is not dead else False
        Allows the frog to ride on a log in the water. Also kills the frog if it
        touches water

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)

        Parameter jsondict: the json dictionary contains all information about
        a level
        Precondition: jsondict is a dictionary
        """
        for x in self._waterlist:
            if self._frog.collides(x.getTile()) == True:
                y = x.waterObjects((self._frog.x,self._frog.y))
                if y == True:
                    self._frog.x = self._frog.x + x.getLogspeed()*dt
                    if self._frog.x < 0 or \
                       self._frog.x > ((jsondict['size'][0])*GRID_SIZE):
                        self._lives = self._lives - 1
                        self._displayLives(jsondict)
                        #self._frog = None
                        return False
                if y == False and self._animator is None:
                    self._lives = self._lives - 1
                    self._displayLives(jsondict)
                    #self._frog = None
                    return False

    def _initializerHelper(self, jsondict, hitboxdict):
        """
        Initializes attributes in the initializer. Initializes the animators and
        the skull and the sounds used in the game.

        Parameter jsondict: the json dictionary contains all information about a level
        Precondition: jsondict is a dictionary

        Parameter hitboxdict: the hitbox dictionary contains all information
        about an image hitbox
        Precondition: hitboxdict is a dictionary
        """
        self._lives = 3
        self._label = GLabel(text = 'Lives:', font_size = ALLOY_SMALL, \
                             font_name = ALLOY_FONT, linecolor ='dark green')
        self._label.y =  jsondict['size'][1]*GRID_SIZE + GRID_SIZE - GRID_SIZE/2
        self._animator = None
        self._animator1 = None
        self._skull = None
        self._hitboxdict = hitboxdict
        self._jumpsound = Sound(CROAK_SOUND)
        self._diesound = Sound(SPLAT_SOUND)
        self._exitsound = Sound(TRILL_SOUND)
        self._laneslist = []
        self._hedgelist = []
        self._roadlist = []
        self._waterlist = []

    def _deathHelper(self,dt, jsondict):
        """
        Returns: True if frog is not dead else False
        Allows the frog to ride on a log in the water. Also kills the frog if it
        touches water. Also kills frog if it hits a car

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)

        Parameter jsondict: the json dictionary contains all information about
        a level
        Precondition: jsondict is a dictionary
        """
        if self._frog != None:
            if self._logRide(dt,jsondict) == False:
                self._createSkull(self._frog.x, self._frog.y, \
                                  jsondict, self._hitboxdict)
                self._frog = None
                self._animator = None
                self._diesound.play()
                self._animator1 = self._skull.animate_slide()
                next(self._animator1)
                return True

            for x in self._roadlist:
                if self._frog.collides(x.getTile()) == True:
                    y = x.roadObjects(self._frog)
                    if y == True:
                        self._lives = self._lives - 1
                        self._displayLives(jsondict)
                        self._createSkull(self._frog.x, self._frog.y, \
                                          jsondict, self._hitboxdict)
                        self._frog = None
                        self._animator = None
                        self._diesound.play()
                        self._animator1 = self._skull.animate_slide()
                        next(self._animator1)
                        return True

    def _exitChecker(self):
        """
        Returns: True if frog is not in exit else False
        Checks if the frog is in the exit.
        """
        for x in self._hedgelist:
            if self._frog.collides(x.getTile()) == True:
                y = x.hedgeobjects((self._frog.x,self._frog.y),False)
                if y == 1:
                    self._exitsound.play()
                    self._frog = None
                    return False
