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

After the files were copied, Maya will execute the command ``npm install --production`` in the dist folder.

Why? When developing in Node.js, we should be able to use ``devDependencies``, which are just like ``dependencies``, except that they are only relevant during development. Examples include test and linting libs.
We shouldn't send those to production – not only because they are not relevant but also because they increase a lot the zip file size.
