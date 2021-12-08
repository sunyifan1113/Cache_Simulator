import sys
import math

# initialize RAM
RAM = []  # a list of byte values in string
fileName = sys.argv[1]
with open(fileName, 'r') as f:
    lines = f.readlines()
    for line in lines:
        if line[-1] == '\n':
            line = line[:-1]
        RAM.append(line)
print("*** Welcome to the cache simulator ***")
print("initialize the RAM:")
TA_input = input()  # have an input line
start = int(TA_input[11:13], 16)  # string manip to get the start
end = int(TA_input[16:18], 16)  # string manip to get the end
actualRAM = []  # to store the values, will set back to original ram at end
for i in range(256):
    actualRAM.append("00")
for i in range(start, end + 1):
    actualRAM[i] = RAM[i]

RAM = actualRAM
memorySize = len(RAM)




print("RAM successfully initialized!")

# configure cache
print("configure the cache:")
C = int(input("cache size: "))
while C < 8 or C > 256:
    C = int(input("Please re-enter cache size (must between 8 and 256 inclusive): "))
B = int(input("data block size: "))
E = int(input("associativity: "))
S = int(C / B / E)  # number of sets

# cache initialization
cache = []
for s in range(S):
    set0 = []
    for e in range(E):
        line = {"valid": 0, "dirty": 0, "tag": "00", "block": ["00"] * B}
        set0.append(line)
    cache.append(set0)
# print(cache)
# to access a block of memory, use cashe[s][e]["block"][b]. s = set #; e = line #; b = block #
print(cache[s][e]["block"])
numHit = 0
numMiss = 0

replacementPolicy = int(input("replacement policy: "))
replacementPolicyDic = {1: "random_replacement", 2: "least_recently_used", 3: "least_frequently_used"}
# 1 = Random replacement
# 2 = Least Recently Used
# 3 = Least Frequently Used
writeHitPolicy = int(input("write hit policy: "))
writeHitPolicyDic = {1: "write_through", 2: "write_back"}
# 1 = write-through
# 2 = write-back
writeMissPolicy = int(input("write miss policy: "))
writeMissPolicyDic = {1: "write_allocate", 2: "no_write_allocate"}
# 1 = write-allocate
# 2 = no write-allocate
print("cache successfully configured!")


################################################################# FUNCTIONS#################################################################

def replaceStuff(tag):
    if replacementPolicy == 1:
        randomReplace(tag)
    elif replacementPolicy == 2:
        print("not implement yet")


def randomReplace(tag):

    first_line = []
    for i in range(8):
        first_line.append("00")
    for i in range(8):
        first_line[i] = RAM[i]

    for b in range(len(cache[s][e]["block"])):
        cache[0][0]["block"][b] = first_line[b]
    cache[0][0]["valid"] = 1
    cache[0][0]["tag"] = tag
    print("eviction_line:0")


def readCache(address):
    binAdd = format(address, '08b')
    s = math.log2(S)
    m = math.log2(memorySize)
    b = math.log2(B)
    t = m - (s + b)

    tag = ""
    setInd = ""
    blockOff = ""

    for i in range(len(binAdd)):
        if (i < t):
            tag = tag + binAdd[i]
        elif (i >= t and i < t + s):
            setInd = setInd + binAdd[i]
        else:
            blockOff = blockOff + binAdd[i]
    find = ""
    find = find + tag + setInd + blockOff

    setInDec = int(str(setInd), 2)
    blockOffInDec = int(str(blockOff), 2)
    toChange = blockOffInDec * 2
    print("set:" + str(setInDec))
    print("tag:" + str(int(str(tag), 2)))

    tag = int(tag, 2) # this converts the tag to hex so it matches whats in the cache
    if (tag == 0):
        tag = "00"
    elif (tag == 8):
        tag = "08"
    else:
        tag = hex(tag).upper()
        tag = tag[-2:]# this converts the tag to hex so it matches whats in the cache

    newData = ""
    if checkHit(address):
        for e in range(E):
            if cache[setInDec][e]["tag"] == tag:
                newData = cache[setInDec][e]["block"][blockOffInDec]
                break
        print("hit:yes")
        print("eviction_line:-1")
        print("ram_address:-1")
        print("data:0x" + newData)
        global numHit
        numHit += 1
    elif not checkHit(address):
        print("hit:no")
        tag = int(tag, 2)
        if(tag == 0): # this converts the tag to hex so it matches whats in the cache
            tag = "00"
        elif(tag == 8):
            tag = "08"
        else:
            tag = hex(tag).upper()# this converts the tag to hex so it matches whats in the cache
            tag = tag[-2:]

        addrIndex = address

        if(address == 0):
            address = "00"
        elif(address == 8):
            address = "08"
        else:
            address = hex(address).upper()
            address = address[-2:]

        replaceStuff(tag)
        print("ram_address:0x" + address)
        print("data:0x" + RAM[addrIndex])
        global numMiss
        numMiss += 1




