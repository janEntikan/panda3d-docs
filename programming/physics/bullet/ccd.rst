.. _ccd:

Bullet Continuous Collision Detection
=====================================

CCD is short for Continuous Collision Detection, which is a workaround for a
common problem in game physics: a fast moving body might not collide with an
obstacle if in one frame it is "before" the obstacle, and in the next one it
is already "behind" the obstacle. At no frame the fast moving body overlaps
with the obstacle, and thus no response is created. This is what CCD is for.
CCD checks for collisions in between frames, and thus can prevent fast moving
objects from passing through thin obstacles.

Bullet has built-in support for CCD, but bodies have to be configured properly
to enable CCD checks.

When checking for collision in between frames Bullet does not use the full
collision shape (or shapes) of a body - this would make continuous collision
detection too slow. Instead Bullet uses a sphere shape, the so-called "swept
sphere". "swept" because the sphere is swept from the original position to the
new position of the body. So, in order to enable CCD checks on a body we have
to setup this sphere, and a CCD motion threshold:

.. only:: python

   .. code-block:: python

      body_np.node().set_ccd_motion_threshold(1e-7)
      body_np.node().set_ccd_swept_sphere_radius(0.50)

.. only:: cpp

   .. code-block:: cpp

      TODO

We have to set up the swept sphere only on the fast moving dynamic bodies.
There is no need to do anything for the static or slow moving obstacles.

One particular use for CCD is firing a bullet (bullet is lowercase here,
indicating that a projectile is meant, not the Bullet physics engine). Below
is a sample showing one way to implement shooting bullets.

.. only:: python

   .. code-block:: python

      bullets = []

      def remove_bullet(task):
        if len(bullets) < 1: return

        bullet_np = bullets.pop(0)
        world.remove_rigid_body(bullet_np.node())

        return task.done

      def shoot_bullet(ccd):
        # Get from/to points from mouse click
        p_mouse = base.mouse_watcher_node.get_mouse()
        p_from = Point3()
        p_to = Point3()
        base.cam_lens.extrude(p_mouse, p_from, p_to)

        p_from = render.get_relative_point(base.cam, p_from)
        p_to = render.get_relative_point(base.cam, p_to)

        # Calculate initial velocity
        v = p_to - p_from
        v.normalize()
        v *= 10000.0

        # Create bullet
        shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))
        body = BulletRigidBodyNode('Bullet')
        body_np = render.attach_new_node(body)
        body_np.node().add_shape(shape)
        body_np.node().set_mass(2.0)
        body_np.node().set_linear_velocity(v)
        body_np.set_pos(p_from)
        body_np.set_collide_mask(BitMask32.all_on())

        # Enable CCD
        body_np.node().set_ccd_motion_threshold(1e-7)
        body_np.node().set_ccd_swept_sphere_radius(0.50)

        world.attach_rigid_body(body_np.node())

        # Remove the bullet again after 1 second
        bullets.append(body_np)
        task_mgr.do_method_later(1, remove_bullet, 'remove_bullet')

.. only:: cpp

   .. code-block:: cpp

      TODO

Most of the code is related to finding the initial velocity vector for the
bullet, which is calculated from the mouse position when shooting the bullet.
