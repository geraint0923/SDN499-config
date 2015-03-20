# SDN499-config
The scripts and tools to setup the virtual SDN experiment environment.
Reference http://archive.openflow.org/wk/index.php/OpenFlow_Tutorial#Import_Virtual_Machine_Image

The finished environment will be look like:

![Image of Yaktocat](https://github.com/geraint0923/SDN499-config/raw/master/img/topo.png)

## Setup Virtual Machine
Download the virtual machine image from OpenFlow official website:

```
wget https://github.com/downloads/mininet/mininet/mininet-2.0.0-113012-amd64-ovf.zip
```

Unzip the image:

```
unzip mininet-2.0.0-113012-amd64-ovf.zip
```

Convert the VMDK image to QCOW2 image so that QEMU/KVM could use:

```
cd mininet-ovf
qemu-img convert -f vmdk -O qcow2 mininet-vm-disk1.vmdk mininet-vm-disk1.qcow2
```

Create three different virtual machine images based on one QCOW2 image:

```
qemu-img create -f qcow2 -b mininet-vm-disk1.qcow2 mininet-vm1.qcow2
qemu-img create -f qcow2 -b mininet-vm-disk1.qcow2 mininet-vm2.qcow2
qemu-img create -f qcow2 -b mininet-vm-disk1.qcow2 mininet-vm3.qcow2
```

Modify the scripts in 'vm' directory to adjust the hard disck image to different QCOW2 images.

## Setup Networks for All three Virtual Machines
Execute the script in 'network' directory to setup VM network:

```
cd network
./vm-net.sh
```

Start up the virtual machines:

```
cd ../vm
./startup1.sh &
./startup2.sh &
./startup3.sh &
```

Log into each of the virtual machines and configure the network:

```
ssh -p 2201(2202/2203 chnage this when log into different VM) mininet@localhost
vim /etc/network/interfaces
```

Update the /etc/network/interfaces in different VMs:

```
# The loopback network interface
auto lo
iface lo inet loopback

# The primary network interface
auto eth0
iface eth0 inet dhcp

auto eth2
iface eth2 inet static
address 10.0.66.10
#address 10.0.66.10	for the second VM
#address 10.0.66.10	for the third VM
netmask 255.255.255.0
```

Reboot the VM to make the configurations work:

```
reboot
```

## Configure the physical SDN switch Pica8

Copy the script network/pica8.sh to the physical SDN switch, and then execute this script:

```
./pica8.sh
```

## Start Up the Ryu Controller

First install Ryu on the host server

```
git clone git://github.com/osrg/ryu.git
cd ryu; python ./setup.py install
```

Then start up the Ryu simple switch controller

```
PYTHONPATH=. ./bin/ryu-manager --verbose ryu/app/simple_switch.py
```

Note that, you can also use your customized switch application script in the last step.

## Done

Currently, the configuration of the whole experiment environment is done. And the experiments could be performed now.
