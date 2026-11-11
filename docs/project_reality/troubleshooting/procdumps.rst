Getting Crash Dumps
===================

To help us debug crashes, please use **ProcDump**. This program creates crash dumps, which are crucial for finding out what caused the problems.

.. important::

   ProcDump Download
      https://docs.microsoft.com/en-us/sysinternals/downloads/procdump

   ProcDump Installation Video Tutorial
      https://www.youtube.com/watch?v=154wpSwhfPU

Standard Method
---------------

#. Open Command Line as Administrator.
#. Go to the location where you saved ProcDump.

   .. code-block:: text
      :caption: Example

      cd C:\Users\User\Downloads\Procdump

#. Run ``procdump.exe -w -mm -b -e 1 -g prbf2.exe``.
#. Start PR.

Alternative Method
------------------

#. Create a shortcut to :file:`procdump.exe` and add the arguments to its target path.

   Arguments
      ``-w -mm -b -e 1 -g prbf2.exe``
   Example
      ``C:\Users\User\Downloads\Procdump\procdump.exe -w -mm -b -e 1 -g prbf2.exe``

#. Run the shortcut as administrator *after* you have launched PR.

Aftermath
---------

ProcDump will close when PR closes. It will generate a :file:`.dmp` file in the same directory as :file:`procdump.exe`. Please upload this :file:`.dmp` file and send it to the developers.
