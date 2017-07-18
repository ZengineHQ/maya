============
Contributing
============

To make sure you're running maya using your local changes, change the alias
so the container runs with your local changes mounted (replace ``path/to/maya`` by your local path)::
  alias maya='docker run -it --rm -v $(pwd):/usr/src/plugin-repo -v $HOME/path/to/maya:/usr/src/app --name maya-running maya'

Install py.test and flake8::

  cd maya
  py.test maya
  flake8 maya

``py.test -s maya`` will display print output.

``py.test -f maya`` will run tests in loop.
