``devinstall`` is a simple-stupid script I use to help me set up and
update develoment and production environments with Python packages I
maintain. The trick is that many of the packages I develop at the
library are depend on the current local version on my workstation at
development time, so I have them installed in "editable" mode, but
this is undesirable for deployment. ``devinstall`` allows me to
install and update different packages from git repositories in
different ways--that is, it allows me to selectively install some
packages in editable mode, while relying on the git repositories for
updates with others. I can quickly set up a new development or
production machine.


.. code:: bash

    $ devinstall install --help
    usage: devinstall install [-h] [-v VENV] repofile

    Take the path of a file with an address of git repositories on
    each line. Gives the option to install directly from the repo or
    to clone the repo and install as editable. optionally, supply the
    name for a virtual environment that will be created where the
    packages will be installed.

    positional arguments:
    repofile              type: Path

    optional arguments:
    -h, --help            show this help message and exit
    -v VENV, --venv VENV  type: Path; default: None

.. code:: bash

    $ devinstall update --help
    usage: devinstall update [-h] [-v VENV] repofile

    Take the path of a file with an address of git repositories on
    each line. This file should contain repos previously installed
    with `devinstall install`. This will update any files that are not
    installed locally. optionally, supply the name for a virtual
    environment where things are installed.

    positional arguments:
    repofile              type: Path

    optional arguments:
    -h, --help            show this help message and exit
    -v VENV, --venv VENV  type: Path; default: None
