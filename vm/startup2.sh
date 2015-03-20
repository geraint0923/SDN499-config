#!/bin/bash
qemu-kvm -enable-kvm -m 2048 -drive file=/home/XXX/vm/openflow/mininet-vm-h2.qcow2,if=virtio -net nic,model=virtio,vlan=2 -net user,vlan=2,hostfwd=tcp::2202-:22 -net nic,model=virtio,macaddr=52:54:00:12:23:20 -net tap,ifname=tap2 -net nic,vlan=1,model=virtio,macaddr=66:54:00:12:33:20 -net tap,vlan=1,ifname=tap22 -nographic
