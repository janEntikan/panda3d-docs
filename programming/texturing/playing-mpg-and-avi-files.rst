.. _playing-mpg-and-avi-files:

Playing MPG and AVI files
=========================

Panda now supports AVI format for textures in Panda.

Usage
-----

.. code-block:: python

   my_movie_texture = loader.load_texture("my_movie.avi")
   my_object.set_texture(my_movie_texture)

The movie subsystem is implemented using FFMPEG. Therefore, it supports all of
the formats that FFMPEG supports. The functions to control the movie are as
follows:

.. code-block:: python

   movie.play()
   movie.stop()
   movie.set_time(t)
   movie.get_time()
   movie.set_loop_count(n)
   movie.get_loop_count()
   movie.set_play_rate(speed)
   movie.get_play_rate()
   movie.is_playing()

If you want to hear the movie's audio as well, you need to load it twice: once
as a texture, and once as a sound file:

.. code-block:: python

   my_sound = loader.load_sfx("my_movie.avi")

Then, you can synchronize the video to the audio:

.. code-block:: python

   my_movie_texture.synchronize_to(my_sound)

From that point forward, playing the audio will cause the texture to update.
This is more accurate than synchronizing the video manually.

For powers-of-two limited graphics hardware
-------------------------------------------

If your graphics hardware does not support non power-of-two textures, your movie
texture size would be shifted up to the next larger power of two size. For
example, if you have a movie of 640 x 360 in size, the generated texture would
be actually 1024 x 512. The result is a texture that contains a movie in the
lower-left corner, and a black pad region to the right and upper portion of the
texture.

To work around this limit, you have to display just the lower-left portion of
the texture. To see a complete demonstration of this process, see the Media
Player sample program.

Issues
------

The video texture works by decoding on a frame by frame basis and copying into
the texture buffer. As such, it is inadvisable to use more than a few high res
video textures at the same time.

Certain encoding formats do not work. So far, DV format has been determined
incompatible with Panda.
