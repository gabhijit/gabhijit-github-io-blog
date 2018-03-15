Title:
Date: 2018-03-15
Category: LTE, Linux Networking, OAI
Tags: OAI, LTE, eNodeB, EPC, netns, Linux
Slug: oai-oaisim-enb-epc-netns
Author: Abhijit Gadgil
Summary: [OpenAirInterface](http://www.openairinterface.org/) is an interesting project, that aims to develop open source software solutions for 4G and 5G cellular network. The project provides an Air Interface Simulator (OAISIM) and implementations of eNodeB and EPC nodes. While there are many tutorials that allow you to connect eNodeB with EPC on different machines, I was not able to find any good tutorial that exploited Linux network namespaces to actually emulate the entire network in a single box. Here we discuss, an approach of how to get that done.

# Background

A bit of a background - OAI Wiki has [got instructions to connect eNodeB with EPC]() where both of them are running on separate machines. The instructions were for a rather old branch (0.4) that worked on Ubuntu 14.04. I just wanted to make sure, it was possible to build and run this setup on Ubuntu 16.04. Also, being able to run each of the node in a network namespace would actually allow a cleaner separation between the nodes. The LTE network architecture is [explained here]. This is reproduced below to better understand how the nodes connect to each other, what networks we are using etc.


# Building OAI

The OAI codebase is actually made up of two repositories available from Eurocomm Gitlab -
1. The

