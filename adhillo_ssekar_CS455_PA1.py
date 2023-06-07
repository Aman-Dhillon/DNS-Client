# Aman, Shruti Sekar - CS455-01
# PA1
import binascii
from socket import *
import sys # Sys module to handle command line arguments
import random # generate random id


## Get hostname from arguments
## Question: Is my-dns-client supposed to be like that or is it a variable for the IP address?
def main(argv): # main function to handle arguments
    #print(len(sys.argv))
    #print(str(sys.argv))
    if (len(sys.argv)!=3): # if less than 3 arguments are passed
    # first argument is file name
    # second argument is my-dns-client
    # third argument is hostname
        return -1 # return error
    

    #return error if second argument unexpected
    if (sys.argv[1]!="my-dns-client"):
        return -1  
    

    # if first and second parameter are good, return the third aka hostname
    return sys.argv[2]

def instantiateHostname(hostname):
    hostname = hostname.split(".") # split the hostname by period
    labelOct = [] # create a list to keep track of label hex values
    for label in hostname: # for each label
        length = len(label) # get the length and append the length in list
        #print(length)
        labelOct.append((length).to_bytes(1,'big'))
        for char in label: # for each character in a label
            #print(char)
            hex_string = ord(char) # get the hex value in the ascii table
            newVal = hex_string.to_bytes(1,'big') # conver the hex string to bytes
            #print(ord(char))
            #print(newVal)
            labelOct.append(newVal) # append the bytes version of char of label to list
            #print(bytearray.fromhex(hex_string))
    labelOct.append((0).to_bytes(1,'big'))  # terminate with root 0x0 value
    #print(labelOct)
    return labelOct

def printHex(x):
    y = str(x) #string representation of the hex value 
    for i in range(0,len(y),4):
        print(f"{y[i]}{y[i+1]}{y[i+2]}{y[i+3]}")

def constructQuery(hostname, labelOct):
    query = bytearray()
    #print("DNS HEADER")
    bitsID = random.getrandbits(16) # generate a random ID
    ID = bytearray(bitsID.to_bytes(2, "big"))
    #int(ID,16)
    query.extend(ID)
    query.extend(bytearray((256).to_bytes(2, "big"))) ##QR...RCODE
    QR = bytearray((0).to_bytes(1,'big'))
    OPCODE = bytearray((0).to_bytes(1,'big'))
    AA = bytearray((0).to_bytes(1,'big'))
    TC = bytearray((0).to_bytes(1,'big'))

    RD = bytearray((1).to_bytes(1,'big'))
    RA = bytearray((0).to_bytes(1,'big'))
    Z = bytearray((0).to_bytes(1,'big'))
    RCODE = bytearray((0).to_bytes(1,'big'))

    QDCOUNT =(1).to_bytes(2,"big")
    query.extend(bytearray(QDCOUNT))
    ANCOUNT =(0).to_bytes(2,"big")
    query.extend(bytearray(ANCOUNT))
    NSCOUNT =(0).to_bytes(2,"big")
    query.extend(bytearray(NSCOUNT))
    ARCOUNT =(0).to_bytes(2,"big")
    query.extend(bytearray(ARCOUNT))
    for value in labelOct:
        query.extend(bytearray(value))
    QTYPE=(1).to_bytes(2,"big")
    query.extend(bytearray(QTYPE))
    QCLASS=(1).to_bytes(2,"big")
    #print(QCLASS)
    query.extend(bytearray(QCLASS))

    #print out dns header in both hex and decimal for the TA to read

    print("DNS QUERY HEADER SECTION")
    print("header.ID="+str(int.from_bytes(ID,'big')))
    print("header.QR="+str(int.from_bytes(QR,'big')))
    print("header.OPCODE="+str(int.from_bytes(OPCODE,'big')))
    print("header.AA="+str(int.from_bytes(AA,'big')))
    print("header.TC="+str(int.from_bytes(TC,'big')))
    print("header.RD="+str(int.from_bytes(RD,'big')))
    print("header.RA="+str(int.from_bytes(RA,'big')))
    print("header.Z="+str(int.from_bytes(Z,'big')))
    print("header.RCODE="+str(int.from_bytes(RCODE,'big')))
    print("header.QDCOUNT="+str(int.from_bytes(QDCOUNT,'big')))
    print("header.ANCOUNT="+str(int.from_bytes(ANCOUNT,'big')))
    print("header.NSCOUNT="+str(int.from_bytes(NSCOUNT,'big')))
    print("header.ARCOUNT="+str(int.from_bytes(ARCOUNT,'big')))
    print("DNS QUERY QUESTION SECTION")
    print("question.QNAME="+hostname)
    print("question.QTYPE="+str(int.from_bytes(QTYPE,'big')))
    print("question.QCLASS="+str(int.from_bytes(QCLASS,'big')))
    print()
    #print("question.QCLASS=0x"+bytes(binascii.hexlify(QCLASS)).decode("ascii"))
    #printHex(query.hex())
    #print(query)

    print("DNS QUERY HEADER IN HEX")
    print("header.ID=0x"+bytes(binascii.hexlify(ID)).decode("ascii"))
    print("header.QR="+hex(0))
    print("header.OPCODE="+hex(0))
    print("header.AA="+hex(0))
    print("header.TC="+hex(0))
    print("header.RD="+hex(1))
    print("header.RA="+hex(0))
    print("header.Z="+hex(0))
    print("header.RCODE="+hex(0))
    #print("header.QDCOUNT="+hex(bytearray(QDCOUNT).decode('ascii')))
    print("header.QDCOUNT=0x"+bytes(binascii.hexlify(QDCOUNT)).decode("ascii"))
    print("header.ANCOUNT=0x"+bytes(binascii.hexlify(ANCOUNT)).decode("ascii"))
    print("header.NSCOUNT=0x"+bytes(binascii.hexlify(NSCOUNT)).decode("ascii"))
    print("header.ARCOUNT=0x"+bytes(binascii.hexlify(ARCOUNT)).decode("ascii"))
    print("DNS QUERY QUESTION IN HEX")
    print("question.QNAME= ",end="")
    for value in labelOct:
        print(bytes(binascii.hexlify(value)).decode("ascii")+ " " ,end="")
    print()
    print("question.QTYPE=0x"+bytes(binascii.hexlify(QTYPE)).decode("ascii"))
    print("question.QCLASS=0x"+bytes(binascii.hexlify(QCLASS)).decode("ascii"))

    print()
    print("COMPLETE DNS QUERY")
    print(query) # actual byte version of query
    return query 

