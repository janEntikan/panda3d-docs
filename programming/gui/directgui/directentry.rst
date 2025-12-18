.. _directentry:

DirectEntry
===========

The DirectEntry creates a field that accepts text entered by the user. It
provides a blinking cursor and support for backspace and the arrow keys. It
can accept either a single line of text, with a fixed width limit (it doesn't
scroll), or it can accept multiple word-wrapped lines.

================= ========================================================================================= =================
Keyword           Definition                                                                                Value
================= ========================================================================================= =================
initial_text       Initial text to load in the field                                                         String
entry_font         Font to use for text entry                                                                Font object
width             Width of field in screen units                                                            Number
num_lines          Number of lines in the field                                                              Integer
cursor_keys        True to enable the use of cursor keys (arrow keys)                                        0 or 1
obscured          True to hide passwords, etc.                                                              0 or 1
command           Function to call when enter is pressed(the text in the field is passed to the function)   Function
extra_args         Extra arguments to the function specified in command                                      [Extra Arguments]
rollover_sound     The sound made when the cursor rolls over the field                                       Sound File Path
click_sound        The sound made when the cursor inside the field                                           Sound File Path
focus             Whether or not the field begins with focus (focus_in_command is called if true)             0 or 1
background_focus   If true, field begins with focus but with hidden cursor, and focus_in_command is not called 0 or 1
focus_in_command    Function called when the field gains focus                                                Function
focus_in_extra_args  Extra arguments to the function specified in focus_in_command                               [Extra Arguments]
focus_out_command   Function called when the field loses focus                                                Function
focus_out_extra_args Extra arguments to the function specified in focus_out_command                              [Extra Arguments]
================= ========================================================================================= =================

Example
-------

.. code-block:: python

   import direct.directbase.DirectStart
   from direct.gui.OnscreenText import OnscreenText
   from direct.gui.DirectGui import *
   from panda3d.core import *

   #add some text
   bk_text = "This is my Demo"
   text_object = OnscreenText(text=bk_text, pos=(0.95, -0.95), scale=0.07,
                             fg=(1, 0.5, 0.5, 1), align=TextNode.ACenter,
                             may_change=1)

   #callback function to set  text
   def set_text(text_entered):
       text_object.set_text(text_entered)

   #clear the text
   def clear_text():
       entry.enter_text('')

   #add text entry
   entry = DirectEntry(text = "", scale=.05, command=set_text,
   initial_text="Type Something", num_lines = 2, focus=1, focus_in_command=clear_text)

   #run the tutorial
   base.run()

This example implements a text entry widget typically seen in web pages.
