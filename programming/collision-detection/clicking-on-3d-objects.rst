.. _clicking-on-3d-objects:

Clicking on 3D Objects
======================

The simplest way to click on 3D objects in Panda3D is to use very simplistic
collision detection coupled with event processing. First, after a
:class:`.CollisionTraverser` and a :class:`.CollisionHandler` have been set up,
attach a :class:`.CollisionRay` node to the camera. This node will have its
"from" collision mask set to :meth:`.GeomNode.get_default_collide_mask()` in
order to be as general as possible.

.. only:: python

   .. code-block:: python

      picker_node = CollisionNode('mouse_ray')
      picker_np = camera.attach_new_node(picker_node)
      picker_node.set_from_collide_mask(GeomNode.get_default_collide_mask())
      picker_ray = CollisionRay()
      picker_node.add_solid(picker_ray)
      my_traverser.add_collider(picker_np, my_handler)

.. only:: cpp

   .. code-block:: cpp

      PT(MouseWatcher) mouse_watcher;
      PT(CollisionRay) picker_ray;
      CollisionTraverser my_traverser = CollisionTraverser("ctraverser");
      PT(CollisionHandlerQueue) my_handler;
      PT(CollisionNode) picker_node;
      NodePath picker_np;

      picker_node = new CollisionNode("mouse_ray");
      picker_np = camera.attach_new_node (picker_node);
      picker_node->set_from_collide_mask(GeomNode::get_default_collide_mask());
      picker_ray = new CollisionRay();
      picker_node->add_solid(picker_ray);
      my_handler = new CollisionHandlerQueue();
      my_traverser.add_collider(picker_np, my_handler);

For any object that you want to be pickable you should add a flag to it. The
easiest way is to use the :meth:`~.NodePath.set_tag()` function:

.. only:: python

   .. code-block:: python

      object1.set_tag('my_object_tag', '1')
      object2.set_tag('my_object_tag', '2')

.. only:: cpp

   .. code-block:: cpp

      object1.set_tag("my_object_tag", "1");
      object2.set_tag("my_object_tag", "2");

The above example sets the tag ``'my_object_tag'`` on two objects in your graph
that you want to designate as pickable. We will check for the presence of this
tag after we get the response back from the collision system.

.. only:: python

   Because :ref:`Actors <loading-actors-and-animations>` use a different
   set-up, the collision system will return the geometry but not the NodePath.
   Use
   :meth:`object.set_python_tag('myObjectTag', 1) <.NodePath.set_python_tag>`
   and :meth:`object.get_python_tag('my_object_tag') <.NodePath.get_python_tag>`
   instead to return the node path of an Actor.

Now assume that the function ``my_function()`` is set up to be called for the
``'mouse1'`` event. In ``my_function()`` is where you call
:meth:`pickerRay.set_from_lens(origin, destX, destY) <.CollisionRay.set_from_lens>`.
This makes the ray's origin ``origin`` and the ray's vector the direction from
``origin`` to the point (``dest_x``, ``dest_y``).

.. only:: python

   .. code-block:: python

      def my_function():
          # First we check that the mouse is not outside the screen.
          if base.mouse_watcher_node.has_mouse():
              # This gives up the screen coordinates of the mouse.
              mpos = base.mouse_watcher_node.get_mouse()

          # This makes the ray's origin the camera and makes the ray point
          # to the screen coordinates of the mouse.
          picker_ray.set_from_lens(base.cam_node, mpos.x, mpos.y)

.. only:: cpp

   .. code-block:: cpp

      void my_function() {
        if (!mouse_watcher->has_mouse()) {
          // The mouse is probably outside the screen.
          return;
        }

        // This gives up the screen coordinates of the mouse.
        LPoint2 mpos = mouse_watcher->get_mouse();

        // This makes the ray's origin the camera and makes the ray point
        // to the screen coordinates of the mouse.
        picker_ray->set_from_lens(window->get_camera(0), mpos.get_x(), mpos.get_y());
      }

After this, you now call the traverser like any other collision, get the
closest object and "pick" it.

.. only:: python

   .. code-block:: python

      def my_function():
          mpos = base.mouse_watcher_node.get_mouse()
          picker_ray.set_from_lens(base.cam_node, mpos.get_x(), mpos.get_y())

          my_traverser.traverse(render)
          # Assume for simplicity's sake that my_handler is a CollisionHandlerQueue.
          if my_handler.get_num_entries() > 0:
              # This is so we get the closest object
              my_handler.sort_entries()
              picked_obj = my_handler.get_entry(0).get_into_node_path()

The node returned by the collision system may not be the object itself, but
might be just a part of the object. In particular, it will be one of the
GeomNodes that make up the object. (The :class:`.GeomNode` class contains
the visible geometry primitives that are used to define renderable objects in
Panda3D.) Since your object might consist of more than one :class:`.GeomNode`,
what you probably would prefer to get is the :class:`.NodePath` that represents
the parent of all of these GeomNodes that is, the :class:`.NodePath` that you
set the ``'my_object_tag'`` tag on above. You can use
:meth:`.NodePath.find_net_tag()` to return the parent :class:`.NodePath` that
contains a specified tag. (There are also other, similar methods on
:class:`.NodePath` that can be used to query the tag specified on a parent
node, such as :meth:`~.NodePath.get_net_tag()` and
:meth:`~.NodePath.has_net_tag()`.
For simplicity, we shall restrict this example to
:meth:`~.NodePath.find_net_tag()`.)

.. only:: python

   Now you can edit ``my_function()`` to look like this:

   .. code-block:: python

      def my_function():
          mpos = base.mouse_watcher_node.get_mouse()
          picker_ray.set_from_lens(base.cam_node, mpos.get_x(), mpos.get_y())
          my_traverser.traverse(render)
          # Assume for simplicity's sake that my_handler is a CollisionHandlerQueue.
          if my_handler.get_num_entries() > 0:
              # This is so we get the closest object.
              my_handler.sort_entries()
              picked_obj = my_handler.get_entry(0).get_into_node_path()
              picked_obj = picked_obj.find_net_tag('my_object_tag')
              if not picked_obj.is_empty():
                  handle_picked_object(picked_obj)
