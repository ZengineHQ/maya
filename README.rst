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

Right now, because the repo is private, the recommended way to install maya is to clone the repo and add it to system path and ``alias maya=maya-runner.py``.

Also install those packages using `pip`_::

    $ pip install docopt
    $ pip install requests
    $ pip install requests[security]

Alternatively, you could try the following::

    $ pip install -ve git+ssh://git@github.com/ZengineHQ/maya.git#egg=zn-maya

Consider managing python using something like `pyenv`_.

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
Build
-------------------

On the build step, maya looks at the plugin ``src`` folder and concatenates all js, html and css files into single files.

To develop plugins along with other developers, all code can be written using a ``wgn`` canonical namespace, e.g.::

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

Maya will replace all the occurrences of ``wgn-`` by the *dashed* namespace and then all the ocurrences of ``wgn`` by the *camelCased* namespace specified on maya.json.

------------
Reusing code
------------

More on this later... (``dependencies`` file)

------------------------
Sublime Text Integration
------------------------

You can create a Sublime Text build system, so every time you press Cmd + b, the code can be deployed to Zengine.

Tools -> Build System -> New Build System... ::

    {
        "cmd": ["maya-runner.py sublime-deploy $file_path"],
        "working_dir": "$project_path",
        "shell": true,
        "path": "/path/to/maya"
    }

Create a sublime project on the root (sibling of maya.json).


------------------------
Frontend Testing in Dev Mode
------------------------

To avoid having to do a full page reload while testing, a refresh button can be injected into a workspace while in dev mode. 

You can either install this `plugin`_ or insert the following code into the console: ::

    var myanchor = document.createElement('a');
    myanchor.href = "javascript:var theRoot = angular.element(document.querySelector('[ng-app=\"wizehive\"]')).injector().get('$rootScope');
    var theScope = angular.element(document.querySelector('[ng-controller=\"PluginDeveloperCntl\"]')).scope();theRoot.$broadcast('devplugin-changed', theScope.plugin.data, true);";
    myanchor.innerHTML = "<i class=\"icon icon-cw\"></i>";
    var li = document.createElement("li");
    li.appendChild(myanchor);
    var theUL = document.querySelector('.navbar-top-links.pull-right');
    theUL.insertBefore(li, theUL.firstChild);

.. _pip: http://www.pip-installer.org/en/latest/
.. _pyenv: https://github.com/yyuu/pyenv
.. _plugin: https://platform.zenginehq.com/?overlay=marketplace&marketplace.action=browse&marketplace.pluginId=331 
