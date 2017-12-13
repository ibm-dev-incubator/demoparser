``csgo-demoparser`` is a library for parsing CS:GO demo files.

As the file is processed events are emitted for which callbacks can
be registered.

Quick start
-----------

1. Install::

        pip install csgo-demoparser

2. Parse a demo::

   >>> from demoparser.demofile import DemoFile
   >>> data = open('/path/to/demofile', 'rb').read()
   >>> df = DemoFile(data)
   >>> df.parse()
