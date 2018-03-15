Title: Linux VRF with MPLS for L3-VPN
Date: 2018-02-27
Category: Linux Networking
Tags: VRF, MPLS, Linux
Slug: linux-vrf-mpls
Author: Abhijit Gadgil
Status: Published
Summary: VRF support for Linux was added in kernel 4.5. In the Linux netdev 1.1 conference, there was a talk about this support, which showed one of the use-case as MPLS-VPN. This blog post tries to re-create the setup from demo on a kernel 4.15.

## VRF Background

Typically VRF is used in VPN implementations, where it is possible to have overlapping address-spaces between one or more customers, in such situations, the isolation required between customers is achieved using VRF. This can as well be achieved using VRF. This is explained in excellent details in [this blog post by cumulus networks](https://cumulusnetworks.com/blog/vrf-for-linux/).

## Re-producing Setup

One of the use-cases for VRF presented during [netdev 1.1]() was using VRFs with MPLS feature (also from Cumulus Networks). One of the things that I wanted to be able to do this is - to re-create the setup, so that it works on any Linux with kernel having the supported features. This exercise turned out to be slightly more involved than I thought before.

### The Topology

This setup is explained in the [document](https://www.netdevconf.org/1.1/proceedings/slides/ahern-vrf-tutorial.pdf).

Here is how it is done -

Each of the device (Host, CE, PE or P) lives in it's own `netns`. `veth` and `bridge` links are used as appropriate to connect the hosts (making sure also that their end-points are in the right `netns`. Linux implementation of `vrf` is a `netdevice`. So one VRF `netdevice` is created for each of the customer in the same PE router, thus there are two VRF `netdevice`s in the PE router. The physical devices (`veth` endpoints) that connect to the customer edge router (CE Router) are enslaved to the VRF `netdevice` corresponding to that customer. For each of the VRF `netdevice`, there's a separate routing table setup for lookup and corresponding `l3mdev` rules are added for making sure the packet lookup happens in the correct routing table.

## Issues / Problems faced

While setting up most of the things was relatively easier, there were a few gotchas

1. It was not obvious, but MPLS labels can be setup only in the main routing table (so specifying table parameter throws `EINVAL` and as with many `RTNETLINK` errors, this one is a bit hard to figure out. Just figured this out by reading the appropriate code.
2. Unless you actually setup using `sysctl -w net.mpls.platform_labels=10000`, setting up label values throws an `EINVAL` error, so one has to first set this up.
3. The way I was going about creating most of the interfaces was, I was first creating an interface in the default namespace and then assigning the `netns` using `ip link set <dev> netns <nsname>`. While this works for `veth` devices, this doesn't work for VRF devices. My first impression was that setting VRF in a non-default `netns` is not allowed, while that is not the case, moving VRF from one netns to another is not allowed. So the best way to go about creating that is - to actually create the VRF device in the correct `netns` first time itself.
4. Faced a weird issue - while the setup looked all fine, was not able to ping from the hosts across MPLS network. The packets were not getting forwarded on one of the PE routers. A debugging using `tcpdump` showed that while the route was properly setup, the packets didn't show up on the corresponding interface. Actually, Dave Ahern of Cumulus who had given the tutorial above helped in solving this issue by basically asking to trace fib events `perf record -efib:* ` and then `perf script`. The lookup was working fine but what was observed was `fib_validate_source` was failing. This was because the VRF routing table didn't have a default route (which is always recommended) and it didn't have a route to the source subnet. Due to absence of this route, the source was treated as `martian`, which was later verified using `sysctl -w net.ipv4.conf.all.log_martian=1`. Finally after adding the route to the source subnet the issue was resolved.
5. After all the above issues were resolved a rather odd issue showed up, while it was possible to ping across hosts, it was not possible to ping the host itself. This is because, when we create a `netns`, the loopback interface `lo` in that network interface is not set as up by default. This is fixed by setting `ip netns exec netnsname ip link setup lo up`.

## Demo

Following [github repository](https://github.com/gabhijit/networking-experiments) has complete setup.

## References

Some references used for this experiment -

1. [Tutorial PDF](https://www.netdevconf.org/1.1/proceedings/slides/ahern-vrf-tutorial.pdf)
2. [Tutorial Video](https://www.youtube.com/watch?v=zxPFFdRN_x4) - See VRF with MPLS use-case
3. Stack-Exchange discussion related to [MPLS labels](https://unix.stackexchange.com/questions/401719/rtnetlink-answers-invalid-argument-mpls-on-mininet)

## Next steps

While the script is fairly well organized, this is still very hard-coded for the above setup and totally inflexible. A better idea would be to make a small tool which can read topology and create setups easily. For example, something like a dot file reader that generates a yaml and a python script that generates topology using this YAML file.

Also, this is a very static setup. Next step would be to run a routing daemon like [bird]() and try similar setup.
