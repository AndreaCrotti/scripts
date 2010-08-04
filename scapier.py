def synacker(host, port):
    # S -> SA -> A with correct values, setting right value
    p = IP(dst = host) / TCP(dport = port, flags = 'S', seq = 0)
    print p.show()
    ans = sr1(p)
    print "got ", ans.show()
    # resending the packet
    p[TCP].flags = 'A'
    p[TCP].ack = ans[TCP].seq + 1
    
    