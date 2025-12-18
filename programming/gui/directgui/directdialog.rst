.. _directdialog:

DirectDialog
============

DirectDialog objects are popup windows to alert or interact with the user. It
is invoked just like the other DirectGUI objects, but it also has some unique
keywords. Integral to DirectDialog are dialog_name, button_text_list,
button_image_list, and button_value_list. The dialog_name should ideally be the
name of the NodePath created to hold the object. The button lists contain the
various properties of the buttons within the dialog box. No maximum number of
buttons needs to be declared.

Panda3D contains a number of shortcuts for common dialog options. For example,
rather than specifying the rather common text list ("Yes","No"), there is a
YesNoDialog that functions exactly like a normal dialog but has button_text_list
already defined. The other similar dialogs are OkCancelDialog, OkDialog,
RetryCancelDialog, and YesNoCancelDialog.

================ ============================================================================================================================== =======================
Keyword          Definition                                                                                                                     Value
================ ============================================================================================================================== =======================
dialog_name       Name of the dialog                                                                                                             String
button_text_list   List of text to show on each button                                                                                            [Strings]
button_geom_list   List of geometry to show on each button                                                                                        [NodePaths]
button_image_list  List of images to show on each button                                                                                          [Image Paths]
button_value_list  List of values sent to dialog command for each button. If value is [] then the ordinal rank of the button is used as its value [Numbers]
button_hot_key_list Shortcut key for each button (the button must have focus)                                                                      [Characters]
button_size       4-tuple used to specify custom size for each button (to make bigger then geom/text for example)                                (Left,Right,Bottom,Top)
top_pad           Extra space added above text/geom/image                                                                                        Number
mid_pad           Extra space added between text/buttons                                                                                         Number
side_pad          Extra space added to either side of text/buttons                                                                               Number
button_pad_sf      Scale factor used to expand/contract button horizontal spacing                                                                 Number
command          Callback command used when a button is pressed. Value supplied to command depends on values in button_value_list                 Function
extra_args        Extra arguments to the function specified in command                                                                           [Extra Arguments]
fade_screen       If 1, fades screen to black when the dialog appears                                                                            0 or 1
================ ============================================================================================================================== =======================

YesNo Dialog Example
--------------------

.. code-block:: python

   import direct.directbase.DirectStart
   from direct.gui.OnscreenText import OnscreenText
   from direct.gui.DirectGui import *
   from direct.task import Task
   from direct.actor import Actor
   from direct.interval.IntervalGlobal import *
   from panda3d.core import *

   # Add some text
   bk_text = "DirectDialog- YesNoDialog Demo"
   text_object = OnscreenText(text=bk_text, pos=(0.85,0.85),
       scale=0.07, fg=(1, 0.5, 0.5, 1), align=TextNode.ACenter, may_change=1)

   # Add some text
   output = ""
   text_object = OnscreenText(text=output, pos=(0.95,-0.95),
       scale=0.07, fg=(1, 0.5, 0.5, 1), align=TextNode.ACenter, may_change=1)

   # Callback function to set text
   def item_sel(arg):
       if arg:
           output = "Button Selected is: Yes"
       else:
           output = "Button Selected is: No"
       text_object.set_text(output)

   # Create a frame
   dialog = YesNoDialog(dialog_name="YesNoCancelDialog", text="Please choose:",
                        command=item_sel)

   base.camera.set_pos(0, -20, 0)
   base.run()

.. note::
   The OkDialog causes an error if being created a second time after destroying
   it with ``my_ok_dialog.destroy()``. To solve this you can use:

   .. code-block:: python

      my_ok_dialog.cleanup()
