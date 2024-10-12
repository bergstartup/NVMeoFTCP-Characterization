#1st arg interface, 2nd arg ipv4 address

ifconfig $1 172.16.137.$2 netmask 255.255.255.248 up
ifconfig $1 mtu 9000 up
ifconfig | grep $1
