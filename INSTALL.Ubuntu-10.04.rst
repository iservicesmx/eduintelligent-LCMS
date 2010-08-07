======================
eduIntelligent LCMS
======================

Installing eduintelligent LCMS on Ubuntu 10.04
===============================================

Introduction
-------------

This guide will help you to setup your development environment with buildout, so
you can test and install eduintelligent LCMS. It is very specific to Ubuntu
Server 10.04, but if you have Ubuntu 10.04 the instructions will be just the
same.


Development environment
------------------------
Buildout_ is a very powerfull system to manage software configuration. Plone is
made by dozens of different software components/libraries (eggs) and Buildout can take care
of almost every detail of all of them, including versions, dependencies and, of
course, installation.

Buildout can install Plone in an *pseudo-isolated* environment. That is, it will
install, uninstall and manage all the eggs that Plone needs without needing
Administrator privileges and without the risk of breaking or cause configuration
conflicts between version packages.

Buildout still depends on the system Python and system-wide libraries/eggs. That's
why I call it *pseudo-isolated* environment. For a true isolated environment, you
might take a look at VirtualEnv_, however I will not cover it on this document.

.. _Buildout: http://www.buildout.org/
.. _VirtualEnv: http://pypi.python.org/pypi/virtualenv

We need to prepare the system so we can take advantage of Buildout's capabilities. So,
open your terminal (Or login if you are on ubuntu Server without X) and type:

    $ sudo aptitude update
    $ sudo aptitude safe-upgrade
    
    #Restart system if appropiate
    
    $ sudo aptitude install build-essential git-core subversion zlib1g-dev libpq-dev postgresql

Let's describe each package:
    * **build-essential**: Meta-package which will trigger the installation of compilers,
      utilities, and development libraries. All those (such as GCC), will be used to
      compile Python 2.4, python libraries, bindings and some parts of Plone and Zope.
    * **git-core**: We use git as the SCM for eduintelligent
    * **subversion**: We might need to get some python code trough svn
    * **zlib1g-dev**: zlib development libraries.
    * **libpq-dev**: Development libraries for PostgreSQL clients. It will be used by psycopg2.
    * **postgresql**: The postgresql server
    
    
Install Python 2.4
~~~~~~~~~~~~~~~~~~~~

Ubuntu 10.04 Ships Python 2.6 by default. Unfortunately, eduintelligent-LCMS needs
Plone 3. As we improve the code base, we will move to Plone 4, wich can work with
more recent versions of Python like 2.6.

Installing Python 2.4 is a very straightforward process. First, we need to download
it and unpack it:
    
    $ wget http://www.python.org/ftp/python/2.4.6/Python-2.4.6.tar.bz2
    
    $ tar -xjf Python-2.4.6.tar.bz2
    
    $ cd Python-2.4.6
    
Then build & install it:
    
    $ sudo mkdir -p /opt/Python2.4
    $ ./configure --prefix=/opt/python2.4 && make && sudo make install
    
Installing Python2.4 in ``/usr/local`` or ``/usr`` will create conflicts when you (or any
other program) that invokes python on the console without specifying the full path.
Also python scripts that use the hashbang ``#!/usr/bin/env python`` will be executed
with Python 2.4 instead of 2.6. This can break some system utilities and programs,
specially on Ubuntu Desktop.

There are some easy fixes for that:
    * Re-link ``/usr/bin/python`` to ``/usr/bin/python2.6``
    * Delete ``/usr/local/bin/python`` (which takes precedence over ``/usr/bin/python``)
    * Install it, as above, in a different path. (You will need to provide the
      full path whenever you want to call python2.4). You might also want to add
      the new python path to ``$PATH`` environment variable. Or you can also install it
      in your home folder. 
       
Let's continue. We have already installed python2.4 somewhere, and we know that
typing ``/opt/python2.4/bin/python2.4`` on the comandline will bring out the
python2.4 prompt.

Next step is to install PIP_. PIP takes care of downloading the right versions of
Python eggs, uncompress them in a temporal folder, build them and install them on a
specific location. Also takes care of dependencies. PIP is commanded by Buildout,
sou you will rarely use it directly.

.. _PIP: http://pip.openplans.org/

So, please, do not close that terminal window/session yet and type:

    $ wget http://peak.telecommunity.com/dist/ez_setup.py
    
    $ sudo /opt/Python2.4/bin/python2.4 ez_setup.py
    
    $ sudo /opt/Python2.4/bin/easy_install pip
    
    
We will also need to install ZopeSkel_. ZopeSkel is collection of Skeletons for
quickstarting Zope and Plone projects. It uses the templating engine of the Paste
project, which is a python development framework for web applications. It does a
lot of things and has very useful tools, but our focus now is to prepare our
development environment for eduIntelligent-LCMS and ZopeSkel and Paster are now
just software dependencies for our goals, and PIP will take care od them for us.
So please, dear reader, just go on with this tutorial, sooner or later you will
understand how everything is laid out.

