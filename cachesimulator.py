
import sys

#initialize RAM
RAM = [] #a list of byte values in string
fileName = sys.argv[1]
with open(fileName, 'r') as f:
    lines = f.readlines()
    for line in lines:
        if line[-1] == '\n':
            line = line[:-1]
        RAM.append(line)
print("*** Welcome to the cache simulator ***")
print("initialize the RAM:")
TA_input = input() # have an input line
start = int(TA_input[11:13],16) # string manip to get the start
end = int(TA_input[16:18],16) #string manip to get the end
actualRAM = [] # to store the values, will set back to original ram at end
for i in range(start, end+1):
    actualRAM.append(RAM[i])
RAM = actualRAM
memorySize = len(RAM)
print("RAM successfully initialized!")

#configure cache
print("configure the cache:")
C = int(input("cache size: "))
while C < 8 or C > 256:
    C = int(input("Please re-enter cache size (must between 8 and 256 inclusive): "))
B = int(input("data block size: "))
E = int(input("associativity: "))
S = int(C/B/E) #number of sets

#cache initialization
cache = []
for s in range(S):
    set0 = []
    for e in range(E):
        line = {"valid":0, "dirty":0, "tag": "00", "block":["00"]*B}
        set0.append(line)
    cache.append(set0)
#print(cache)
#to access a block of memory, use cashe[s][e]["block"][b]. s = set #; e = line #; b = block #

numHit = 0
numMiss = 0

replacementPolicy = int(input("replacement policy: "))
replacementPolicyDic = {1:"random_replacement", 2:"least_recently_used", 3:"least_frequently_used"}
#1 = Random replacement
#2 = Least Recently Used
#3 = Least Frequently Used
writeHitPolicy = int(input("write hit policy: "))
writeHitPolicyDic = {1:"write_through", 2:"write_back"}
#1 = write-through
#2 = write-back
writeMissPolicy = int(input("write miss policy: "))
writeMissPolicyDic = {1:"write_allocate", 2:"no_write_allocate"}
#1 = write-allocate
#2 = no write-allocate
print("cache successfully configured!")

#Cache Simulation
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
        print("cache_size:",C)
        print("data_block_size:",B)
        print("associativity:",E)
        print("replacement_policy:",replacementPolicyDic[replacementPolicy])
        print("write_hit_policy:",writeHitPolicyDic[writeHitPolicy])
        print("write_miss_policy:",writeMissPolicyDic[writeMissPolicy])
        print("number_of_cache_hits:",numHit)
        print("number_of_cache_misses:",numMiss)
        print("cache content:")
        for s in range(S):
            for e in range(E):
                print(cache[s][e]["valid"],cache[s][e]["dirty"],cache[s][e]["tag"],end="")
                for b in range(B):
                    print(" "+cache[s][e]["block"][b],end="")
                print()
        
    elif option[0] == "memory-view":
        print("memory size:",memorySize)
        print("memory_content:")
        print("address:data")
        for i in range(0, memorySize, 8):
            print(hex(i).upper()+":",end="")
            for j in range(8):
                print(RAM[i+j]+" ",end="")
            print()
    
    elif option[0] == "cache-dump":
        with open("cache.txt", 'w') as f:
            for s in range(S):
                for e in range(E):
                    for b in range(B):
                        f.write(cache[s][e]["block"][b]+" ")
                    f.write("\n")
    
    elif option[0] == "memory-dump":
        with open("ram.txt", 'w') as f:
            for i in range(memorySize):
                f.write(RAM[i]+"\n")
            
            
    elif option[0] == "quit":
        break
    