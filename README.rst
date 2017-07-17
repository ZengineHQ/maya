=======
maya
=======

Zengine Plugin Build Automation.

With maya, developers can code Zengine plugins in a way they are used to:

* using any IDE of choice
* using version control
* testing code
* spliting code into different files
* reusing code between plugins
* collaborating on plugins with other developers

------------
Installation
------------

Maya should be run as Docker container, so be sure that you have `Docker`_ installed::

    docker --version

Clone the maya repo and build the Docker image::

    $ cd path/to/maya
    $ docker build -t maya .

`Add a shell alias <http://stackoverflow.com/questions/8967843/how-do-i-create-a-bash-alias>`_::

    alias maya="docker run -it --rm -v `pwd`:/usr/src/plugin-repo --name maya-running maya"

-----
CLI
-----

After installation, you will have a ``maya`` command on your terminal that has this basic interface::

  maya (build | deploy | publish) [<plugin>] [--frontend | --backend] [--env=ENV]

You can issue commands like::

  maya build
  maya deploy portals
  maya deploy --frontend
  maya publish portals --env=stage

Rules are:

* If no plugin is specified, the task will be done for all plugins listed in ``maya.json``.
* If no "area" is specified, the task will be done for both frontend and backend code.
* If no environment is specified, the default specified in ``maya.json`` will be used.

------------------
Maya Project Setup
------------------

A maya project consists of code for one or more Zengine plugins. You can also reuse code among plugins.

All code is written using a generic namespace, ``wgn``, that gets replaced during the ``build`` task.

Every developer should keep his or her own copy of a plugin, separate from other developers, and separate from the production copy. Each copy will result in a different plugin ID, namespace and route. For this reason, every maya task is done against an ``environment``.

An environment contains the Zengine API endpoint (dev, stage, production), the developer access token, and the developer-specific plugin settings.

Environments are defined in a file called ``maya.json`` and look as follows::

  {
    "environments": {
      "stage": {
        "api_endpoint": "stage-api.zenginehq.com",
        "access_token": "[insert developer token here]",
        "plugins": {
          "some-plugin1": {
            "id": 256,
            "namespace": "pluginOneNamespace",
            "route": "/plugin-one-route",
            "services": {
              "some-plugin1-service": {
                "id": 101
              }
            }
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

To use maya, your project structure must be as follows::

  your-project/

    plugins/

      some-plugin1/
        src/
        plugin-register.js

      some-plugin2/
        src/
        plugin-register.js

    backend/

      some-plugin1-service/
        _runner/*
        package.json
        plugin.js

    maya.json

---------------
Build Execution
---------------

On the build step, maya looks at the plugin's ``src`` folder and concatenates all JS, HTML and CSS files into the respective single files that Zengine expects.

Code can and should be written using the ``wgn`` canonical namespace, e.g.::

    plugin.controller('wgnVotingMainCtrl', ['$scope', 'wgnVotingPluginBootstrap', 'wgnVotingPluginModel',
        function ($scope, bootstrap, plugin) {
            // ...
        }
    ]);

::

    <script type="text/ng-template" id="wgn-voting-list">
        <div ng-controller="wgnVotingListController">
            ...
        </div>
    </script>

Maya will replace all the occurrences of ``wgn-`` by the *dashed* namespace and then all the occurrences of ``wgn`` by the *camelCased* namespace specified in ``maya.json``.

In addition, all occurrences of the magic string ``{replace-route}`` will be replaced with the route specified in ``maya.json``.

----------------------
Using Backend Services
----------------------

Please refer to the `backend docs`_.

------------
Reusing Code
------------

It is possible to use external modules in a maya codebase. This enables code abstraction and reuse among multiple plugins and developers.

Suppose we want to include a module called ``zn-module-grid`` in the ``some-plugin1`` plugin.

In ``plugins/some-plugin1`` you can have this minimal ``package.json`` file::

    {
      "dependencies": {
        "zn-underscore": "git@gitlab.com:zn-modules-frontend/module-grid.git#1.0.0"
      }
    }

In ``plugins/some-plugin1``, execute ``npm install`` – which will download the ``zn-module-grid`` code to ``plugins/some-plugin1/node_modules/zn-module-grid``.

During the maya build process, maya will scan for ``package.json`` dependencies and include those dependencies in the build path. In this example, files inside ``plugins/some-plugin1/node_modules/zn-module-grid/src`` will be included in the corresponding JS, HTML and CSS build files.

External modules can be hosted anywhere, as long as they are reachable via ``npm install``. For now, we are using `a GitLab group <https://gitlab.com/zn-modules-frontend>`_ to store all modules.

The file structure and conventions of an external maya module are exactly the same as a maya-enabled project. Maya will include files in the `src` folder and ignore all the rest. You can use sibling folder and file locations to store tests, docs, etc.

If a module is listed as a dependency in ``package.json`` but doesn't have an ``src`` folder, it won't be included in the scan path. This module may be one with a custom structure that is dealt with via scripting outside of maya (e.g., it could be a module that contains other modules, aka "mother repo").

----------------------------
Frontend Testing in Dev Mode
----------------------------

To avoid having to do a full page reload while testing, this `plugin`_ can be installed. It will inject a refresh button into the workspace that can be used to refresh your plugin code while in dev mode.

.. _Docker: https://docs.docker.com/docker-for-mac/install/
.. _pip: http://www.pip-installer.org/en/latest/
.. _plugin: https://platform.zenginehq.com/?overlay=marketplace&marketplace.action=browse&marketplace.pluginId=331
.. _backend docs: /BACKEND.rst
