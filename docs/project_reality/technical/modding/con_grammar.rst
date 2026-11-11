
.con File Grammar
=================

``.con`` files are the main setup files for Battlefield 2. They control everything in the game, like weapons, maps, objects, and player settings. You can run these files using the game engine or through the in-game console. However, commands that span multiple lines, such as ``beginRem``, only work when run by the engine. Battlefield 2 improves upon the basic commands of Battlefield 1942 by adding a simple scripting language to its console commands, allowing for loops and complete conditional statements.

Comments
--------

The ``.con`` file language allows for two kinds of comments: block comments and line comments.

Block Comments
^^^^^^^^^^^^^^

Block comments can cover several lines. They start with ``beginRem`` and finish with ``endRem``. Any text placed between these two commands is completely ignored by the program.

.. code-block:: text

   beginRem
   This entire block of text
   is a comment and will be ignored.
   endRem

Line Comments
^^^^^^^^^^^^^

Line comments start with the ``rem`` keyword. Anything written after ``rem`` on the same line is considered a comment and is ignored.

.. code-block:: text

   rem This is a single-line comment.

Statements
----------

A statement is made up of a command, which can be followed by several arguments separated by spaces. If an argument includes spaces, you should put it in double quotes.

.. code-block:: text

   commandClass.commandMethod argument1 "argument with spaces"

The specific command you use will determine how many arguments it needs and what kind of information those arguments should contain. To get a full list of all available commands, you can use the GNU ``strings`` tool on the :file:`bf2.exe` file.

CRD Argument Type
-----------------

Many commands use a Continuous Random Distribution (CRD) argument. This argument helps create a random number based on specific settings. A CRD argument always has four parts, separated by forward slashes (/).

.. code-block:: text

   CRD_TYPE/Number1/Number2/Symmetry

The first part, ``CRD_TYPE``, tells the system what kind of random distribution to use. The second and third parts are always numbers, and their meaning changes depending on the distribution type. The fourth part, ``Symmetry``, is a simple on/off switch (a boolean flag).

.. list-table::
   :header-rows: 1

   * - CRD_TYPE
     - Description
   * - ``CRD_NONE``
     - Gives back ``Number1`` exactly as it is, with no changes. ``Number2`` is not used.
   * - ``CRD_UNIFORM``
     - Provides a random whole number between ``Number1`` and ``Number2``, including both ``Number1`` and ``Number2``.
   * - ``CRD_EXPONENTIAL``
     - Generates a random number using an exponential distribution, where ``Number1`` is the average value. ``Number2`` is not used.
   * - ``CRD_NORMAL``
     - Produces a random number following a normal (bell curve) distribution. Here, ``Number1`` is the average, and ``Number2`` controls how spread out the numbers are (the variance).

The fourth part, Symmetry, is a boolean value (either ``0`` or ``1``). If you set it to ``1``, there's a 50% chance that the final random number will be made negative. If it's set to ``0``, the number will not be changed.

CRD_TYPE Examples
^^^^^^^^^^^^^^^^^

``ObjectTemplate.TimeToLive CRD_NONE/240/0/0``
   The ``TimeToLive`` will be set precisely to ``240``. This command works exactly like simply typing ``240``.

``ObjectTemplate.TimeToLive CRD_UNIFORM/2/7/0``
   ``TimeToLive`` will be a random whole number chosen from ``2`` to ``7``, including both ``2`` and ``7``.

``ObjectTemplate.rotationalSpeedInDof CRD_EXPONENTIAL/-20/0/1``
   This command uses an exponential distribution with an average value (mean) of ``-20``. The outcome will be a random number. Because the symmetry flag is set to ``1``, there's an equal chance (50/50) that this number will be either positive or negative.

   .. note::

      It's worth noting that ``CRD_EXPONENTIAL`` is often used incorrectly. For instance, if you use a command like ``ObjectTemplate.initRotation CRD_EXPONENTIAL/0/180/1``, it will always give you ``0``. This is because the average (mean) is set to ``0``, and the ``180`` argument is simply ignored.

``ObjectTemplate.rotationalSpeedInDof CRD_EXPONENTIAL/-20/0/1``
   The exponential distribution creates a curve that quickly goes down and then flatens out. It's figured out by using the formula ``-mean * ln(random(0,1))``. First, a random number between ``0`` and ``1`` (not including ``0`` or ``1``) is picked. Then, its natural logarithm is found, and this result is multiplied by the negative of the average (mean).

   For example, if the random number is ``0.1``, its natural logarithm is about ``-2.3``. If the average (mean) is ``-20``, the calculation would be ``-(-20) * -2.3 = -46``. Since the symmetry flag is ``1`` (meaning true), there's a 50% chance that this ``-46`` will become ``46``.

   .. note::

      People often use this distribution incorrectly. For example, if you use ``ObjectTemplate.initRotation CRD_EXPONENTIAL/0/180/1``, it will always give you ``0`` because the average (mean) is ``0``, and the ``180`` argument is simply ignored.

