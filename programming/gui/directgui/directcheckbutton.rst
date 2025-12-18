.. _directcheckbutton:

DirectCheckButton
=================

DirectCheckButtons are similar to buttons, except they represent a binary state
that is toggled when it is clicked. Their usage is almost identical to regular
buttons, except that the text area and box area can be modified separately.

============== ================================================================================== ========================
Keyword        Definition                                                                         Value
============== ================================================================================== ========================
text_scale     Scale of the displayed text                                                        (sx,sz)
indicator_value The initial boolean state of the checkbox                                          0 or 1
box_image       Image on the checkbox                                                              Image Path
box_image_color  Color of the image on the box                                                      (R,G,B,A)
box_image_scale  Scale of the displayed image                                                       Number
box_placement   Position of the box relative to the text area                                      ‘left’,’right’
box_relief      Relief appearance of the checkbox                                                  DGG.SUNKEN or DGG.RAISED
box_border      Size of the border around the box                                                  Number
command        Command the button performs when clicked(0 or 1 is passed, depending on the state) Function
extra_args      Extra arguments to the function specified in command                               [Extra Arguments]
command_buttons Which mouse button must be clicked to do the command                               LMB, MMB, or RMB
rollover_sound  The sound made when the cursor rolls over the button                               Sound File Path
click_sound     The sound made when the cursor clicks on the button                                Sound File Path
press_effect    Whether or not the button sinks in when clicked                                    <0 or 1>
============== ================================================================================== ========================

Example
-------

.. code-block:: python

   import direct.directbase.DirectStart
   from direct.gui.OnscreenText import OnscreenText
   from direct.gui.DirectGui import *
   from panda3d.core import *

   # Add some text
   bk_text = "This is my Demo"
   text_object = OnscreenText(text=bk_text, pos=(0.95,-0.95), scale=0.07,
                             fg=(1, 0.5, 0.5, 1), align=TextNode.ACenter,
                             may_change=1)

   # Callback function to set  text
   def set_text(status):
       if status:
           bk_text = "Checkbox Selected"
       else:
           bk_text = "Checkbox Not Selected"
   text_object.set_text(bk_text)

   # Add button
   b = DirectCheckButton(text = "CheckButton" ,scale=.05,command=set_text)

   # Run the tutorial
   base.run()

Programmatically changing the indicator_value
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you programmatically want to change the checkbutton's indicator_value, you need
to call ``set_indicator_value`` afterwards to update the checkbutton, like:

.. code-block:: python

   b["indicator_value"] = True
   b.set_indicator_value()

box_image and other box\* keywords
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Just as DirectButton may be passed a 4-tuple of values to be used in the four
button states, the box\* keyword arguments may be supplied with multiple entries
to denote the unchecked and checked state. To supply arguments to be used in the
two states of the checkbox, construct a 3-tuple of values with a 'None' in the
final entry, i.e. (unchecked, checked, None). For example, to set two different
images for the unchecked and checked states:

.. code-block:: python

   box_image = ("path_to_disabled_image.jpg", "path_to_enabled.jpg", None)
