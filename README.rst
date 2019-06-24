===============
tester
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


Todos
-----

* write more tests
* implement the concept of virtual environments, i.e. software  must make sure that just one test will run in each virtual environment.