``ObjectTemplate.timeToLive CRD_NORMAL/2/3.5/0``
   A normal distribution looks like a bell curve. The second number is the average (mean), and the third number is the variance, which tells you how spread out the numbers will be. The fourth number, symmetry, matters when the average is not ``0``.

   Variance helps define the range where about 80% of the numbers generated will land. In this case, with an average of ``2`` and a variance of ``3.5``, roughly 80% of the numbers will be between ``2 +/- 3.5`` (which is from ``-1.5`` to ``5.5``). The other 20% will be outside this range.

`Source <https://bfmods.com/mdt/scripting/CRD.html>`_

Variables
---------

You need to define variables before you use them, and they must follow a specific naming rule, which is a simplified version of `Hungarian Notation <https://en.wikipedia.org/wiki/Hungarian_notation>`_.

**Mutable Variables** (variables that can be changed) must begin with ``v_``.

.. code-block:: text

   var v_dongs = test

**Immutable Variables** (constants, which cannot be changed) must begin with ``c_``.

.. code-block:: text

   const c_butts = test

To save the result of a command into a variable, add ``-> v_varname`` after the command.

.. code-block:: text

   someCommandThatReturnsAValue -> v_result

Conditionals
------------

Conditional statements work like standard programming logic. They check an 'expression' to decide what to do next.

- ``if ... endIf``
- ``if ... elseIf ... endIf``
- ``while ... endWhile``

Expressions
^^^^^^^^^^^

An expression generally follows this simple structure:

.. code-block:: text

   <variable> <comparator> <value>

:Variable: This can be any variable name that starts with either ``v_`` or ``c_``.
:Comparator: This is a comparison operator, such as ``==`` (equals), ``!=`` (not equals), ``>`` (greater than), ``>=`` (greater than or equals), ``<`` (less than), or ``<=`` (less than or equals). You might also see text versions like ``equals`` and ``notEquals``.
:Value: This is a specific piece of text or a number. If it's text and contains spaces, it needs to be enclosed in quotes.

return, include, and run
^^^^^^^^^^^^^^^^^^^^^^^^

``return``
   This command stops the current :file:`.con` file from running and gives control back to the file that started it.

``include``
   This command tells the system to read and process another :file:`.con` file. Unlike ``run``, ``include`` doesn't create a separate environment (scope) for the included file.

``run``
   :Arguments: You can send information (arguments) to the file being run. These arguments will show up as ``v_arg1``, ``v_arg2``, and so on, in the file that is called.
   :Scope: ``run`` creates a new, isolated environment (scope) for the file it calls, whereas ``include`` does not.

   This command tells the system to read and process another :file:`.con` file.

Examples
^^^^^^^^

This file, :file:`main.con`, uses other :file:`.con` files.

.. code-block:: text
   :caption: main.con

   rem Main file to demonstrate `include` and `run`.
   var v_someValue = 10
   echo v_someValue
   run sub.con 1 2 3
   echo v_someValue

The file below, :file:`sub.con`, is started by :file:`main.con` and demonstrates how arguments are passed and how scopes work differently.

.. code-block:: text
   :caption: sub.con

   rem Sub-file to show `return`, arguments, and scope.
   if v_arg1 == 1
      rem v_arg1, v_arg2, v_arg3 are set to 1, 2, 3 from :file:`main.con`
      echo "Arguments passed correctly:" v_arg1 v_arg2 v_arg3
      rem Since `run` was used, `v_someValue` from :file:`main.con` is not in scope here.
      echo "v_someValue from main.con is NOT in scope here."
      rem return stops execution of this file.
      return
   endIf

When you run :file:`main.con`, you'll see ``v_someValue`` with its original value before the ``run`` command. Inside :file:`sub.con`, ``v_arg1``, ``v_arg2``, and ``v_arg3`` will be accessible, but ``v_someValue`` from :file:`main.con` won't be. The ``return`` command will then stop :file:`sub.con` from running further.

Final Example
-------------

This example shows you how to check if a file exists and, if it doesn't, how to copy it over.

.. code-block:: text

   var v_tst
   fileManager.fileExists movies/menu.bik -> v_tst
   if v_tst == 0
      fileManager.copyFile ../../mods/bf2/movies/menu.bik movies/menu.bik
      fileManager.copyFile ../../mods/bf2/movies/menu_loggedin.bik movies/menu_loggedin.bik
   endIf
