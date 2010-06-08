=======================
eduIntelligent LCMS
=======================
Introduction
-----------------------

eduintelligent is a LCMS (Learning Content Management System) developed on top of
plone by iServices de México.

Key features:
+ Allow instructors to upload education material, either by TTW (trough the web)
  edition or by uploading SCORM (Only v1.2) or zip content packages.
+ Implements basic user activity tracking according to SCORM 1.2 standard.
+ Students can run Exams or quizzes and get graded.
+ Exams and quizzes are folderish objects that accept Question items. Currently
  we have support for choice-type and open-type questions.
+ The main content object is a Trainning Center. Each Trainning center has its
  own news, events, Courses Folder, Polls, Users and groups. Each Trainning Center
  can be independent of each other.
+ Special package for tracing user's connectivity (Database independent of ZODB)


Installation
-------------

By now, these instructions are for Ubuntu Linux, so Please, adapt them to your 
system.

First, we need to install development packages.

    $ sudo aptitude install build-essential python-paste python-dev ipython git-core subversion gedit-plugins python-pip zlib1g-dev
    
Ubuntu 10.04 no longer ships python 2.4. If Python 2.4 is available on your 
package manager, you can use it instead. Just make sure you install python2.4 and
python2.4-dev or their equivalent in yout packaging system.

So, to compile python 2.4 we need to do:

 $ wget http://www.python.org/ftp/python/2.4.6/Python-2.4.6.tar.bz2
 $ tar -xjf Python-2.4.6.tar.bz2
 $ cd Python-2.4.6 
 $ ./configure && make && sudo make install
    
Next step is to download and install easy_install.

 $ wget http://peak.telecommunity.com/dist/ez_setup.py
 $ sudo python2.4 ez_setup.py
    
Next step is ZopeSkel.

 $ sudo easy_install-2.4 ZopeSkel
    
Now your computer is set and ready to run the buildout. So, go to the directory
where this README.txt file is. Run the following command:

 $ python2.4 bootstrap.py

This will install zc.buildout for you.

Installing dependencies for postgresql
--------------------------------------
  $ sudo aptiude install libpq-dev


Running buildout
-----------------
To create an instance of Plone and eduintelligent run:

 $ bin/buildout

This will download Plone's eggs and products for you, as well as other
dependencies (Including PIL), create a new Zope 2 installation (unless you specified
an existing one when you ran "paster create"), and create a new Zope instance
configured with these products.

You can start your Zope instance by running:

 $ bin/instance start

or, to run in foreground mode:

 $ bin/instance fg

To run unit tests, you can use:

 $ bin/instance test -s my.package

Using a different Python installation
--------------------------------------

Buildout will use your system Python installation by default. However, Zope
2.10 (and by extension, Plone) will only work with Python 2.4. You can verify
which version of Python you have, by running:

 $ python -V

If that is not a 2.4 version, you need to install Python 2.4 from
http://python.org. If you wish to keep another version as your main system
Python, edit buildout.cfg and add an 'executable' option to the "[buildout]"
section, pointing to a python interpreter binary:

 [buildout]
 ...
 executable = /path/to/python

Working with buildout.cfg
-------------------------

You can change any option in buildout.cfg and re-run bin/buildout to reflect
the changes. This may delete things inside the 'parts' directory, but should
keep your Data.fs and source files intact.

To save time, you can run buildout in "offline" (-o) and non-updating (-N)
mode, which will prevent it from downloading things and checking for new
versions online:

 $ bin/buildout -Nov

=======================
Looking at source code
=======================

All the code from eduintelligent has been eggified and is under the src/ directory.

This is a brief description of each package:

TODO: Write a description of each package

=============
Using Windows
=============

To use buildout on Windows, you will need to install a few dependencies which
other platforms manage on their own.

Here are the steps you need to follow (thanks to Hanno Schlichting for these):

Python (http://python.org)
--------------------------

  - Download and install Python 2.4.4 using the Windows installer from
    http://www.python.org/ftp/python/2.4.4/python-2.4.4.msi
    Select 'Install for all users' and it will put Python into the
    "C:\Python24" folder by default.

  - You also want the pywin32 extensions available from
    http://downloads.sourceforge.net/pywin32/pywin32-210.win32-py2.4.exe?modtime=1159009237&big_mirror=0

  - And as a last step you want to download the Python imaging library available
    from http://effbot.org/downloads/PIL-1.1.6.win32-py2.4.exe

  - If you develop Zope based applications you will usually only need Python 2.4
    at the moment, so it's easiest to put the Python binary on the systems PATH,
    so you don't need to specify its location manually each time you call it.

    Thus, put "C:\Python24" and "C:\Python24\Scripts" onto the PATH. You can
    find the PATH definition in the control panel under system preferences on
    the advanced tab at the bottom. The button is called environment variables.
    You want to add it at the end of the already existing PATH in the system
    section. Paths are separated by a semicolons.

  - You can test if this was successful by opening a new shell (cmd) and type
    in 'python -V'. It should report version 2.4.4 (or whichever version you
    installed).

    Opening a new shell can be done quickly by using the key combination
    'Windows-r' or if you are using Parallels on a Mac 'Apple-r'. Type in 'cmd'
    into the popup box that opens up and hit enter.


Subversion (http://subversion.tigris.org)
-----------------------------------------

  - Download the nice installer from
    http://subversion.tigris.org/files/documents/15/35379/svn-1.4.2-setup.exe

  - Run the installer. It defaults to installing into
    "C:\Program Files\Subversion".

  - Now put the install locations bin subfolder (for example
    "C:\Program Files\Subversion\bin") on your system PATH in the same way you
    put Python on it.

  - Open a new shell again and type in: 'svn --version' it should report
    version 1.4.2 or newer.


MinGW (http://www.mingw.org/)
-----------------------------

  This is a native port of the gcc compiler and its dependencies for Windows.
  There are other approaches enabling you to compile Python C extensions on
  Windows including Cygwin and using the official Microsoft C compiler, but this
  is a lightweight approach that uses only freely available tools. As
  it's used by a lot of people chances are high it will work for you and there's
  plenty of documentation out there to help you in troubleshooting problems.

  - Download the MinGW installer from
    http://downloads.sourceforge.net/mingw/MinGW-5.1.3.exe?modtime=1168794334&big_mirror=1

  - The installer will ask you which options you would like to install. Choose
    base and make here. It will install into "C:\MinGW" by default. The install
    might take some time as it's getting files from sourceforge.net and you
    might need to hit 'retry' a couple of times.

  - Now put the install location's bin subfolder (for example "C:\MinGW\bin") on
    your system PATH in the same way you put Python on it.

  - Test this again by typing in: 'gcc --version' on a newly opened shell and
    it should report version 3.4.2 or newer.


Configure Distutils to use MinGW
--------------------------------

  Some general information are available from
  http://www.mingw.org/MinGWiki/index.php/Python%20extensions for example but
  you don't need to read them all.

  - Create a file called 'distutils.cfg' in "C:\Python24\Lib\distutils". Open it
    with a text editor ('notepad distutils.cfg') and fill in the following lines:

    [build]
    compiler=mingw32

    This will tell distutils to use MinGW as the default compiler, so you don't
    need to specify it manually using "--compiler=mingw32" while calling a
    package's setup.py with a command that involves building C extensions. This
    is extremely useful if the build command is written down in a buildout
    recipe where you cannot change the options without hacking the recipe
    itself. The z2c.recipe.zope2install used in ploneout is one such example.
