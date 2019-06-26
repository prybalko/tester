===============
Tester
===============

Command-line software in Python 3 that is able to run tests implemented in Python and Bash scripts.

Features
--------


* Run tests implemented in Python (the choice of testing framework is free) and Bash scripts.
* Start the test runs in the background.
* Query the status of running tests (during the test run and afterwards).

Tech
----

Tester uses some open source projects to work properly:

* `pytest <https://docs.pytest.org/en/latest/>`_ - test framework.
* `pytest-xdist <https://docs.pytest.org/en/3.0.0/xdist.html>`_ - pytest plugin for distributed testing.
* `peewee <http://docs.peewee-orm.com/en/latest/>`_ - simple and small ORM.

Usage
-----

Install from source using pip:

.. code-block:: bash

    git clone git@github.com:prybalko/tester.git
    pip install -e tester

Python >= 3.6 supported.

Run tests in the foreground

.. code-block:: bash

	$ tester run
	=================== test session starts =========================================
	platform linux -- Python 3.7.3, pytest-4.6.3, py-1.8.0, pluggy-0.12.0
	collected 3 items

	tests/test_dummy.sh .                                                      [ 33%]
	tests/test_sample.py ..                                                    [100%]

	=================== 3 passed in 0.21 seconds ====================================

Run tests in the background

.. code-block:: bash

	$ tester start

Get tests status

.. code-block:: bash

	$ tester status
	 id        pid       test                                              status
	 1         23401     tests/test_dummy.sh                               passed
	 2         23401     tests/test_sample.py::test_mytest                 passed
	 3         23401     tests/test_sample.py::TestClass::test_one         passed


Distributed testing
___________________
Distributed test execution is delegated to `pytest-xdist <https://docs.pytest.org/en/3.0.0/xdist.html>`_ plugin.

To send tests to multiple CPUs, type:

.. code-block:: bash

	$ tester start -n NUM

To send tests to remote SSH account:

.. code-block:: bash

	$ tester start -d --tx ssh=myhostpopen --rsyncdir mypkg mypkg

This will synchronize your mypkg package directory to a remote ssh account and then locally collect tests and send them to remote places for execution.

The basic command to run tests on multiple platforms is:

.. code-block:: bash

	$ tester start --dist=each --tx=spec1 --tx=spec2

For more information please see `pytest-xdist <https://docs.pytest.org/en/3.0.0/xdist.html>`_  docs.

Todos
-----

* add more tests