:Interesting Note:
    The Django_ admin app, borrows some concepts from Paster.

.. _ZopeSkel: http://plone.org/products/zopeskel
.. _Django: http://djangoproject.com


So, as I was saying, we need to install ZopeSkel:

    $ sudo /opt/Python2.4/bin/pip install ZopeSkel
    
And that's it. Congratulations for reaching so far! Your development environment
is already set. Now we'll move along with the next section.


Download a copy of eduIntelligent-LCMS
---------------------------------------

The github repo for eduIntellignet-LCMS is here_. So, in any directory you want
(You no longer need root permissions for these), type this command:

.. _here: http://github.com/iservicesmx/eduintelligent-LCMS 

    $ git clone git://github.com/iservicesmx/eduintelligent-LCMS.git
    
This will clone the project and download a local copy for you. Now, let's enter to
the directory and run the bootstrap.py script:
    
    $ /opt/Python2.4/bin/python2.4 bootstrap.py
    
This command will create some directories, namely: ``bin/``, ``parts/``, ``eggs/`` and
``develop-eggs/``. Right now, the only file inside ``bin/`` is:

  * ``bin/buildout`` This script will download all the needed dependencies and store them on
    the ``eggs/`` directory. It will compile some packages if they need it. It will finally
    create the ``bin/instance`` script. Take a look at this script, see how buildout manipulares
    the python path. That's how Buildout does it's magic.

Run the ``bin/buildout`` script.
    
    $ bin/buildout
    
Sit back, relax, go for a cofee. It dependes on your bandwidth and your CPU power,
but this process takes some time.

Once this process has finished, buildout wil have created more scripts inside
the ``bin/`` directory:

  * ``bin/i18ndude`` This is a tool for managing translations. It can extract messages,
    merge them into on or more ``.po`` files and compile them.
  
  * ``bin/instance`` This is, perhaps, the more interesting script. It controls
    the Plone instance. It has several options and switches, but by now we will only
    use it to start Plone in foreground mode.
  
  * ``bin/zopepy`` This is a handy python interpreter that has the same list of python
    eggs that the ``bin/instance``. This is useful for testing and debugging.
       
We have our development environment set-up and Plone is ready to run. Let's move
on to configure all the needed parts for eduintelligent-LCMS.

Configure PostgreSQL and configure databases
---------------------------------------------
First step. Create the postgreSQL role ``eduintelligent`` that will be able to login
using password authentication and create databases, but will not be able to create
roles and will not have superuser powers:

    $ sudo su postgres
    
    $ createuser -ldPRS eduintelligent
    
You will be asked to supply a password for the new role. Next step is to enable
password authentication for recenlty added role. We need to edit the
file ``/etc/postgresql/8.4/main/pg_hba.conf`` (either logged in as postgres user or
root), and comment the following line:

    local   all         all                               trust
    
and then add the following line at the end of the file:

    local   all     eduintelligent     password

If you did the above logged in as the postgresql user, then exit:

    $ exit

Restart postgresql server

    $ sudo service postgresql-8.4 restart
    
Try to login as the eduintelligent user:

    $ psql -U eduintelligent -W postgresql

You should see the psql cmdline prompt. If you get a authentication error instead,
please review the configuration again and make sure you have restarted the
postgresql server.

Create the database and schemas
--------------------------------

Create the database ``eduintelligent_logs``. This database will be used by
``eduintelligent.loginhistory``, ``eduintelligent.database`` and
``eduintelligent.messages``:

    $ #Login as postgresql user if needed
    $ sudo su postgresql
    
    $ createdb --encoding=UTF-8 --owner=eduintelligent -U eduintelligent - W eduintelligent_logs

Go back to the eduintelligent-LCMS directory. Before you run the ``create_schemas.sh``
script, edit the following files and configure the user and password for the
eduintelligent role (Yes, the password you supplied in the section above.):
    
  * ``src/eduintelligent.loginhistory/eduintelligent/loginhistory/dbclasses.py``
  * ``src/eduintelligent.loginhistory/eduintelligent/loginhistory/dbclasses.py``
    
Finally run the script:

    $ ./create_schemas.sh
    

Install eduintelligent.policy
------------------------------

Run Plone in foreground mode:

    $ bin/instance fg
    
Open a web browser and point it to ``http://localhost:8080/`` . Login as admin (The
password is in the ``buildout.cfg`` file).

Create a Plone site and then install ``eduintelligent.policy`` product. It will
install all the dependencies.

Configure membrane
-------------------
We need to associate the eduMember content-type with TrainingCenter content-tye.
Open your browser and point it to
``http://localhost:8080/YourPloneSite/membrane_tool/manage_main``. There's a
multiple selection menu. Select ``TrainingCenter`` and ``eduMember``. Click on
``Sumbit``.

TODO LIST
-----------
  * Configure PloneArticle
  * Configure eduIntelligent Database in the plone control panel.
  * Lot's of details I'm probably missing.
  