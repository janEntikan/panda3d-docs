.. _particle-renderers:

Particle Renderers
==================

Particle renderers add particles to the visible scene graph according to the
information stored in the particle objects and the type of renderer. All
particle renderers have the following parameters:

============ ===================================== =======================================================
**Variable** **Definition**                        **Values**
alpha_mode    Alpha setting over particle lifetime  PR_ALPHA_NONE, PR_ALPHA_OUT, PR_ALPHA_IN, PR_ALPHA_USER
user_alpha    Alpha value for ALPHA_USER alpha mode Boolean
============ ===================================== =======================================================


The following list contains the different types of renderers and their unique
parameters.

PointParticleRenderer
~~~~~~~~~~~~~~~~~~~~~


Renders particles as pixel points.

============ ============================================================= ================================
**Variable** **Definition**                                                **Values**
point_size    Width and height of points, in pixels                         [0, infinity)
start_color   Starting color                                                (r, g, b, a)
end_color     Ending color                                                  (r, g, b, a)
blend_type    How the particles blend from the start color to the end color ONE_COLOR, BLEND_LIFE, BLEND_VEL
blend_method  Interpolation method between colors                           LINEAR, CUBIC
============ ============================================================= ================================


ONE_COLOR: point is always the starting color.

BLEND_LIFE: color is interpolated from start to end according to the age of
the point

BLEND_VEL: color is interpolated between start to end according to the
velocity/terminal velocity.

LineParticleRenderer
~~~~~~~~~~~~~~~~~~~~


Renders particles as lines between their current position and their last
position.

============ ===================== ============
**Variable** **Definition**        **Values**
head_color    Color of leading end  (r, g, b, a)
tail_color    Color of trailing end (r, g, b, a)
============ ===================== ============


SparkleParticleRenderer
~~~~~~~~~~~~~~~~~~~~~~~


Renders particles star or sparkle objects, three equal-length perpendicular
axial lines, much like jacks. Sparkle particles appear to sparkle when viewed
as being smaller than a pixel.

============ ====================================================== ===============
**Variable** **Definition**                                         **Values**
center_color  Color of center                                        (r, g, b, a)
edge_color    Color of edge                                          (r, g, b, a)
birth_radius  Initial sparkle radius                                 [0, infinity)
death_radius  Final sparkle radius                                   [0, infinity)
life_scale    Whether or not sparkle is always of radius birth_radius NO_SCALE, SCALE
============ ====================================================== ===============


SpriteParticleRenderer
~~~~~~~~~~~~~~~~~~~~~~


Renders particles as an image, using a Panda3D texture object. The image is
always facing the user.

================ ========================================================================= =============
**Variable**     **Definition**                                                            **Values**
texture          Panda texture object to use as the sprite image                           (r, g, b, a)
color            Color                                                                     (r, g, b, a)
x_scale_flag       If true, x scale is interpolated over particle’s life                     Boolean
y_scale_flag       If true, y scale is interpolated over particle’s life                     Boolean
anim_angle_flag    If true, particles are set to spin on the Z axis                          Boolean
initial_X_Scale  Initial x scaling factor                                                  [0, infinity)
final_X_Scale    Final x scaling factor                                                    [0, infinity)
initial_Y_Scale  Initial y scaling factor                                                  [0, infinity)
final_Y_Scale    Final y scaling factor                                                    [0, infinity)
non_animated_theta If false, sets the counterclockwise Z rotation of all sprites, in degrees Boolean
alpha_blend_method Sets the interpolation blend method                                       LINEAR, CUBIC
alpha_disable     If true, alpha blending is disabled                                       Boolean
================ ========================================================================= =============


GeomParticleRenderer
~~~~~~~~~~~~~~~~~~~~


Renders particles as full 3D objects. This requires a geometry node.

============ =========================== ==========
**Variable** **Definition**              **Values**
geom_node     A geometry scene graph node
============ =========================== ==========
