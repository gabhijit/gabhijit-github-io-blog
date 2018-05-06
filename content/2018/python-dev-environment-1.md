Title: Python Project Workflows - Part 2
Date: 2018-05-06
Category: Python Development
Tags: pylint, pip, pipenv, virtualenv
Slug: python-dev-environment-2
Author: Abhijit Gadgil
Summary: In the [first post](), we looked at what are typical issues in setting up Python project workflows and took an overview of the tools of the trade. In this post, we are going to be looking closely at `pipenv` a tool for managing Python project dependencies.

# Intended Audience

Some background working in Python would be certainly useful. This document tries to provide an overview of the role of `requirements.txt` and how it is used along with `pip` and `setuptools`, but is not a tutorial on `requirements.txt`.

To better understand some of the issues we are addressing in this document, having read first part of this tutorial would be quite useful.

# Introduction

As seen in Part 1 of the series of blog, `requirements.txt` file can be used to track external dependencies of our project. Often, one may not necessarily have a separate `requirements.txt` file, but the dependencies can be tracked directly in the `setup.py` if one is using `setuptools` for building, installing and publishing the project. The way this works is `setup` function in `setuptools` takes an argument called `install_requires` and typically this list is generated from the `requirements.txt` file above, with something very simple like `install_requires=open('requirements.txt', 'r').readlines()`. This will make sure whenever we are trying to `install` the project, these dependencies (and their dependencies) are installed as well.

One of the challenges with `requirements.txt`, when using [semantic versioning]() (which is always recommended) is whether to specify exact versions of dependencies (using eg. say `requests==2.18.4`) or using the versions that are compatible with our Project. While it may be desirable to use latest compatible versions, it might resulting in different builds at different times of the same project (commit as well) to result in using different versions of dependencies and hence the builds are no longer reproducible, so it probably is a good idea to use fixed versions of dependencies and whenever the dependencies are updated, they undergo a proper testing and then a newer version of project can use newer version of dependencies.

As we have seen `pip freeze` can be used to generate exact version of dependencies installed. However this is still not most ideal, the reason being `pip freeze` will collect all dependencies (which is good), but won't tell us which dependencies were installed to satisfy which dependencies or in other words, it doesn't show dependency graphs and how they are resolved.

We might require separate environment for development and separate environment for deployment. Some of the dependencies that were installed during development are often not required in a deployment environment (eg. tools like `pylint` that are used for code linting, or `mock`, `unittest` that are used for unit-testing etc.) Usually it's not a harm to install those in a deployment environment as well, but more software on the production machine means bigger attack surface usually so it's best avoided.

So how do we solve this issue? In comes `pipenv`. Next we'll look at some sample use of `pipenv` and how the problem described above can be addressed and some things to keep in mind.

# Dependencies

Every project is likely to have dependencies on some libraries that are developed separately and maintained by someone else. In fact effectively tracking dependencies, can become quite a challenging task. Let's look at some of the challenges -

## Conflicting Dependencies

While Python's standard library is quite extensive, almost always we need a functionality that is better provided by some packages. A very good example is the [requests]() package, which is a great substitute for the Python standard library's `httplib` or `urllib2`. It's very likely that you have a code-base that works with a specific version of `requests` (say version-a) and another code-base that work with another version of `requests` (say version-b) and unfortunately they are incompatible. The two code bases are not related to each other, so likely you would want to use both the versions in the respective code base. Python solves this problem using a tool called `virtualenv`. What `virtualenv` essentially does is creates a self contained Python environment in a single directory and does tricks with `sys.path` such that the Python interpreter finds packages and modules from inside this directory. Think of this as a Python equivalent of `chroot`, loosely speaking. In fact, if a developed Python application is going to be containerized, `virtualenv` will almost be a required one.

Key Takeaway : *Every project should have it's on `virtualenv`.*


## Transitive Dependencies

