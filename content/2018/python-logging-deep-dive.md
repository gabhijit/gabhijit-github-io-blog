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


# Logging Architecture

Loggers, Handlers, Formatters and Hierarchy

# Some Important Details

Speak about when you are doing logging for a library, what's the approach you should take

# Some Real World Examples

Speak about how logging configuration happens in Django what are the caveats.

# Summary

Overview
