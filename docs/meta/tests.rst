*************
Writing tests
*************

We are using pytests_ in order to write our tests.

How to run
==========

Before running the tests, make sure the dependencies in `requirements-dev.txt` are installed.
Running the tests will clean your mongodb and remove every extensions, so make sure you made a backup if needed. Tests **must** go inside `tests/` folder.

You might need to install `chromedriver` (chrome driver) or `geckodriver` (Firefox driver).

To run the tests, the simplest way is to execute `pytest tests/ --driver [Firefox|Chrome]` to launch the whole test suite. If you want to only execute the tests included in `tests/test_foo.py`, then you might launch the command `pytest tests/test_foo.py --driver [Firefox|Chrome]`.

If you have problem with the tests, it might be because they are launched with `python2` instead of `python3`. In this case, instead of running `pytest [args]`, run `python3 -m pytest [args]`

Test architecture
=================

We can divide our testing architecture in three parts.

Travis
------

We are using travis_ for continuous integrations. Each time a commit 
is pushed on `master`, `travis` will install every things `tozti` needs
to run and also execute our test suite. This enable us to see in a glance
if the modifications we made are breaking something.

Unit testing
------------

Unit testing is one of the two types of tests we have. It consists on 
testing some functions independently from all other. As they are very long
to write, only the topological sort and the mechanism to find extensions
have unit tests.

Integration testing
-------------------

Integration tests are not targeting a single functions (like unit tests), 
but are testing how the whole of Tozti behave. We uses integrations testing
intensively to test the storage, the router and the js-router mechanism.

Here, a test consists on:

- loading an extension 
- launching tozti
- testing one functionnality
- closing tozti

Writing tests for Tozti with pytests
====================================

Writing a test with pytest is easy. First, you need to create a python file prefixed by `tests_` which will contain your test function. A test file can contain several test functions and should import `pytest`.
A test function must have a name starting with `test_`. It's name must be explicit as it will be displayed when the test failed. Finally, a test fails if it raise an exception. One convenient way to write tests is by using assertion. `æssert expr` will do nothing if `expr` is evaluate to `False`, otherwise it will fail.

A test should:

- not rely on data not defined inside the test. If you have 10 tests, then the result of executing the test must be independent of the order in which they are executed
- be precise and test one thing
- change rarely. Each time you edit a test it is losing of its purpose

Passing parameters to a test
----------------------------

Most of the time your tests will take no arguments and will be self contained. But sometime, you'll want to write a generic test and use it on different input and output.
For exemple, to test a function `foo` that take two arguments and compute their sum, you could do this::

    def test_foo_1():
        assert(foo(3, 4) == 7)
    def test_foo_2():
        assert(foo(0, 4) == 4)

This is correct, but it is more convenient to write::

    @pytest.mark.parametrize("a, b, expected", [(3, 4, 7), (0, 4, 4)])
    def test_foo(a, b, expected):
        assert(foo(a, b) == expected)

Here, we are *parametrizing* the test over the arguments `a`, `b` and `expected`. 

The notion of Fixture
---------------------

Sometime you want to execute something before and after your test. Like laynching a background process, initializing the connection to a database and making sure it is closed correctly. Pytest introduce the notions of fixture_ to do that. I will not dwelt to much about it, as their are several ressources about them online.

You can find one usefull fixture in the file `tests/commons.py`. This fixture, called `tozti`, will:

- install a serie of extension if needed
- launch tozti
- Then the test will be executed
- make sure tozti is completly closed

To use it, you must import `tozti` from the file `tests/commons.py`. One simple exemple of use is as follow::

    from tests.commons import tozti

    @pytest.mark.extensions(["extension1", "extension2", ...., "extensionn"])
    def test_ultra_super_genial(tozti):
        test_something

The line `@pytest.mark.extensions(...)` is used to specify the names of the extensions to install. The extensions themself must be put inside of the folder `tests/extensions`.
You can then use the object `tozti` (which is a `subprocess.Popen` object if `tozti` could be launched, `None` otherwise) in order to perform some operations. For exemple, the function `tozti_still_running(tozti)` return `True` if `tozti` is stil running.





.. _pytests: https://docs.pytest.org/en/latest/
.. _travis: https://travis-ci.org
.. _fixture: https://docs.pytest.org/en/latest/fixture.html