def checkHit(address):
    binAdd = format(address, '08b')
    s = math.log2(S)
    m = math.log2(memorySize)
    b = math.log2(B)
    t = m - (s + b)

    tag = ""
    setInd = ""
    blockOff = ""

    for i in range(len(binAdd)):
        if i < t:
            tag = tag + binAdd[i]
        elif t <= i < t + s:
            setInd = setInd + binAdd[i]
        else:
            blockOff = blockOff + binAdd[i]
    tag = int(tag, 2)
    if (tag == 0):
        tag = "00"
    elif (tag == 8):
        tag = "08"
    else:
        tag = hex(tag).upper()
        tag = tag[-2:]
    setInDec = int(str(setInd), 2)
    for e in range(E):
        if cache[setInDec][e]["valid"] == 1:
            if cache[setInDec][e]["tag"] == tag:
                return True
        else:
            return False


# Cache Simulation
while True:
    print("*** Cache simulator menu ***")
    print("type one command:")
    print("1. cache-read")
    print("2. cache-write")
    print("3. cache-flush")
    print("4. cache-view")
    print("5. memory-view")
    print("6. cache-dump")
    print("7. memory-dump")
    print("8. quit")
    option = input().split()
    if option[0] == "cache-read":
        address = int(option[1].lower(), 16)
        readCache(address)

    elif option[0] == "cache-write":
        address = option[1]
        data = option[2]

    elif option[0] == "cache-flush":
        for s in range(S):
            for e in range(E):
                cache[s][e]["valid"] = 0
                cache[s][e]["dirty"] = 0
                cache[s][e]["tag"] = "00"
                for b in range(B):
                    cache[s][e]["block"][b] = "00"
        numHit = 0
        numMiss = 0
        print("cache_cleared")

    elif option[0] == "cache-view":
        print("cache_size:", C)
        print("data_block_size:", B)
        print("associativity:", E)
        print("replacement_policy:", replacementPolicyDic[replacementPolicy])
        print("write_hit_policy:", writeHitPolicyDic[writeHitPolicy])
        print("write_miss_policy:", writeMissPolicyDic[writeMissPolicy])
        print("number_of_cache_hits:", numHit)
        print("number_of_cache_misses:", numMiss)
        print("cache content:")
        for s in range(S):
            for e in range(E):
                print(cache[s][e]["valid"], cache[s][e]["dirty"], cache[s][e]["tag"], end="")
                for b in range(B):
                    print(" " + cache[s][e]["block"][b], end="")
                print()

    elif option[0] == "memory-view":
        print("memory size:", memorySize)
        print("memory_content:")
        print("address:data")
        for i in range(0, memorySize, 8):
            label = str(hex(i))
            hex_part = label[-2:].upper()
            if (i == 0):
                print("0x" + "00" + ":", end="")
            elif (i == 8):
                print("0x" + "08" + ":", end="")
            else:
                print("0x" + hex_part + ":", end="")
            for j in range(8):
                print(RAM[i + j] + " ", end="")
            print()

    elif option[0] == "cache-dump":
        with open("cache.txt", 'w') as f:
            for s in range(S):
                for e in range(E):
                    for b in range(B):
                        f.write(cache[s][e]["block"][b] + " ")
                    f.write("\n")

    elif option[0] == "memory-dump":
        with open("ram.txt", 'w') as f:
            for i in range(memorySize):
                f.write(RAM[i] + "\n")


    elif option[0] == "quit":
        break
