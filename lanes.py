"""
Lanes module for Froggit

This module contains the lane classes for the Frogger game. The lanes are the vertical
slice that the frog goes through: grass, roads, water, and the exit hedge.

Each lane is like its own level. It has hazards (e.g. cars) that the frog has to make
it past.  Therefore, it is a lot easier to program frogger by breaking each level into
a bunch of lane objects (and this is exactly how the level files are organized).

You should think of each lane as a secondary subcontroller.  The level is a subcontroller
to app, but then that subcontroller is broken up into several other subcontrollers, one
for each lane.  That means that lanes need to have a traditional subcontroller set-up.
They need their own initializer, update, and draw methods.

There are potentially a lot of classes here -- one for each type of lane.  But this is
another place where using subclasses is going to help us A LOT.  Most of your code will
go into the Lane class.  All of the other classes will inherit from this class, and
you will only need to add a few additional methods.

If you are working on extra credit, you might want to add additional lanes (a beach lane?
a snow lane?). Any of those classes should go in this file.  However, if you need additional
obstacles for an existing lane, those go in models.py instead.  If you are going to write
extra classes and are now sure where they would go, ask on Piazza and we will answer.

# YOUR NAME AND NETID HERE
# DATE COMPLETED HERE
"""
from game2d import *
from consts import *
from models import *

# PRIMARY RULE: Lanes are not allowed to access anything in any level.py or app.py.
# They can only access models.py and const.py. If you need extra information from the
# level object (or the app), then it should be a parameter in your method.

class Lane(object):         # You are permitted to change the parent class if you wish
    """
    Parent class for an arbitrary lane.

    Lanes include grass, road, water, and the exit hedge.  We could write a class for
    each one of these four (and we will have classes for THREE of them).  But when you
    write the classes, you will discover a lot of repeated code.  That is the point of
    a subclass.  So this class will contain all of the code that lanes have in common,
    while the other classes will contain specialized code.

    Lanes should use the GTile class and to draw their background.  Each lane should be
    GRID_SIZE high and the length of the window wide.  You COULD make this class a
    subclass of GTile if you want.  This will make collisions easier.  However, it can
    make drawing really confusing because the Lane not only includes the tile but also
    all of the objects in the lane (cars, logs, etc.)
    """

    # LIST ALL HIDDEN ATTRIBUTES HERE

    # Attribute _tile: The lane tile
    # Invariant: _tile is a GTile

    # Attribute _logspeed: The speed of a log from json dictionary
    # Invariant: _logspeed is a value of speed in integer

    # Attribute _lanedict: lane configuration from json dictionary
    # Invariant: _lanedict is a dictionary

    # Attribute _buffer: The distance an object in a lane goes offscreen
    # Invariant: _buffer is an integer

    # Attribute _objs: The object images in a lane
    # Invariant: _objs is a list of GImages

    # Attribute _exit: The number of exits filled
    # Invariant: _exit is an integer


    def getLeft(self):
        """
        Returns the left side of tile.
        """
        return self._tile.left

    def setLeft(self,value):
        """
        Sets the value of the left side

        Parameter value: position of tile left side
        Precondition: value is an integer
        """
        self._tile.left = value

    def getBottom(self):
        """
        Returns the bottom side of tile.
        """
        return self._tile.bottom

    def setBottom(self,value):
        """
        Sets the value of the bottom side of tile

        Parameter value: position of tile bottom
        Precondition: value is an integer
        """
        self._tile.bottom = value

    def getTile(self):
        """
        Returns the tile.
        """
        return self._tile

    def getLogspeed(self):
        """
        Returns the speed of a log.
        """
        return self._logspeed

    def __init__(self, width,height,lane, hitbox):
        """
        Initializes a level with lanes and objects

        Parameter width: the width of the lane
        Precondition: width is an integer or float

        Parameter height: the height of the lane
        Precondition: height is an integer or float

        Parameter lane: each lane in the level
        Precondition: lane is the type set by the json dictionary

        Parameter hitbox: the hitbox of each object from objects.json
        Precondition: hitbox is a dictionary
        """
        self._lanedict = lane
        self._tile = GTile(width = width, height = height, \
                           source = self._lanedict['type'] + '.png')
        self._objs = []
        self._exit = 0

        if 'objects' in self._lanedict:
            for obj in self._lanedict['objects']:
                objimg = GImage( source = obj['type'] + '.png')
                objimg.x = obj['position']*GRID_SIZE + GRID_SIZE/2
                objimg.hitbox = hitbox['images'][obj['type']]['hitbox']
                if 'speed' in self._lanedict and self._lanedict['speed'] < 0:
                    objimg.angle = 180
                self._objs.append(objimg)

        if self._lanedict['type'] == 'water':
            self._logspeed = self._lanedict['speed']

    # ADDITIONAL METHODS (DRAWING, COLLISIONS, MOVEMENT, ETC)
    def update(self,dt, jsondict):
        """
        Updates the game objects each frame.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)

        Parameter jsondict: the json dictionary contains all information about
        a level
        Precondition: jsondict is a dictionary
        """
        self._buffer = jsondict['offscreen']
        if 'speed' in self._lanedict:
            steps = self._lanedict['speed']*dt
            for obj in self._objs:
                obj.x = obj.x + steps
                moveobj = False
                moveobj1 = False
                if obj.x < (0 - self._buffer*GRID_SIZE):
                    moveobj = True
                    d = obj.x + self._buffer*GRID_SIZE
                elif obj.x > ((jsondict['size'][0])*GRID_SIZE + \
                               self._buffer*GRID_SIZE):
                    moveobj1 = True
                    d = obj.x - ((jsondict['size'][0])*GRID_SIZE +\
                                  self._buffer*GRID_SIZE)
                if moveobj == True:
                    obj.x = ((jsondict['size'][0])*GRID_SIZE + \
                              self._buffer*GRID_SIZE) + d
                elif moveobj1 == True:
                    obj.x = 0 - self._buffer*GRID_SIZE + d

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
        self._tile.draw(view)
        for obj in self._objs:
            obj.y = self._tile.y
            obj.draw(view)


