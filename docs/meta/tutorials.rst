*********
Tutorials
*********

Using git
=========

We will give a short list of usefull git commands in this section. For a more
complete introduction to git, please refer to the following links:

- the `gittutorial <https://git-scm.com/docs/gittutorial>`_
- the `atlassian tutorials <https://www.atlassian.com/git/tutorials>`_,
  particularly `setting up a repository
  <https://www.atlassian.com/git/tutorials/setting-up-a-repository>`_, `saving
  changes <https://www.atlassian.com/git/tutorials/saving-changes>`_, `undoing
  changes <https://www.atlassian.com/git/tutorials/saving-changes>`_, `syncing
  <https://www.atlassian.com/git/tutorials/syncing>`_ and `using branches
  <https://www.atlassian.com/git/tutorials/using-branches>`_.
- an `interactive tutorial <https://try.github.io/levels/1/challenges/1>`_ by
  github


Golden rules
------------

- The branch master is here only for working and tested stuff. Never commit to
  it directly but instead pull commits from other branches to it once they make
  a consistent group.
- Never alter commits that have been pushed to a public (remote) repository.


Cheatsheet
----------

``git clone <repo>``
   Create a local copy of the distant repository ``repo``.

``git add <file>``
   Add a file to the next commit, this is called *staging* a file.

``git commit -m "<message>"``
   Commit the staged files with the specified message (instead of launching the
   editor).

``git push <remote> <branch>``
   Push ``branch`` to the ``remote`` repository. By default ``remote``
   is set to ``origin`` (i.e. the repository you cloned).

``git fetch <remote> <branch>``
   Download the ``branch`` from the ``remote`` repository.

``git merge <branch>``
   Combine ``branch`` onto the current branch. If there are conflicts they will
   be explained. It will fast-forward if possible.

``git pull <remote> <branch>``
   Equivalent to ``git fetch`` followed by ``git merge``.

``git checkout <file>``
   Revert ``file`` in the working directory to it's last commited state.

``git checkout <branch>``
   Switch the working directory to ``branch``. Uncommited changes in the
   working directory are kept. It will transparently create a new local
   tracking branch if ``branch`` is a remote branch.


Using branches
--------------

Branches are used to separate independant parts of the work to identify what is
related and what is not. Once the work is done the branch should be merged back
into the master. A branch is just a named reference to a commit (which is the
``HEAD`` of the branch) so it's really lightweight and should be abused.

Say you want to work on something new called ``feature1``. First you have to
check out the branch you want to fork from (probably master) with ``git
checkout master``, then create the branch with ``git branch feature1``. You
could also use ``git checkout -b feature1`` instead which will additionnaly
checkout the branch (as you probably want to work on it right away).

Now the branch is local, you might want to push it upstream. To do it, use
``git push -u origin feature1``. If you want to change the upstream name of the
branch, use ``git push -u origin feature1:better-name``.

If you want to work on a branch that already exists remotely but not locally,
you want to create a local branch that *tracks* the remote branch with ``git
branch -t local_feature1 origin/feature1``. But most of the time you want the
branch to have the same name and there is a shortcut for that: ``git checkout
feature1`` will do exactely what you want (create a local *tracking* branch)
and check it out.

Now that some work is done, you want to merge back the ``feature1`` branch onto
``master``. To do that, checkout master with ``git checkout master``, merge the
branch with ``git merge --no-ff feature1``, resolve the conflicts if there are
any, then ``git commit`` and finally push your changes with ``git push origin
master``.

If you are sure that the branch is not going to be used anymore you can delete
it (it just deletes the reference). To delete the local branch type ``git
branch -d feature1`` (or ``-D`` if it wasn't merged, but careful you will loose
the commits), to delete the remote branch, use ``git push origin :feature1``.
If the branch is not going to be used anymore but you feel it was important
enough to keep track of it, you can tag it just before deleting it with ``git
tag archiving-name feature1``. Names can contain slashs so an appropriate name
for the tag might be ``dead/feature1``.


How to write good commit messages
---------------------------------

TODO: magic messages
