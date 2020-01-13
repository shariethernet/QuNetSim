import sys

sys.path.append("../..")
from components.host import Host
from backends.cqc_backend import CQCBackend
from components.network import Network
from components.logger import Logger
from objects.daemon_thread import DaemonThread
from objects.qubit import Qubit

wait_time = 10


def main():
    # Initialize a network
    network = Network.get_instance()

    # Define the host IDs in the network
    nodes = ['Alice', 'Bob', 'Eve']

    network.delay = 0.0

    # Start the network with the defined hosts
    network.start(nodes)

    # Initialize the host Alice
    host_alice = Host('Alice')

    # Add a one-way connection (classical and quantum) to Bob
    host_alice.add_connection('Bob')

    # Start listening
    host_alice.start()

    host_bob = Host('Bob')
    # Bob adds his own one-way connection to Alice and Eve
    host_bob.add_connection('Alice')
    host_bob.add_connection('Eve')
    host_bob.start()

    host_eve = Host('Eve')
    host_eve.add_connection('Bob')
    host_eve.start()

    # Add the hosts to the network
    # The network is: Alice <--> Bob <--> Eve
    network.add_host(host_alice)
    network.add_host(host_bob)
    network.add_host(host_eve)

    # Generate random key
    key_size = 8  # the size of the key in bit
    hosts = {'Alice': host_alice,
             'Bob': host_bob,
             'Eve': host_eve}

    # Run Alice and Eve
    thread_alice = DaemonThread(host_alice.send_key, args=(host_eve, key_size))
    thread_eve = DaemonThread(host_eve.receive_key, args=(host_alice, key_size))

    thread_alice.join()
    thread_eve.join()

    print('SENDER KEYS')
    print(host_alice.qkd_keys)

    print('RECEIVER KEYS')
    print(host_eve.qkd_keys)

    for h in hosts.values():
        h.stop()
    network.stop()


if __name__ == '__main__':
    main()