class Grass(Lane):                           # We recommend AGAINST changing this one
    """
    A class representing a 'safe' grass area.

    You will NOT need to actually do anything in this class.  You will only do anything
    with this class if you are adding additional features like a snake in the grass
    (which the original Frogger does on higher difficulties).
    """
    pass

    # ONLY ADD CODE IF YOU ARE WORKING ON EXTRA CREDIT EXTENSIONS.


class Road(Lane):                           # We recommend AGAINST changing this one
    """
    A class representing a roadway with cars.

    If you implement Lane correctly, you do really need many methods here (not even an
    initializer) as this class will inherit everything.  However, roads are different
    than other lanes as they have cars that can kill the frog. Therefore, this class
    does need a method to tell whether or not the frog is safe.
    """

    # DEFINE ANY NEW METHODS HERE
    def roadObjects(self,frog):
        """
        Returns: True if frog collides with road object else False
        Checks if a road object contains the frog.

        Parameter frog: the animated frog in the level
        Precondition: frog is a Frog class inherited from GSprite
        """
        for x in self._objs:
            if x.collides(frog) == True:
                if 'car' in x.source or 'trailer' in x.source or 'truck' in x.source:
                    return True
        return False


class Water(Lane):
    """
    A class representing a waterway with logs.

    If you implement Lane correctly, you do really need many methods here (not even an
    initializer) as this class will inherit everything.  However, water is very different
    because it is quite hazardous. The frog will die in water unless the (x,y) position
    of the frog (its center) is contained inside of a log. Therefore, this class needs a
    method to tell whether or not the frog is safe.

    In addition, the logs move the frog. If the frog is currently in this lane, then the
    frog moves at the same rate as all of the logs.
    """

    def waterObjects(self,point):
        """
        Returns: True if log contains frog else False
        Checks if a water object contains the frog

        Parameter point: point is the center of the frog
        Precondition: point is a coordinate (x,y)
        """

        for x in self._objs:
            if x.contains(point) == True:
                if 'log' in x.source:
                    return True
        return False


class Hedge(Lane):
    """
    A class representing the exit hedge.

    This class is a subclass of lane because it does want to use a lot of the features
    of that class. But there is a lot more going on with this class, and so it needs
    several more methods.  First of all, hedges are the win condition. They contain exit
    objects (which the frog is trying to reach). When a frog reaches the exit, it needs
    to be replaced by the blue frog image and that exit is now "taken", never to be used
    again.

    That means this class needs methods to determine whether or not an exit is taken.
    It also need to take the (x,y) position of the frog and use that to determine which
    exit (if any) the frog has reached. Finally, it needs a method to determine if there
    are any available exits at all; once they are taken the game is over.

    These exit methods will require several additional attributes. That means this class
    (unlike Road and Water) will need an initializer. Remember to user super() to combine
    it with the initializer for the Lane.
    """

    # LIST ALL HIDDEN ATTRIBUTES HERE
        # Attribute _lilypads: tracks which lilypad is filled
        # Invariant: _lilypads is a dictionary

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER TO SET ADDITIONAL EXIT INFORMATION
    def __init__(self, width,height,lane, hitbox):
        """
        Initializes a hedge lane

        Parameter width: the width of the lane
        Precondition: width is an integer or float

        Parameter height: the height of the lane
        Precondition: height is an integer or float

        Parameter lane: each lane in the level
        Precondition: lane is the type set by the json dictionary

        Parameter hitbox: the hitbox of each object from objects.json
        Precondition: hitbox is a dictionary
        """
        super().__init__(width,height,lane, hitbox)
        self._lilypads = {}
        self._exit = 0
        for x in self._objs:
            if x.source == 'exit.png':
                self._exit = self._exit + 1

    # ANY ADDITIONAL METHODS
    def hedgeobjects(self, point,check):
        """
        Returns: 0 if frog in hedge, 1 if frog in exit, 2 if frog in opening
        Checks if a hedge object contains the frog

        Parameter point: point is the center of the frog
        Precondition: point is a coordinate (x,y)

        Parameter check: check is True when hedge is the next lane
        Precondition: check is a boolean
        """
        countlilypad = 0
        for x in self._objs:
            if x.contains(point) == True:
                if x.source == 'exit.png':
                    if countlilypad in self._lilypads:
                        return 0
                    else:
                        if check == False:
                            self._lilypads[countlilypad] = True
                        return 1
                elif x.source == 'open.png':
                    return 2
            if x.source == 'exit.png':
                countlilypad = countlilypad + 1
        return 0

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
        self._tile.draw(view)
        countlilypad = 0
        for obj in self._objs:
            obj.y = self._tile.y
            obj.draw(view)
            if obj.source == 'exit.png':
                if countlilypad in self._lilypads:
                    safefrog =  GImage(x = obj.x, y = obj.y, source = FROG_SAFE)
                    safefrog.draw(view)
                countlilypad = countlilypad + 1

    def isLilypadfilled(self):
        """
        Returns: True if all exits filled else False
        Checks if all lilypads are filled
        """

        if self._exit == len(self._lilypads):
            return True
        else:
            return False

# IF YOU NEED ADDITIONAL LANE CLASSES, THEY GO HERE
