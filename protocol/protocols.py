from cqc.pythonLib import qubit

TELEPORT = 2
SUPERDENSE = 3
SEND_UDP_PACKET = 4
TERMINATE_UDP_PACKET = 5



def teleport(Sender, receiver, q):
    Sender.sendClassical(receiver, [1])
    qA = Sender.createEPR(receiver)
    q.cnot(qA)
    q.H()
    a = q.measure()
    b = qA.measure()
    m=2
    Sender.sendClassical(receiver, [m, a, b])


def receive_teleport(Receiver):
    qB = Receiver.recvEPR()
    data = Receiver.recvClassical()
    message = list(data)
    a = message[0]
    b = message[1]

    # Apply corrections
    if b == 1:
        qB.X()
    if a == 1:
        qB.Z()

    return qB


def encode(message, qubit):
    """
    Return a qubit encoded with the message message.

    Params:
    message -- the message to encode
    qubit -- the qubit to encode the message

    """
    if message == '00':
        # do nothing (i.e. perform identity)
        pass
    elif message == '01':
        qubit.X()
    elif message == '10':
        qubit.Z()
    elif message == '11':
        qubit.X()
        qubit.Z()
    else:
        raise Exception("Not possible to encode this message")

    return qubit


def decode(qA, qB):
    """
    Return the message encoded into qA with the support of qB.

    Params:
    qA -- the qubit the message is encoded into
    qB -- the supporting entangled pair

    """
    qA.cnot(qB)
    qA.H()

    # Measure
    a = qA.measure()
    b = qB.measure()

    return str(a) + str(b)


def send_superdense(Sender, message, receiver):
    qA = Sender.createEPR(receiver)
    encode(message, qA)
    Sender.sendQubit(qA, receiver)


def receive_superdense(Receiver, should_decode=True):
    qB = Receiver.recvEPR()
    qA = Receiver.recvQubit()
    if should_decode:
        return decode(qA, qB)
    else:
        return [qA, qB]


def add_checksum(Sender, qubits, size=2):
    i = 0
    check_qubits = []
    while i < len(qubits):
        check = qubit(Sender)
        j = 0
        while j < size:
            qubits[i + j].cnot(check)
            j += 1

        check_qubits.append(check)
        i += size
    return check_qubits
