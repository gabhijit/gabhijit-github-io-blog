Title:
Date: 2018-03-15
Category: LTE, Linux Networking, OAI
Tags: OAI, LTE, eNodeB, EPC, netns, Linux
Slug: oai-oaisim-enb-epc-netns
Author: Abhijit Gadgil
Summary: [OpenAirInterface](http://www.openairinterface.org/) is an interesting project, that aims to develop open source software solutions for 4G and 5G cellular network. The project provides an Air Interface Simulator (OAISIM) and implementations of eNodeB and EPC nodes. While there are many tutorials that allow you to connect eNodeB with EPC on different machines, I was not able to find any good tutorial that exploited Linux network namespaces to actually emulate the entire network in a single box. In theory, that looked quite reasonable, so eventually ended up making that setup up and running. There are a few findings, discussed below.

# Background

A bit of a background - OAI Wiki has [got instructions to connect eNodeB with EPC]() where both of them are running on separate machines. The instructions were for a rather old branch (0.4) that worked on Ubuntu 14.04. I just wanted to make sure, it was possible to build and run this setup on Ubuntu 16.04. Also, being able to run each of the node in a network namespace would actually allow a cleaner separation between the nodes. The LTE network architecture is [explained here]. This is reproduced below to better understand how the nodes connect to each other, what networks we are using etc.


# Building OAI

The OAI codebase is actually made up of two repositories available from Eurocomm Gitlab -
1. The RAN side is implemented in the [openairinterface5g repository]()
2. The CN side is implemented in the [openair-cn repository]()

Building the RAN side was a bit involved and faced following issues -

1. The original version for which documentation was available for setting up OAISIM with CN, was 0.4, however it was not building on Ubuntu 16.04. The problem was some of the ASN.1 files were patched with an older version of [asn1c]() which was available for Ubuntu 14.04. Finally after trying out different versions, figured out that version 0.6.1 works fine, that uses asn1c hosted on [eurocomm gitlab]().

2. The head of the develop branch was having issue with libconfig, so it was not possible to use the head of the develop branch.

3. I was trying to build inside kernel 4.15.0, the UE IP module build was failing for this kernel. As a side note in order to build and run CN, kernel version higher than 4.7.0 is required, this is because the GTP module is available in Linux tree starting kernel version 4.7.0 . The Linux kernel timer interfaces had a few modifications in kernel version 4.15.0. Hence the UI IP module was not building with it. Finally was able to build the OAISIM executable.

4. There was another issue - `libnettle` available on Ubuntu 14.04 was major version 2.X. The one available on Ubuntu 16.04 was 3.X and signatures of some of the functions were changed, so that was required to be fixed.

5. Also had to use the Free Diameter hosted on [eurocomm gitlab]() to build the CN side.

Eventually executables for oaisim, hss, mme and spgw are built. I didn't follow the `-I` option available with most of the build scripts. The reason being, some of them are patching older versions of software, so just wanted to see how it goes without having to do that. Only a couple of dependencies were obtained from the source as described above (asn1c and free diameter), but everything else is a package available from a standard repository and nothing is patched. I particularly don't like patching older versions of dependencies with some non-standard sources, because that makes the build very fragile and only works on a very limited set of environments.


# Running OAI

In trying to run OAI inside the same Linux machine, we are making use of network namespaces to achieve that. So basically each network namespace provides isolation between the nodes and the nodes are connected using `veth` pairs and/or `bridge` interfaces wherever required. Figure below explains the topology and the networks we are using -

1. The eNodeB MME - S1-MME interface is implemented as a 10.0.0.0/24 network
2. The MME-HSS - S6A interface is implemented as a 10.0.1.0/24 network
3. The MME-SGW - S1-U interface is implemented as a 10.0.2.0/24 network
4. The MME-SGW - S11 interface is implemented as a 10.0.3.0/24 network
5. The HSS-Host implements another interface for communication between the HSS and MySQL running in default (host) namespace.
6. The PGW - SGi interface is right now implemented as a 10.0.5.0/24 network through a bridge.


