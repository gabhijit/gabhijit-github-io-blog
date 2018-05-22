Title: Python Logging Deep(ish) Dive
Date: 2018-05-08
Category: Python
Tags: python logging
Slug: python-logging-deep-dive
Author: Abhijit Gadgil
Summary: Python Logging module is perhaps one of the most widely used and often not so well understood module. While most of the things are documented quite well, sometimes it's easy to miss out a few things. Here we take a look at Python's Logging module in a bit more details, trying to get under the hood to figure out what's really happening.

# Introduction

One of the reasons I got a little curious about logging module was thanks to `pylint`. While I was running `pylint` on one of my code I saw at quite a few places the following warning message -
```
logging-not-lazy (W1201): *Specify string format arguments as logging function parameters*
```

While my code had a few instances of equivalent of the following -

```
log.info("Log Something val %d" % (val))
```
While the message was saying I should probably use something like
```
log.info("Log Something val %d" , val)
```

Now, the natural question is why should that matter? The answer is "While the former string substitution will be evaluated regardless of whether a particular error is enabled or not, ie to say this particular log record will be emitted on not, while the latter is a function call that happens only when the log record is 'emitted'.

Suggested different option of using `string.format` is also not a choice here as well for the same reason and you would see a similar warning as above.

```
:logging-format-interpolation (W1202): *Use % formatting in logging functions and pass the % parameters as arguments*
```

So this prompted in taking a more closer look at the documentation and figure out some of the subtleties. We discuss all the findings in little more details.

# A Bit More About These Warnings

As we have seen in the previous section, it is important to pass parameters as arguments to logging function rather than using '%' substitution or using `string.format`. Let's take a look at this in little more detail by profiling the code. Let's run this through our [context profiler](). Here's the relevant code and corresponding details -

```
import logging
import time

import profiler

iterations = 1000000
l = logging.getLogger(__name__)
l.addHandler(logging.NullHandler())

l.setLevel(logging.INFO)

class Foo(object):
    def __str__(self):
        return "%s" % self.__class__

with profiler.Profiler(enabled=True, contextstr="non lazy logging") as p:
    for i in range(iterations):
        l.debug("Hello There. %s" % Foo())

p.print_profile_data()

with profiler.Profiler(enabled=True, contextstr="lazy logging") as p:
    for i in range(iterations):
        l.debug("Hello There. %s", Foo())
p.print_profile_data()
```

And here is the output of running the above code

```
profile: non lazy logging: enter
         4000003 function calls in 1.058 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
  1000000    0.231    0.000    0.655    0.000 /usr/lib/python2.7/logging/__init__.py:1145(debug)
  1000000    0.272    0.000    0.424    0.000 /usr/lib/python2.7/logging/__init__.py:1360(isEnabledFor)
  1000000    0.385    0.000    0.385    0.000 lazy_logging.py:13(__str__)  <-------------- Check this line
  1000000    0.152    0.000    0.152    0.000 /usr/lib/python2.7/logging/__init__.py:1346(getEffectiveLevel)
        1    0.018    0.018    0.018    0.018 {range}
        1    0.000    0.000    0.000    0.000 /home/gabhijit/backup/personal-code/gabhijit-github-io-blog/sources/misc/python/logging/profiler.py:29(__exit__)
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}


profile: non lazy logging: exit

profile: lazy logging: enter
         3000003 function calls in 0.591 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
  1000000    0.195    0.000    0.580    0.000 /usr/lib/python2.7/logging/__init__.py:1145(debug)
  1000000    0.245    0.000    0.385    0.000 /usr/lib/python2.7/logging/__init__.py:1360(isEnabledFor)
  1000000    0.140    0.000    0.140    0.000 /usr/lib/python2.7/logging/__init__.py:1346(getEffectiveLevel)
        1    0.010    0.010    0.010    0.010 {range}
        1    0.000    0.000    0.000    0.000 /home/gabhijit/backup/personal-code/gabhijit-github-io-blog/sources/misc/python/logging/profiler.py:29(__exit__)
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}


profile: lazy logging: exit
```
So our `__str__` for the class Foo was called even when the `logging.debug`  is not enabled. This might look like a convoluted example, but this proves an important point, especially when we are logging in critical path, extra cycles are spent in evaluating the string even when the relevant level is not enabled. When the parameters to be evaluated are themselves more expensive this could be an un-necessary penalty, so this should be avoided.

Let's look at the logging architecture in little more details through use of some examples and what exactly is handling under the hood.

# Logging Architecture

The complete logger flow is described below, taken from the excellent [logging howto]()



We quickly go through each of the main classes, to provide a quick overview. Reading in more details about the HOWTO pointed above is highly recommended for further details.

## `Logger` Class

From the HOWTO above -

> Logger objects have a threefold job. First, they expose several methods to application code so that applications can log messages at runtime. Second, logger objects determine which log messages to act upon based upon severity (the default filtering facility) or filter objects. Third, logger objects pass along relevant log messages to all interested log handlers.

So basically, Logger classes are main entry point into the logging system. A more simple description of `Logger` class can be, they create `LogRecord` objects depending upon current configuration and handle them. The main function that does this looks like following (taken from `/usr/lib/python-2.7/logging/__init__.py`)

```
    def _log(self, level, msg, args, exc_info=None, extra=None):
        """
        Low-level logging routine which creates a LogRecord and then calls
        all the handlers of this logger to handle the record.
        """
        if _srcfile:
            #IronPython doesn't track Python frames, so findCaller raises an
            #exception on some versions of IronPython. We trap it here so that
            #IronPython can use logging.
            try:
                fn, lno, func = self.findCaller()
            except ValueError:
                fn, lno, func = "(unknown file)", 0, "(unknown function)"
        else:
            fn, lno, func = "(unknown file)", 0, "(unknown function)"
        if exc_info:
            if not isinstance(exc_info, tuple):
                exc_info = sys.exc_info()
        record = self.makeRecord(self.name, level, fn, lno, msg, args, exc_info, func, extra)
        self.handle(record)

    def handle(self, record):
        """
        Call the handlers for the specified record.

        This method is used for unpickled records received from a socket, as
        well as those created locally. Logger-level filtering is applied.
        """
        if (not self.disabled) and self.filter(record):
            self.callHandlers(record)

```

A couple of points to note here - `_log` function will be called looking at the current logging `LEVEL` of the logger and the handlers are called only if this is logger is `enabled` and any of the 'filters' associated with this logger allow the record to be passed. [Question - why do all the work - when the logger is disabled?](https://stackoverflow.com/questions/50453121/logger-disabled-check-much-later-in-python-logging-module-whats-the-rationale)

## `Handler` Class

This class actually 'handles' the LogRecords emitted. Typically by calling the 'Formatter' for the LogRecord and then `emit`ing the record. A word about `emit` here is important - The Handler's handle method calls `emit` holding the Handler's lock (see below), so it's important to pay attention to `emit` and try it as far as possible that it is not a blocking one. Some of the implementation of handlers actually have an `emit` function that is blocking. Python 3.2 onwards there is a QueueHandler that implements a non-blocking `emit`. So it might be a good idea to consider using that.

## `Formatter` Class

## `Filter Class

## `LoggerAdapter` Class

# What happens when you do `import logging`

When you do `import logging`, there are a number of things that happen under the hood. For example a `RootLogger` instance is created when the `logging` module is imported. Actually all the loggers created in a Python process form a hierarchy with `RootLogger` being at the 'root' of the hierarchy.

Speak about when you are doing logging for a library, what's the approach you should take

# Some Real World Examples

Speak about how logging configuration happens in Django what are the caveats.

# Summary

Overview
