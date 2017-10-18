Events
------

As demo files are parsed events are emitted. Callbacks can be
registered for each event. The arguments passed to the callbacks
are described for each event below.

-----

.. _event_baseline_create:

``baseline_create``
  An instance baseline has been created.

  Callback arguments:
      :class_id: Server class ID.
      :table: Data table for this server class.
      :baseline: Instance baseline object.

.. _event_change:

``change``
  An entity's property has been changed.

  Callback arguments:
      :entity: Entity being created or updated.
      :table_name: Table which contains the property being updated.
      :var_name: Name of property being updated.
      :value: New value of property.

.. _event_datatable_ready:

``datatable_ready``
  Data table has been created and all pending baselines have been handled.

  Callback arguments:
      :table: Data table instance

.. _event_demo_packet:

``demo_packet``
  An event for each type of demo packet will be emitted. Demo packets
  are instances of SVC and NET classes.

  Callback arguments:
        :class_name: Name of packet.
        :packet: Instance of approprite NET\_ or SVC\_ class.


  The following is a list of all demo packet types:

  .. include:: demopacket.rst


.. _event_end:

``end``
  Processing has finished.


.. _event_game_event:

``game_event``
  An event for the specific type of game event will be emitted.

  Callback arguments:
      :event: Game event object.
      :msg: The original message of type SVC_GameEvent which triggered
            this event.

  The following is a list of game events for CS:GO:

  .. include:: game_events.rst

.. _event_string_table_update:

``string_table_update``
  An entry in a string table has been updated.

  Callback arguments:
      :table: String table instance.
      :index: Index of entry being updated.
      :entry: The updated entry.
      :user_data: User data for the updated entry.

.. _event_tick_start:

``tick_start``
  Start of new game tick.

  Callback arguments:
        :current_tick: Tick which has just started.

.. _event_tick_end:

``tick_end``
  End of game tick.

  Callback arguments:
        :current_tick: Tick which has just ended.

.. _event_user_msg:

``user_message``
  An event for the specific type of user message will be emitted for each
  user message command. A callback can be added for each specific type of
  user message.

  .. code-block:: python

          def um_chat(msg_type, msg):
              assert msg_type == 'SayText2'

          d = demofile(...)
          d.add_callback('SayText2', um_chat)


  Callback arguments:
        :message_type: One of types listed below.
        :message: Instance of the specied user message class.


  The following is a list of all user message types:

  .. include:: user_messages.rst
