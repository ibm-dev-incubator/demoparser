==============
Detailed Usage
==============

This example shows how you can collect information from a demo file. In
this case it's gathering data about every player death.

In order to do this you need to know which event to add a callback for.
The first step is to check the list of `game events`_. From the above documentation you
can see the structure of the ``player_death`` event.

You need an instance of :py:class:`demoparser.demofile.DemoFile` to parse
the demo::

        from demoparser.demofile import DemoFile

and a callback function for the ``player_death`` event:

.. literalinclude:: ../../demoparser/examples/player_death.py
     :lines: 6-30


.. note::
    The DemoFile instance should generally be in-scope for callback functions.
    Often a callback will need to refer to the list of active entities or
    other parser state.


Retrieving the event data by name requires an extra step and some background
information.

At the beginning of the demo a message containing all game events is
sent (svc_GameEventList). Each item in the list contains an event ID and
a list of keys with their type and name.

When an event occurs during the game the message from the server only contains
the type and value. To understand what those values refer to you consult 
the game event from the list of events (this event is the first argument
to the callback). The list of keys from the server message and the list of
keys in the game event are in the same order. 

Here's a portion of what's in the message passed to the callback::

    eventid: 23
    keys {
      type: 4
      val_short: 5
    }
    keys {
      type: 4
      val_short: 28
    }
    keys {
      type: 4
      val_short: 6
    }
    keys {
      type: 1
      val_string: "knife_default_ct"
    }
    keys {
      type: 6
      val_bool: false
    }

and here's what's in the event::

    eventid: 23
    name: "player_death"
    keys {
      type: 4
      name: "userid"
    }
    keys {
      type: 4
      name: "attacker"
    }
    keys {
      type: 4
      name: "assister"
    }
    keys {
      type: 1
      name: "weapon"
    }
    keys {
      type: 6
      name: "headshot"
    }


Therefore, the value of ``userid`` is ``msg.keys[0].val_short`` because
``userid`` is the zeroth element in the list of game event keys.


Now that a callback is defined the demo file can be parsed.

.. literalinclude:: ../../demoparser/examples/player_death.py
     :lines: 33-37


Output::

     --- Player Death at tick 4156---
    b0RUP killed by duMzyy * ringwald with knife_default_ct. Headshot? No.
    Attacker: health = 100 position = {'x': -420.1773681640625, 'y': -186.3490753173828, 'z': -215.97097778320312}
    Victim: position = {'x': -454.6003112792969, 'y': -176.74295043945312, 'z': -219.0527801513672}

     --- Player Death at tick 4200---
    duMzyy * ringwald killed by smF with knife_t. Headshot? No.
    Attacker: health = 100 position = {'x': -454.4964599609375, 'y': -157.48977661132812, 'z': -219.96875}
    Victim: position = {'x': -451.5458679199219, 'y': -189.49244689941406, 'z': -215.96875}


.. _game events: https://wiki.alliedmods.net/Counter-Strike:_Global_Offensive_Events
