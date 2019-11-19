#### Access flask server from within docker container

Change the host that flask is running on to '0.0.0.0'. The localhost in the container is local only to the container, not to your computer:

`flask run -h 0.0.0.0`

This will bind the app to all network interfaces on the container and will be reachable by your machine

#### Why Is LocalHost Unreachable?

Docker containers are their own little self-contained networks. They have an external interface, eth0, they have an external ip address, they have routing tables, and a localhost. Localhost doesn't map to an external interface, and it's generally bad practice to try to do so.

Let's take a simple container as an example, I'll just run a linux container like so:

docker run -it ubuntu bash
Now I can check out the network details inside that container by running apt-get update && apt-get install net-tools:
```
ifconfig
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 172.17.0.2  netmask 255.255.0.0  broadcast 172.17.255.255
        ether 02:42:ac:11:00:02  txqueuelen 0  (Ethernet)
        RX packets 11286  bytes 16471897 (16.4 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 3421  bytes 189224 (189.2 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        loop  txqueuelen 1  (Local Loopback)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

`lo` is loopback, or localhost. It's a completely separate interface and is not externally facing, eth0, however, is. You can bind to it, but I wouldn't guarantee that the ip address is the same all the time. 

So the easiest way is to bind flask to all of them.

`loopback` is simply for the network to communicate with itself, nothing more. It doesn't need to have an externally facing component, because by design it's not intended for external communication