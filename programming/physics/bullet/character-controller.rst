.. _character-controller:

Bullet Character Controller
===========================

Bullet comes with a simple character controller already included. A character
controller is a class intended to provide a simple way of controlling a player
(or NPC) object the way we are used to from many first-person-shooters or
role-playing-games. Achieving satisfying results for character movement is
usually a difficult thing when using "physicals", e. g. rigid bodies. The
solution is to use so-called "kinematic" objects, that is objects which don't
respond to forces, and instead get moved by pushing/turning them around by
hand.

Notice: The module panda3d.bullet doesn't implement it's own character
controller. It simple exposes the character controller which comes with the
Bullet physics engine. This character controller is still in an early stage,
and it lacks a few features. In particular, Bullet does not implement a proper
interaction between dynamic bodies and the character controller.

Setup
-----

The following code will first create a shape with total height of 1.75 units
and total width of 0.8 units. We have to subtract twice the radius from the
total height in order to get the length of the cylindrical part of the capsule
shape.

.. only:: python

   .. code-block:: python

      from panda3d.bullet import BulletCharacterControllerNode
      from panda3d.bullet import BulletCapsuleShape
      from panda3d.bullet import ZUp

      height = 1.75
      radius = 0.4
      shape = BulletCapsuleShape(radius, height - 2*radius, ZUp)

      player_node = BulletCharacterControllerNode(shape, 0.4, 'Player')
      player_np = self.world_np.attach_new_node(player_node)
      player_np.set_pos(-2, 0, 14)
      player_np.set_h(45)
      player_np.set_collide_mask(BitMask32.all_on())

      world.attach_character(player_np.node())

.. only:: cpp

   .. code-block:: cpp

      float height = 1.75;
      float radius = 0.4;

      PT(BulletCapsuleShape) c_shape = new BulletCapsuleShape(radius, height -2 * radius);
      PT(BulletCharacterControllerNode) controller;
      controller = new BulletCharacterControllerNode(c_shape, 0.4f, name.c_str());
      physics_world->attach_character(controller);

      NodePath cha_np = window->get_render().attach_new_node(controller);
      cha_np.set_pos(-2, 0, 14);
      cha_np.set_h(45);
      cha_np.set_collide_mask(mask1);

Moving
------

Now that we have a character controller within our scene we need to control
it's movement. The following code snippet shows one way of moving the
character controller by keyboard input. Of course a character controller
representing a NPC (non-player character) would not read the keyboard state
but have the linear velocity (``speed``) and the angular velocity (``omega``)
computed by some kind of AI algorithm.

.. only:: python

   .. code-block:: python

      def process_input(self):
          speed = Vec3(0, 0, 0)
          omega = 0.0

          if input_state.is_set('forward'): speed.set_y( 3.0)
          if input_state.is_set('reverse'): speed.set_y(-3.0)
          if input_state.is_set('left'):    speed.set_x(-3.0)
          if input_state.is_set('right'):   speed.set_x( 3.0)
          if input_state.is_set('turn_left'):  omega =  120.0
          if input_state.is_set('turn_right'): omega = -120.0

          self.player.set_angular_movement(omega)
          self.player.set_linear_movement(speed, True)

.. only:: cpp

   .. code-block:: cpp

      void character_move (std::vector<bool> *KeyMap) {
              LVecBase3 speed = LVecBase3(0, 0, 0);
              float omega = 0.0;

              if (KeyMap->at(MOVE_FORWARD)) { speed.set_y (3.0); }
              if (KeyMap->at(MOVE_REVERSE)) { speed.set_y (-3.0); }
              if (KeyMap->at(MOVE_LEFT)) { speed.set_x (-3.0); }
              if (KeyMap->at(MOVE_RIGHT)) { speed.set_x (3.0); }
              if (key_map->at(TURN_LEFT)) { omege = 120.0; }
              if (key_map->at(TURN_RIGHT)) { omega = -120.0 }

              controller->set_linear_movement(speed, true);
              controller->set_angular_movement(omega);
      }

Jumping
-------

Next we want to make the character controller jump. The following code snippet
shows a sample method which will make the character jump. We could for example
call this method when the player presses a specific key.

After setting the maximum jump height and the initial upward speed we need to
trigger the jump using the
:meth:`~panda3d.bullet.BulletCharacterControllerNode.do_jump()` method.

.. only:: python

   .. code-block:: python

      def do_jump(self):
          self.player.set_max_jump_height(5.0)
          self.player.set_jump_speed(8.0)
          self.player.do_jump()

.. only:: cpp

   .. code-block:: cpp

      void do_jump(void ) {
          controller->set_max_jump_height(5.0)
          controller->set_jump_speed(8.0)
          controller->do_jump()
      }

It is possible to check whether the character controller is airborne using the
:meth:`~panda3d.bullet.BulletCharacterControllerNode.is_on_ground()` method.

Crouching
---------

Finally we want the character to crouch or duck. To achieve this we simply
change the scale of the character's collision shape. Here in this example we
reduce the vertical dimension to 60 percent (0.6) when crouching, while the
normal vertical scale is 1.0. We don't change the horizontal scales. In a more
realistic example, one would have the player enter a crouching animation.

Since we have the visual node of the player reparented to the character
controller node it will automatically change its scale to match the player.

.. only:: python

   .. code-block:: python

      self.crouching = False

      def do_crouch(self):
          self.crouching = not self.crouching
          sz = self.crouching and 0.6 or 1.0

          self.player.get_shape().set_local_scale(Vec3(1, 1, sz))

          self.player_np.set_scale(Vec3(1, 1, sz) * 0.3048)
          self.player_np.set_pos(0, 0, -1 * sz)
