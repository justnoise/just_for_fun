
class Netset(object):
    """
    Creates a prefix tree of IPs in a set each node in the tree is
    represented by a 3 element list The first child represents a 0 in
    the prefix tree the second child represents a 1 in the prefix tree
    the third entry tells us if this is the terminal node of a network
    prefix

    A network that looks like:
    '128.0.0.0/2'
    is represented by a bitstring of [1,0]
    and as a prefix tree would look like
          [None ,  , False]
                  \
            [  , None, False]
             /
     [None, None, True]

    or in single line form:
    [None, [[None, None, True], None, False], False]
    """
    def __init__(self, ips = None, match_supernet=False):
        # todo: document matching supernets
        self.root = self._new_node()
        if ips and type(ips) not in (list, tuple):
            raise TypeError("ips must be a list or tuple")
        if ips:
            for ip in ips:
                self.add_ip(ip)
        self.match_supernet = match_supernet

    def add_ip(self, ip):
        ip_bitstring = self._ip_to_bitstring(ip)
        node = self.root
        for i, b in enumerate(ip_bitstring):
            if node[b]:
                node = node[b]
            else:
                node[b] = self._new_node()
                node = node[b]
        node[2] = True

    def has_ip(self, ip):
        ip = self._ip_to_bitstring(ip)
        node = self.root
        for b in ip:
            if node == None:
                return False
            if node[2]:
                return True
            else:
                node = node[b]
        if node == None:
            return False
        elif self.match_supernet:
            return True
        else:
            return node[2]

    def _new_node(self):
        """ [zero child, one child, terminus]"""
        return [None, None, False]

    def _ip_char_to_binary(self, ip):
        char_bin = ''.join(["{:08b}".format(int(oct)) for oct in ip.split('.')])
        return map(int, char_bin)

    def _ip_to_bitstring(self, ip):
        parts = ip.split('/')
        cidr = 32
        ip = parts[0]
        ip_bits = self._ip_char_to_binary(ip)
        if len(parts) == 2:
            cidr = int(parts[1])
            ip_bits = ip_bits[:cidr]
        return ip_bits


def test():
    exact_ip = '240.140.255.255'
    ns = Netset([exact_ip])
    assert ns.has_ip(exact_ip) == True
    assert ns.has_ip('240.140.255.254') == False

    network = '128.0.0.0/8'
    ns = Netset([network])
    assert ns.has_ip('128.255.255.255') == True
    assert ns.has_ip('128.128.0.0') == True
    assert ns.has_ip('192.0.0.0/1') == False
    assert ns.has_ip('127.0.0.0') == False

    network = '54.192.0.0/10'
    ns = Netset([network], match_supernet=True)
    assert ns.has_ip('54.255.0.0/16') == True
    assert ns.has_ip('54.0.0.0/8') == True
    assert ns.has_ip('55.0.0.0/8') == False

    print "PASSED"

if __name__ == '__main__':
    test()
