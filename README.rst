``demoparser`` is a library for parsing CS:GO demo files.

As the file is processed events are emitted for which callbacks can
be registered. This is how 

Quick start
-----------

1. Install::

        pip install demoparser

2. Parse a demo::

   >>> from demoparser.demofile import DemoFile
   >>> data = open('/path/to/demofile', 'rb').read()
   >>> df = DemoFile(data)
   >>> df.parse()
