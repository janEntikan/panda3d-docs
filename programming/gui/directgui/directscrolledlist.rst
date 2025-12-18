.. _directscrolledlist:

DirectScrolledList
==================

DirectScrolledLists create a list of DirectGuiWidgets. Each object is created
individually and can then be added to the list. Some useful methods are:

.. code-block:: python

   add_item(item, refresh)
   get_item_index_for_item_id(self, item_id)
   get_selected_index(self)
   get_selected_text(self)
   remove_item(self, item, refresh)
   scroll_by(self, delta)
   scroll_to(self, index, centered)
   scroll_to_item_id(self, item_id, centered)
   select_list_item(self, item)

In the above methods, item is a new item, either a string or a DirectGUI
element, and item_id is an arbitrary identification number for each item (but
not necessarily a zero-based index number). The item_id for a new item is the
return value of add_item(). The centered parameter is a boolean; if true, the
list scrolls so that the given index is centered, otherwise it scrolls so that
the index is on top of the list.

The items option should either be a list of DirectGUI items or of strings. If
strings are used, the item_make_function (and possibly item_make_extra_args) option
should be defined to point to a function that will take the supplied string,
the index, and the extra args as parameters and return a DirectGUI object to
insert into the list. If items is a list of strings and item_make_function is
not specified, it will create a list of DirectLabels. item_make_function is
redundant if a list of DirectGUI objects is passed into items to begin with.

DirectScrolledLists come with two scroll buttons for navigating through the
list. By default, they both start at (0,0,0) relative to the list with size 0,
and their positions and size need to be set explicitly. You can set any of the
values except relief appearance as you initialize the list:

.. code-block:: python

   my_scrolled_list = DirectScrolledList(incButton_propertyName=value,
                                       decButton_propertyName=value)

inc_button scrolls forward through the list; dec_button backward. Note that this
only works for initialization. To change a property of the scroll buttons later
in the program, you must use:

.. code-block:: python

   my_scrolled_list.inc_button['property_name'] = value
   my_scrolled_list.dec_button['property_name'] = value

Unlike the first method, this does not work with NodePath options like position;
use ``set_pos(...)`` for that.

For example, the following creates a scrolled list and resizes and moves the
buttons appropriately.

.. code-block:: python

   my_scrolled_list = DirectScrolledList(
       incButton_pos=(.5, 0, 0), incButton_text="Inc",
       decButton_pos=(-.5, 0, 0), decButton_text="Dec")
   my_scrolled_list.inc_button['frame_size'] = (0, 0.2, 0, 0.2)
   my_scrolled_list.dec_button['frame_size'] = (0, 0.2, 0, 0.2)
   my_scrolled_list.inc_button['text_scale'] = .2
   my_scrolled_list.dec_button['text_scale'] = .2

================= ==================================================== ==============================
Keyword           Definition                                           Value
================= ==================================================== ==============================
command           Function called when the list is scrolled            Function
extra_args         Extra arguments to the function specified in command [Extra Arguments]
text_scale        Scale of the displayed text                          (sx,sz)
items             List of the objects to appear in the ScrolledList    [DirectGUI items] or [Strings]
num_items_visible   Number of items visible at a time                    Number
force_height       Forces the height of the list to be a given number   Number
item_make_function  Function that makes DirectGUI items out of strings   Function
item_make_extra_args Extra arguments to the function in item_make_function  [Extra Arguments]
================= ==================================================== ==============================

A small example on how to use it:

.. code-block:: python

   from direct.directbase import DirectStart
   from direct.gui.DirectGui import *
   from panda3d.core import *

   b1 = DirectButton(text=("Button1", "click!", "roll", "disabled"),
                     text_scale=0.1, border_width=(0.01, 0.01),
                     relief=2)

   b2 = DirectButton(text=("Button2", "click!", "roll", "disabled"),
                     text_scale=0.1, border_width=(0.01, 0.01),
                     relief=2)

   l1 = DirectLabel(text="Test1", text_scale=0.1)
   l2 = DirectLabel(text="Test2", text_scale=0.1)
   l3 = DirectLabel(text="Test3", text_scale=0.1)

   num_items_visible = 4
   item_height = 0.11

   my_scrolled_list = DirectScrolledList(
       decButton_pos=(0.35, 0, 0.53),
       decButton_text="Dec",
       decButton_text_scale=0.04,
       decButton_borderWidth=(0.005, 0.005),

       incButton_pos=(0.35, 0, -0.02),
       incButton_text="Inc",
       incButton_text_scale=0.04,
       incButton_borderWidth=(0.005, 0.005),

       frame_size=(0.0, 0.7, -0.05, 0.59),
       frame_color=(1,0,0,0.5),
       pos=(-1, 0, 0),
       items=[b1, b2],
       num_items_visible=num_items_visible,
       force_height=item_height,
       itemFrame_frameSize=(-0.2, 0.2, -0.37, 0.11),
       itemFrame_pos=(0.35, 0, 0.4),
   )

   my_scrolled_list.add_item(l1)
   my_scrolled_list.add_item(l2)
   my_scrolled_list.add_item(l3)

   for fruit in ['apple', 'pear', 'banana', 'orange']:
       l = DirectLabel(text=fruit, text_scale=0.1)
       my_scrolled_list.add_item(l)

   base.run()
