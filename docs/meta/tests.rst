*************
Writing tests
*************

We are using pytest_ in order to write our tests.

How to run
==========

Before running the tests, make sure the dependencies in ``requirements-dev.txt`` are installed.
Running the tests will clean your mongodb and remove every extensions, so make sure you made a backup if needed. Tests **must** go inside ``tests/`` folder.

You might need to install ``chromedriver`` (chrome driver) or ``geckodriver`` (Firefox driver).

To run the tests, the simplest way is to execute ``pytest tests/ --driver [Firefox|Chrome]`` to launch the whole test suite. If you want to only execute the tests included in ``tests/test_foo.py``, then you can use the command ``pytest tests/test_foo.py --driver [Firefox|Chrome]``.

If you have any problems with the tests, it might be because they are launched with ``python2`` instead of ``python3``. In this case, instead of running ``pytest [args]``, run ``python3 -m pytest [args]``

Test architecture
=================

We can divide our testing architecture into three parts.

Travis
------

We are using travis_ for continuous integrations. Each time a commit 
is pushed on ``master``, ``travis`` will install everything ``tozti`` needs
to run and also execute our test suite. This enables us to see in a glance
if the modifications we made are breaking something.

Unit testing
------------

Unit testing is one of the two types of tests we have. It consists in 
testing some functions independently from all others. As they are very long
to write, only the topological sort and the mechanism to find extensions
have unit tests.

Integration testing
-------------------

Integration tests do not target a single functions (like unit tests), 
but tests the behaviour of the whole of Tozti. We use intensive integration testing
in order to test the storage, the router and the js-router mechanisms.

Here, a test consists of:

- loading an extension 
- launching tozti
- testing one functionality
- closing tozti

Writing tests for Tozti with pytest
====================================

Writing a test with pytest is easy. First, you need to create a python file prefixed by ``tests_`` which will contain your test function. A test file can contain several test functions and should import ``pytest``.
A test function must have a name starting with ``test_``. Its name must be explicit as it will be displayed upon test failure. Finally, a test fails if it raises an exception. Assertions are convenient when writing tests. ``assert expr`` will do nothing if ``expr`` evaluates to ``False``, and will fail otherwhise.

A test should:

- not rely on data not defined inside of the test. If you have 10 tests, then the result of executing the test must be independent of the order in which they are executed
- be precise and test only one thing
- change rarely. Each time you edit a test it looses part of its purpose.

Passing parameters to a test
----------------------------

Most of the time your tests will not take any arguments and will be self contained. But sometimes, you will want to write a generic test and use it on different inputs and outputs.
For exemple, to test a function ``foo`` that takes two arguments and computes their sum, you could do this::

    def test_foo_1():
        assert(foo(3, 4) == 7)
    def test_foo_2():
        assert(foo(0, 4) == 4)

This is correct, but it is more convenient to write::

    @pytest.mark.parametrize("a, b, expected", [(3, 4, 7), (0, 4, 4)])
    def test_foo(a, b, expected):
        assert(foo(a, b) == expected)

Here, we are *parameterizing* the test over the arguments ``a``, ``b`` and ``expected``. 

The notion of Fixture
---------------------

You may want to execute something before and after your test. For instance launch a background process, initialize the connection to a database and make sure it is correctly closed. That is what Pytest's fixture_ is for. I will not dwell on it too much, as there are several online ressources.

You can find one particularly useful fixture in the file ``tests/conftest.py``. This fixture, called ``tozti``, will:

- install a series of extension if needed
- launch tozti
- execute Tozti
- completly close Tozti

The following is a simple example of how to use it::

    @pytest.mark.extensions(["extension1", "extension2", ...., "extensionn"])
    def test_ultra_super_genial(tozti):
        test_something

The line ``@pytest.mark.extensions(...)`` is used to specify the names of the extensions which should be installed. The extensions themselves must be put in the folder ``tests/extensions``.
You can then use the object ``tozti`` (which is a ``subprocess.Popen`` object if ``tozti`` could be launched, ``None`` otherwise) in order to perform some operations. For exemple, the function ``tozti_still_running(tozti)`` returns ``True`` if ``tozti`` is still running.


Other fixture are also present in ``tests/conftest.py``. The fixture ``db`` will load a mongodb database and empty it before the test for exemple. Notice that importing ``tests/conftest.py`` is not needed in order to use the fixtures as this file is automatically loaded by ``pytest``. As such you should beware with defining variables named ``db`` or ``tozti``. 
You can find other usefull fonctions inside ``tests/commons.py``. To include a function defined there (for exemple ``tozti_still_running``), please add the following line::

    from tests.commons import tozti_still_running




.. _pytest: https://docs.pytest.org/en/latest/
.. _travis: https://travis-ci.org
.. _fixture: https://docs.pytest.org/en/latest/fixture.html
