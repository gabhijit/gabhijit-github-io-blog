Title: Python Project Workflows - Part 3
Date: 2018-05-06
Category: Python
Tags: pylint, Python
Slug: python-dev-environment-3
Author: Abhijit Gadgil
[//] # FIXME : Need to fix the link to draft
Summary: In the [first part]() we looked at a few challenges involved when developing a Python project in a collaborative environment. In the [second part]() we looked at how `Pipenv` addresses some of those issues. In this part of the series we are going to take a closer look at how one can use code linting tools. Specifically we are going to be looking in details at using `pylint`.

# Introduction

Python being a dynamically typed and interpreted language, there is no such thing as 'compile time' and most of the errors (even related to syntax) show up only at the run-time and that's kind of not good,  which can and should be easily avoided. So it's very important to have your code checked by some linting tools before it goes into the repository. Further, often, it's a good practice that certain coding guidelines are followed by the development team, in fact it's even better if they can be enforced using tools, so there is some level of consistency in the way a project is developed. Early is better than late. [`pylint`](https://www.pylint.org/) is an excellent tool to achieve both of these objectives (and more). In the discussion that follows, we are going to take a closer look at how `pylint` can be integrated into the development workflow.

# Python linting tools overview

There are a number of syntax and error checker tools for Python and [this]() and [this]() discussion on SF compares them in great details, so won't repeat here. Choice of `pylint` was somewhat influenced by these discussions, but it was more like, used it, found it useful and just started using it.

# A simple `pylint` Workflow

It's easiest to get started with `pylint` by something as simple as -

`pylint modulename.py` or `pylint packagename` and if one is running `pylint` for the first time, chances are the code will get rated at a very low value (don't feel terrible if it reports a number less than 5.0 out of 10.0). `pylint` categorizes issues it observes with the code into five categories -

1. Convention : The code is not following the `pep8` convention and some more.

2. Refactoring : Possible refactoring possible (identifying duplicate code etc.)

3. Warnings : Something that's bad - which is going to make the code smell bad eventually, but not necessarily an error.

4. Error: Syntax error or undefined variable (something you just cannot and should not ignore).

5. Fatal: For some reasons, `pylint` reported a fatal error and couldn't continue.

`pylint` being highly configurable uses a default configuration about the kind of messages it reports and kind of messages it ignores. A [detailed list of pylint messages]() is available here. What defaults `pylint` uses can be found out by running `pylint --generate-rcfile`. The details of configuration file can be read about in the [documentation](). Often though, it's probably a good idea to tweak the configuration file as we'll see in the next section. Based upon the number of lines analyzed and the total message count then `pylint` assigns a 'score' to the code. `pylint` also generates a detailed report for the errors and can track a bit of history (current score compared to previous score) of executions.

# A detailed `pylint` Workflow

One of the best ways to start using `pylint` is to generate our own `pylint` configuration file and then tweak it to our own needs. We'd go through a simple workflow about how to do it, but this is something that is best tailored for individual project.

First start with a default `pylintrc` file generated through `pylint --generate-rcfile` and then tweak it to your own environment, preferences or coding standards.

## Enabling and Disabling Certain messages

There are many ways how one could enable or disable which `pylint` messages are reported - 1) Through command-line, 2) Through configuration file and 3) through editor directives. What I usually follow is to do it through configuration and only occasionally resort to inline directives, but avoid using command-line directives except when one wants to experiment with which directives to use (and finally add them to the configuration file.).

Here are some of the guidelines that I follow -

1. Start with enabling everything

2. Disable certain types of Convention and Refactor messages (this is usually a matter of taste, so probably not a good idea to recommend which are recommended ones.).

3. Enable ALL Warnings, Errors and Fatal messages. A note: I always disable `fixme` warnings because I almost always have a few `FIXME`s in the code and they shouldn't unnecessarily lower the score. Another nagging warning is a `global-statement`, which I often don't disable in the `pylintrc` file, but sometimes may disable it in a given file using the editor directive. As something like global statements should best be left to the decision of code reviewer upon whether (s)he is fine with it or not.

Once this is setup, it's probably a better idea to track the `pylintrc` file in the VCS, so subsequent invocations can use this file and there will be consistency in the way the code is analyzed.

## A bit more about `pylint` Score

# Integrating `pylint` with git

# 'pylint' Workflow Summary

# Few More Points
