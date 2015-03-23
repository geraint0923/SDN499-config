
# Setting up the network (the topo-2sw-2host.py file can be found in ~/mininet/custom/)
```
$ sudo mn --custom topo-2sw-2host.py --topo mytopo --mac --switch ovsk,protocols=OpenFlow13 --controller=remote

```

# Adding rules
```
mininet> sh ovs-ofctl  -O OpenFlow13 add-flow s0 in_port=2,actions=output:1,push_mpls:0x8847,set_mpls_label0:,output:3
mininet> sh ovs-ofctl  -O OpenFlow13 add-flow s0 in_port=1,actions=output:2,push_mpls:0x8847,set_mpls_label:0,output:3
mininet> sh ovs-ofctl  -O OpenFlow13 add-flow s2 in_port=1,actions=output:2,push_mpls:0x8847,set_mpls_label:8,output:3
mininet> sh ovs-ofctl  -O OpenFlow13 add-flow s2 in_port=2,actions=output:1,push_mpls:0x8847,set_mpls_label:8,output:3
mininet> sh ovs-ofctl  -O OpenFlow13 add-flow s1 in_port=1, actions=output:3,push_mpls:0x8847,set_mpls_label:4,output:4
mininet> sh ovs-ofctl  -O OpenFlow13 add-flow s1 in_port=3, actions=output:1,push_mpls:0x8847,set_mpls_label:4,output:4

```
# Dump MPLS
```
mininet> h3 tcpdump -l -XX -n -i h3-eth0 > /tmp/test &

```
or you can do:

```
mininet> h3 tcpdump -l -XX -n any > /tmp/test &

```

# Ping to active sending packets
```
mininet> h1 ping h2

```

# Run the send_pkt.py
```
$ ~/ryu/bin/ryu-manager send_pkt.py

```

# Check the MPLS
```
$ tail -f /tmp/test

```
