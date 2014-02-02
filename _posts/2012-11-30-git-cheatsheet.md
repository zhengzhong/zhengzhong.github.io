---
layout: post
title: Git Cheatsheet
categories: ['coding']
tags: ['Git']
---


This post lists all the Git command that I use frequently.

[Pro Git](http://git-scm.com/book) is an excellent book on how to use Git.


Clone a repository
===================

    # Clone from an existing ("bare") remote repo.
    $ git clone git://<repo-url>  <local-directory>
    $ git clone http://<repo-url> <local-direcotry>


Create a bare repository
=========================

    # initialize a bare repository
    $ cd <directory>
    $ git init --bare

    # turn an existing "non-bare" repository into a "bare" one
    $ git clone --bare -l <non-bare-repo> <new-bare-repo>


Set user information
=====================

    # Set user info globally (applicable on all the Git repos on this computer)
    $ git config --global user.name  "<global username>"
    $ git config --global user.email "<global user email>"

    # Check global user info
    $ git config --get --global user.name
    $ git config --get --global user.email

    # Set user info locally (per repo)
    $ cd <local-repo>
    $ git config --local user.name  "<repo-specific username>"
    $ git config --local user.email "<repo-specific user email>"

    # Check local user info
    $ git config --get --local user.name
    $ git config --get --local user.email


Check and set end-of-line setting
==================================

    $ git config --global --get core.autocrlf  # Should be "true"
    $ git config --global core.autocrlf true   # Set it to "true"


Undo changes
=============

    # restore the entire working tree to the last committed state
    $ git reset --hard HEAD

    # unstage one staged file
    $ git reset HEAD <file-name>

    # restore one untracked file
    $ git checkout --   <file-name>
    $ git checkout HEAD <file-name>


Push changes to remote repository
==================================

    # prepare the http.proxy config: check, add, or unset
    $ git config --get http.proxy
    $ git config --global --add http.proxy <proxy>
    $ git config --global --unset http.proxy

    # check branches
    $ git branch -v

    # check remotes
    $ git remote -v

    # add remote repo (if not yet added)
    $ git remote add origin <repo>

    # push to remote
    $ git push origin master


Create tags
============

    # list available tags in alphabetical order (the order has no real importance)
    $ git tag

    # show details about a tag
    $ git show <tag-name>

Git uses two main types of tags: *lightweight* and *annotated*.

* A *lightweight* tag is just a pointer to a specific commit (very much like a branch that doesn't change).
* *Annotated* tags are stored as full objects in the Git database. They're checksummed; contain the
  tagger name, e-mail, and date; have a tagging message; and can be signed and verified with GNU
  Privacy Guard (GPG).

In general, annotated tags are recommended as they contain all this information. Lightweight tags
are used for creating temporary tags.

    # create an annotated tag (with the '-a' option)
    $ git tag -a <tag-name> -m "<message>"

    # tag a specific commit
    $ git tag -a <tag-name> -m "<message>" <commit-SHA>

    # create a lightweight tag (do not supply any option)
    $ git tag <tag-name>

By default, the ``git push`` command doesn't transfer tags to remote servers. Tags need to be
pushed explicitly.

    # push a tag to the 'origin' remote server
    $ git push origin <tag-name>

    # transfer all tags to the 'origin' remote server
    $ git push origin --tags


Rename a remote tag
====================

To renaming an existing tag to a new name:

    $ git tag new-tag old-tag             # Create new-tag as an alias of old-tag (locally)
    $ git tag old-tag                     # Delete old-tag (locally)
    $ git push origin :refs/tags/old-tag  # Delete old-tag from remote repository
    $ git push --tags                     # Push tags to remote repository (thus create new-tag)

Then for all other local repositories, to synchronize tags with remote repository:

    $ git tag -l | xargs git tag -d  # Delete all tags from local repository
    $ git fetch                      # Get tags back from remote repository


Work with local branches
=========================

Local branches can be used by a single developer, when collaboration is not needed. A typical workflow is:

**Step 1:** Create and checkout a local branch from ``master``

    # Make sure we are at master
    $ git branch
      ...
    * master
      ...

    # Create and checkout a local branch from master.
    $ git check -b local-dev

**Step 2:** Work on the local branch -- all changes are committed in this local branch.

**Step 3:** As the ``master`` branch might also evolve, keep the local branch updated.

To merge changes from ``master`` into the local branch, ``git rebase`` is preferred to ``git merge``.

    # Update the master branch.
    $ git checkout master
    $ git pull

    # Merge (via git rebase) changes from master back into the local branch.
    $ git checkout local-dev
    $ git rebase master

**Step 4:** Once the development is done, merge changes into ``master``, and push to the remote repository.

If the local branch is synchronized with ``master`` via ``git rebase``, merging from the local branch into ``master``
should simply be a fast-forward merge.

    $ git checkout master
    $ git merge local-dev
    $ git push

**Step 5:** Final step: delete the local branch.

    $ git branch -d local-dev


Create and apply patches
=========================

To create patches from one repo, start by listing the changelog:

    $ git log --pretty=oneline
    d241dcf39ed2a3ff58dbba0c12489038c2019215 Added content in homepage.
    b537f59855019c03e3f72422cd033d62022f5240 Committed first version of my Jekyll site.
    90d33f4a800253d2f4fa39950d7652f9b4fde5dc Initial commit

To create patches for the last two commits, note down the SHA of the commit right before (only
several first letters will be enough) and use it as a starting point:

    $ git format-patch 90d33f4a80
    0001-Committed-first-version-of-my-Jekyll-site.patch
    0002-Added-content-in-homepage.patch

This will generate two patch files, each containing one commit.

To create a single patch file with all changes in it:

    $ git format-patch 90d33f4a80 --stdout > all-changes.patch

Copy these patch files to another repository where the patches need to be applied:

    # To check what files are affected by one patch:
    $ git apply --stat 0001-Committed-first-version-of-my-Jekyll-site.patch

    # To see if the patch can be applied smoothly:
    $ git apply --check 0001-Committed-first-version-of-my-Jekyll-site.patch

    # If nothing is returned from the previous command, apply it:
    $ git apply 0001-Committed-first-version-of-my-Jekyll-site.patch

    # If there are errors, we can still apply just the parts that will work.
    # Following command will apply the patch while generating *.rej files:
    $ git apply --reject 0001-Committed-first-version-of-my-Jekyll-site.patch

