"""
Models module for Froggit

This module contains the model classes for the Frogger game. Anything that you
interact with on the screen is model: the frog, the cars, the logs, and so on.

Just because something is a model does not mean there has to be a special class for
it. Unless you need something special for your extra gameplay features, cars and logs
could just be an instance of GImage that you move across the screen. You only need a new
class when you add extra features to an object.

That is why this module contains the Frog class.  There is A LOT going on with the
frog, particularly once you start creating the animation coroutines.

If you are just working on the main assignment, you should not need any other classes
in this module. However, you might find yourself adding extra classes to add new
features.  For example, turtles that can submerge underneath the frog would probably
need a custom model for the same reason that the frog does.

If you are unsure about  whether to make a new class or not, please ask on Piazza. We
will answer.

# YOUR NAME AND NETID HERE
# DATE COMPLETED HERE
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other than
# consts.py.  If you need extra information from a lane or level object, then it
# should be a parameter in your method.


class Frog(GSprite):         # You will need to change this by Task 3
    """
    A class representing the frog

    The frog is represented as an image (or sprite if you are doing timed animation).
    However, unlike the obstacles, we cannot use a simple GImage class for the frog.
    The frog has to have additional attributes (which you will add).  That is why we
    make it a subclass of GImage.

    When you reach Task 3, you will discover that Frog needs to be a composite object,
    tracking both the frog animation and the death animation.  That will like caused
    major modifications to this class.
    """
    # LIST ALL HIDDEN ATTRIBUTES HERE
    # Attribute _svert: the starting vertical position of frog
    # Invariant: _svert is an integer

    # Attribute _fvert: the final vertical position of frog
    # Invariant: _fvert is an integer

    # Attribute _shorz: the starting horizontal position of frog
    # Invariant: _shorz is an integer

    # Attribute _fhorz: the final horizontal position of frog
    # Invariant: _fhorz is an integer

    # Attribute _steps: vertical steps in one animation frame
    # Invariant: _steps is a float

    # Attribute _steps2: horizontal steps in one animation frame
    # Invariant: _steps2 is a float

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    def __init__(self, x, y, source, format):
        """
        Initializes the frog.

        Parameter x: the x coordinate of the center of frog

        Parameter y: the y coordinate of the center of frog

        Parameter source: the source sprite of the frog

        Parameter format: the format of the sprite sheet
        """
        super().__init__(x = x, y = y, source = source, format = format)

    def animate_slide(self,direction,width):
        """
        Animates a frog movement of the sprite over FROG_SPEED seconds

        This method is a coroutine that takes a break (so that the game
        can redraw the image) every time it moves it. The coroutine takes
        the dt as periodic input so it knows how many (parts of) seconds
        to animate.

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.

        Parameter direction: The direction to slide.
        Precondition: direction is a string and one of 'up', 'down', 'left',
        or 'right'

        Parameter width: The width of the level
        Precondition: width is an integer
        """
        self._svert = self.y
        self._shorz = self.x
        if direction == 'up':
            self._fvert = self._svert+GRID_SIZE
            self._steps = (self._fvert-self._svert)/FROG_SPEED
        elif direction == 'down':
            self._fvert = self._svert-GRID_SIZE
            self._steps = (self._fvert-self._svert)/FROG_SPEED
        elif direction == 'left':
            self._fhorz = self._shorz-GRID_SIZE
            self._steps2 = (self._fhorz-self._shorz)/FROG_SPEED
        elif direction == 'right':
            self._fhorz = self._shorz+GRID_SIZE
            self._steps2 = (self._fhorz-self._shorz)/FROG_SPEED
        animating = True
        while animating:
            dt = (yield)
            animating = self._animateHelper(dt,direction,width)

    # ADDITIONAL METHODS (DRAWING, COLLISIONS, MOVEMENT, ETC)
    def _animateHelper(self,dt,direction,width):
        """
        Returns: True if animation is still going else False
        Animates a frog movement of the sprite over FROG_SPEED seconds.

        This method is a coroutine that takes a break (so that the game
        can redraw the image) every time it moves it. The coroutine takes
        the dt as periodic input so it knows how many (parts of) seconds
        to animate.

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.

        Parameter direction: The direction to slide.
        Precondition: direction is a string and one of 'up', 'down', 'left',
        or 'right'

        Parameter width: The width of the level
        Precondition: width is an integer
        """
        animating = True
        if direction == 'up' or direction == 'down':
            amount = self._steps*dt
            self.y = self.y+amount
            if abs(self.y-self._svert) >= GRID_SIZE:
                self.y = self._fvert
                animating = False
            frac = abs(2*(self.y-self._svert)/(GRID_SIZE))
        else:
            amount = self._steps2*dt
            self.x = self.x+amount
            if abs(self.x-self._shorz) >= GRID_SIZE:
                self.x = self._fhorz
                animating = False
            if direction == 'left' and self.x <= GRID_SIZE/2:
                self.x = GRID_SIZE/2
                animating = False
            if direction == 'right' and self.x >= width - GRID_SIZE/2:
                self.x = width - GRID_SIZE/2
                animating = False
            frac = abs(2*(self.x-self._shorz)/(GRID_SIZE))
        if frac < 1:
            frame = frac*(4)
            self.frame = round(frame)
        else:
            frac = frac-1
            frame = 4-frac*(4)
            self.frame = round(frame)
        return animating


# IF YOU NEED ADDITIONAL LANE CLASSES, THEY GO HERE
class Skull(GSprite):         # You will need to change this by Task 3
    """
    A class representing the skull

    The skull is represented as a sprite
    """
    # LIST ALL HIDDEN ATTRIBUTES HERE

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    def __init__(self, x, y, source, format):
        """
        Initializes the skull.

        Parameter x: the x coordinate of the center of skull

        Parameter y: the y coordinate of the center of skull

        Parameter source: the source sprite of the skull

        Parameter format: the format of the sprite sheet
        """
        super().__init__(x = x, y = y, source = source, format = format)

    def animate_slide(self):
        """
        Animates a death over DEATH_SPEED seconds

        This method is a coroutine that takes a break (so that the game
        can redraw the image) every time it moves it. The coroutine takes
        the dt as periodic input so it knows how many (parts of) seconds
        to animate.

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float
        """
        time = 0
        animating = True
        while animating:

            dt = (yield)
            time = time + dt


            frac = time/DEATH_SPEED

            frame = frac*(7)
            self.frame = round(frame)

            if time >= DEATH_SPEED:
                animating = False
