=======
maya
=======

Zengine Plugin Build Automation.

With maya, developers can code zengine plugins in a way they are used to – e.g. they can:

* use any editor of choice
* use version control
* test code
* split code into different files
* reuse code between plugins
* collaborate on the same plugin with other developers

------------
Installation
------------

Use `pip`_::

    $ pip install -ve git+ssh://git@github.com/ZengineHQ/maya.git#egg=zn-maya --user

It's also good to install this optional package::

    $ sudo pip install requests[security]

-----
CLI
-----

After installation, you will have a ``maya`` command on your terminal that has this basic interface::

  maya (build | deploy | publish) [<plugin>] [<environment>]

So you can issue commands like::

  maya build
  maya deploy portals
  maya publish portals stage

Rules are:

* If no plugin was specified, the task will be done for all plugins.
* If no environment was specified, the default one will be used.

---------------
Maya Project
---------------

A maya project basically consists of code for one or more zengine plugins. You can also have code that is reused among plugins. 
All code is written using a generic namespace that gets replaced during the ``build`` task.

Every developer should have a zengine account with its own versions of the plugins (i.e., different ids, namespaces and routes). For this reason, every maya task is done against an ``environment``.

An environment contains the zengine api endpoint (dev, stage, prod), the developer access token and the developer-specific plugin settings. Environments are specified in a config file called ``maya.json`` which looks similar to::

  {
    "environments": {
      "stage": {
        "api_endpoint": "stage-api.zenginehq.com",
        "access_token": "[insert developer token here]",
        "plugins": {
          "some-plugin1": {
            "id": 256,
            "namespace": "pluginOneNamespace",
            "route": "/plugin-one-route"
          },
          "some-plugin2": {
            "id": 257,
            "namespace": "pluginTwoNamespace",
            "route": ""
          }
        },
        "default": true
      }
    }
  }

To use maya, your project structure must be the following::

  your-project/
    maya_build/

    plugins/
      common/
        reusable-code1/
          src/
        reusable-code2/
          src/

      some-plugin1/
        src/
        dependencies
        plugin-register.js

      some-plugin2/
        src/
        dependencies
        plugin-register.js

    maya.json

-------------------
Canonical Namespace
-------------------

More on this later... (``wgn`` on angular components, ``wgn-`` on html templates)

------------
Reusing code
------------

More on this later... (``dependencies`` file)

------------------------
Sublime Text Integration
------------------------

More on this later... (instructions to create sublime build system that uses ``sublime-deploy`` task)

.. _pip: http://www.pip-installer.org/en/latest/
