Title: Thinking in Python - Part 1
Date: 2019-03-31
Category: Python
Tags: python, beginners
Slug: thinking-in-python-2
Author: Abhijit Gadgil
Summary: Previous post looked at a simple data handling problem, in this post, we are going to look at another problem of running Random experiments in Python

# Introduction

Birthday paradox problem discusses that in a group of randomly chosen people, what is the probability that two or more people will share their birthdays? [Wikipedia]() has got an extensive mathematical treatment of the problem and it surely by itself is worth a read. But somewhat quite un-intuitive result is if there are about 25 people in a room, the probability that at-least two of them will share their birthday is about half. The result might sound very surprising, but is indeed true.

Let's say we want to verify that this result is indeed true? How can we go about it?

# An Approach

What if we run an experiment where we randomly select a group of N people many times and actually find out how many of those times the above particular assertion holds true. Is that solution going to be close to actual mathematical probability?


## First Steps

How do you find birthdays for individuals? It's actually pretty simple if we ignore the complexity associated with leap years, and choose random numbers between 1 and 365, we can call that number as a birthday of a person.
