=================================
Build and Deploy Backend Services
=================================

When deploying a backend service, Maya will generate a zip file and upload it to Zengine.

The build process was designed to generate a zip file that only has the essential files required to run your backend code in production.
That said, it is important to understand how the build process works, to make sure the backend code is structured accordingly.

-----------
Dist folder
-----------

On the build process, Maya will: 

* copy the essential files to a folder named ``dist``
* do some additional work on that folder
* zip that ``dist`` folder to a file named ``dist.zip``

Files and folders that will be copied to ``dist`` are:

* _runner
* lib
* src
* plugin.js
* package.json

The ``_runner`` and ``lib`` folders are the ones from the original zip file.
The ``plugin.js`` and ``package.json`` are standard for Zengine backend services.

The ``src`` folder is meant to include the files that you want to ship to production. Usually those are additional javascript files.
Why? This way, you can have test and docs files in other folders and maya won't bother to include those in the zip file.

After the files were copied, Maya will execute the command ``npm install --production`` in the dist folder.

Why? When developing in Node.js, we should be able to use ``devDependencies``, which are just like ``dependencies``, except that they are only relevant during development. Examples include test and linting libs.
We shouldn't send those to production – not only because they are not relevant but also because they increase the zip file size. That command will generate a ``node_modules`` folder inside ``dist`` that only has the production modules.

-------------
Common issues
-------------

**"The plugin runner or libraries code can't be modified."**

Download the zip from Zengine again, delete ``_runner`` and ``lib`` (both on the backend service folder and the corresponding dist folder). Paste the ``_runner`` and ``lib`` from the downloaded zip on the backend service folder.

Warning: Sometimes when you download a ``_runner`` folder from Zengine, it doesn't come with ``_runner/config.json``. Make sure you have that file.