We have looked at how `virtualenv` could help us solve the problem of conflicting dependencies on a developer's machine. However, now when we look at an individual project, how do we install the dependencies. One good thing about `virtualenv` is, when you create a virtual environment, it installs `pip` Python's recommended package manager inside the virtual environment. So one should always use this `pip` for installing additional dependencies.

A small digression here before we look more at dependencies and transitive dependencies. Typically if you are using Linux platform for development, your distribution will also provide the distribution specific versions of Python packages (like `rpm` or `deb`) supported by the package manager of your distribution (like `yum` or `apt`). Whenever you are developing using Python you should *never* use these packages - often these packages are outdated, second their dependencies come as distribution specific packages like `rpm` or `deb` (and not as pip packages) and they are not so straight forward to use in a virtual environment.

One of the advantages of using `pip` is, if the package you are using has dependencies itself, they are also installed recursively till all dependencies are resolved.

Key Takeaway : *Always use `pip` to install dependencies in a virtual environment created by `virtualenv`*

## Reproducibility

Once we start with a virtual environment and use `pip` to install packages, often we have a pretty good starting point for the Project's development. It may not though be enough or always optimal. For example a question one might want to ask is - should the virtual environment itself be maintained inside `git`? It's not a very bad idea, but probably not a recommended one. A natural question then is how can a team collaborate effectively? One of the ways to solve that problems is by maintaining a `requirements.txt` file, that lists down your dependencies and their respective versions and instead maintain that file in a `git` repository. `pip` allows installing packages listed in a file using a command like `pip -r requirements.txt` say. Pip also allows a command called `pip freeze` that looks at currently installed packages in a `virtualenv` and generates a list of packages with their version. So something like `pip freeze > requirements.txt` would help you generate the `requirements.txt` and then this file can be tracked in `git`. So someone cloning (or forking) the repository can simply do a `pip -r requirements.txt` after cloning the repository and would have identical versions of packages installed (well almost - we'd look at a subtle issue and how to fix that later.)

Key Takeaway : *Use a `requirements.txt` file to track your dependencies and generate it using `pip freeze`.*

# Separate Environments

What we have described so far should be 'good enough' when starting a project. However when the scope of the project starts improving, unit tests are added, coding guidelines are to be enforced, there might be more needed to be done than what we have discussed so far. Let's look at some of the challenges. What `pip freeze` does is it lists down all the packages (with their installed versions) that are installed by pip. But let's consider this - You want to run some unit tests while building a project and you are using tools like `nose` to do so and have installed it using `pip`, `pip freeze` will catch that for you as well. In a development environment you want to run certain sanity checks etc and are using tools like `pylint` (see below for more about `pylint`), but may be you don't want those in a production environment. So you want to kind of keep the installed dependencies in a development environment different from those in production environment, tools like `pipenv` help yo fix that problem. In the next article of this series, we are going to take a closer look at `pipenv`.

# Code Quality

Often as the size of a team working on a project grows, it is often not sufficient to simply document 'recommended' practices and conventions, there needs to be a way to enforce some. (for instance you might want your code to strictly adhere to `pep8` and code not conforming to `pep8` is not admissible). Python also being a weakly typed and interpreted languages, a number of errors show up at the run-time, so it's a better practice to actually use some code linting tools that will analyze your code (often without running it) and highlight potential errors that can be easily fixed during the development itself. In a subsequent post we will take a more detailed look at `pylint` and how it can be integrated into the development workflow to ensure certain code quality.


# Summary

In this part, we discussed typical challenges in developing a Python project from an ecosystem perspective and provided an overview of some tools that can help address. In summary, following just the three simple practices should start as a good starting point
1. Every Project should have it's own `virtualenv`.
2. Always use `pip` to install dependencies in a virtual environment created by `virtualenv`.
3. Use `requirements.txt` file to track your dependencies and generate it using `pip freeze`.

In remaining parts we would look at how to use `pipenv` to setup separate Development and Production environments, how to use `pylint` and integrate it as a `git pre-commit hook` to enforce certain coding standards and automatically check for errors in Python code without waiting for them to show up at run-time.

