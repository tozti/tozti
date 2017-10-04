:orphan:

.. _meta:

*********************
Internal organisation
*********************

How we communicate
==================

Github
------

The main home for things we produce is on the `github organization`_.
Everything that we don't want to be lost should be put there in one way or
another at some point. If you want to attract attention in an issue you
can ping people or a team by prefixing it's name with an "@" character.

Don't fear to start an issue about anything that bugs you, if the issue is
trivial it's going to be rapidly closed. If you want some review on the code
you are writing in a feature branch, you can start a pull request long before
it's ready to be merged, this is the ideal place to talk about a specific part
of the code.

TODO (issue tagging)

Slack
-----

Our `slack workspace`_ hosts discussions about the project (or not). It's the
ideal space to have informal discussions, online meetings or to notify a team.
Even if we put a lot of effort into making it organized, messages will get lost
at some point, so if you come up with something interesting enough, be sure to
sum it up and write about it in a related issue or in the present
documentation.

Still, to keep it somewhat organized, try to stick to the following policies:

- When you create a temporary channel (*eg* for a meeting), don't forget to
  archive it when it's ended so that it doesn't clutter the list. Don't create
  unnecessary channels as this is the best way to get to "where was this
  interesting link again?".
- Keep the "#general" channel tidy: it should only contain important
  announcement. If you want to reply, use the *start a thread* feature -- this
  feature is handy, you are welcome to (ab)use it on other channels too.
- If a specific message is important in a channel be sure to make it *sticky*
  but don't forget to unstick it when as soon as it's obsolete.

The documentation
-----------------

The final consensus of any midly important discussion or the explaination about
a complex piece code should end up in this documentation. There are 3 main parts:

- the user part -- explainations about the UI and high level stuff about
  how the internals work
- the developper part -- in-depth explainations about how the code works and how
  one should interact with it
- the internal part -- you are reading it

If you feel like you are in the process of finishing something important, start
writing about it in the documentation. If you don't feel confident writing it
(or don't have the time right now) start an issue in the documentation
repository stating that this should be done together with some explainations or
a link to what should be documented.

The documentation is written in *reStructuredText* (reST) markup and uses the
`sphinx`_ tool to render in *HTML*. You can look at `this cheatsheet`_ for an
introduction to reST. The `specification`_ is useful too. The documentation is
being built automatically by `readthedocs.io`_ but if you want to build it
locally before pushing your changes, just type ``make html`` inside the
``docs`` directory. The built documentation will sit inside
``docs/_build/html``. Tip: ``python3 -m http.server 8080`` starts an HTTP
server listening on port 8080 and serving the local directory. Be sure not to
include the build result in your commits.


Using git
=========

TODO (basics, feature branch workflow, magic commit messages)


.. _github organization: https://github.com/tozti
.. _slack workspace: https://groupware-ens.slack.com
.. _restructured text: http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html
.. _sphinx: http://www.sphinx-doc.org/en/stable/
.. _this cheatsheet: http://www.sphinx-doc.org/en/stable/rest.html
.. _specification: http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html
.. _readthedocs.io: https://tozti.readthedocs.io/en/latest/