# Send message to the socket
# Question: The receive function is timing out. Is this due to our message?
def socketFunc(message):
    #connected=False
    print()
    i=1
    while(i <= 3): # only 3 times you can try to connect to the socket
        #print(i)
        try:
            serverName = "8.8.8.8"
            serverPort = 53
            clientSocket = socket(AF_INET,SOCK_DGRAM)
            clientSocket.settimeout(5)
            print("Contacting DNS server...")
            clientSocket.connect((serverName,serverPort))
            print("Sending DNS query...")
            clientSocket.send(message)
            print("DNS Response Received (attempt " + str(i) + " out of 3)")
            msg = clientSocket.recv(10000)
            if msg != b'':
                clientSocket.close()
                #print(msg)
                print("Processing DNS Response")
                return msg
        except:
            i+= 1
            clientSocket.close()
            print()

        #print(i)
        
    return -1
    
def responseParse(response):
    list1 = []
    for byt in response: # get list bytes and append the hex value to a new list
        list1.append(hex(byt))
    #print(list1)
    #print(type(list1[0]))
    #print(list1[0])
    #print(list1)
    ID = list1[0]+" "+list1[1] # ge the ID
    #idHalf1 = bin(int(list1[0],16))[2:]
    #idHalf2 = bin(int(list1[1],16))[2:]
    print()
    print("RESPONSE")
    print("header.ID="+ID)

    # print header information

    # print flags as binary, then break down each bit and assign to according header section
    flags = list1[2]
    flags2 = list1[3]
    flagHalf1 = bin(int(flags,16))[2:]
    flagHalf2 = bin(int(flags2,16))[2:]
    #print(flagHalf1)
    #print(flagHalf2)
    print("header.QR="+str(int(flagHalf1[0],2)))
    print("header.OPCODE="+str(int(flagHalf1[1:5],2)))
    print("header.AA="+str(int(flagHalf1[5],2)))
    print("header.TC="+str(int(flagHalf1[6],2)))
    print("header.RD="+str(int(flagHalf1[7],2)))
    print("header.RA="+str(int(flagHalf2[0],2)))
    print("header.Z="+str(int(flagHalf2[1:4],2)))
    print("header.RCODE="+str(int(flagHalf2[4:8],2)))
    qdCount = list1[4][2:]+list1[5][2:]
    qdCount = int(qdCount,16)
    #print(qdCount)
    #qd1 = int(list1[4],16)
    #qd2 = int(list1[5],16)
    #print(qd1)
    #print(qd2)
    print("header.QDCOUNT="+str(qdCount))
    anCount = list1[6][2:]+list1[7][2:]
    anCount = int(anCount,16)
    print("header.ANCOUNT="+str(anCount))
    nsCount = list1[8][2:]+list1[9][2:]
    nsCount = int(nsCount,16)
    print("header.NSCOUNT="+str(nsCount))
    arCount = list1[10][2:]+list1[11][2:]
    arCount = int(arCount,16)
    print("header.ARCOUNT="+str(arCount))

    print()
    i=12
    qname=""
    nextLength= int(list1[i][2:],16)
    # print out qname in ascii
    while (nextLength!=0): 
        #print("I: " + str(i))
        #print("NEXTLENGTH:" + str(nextLength))
        currentNum = i
        i+=1
        for j in range(currentNum+1,currentNum+nextLength+1): # get the character in between the length labels
            #print("J"+str(int(list1[j])[2:],16))
            #rint(list1[j][2:])
            qname+=chr(int(list1[j][2:],16)) # add ascii version of character to the qname
            i+=1
        nextLength= int(list1[i][2:],16) # get the next length
        if nextLength!=0: # add period if not the last length label
            qname+="."
    #print question section 
    print("question.QNAME="+qname)
    qType = list1[i+1][2:]+list1[i+2][2:]
    qType = int(qType,16)
    print("question.QTYPE="+str(qType))
    qClass = list1[i+3][2:]+list1[i+4][2:]
    qClass = int(qClass,16)
    print("question.QCLASS="+str(qClass))

    records = list1[i+5:]
    numrecords = (int) (len(records)/16)
    #print(records)
    # 0,1, 16/17
    """ currentRecord = []
    FullRecord = []
    for i in range(len(records)+1):
        if i!=0 and i%16==0:
            currRecord = currentRecord.copy()
            FullRecord.append(currRecord)
            currentRecord=[]
        
    print(FullRecord)

    for list2 in FullRecord:
        print(len(list2))
    for i in range(numrecords): """
    currentIndex = 0
    while currentIndex < len(records): # while bytes left to parse in records
        print()
        # print the response columns for the answers
        #print(currentIndex)
        name=records[currentIndex][2:]
        currentIndex += 1
        name += records[currentIndex][2:]
        currentIndex += 1
        name = int(name,16)
        print("answer.NAME="+str(name))
        
        Type = records[currentIndex][2:]
        currentIndex += 1
        Type += records[currentIndex][2:]
        currentIndex += 1
        Type = int(Type,16)
        print("answer.TYPE="+str(Type))

        Class = records[currentIndex][2:]
        currentIndex += 1
        Class += records[currentIndex][2:]
        currentIndex += 1
        Class = int(Class,16)
        print("answer.CLASS="+str(Class))

        ttl = records[currentIndex][2:]
        currentIndex += 1
        ttl+=records[currentIndex][2:]
        currentIndex += 1
        ttl+= records[currentIndex][2:]
        currentIndex += 1
        ttl+= records[currentIndex][2:]
        currentIndex += 1
        ttl = int(ttl,16)
        print("answer.TTL="+str(ttl))

        RDlength = records[currentIndex][2:]
        currentIndex += 1
        RDlength+= records[currentIndex][2:]
        currentIndex += 1
        RDlength = int(RDlength,16)
        print("answer.RDLENGTH="+str(RDlength))

        if Type !=1: # if not type 1 record
            cname=""
            nextLength= int(records[currentIndex][2:],16) # get the length of the label
            while nextLength !=0: # while the label hasn't ended
                #print(str(nextLength) + " nextLength")
                currChar = currentIndex # get current index of the character
                currentIndex+=1  
                for j in range(currChar+1,currChar+nextLength+1): # for the length of the label
                    #print(str(j)+" J")
                    #print(str(records[j][2:]) + " record value")
                    cname+=chr(int(records[j][2:],16)) # add the ascii value of the label to the cname string
                    #print(str(currentIndex) + " currentIndex")
                    currentIndex+=1 
                nextLength=int(records[currentIndex][2:],16) # check next length
                if nextLength!=0: # as long as not the last label, add a period to separate bytes
                    cname+="."
            #print(currentIndex)
            currentIndex+=1 # takes care of root 0x0
            print("answer.RDATA="+str(cname))
        else:  # print out 4 bytes of IP address if type is 1 (A record)
            ipAddress = ""
            ipAddress+= str(int(records[currentIndex][2:],16))
            currentIndex += 1
            ipAddress+="."

            ipAddress+= str(int(records[currentIndex][2:],16))
            currentIndex += 1
            ipAddress+="."

            ipAddress+= str(int(records[currentIndex][2:],16))
            currentIndex += 1
            ipAddress+="."

            ipAddress+= str(int(records[currentIndex][2:],16))
            currentIndex += 1
            print("answer.RDATA="+str(ipAddress)+"\t## resolved IP address ##")

    '''
    for i in range(0,len(records),16):
        print()
        #print(records[i+15])
        name = records[i][2:] + records[i+1][2:]
        name = int(name,16)
        print("answer.NAME="+str(name))

        Type = records[i+2][2:] + records[i+3][2:]
        Type = int(Type,16)
        print("answer.TYPE="+str(Type))
        

        Class = records[i+4][2:] + records[i+5][2:]
        Class = int(Class,16)
        print("answer.CLASS="+str(Class))

        ttl = records[i+6][2:] + records[i+7][2:] + records[i+8][2:] + records[i+9][2:]
        ttl = int(ttl,16)
        print("answer.TTL="+str(ttl))

        RDlength = records[i+10][2:] + records[i+11][2:]
        RDlength = int(RDlength,16)
        print("answer.RDLENGTH="+str(RDlength))

        ipAddress = ""
        for j in range(4):
            if j!=0:
                ipAddress+="."
            ipAddress+= str(int(records[i+12+j][2:],16))
        #Rdata = records[i+12][2:] + records[i+13][2:] + records[i+14][2:] + records[i+15][2:]
        #Rdata = int(Rdata,16)
        print("answer.RDATA="+str(ipAddress))

        """ currentRecord = records[i*numrecords:i*numrecords+16]
        print(currentRecord)
        print()
        print("Record #" + str(i+1))
        name = records[i*numrecords][2:] + records[i*numrecords+1][2:]
        name = int(name,16)
        print("answer.NAME="+str(name)) """
    '''

    '''
    name = 2
    type = 2
    class = 2
    ttl = 4
    data = 2
    address = 4
    We have our byte values in a list - we can actually get the integer values as well
    If we're parsing and assigning values right, we need to concatenate the bytes and their meaning
    Readable: 
    '''

    #print(int.from_bytes(response,'big'))
    #print(codecs.getencoder(response))
    #response.decode('utf-8')
    #responseSplit = response.split(b"\x")
    #print(responseSplit)
    return

# once entering the file, 
if __name__ == "__main__":
    # get hostname using argument function
    hostname = main(sys.argv[1:])
    # if the hostname is an error
    if hostname == -1:
        print("Error in cmd arguments")
    else: # if hostname is okay
        #print("continue")
        print("Preparing DNS Query ...")
        print()
        labelOct = instantiateHostname(hostname) # to get set the hostname hex values
        message = constructQuery(hostname,labelOct) # construct and create query in hex and decimal
        response = socketFunc(message) # send query to socket and get response back
        if response != -1: # if not invalid or timed out
            responseParse(response) # parse and print the response message and IP addresses



#####
'''
Questions to ask: 
1. Is it okay to use import binascii module?
2. For printing out the complete dns query in hex, is it okay to have the flags section
as 0x0 or should we write the flags together concatenated (0x100)
3. Is the complete DNS query a repeat of printing the question and header in hex, or to print
simply the bytearray that we are sending to the socket?
4. For google.com, it doesn't print additional records
'''