.. _directslider:

DirectSlider
============

Use a DirectSlider to make a slider, a widget that allows the user to select a
value between a bounded interval.

A DirectSlider consists of a long bar, by default horizontal, along with a
"thumb", which is a special button that the user may move left or right along
the bar. The normal DirectGui parameters such as frame_size, geom, and relief
control the look of the bar; to control the look of the thumb, prefix each of
these parameters with the prefix "thumb\_", e.g. ``thumb_frameSize``.

If you want to get (or modify) the current value of the slider (by default, the
range is between 0 and 1), use ``my_slider['value']``.

=========================================================== ============================================================================= ==========================================
Keyword                                                     Definition                                                                    Value
=========================================================== ============================================================================= ==========================================
value                                                       Initial value of the slider                                                   Default is 0
range                                                       The (min, max) range of the slider                                            Default is (0, 1)
page_size                                                    The amount to jump the slider when the user clicks left or right of the thumb Default is 0.1
orientation                                                 The orientation of the slider                                                 HORIZONTAL or VERTICAL
command                                                     Function called when the value of the slider changes (takes no arguments)     Function
extra_args                                                   Extra arguments to the function specified in command                          [Extra Arguments]
thumb_geom, thumb_relief, thumb_text, thumb_frameSize, etc. Parameters to control the look of the thumb                                   Any parameters appropriate to DirectButton
=========================================================== ============================================================================= ==========================================

Example
-------

.. code-block:: python

   import direct.directbase.DirectStart
   from direct.gui.DirectGui import *

   def show_value():
       print(slider['value'])

   slider = DirectSlider(range=(0,100), value=50, page_size=3, command=show_value)

   base.run()

"range" sets values between 0 and 100 "value" sets initial value to 50
"page_size" sets the step between mouseclicks to 3 (approximately) "command"
calls the show_value-function implemented above
