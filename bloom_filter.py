import array
import math
import hashlib
import csv
import sys

#START OF CODE BY WILFREDO LUGO
#will be used as global functions
def makeBitArray(bitSize, fill = 0):
    intSize = bitSize >> 5                   # number of 32 bit integers
    if (bitSize & 31):                      # if bitSize != (32 * n) add
        intSize += 1                        #    a record for stragglers
    if fill == 1:
        fill = 4294967295                                 # all bits set
    else:
        fill = 0                                      # all bits cleared

    bitArray = array.array('I')          # 'I' = unsigned 32-bit integer
    bitArray.extend((fill,) * intSize)
    return(bitArray)

# testBit() returns a nonzero result, 2**offset, if the bit at 'bit_num' is set to 1.
def testBit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = 1 << offset
    return(array_name[record] & mask)

# setBit() returns an integer with the bit at 'bit_num' set to 1.
def setBit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = 1 << offset
    array_name[record] |= mask
    return(array_name[record])

# clearBit() returns an integer with the bit at 'bit_num' cleared.
def clearBit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = ~(1 << offset)
    array_name[record] &= mask
    return(array_name[record])

# toggleBit() returns an integer with the bit at 'bit_num' inverted, 0 -> 1 and 1 -> 0.
def toggleBit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = 1 << offset
    array_name[record] ^= mask
    return(array_name[record])

#usage examples
# bloomArray  = makeBitArray(10) #Creates a 10 bit array
# setBit(bloomArray,5) #Set Bit 5 of bloomArray to 1
# clearBit(bloomArray,5) #Set Bit 5 of bloomArray to 0
# testBit(bloomArray,5) # Returns a non-zero value if bit 5 is not zero.

#END OF CODE BY WILFREDO LUGO


#class to represent and create an instance of a Bloom Filter
#   Our Bloom Filter depends only on the amount of emails in the input CVS file.
class BloomFilter:
    def __init__(self, n):
        #n: number of items in the filter; will be taken as the number of emails in the input
        self.n = n
        #p: probability of false positives; given as 0.0000001
        self.p = 0.0000001
        #m: number of bits in the filter
        self.m = math.ceil((n * math.log(0.0000001)) / math.log(1 / pow(2, math.log(2))))
        #k: number of hash functions
        self.k = round((self.m / n) * math.log(2))
        #bit array of the Bloom Filter
        self.bloomArray = makeBitArray(self.m)

    #add the added elements' hashed indexes into the bloom array
    def add(self, email):
        #for every hash function, add the hashed index into the bloom array
        for hash in range(self.k):
            hashed = int(hashlib.sha256(email.encode('utf-8')).hexdigest(), 16) % self.m
            setBit(self.bloomArray, hashed)

    #check if the desired elements' hashed indexes are set to 1 in the bloom array
    def check(self, email):
        #for every hash function, check if the hashed index is set to 1
        for hash in range(self.k):
            hashed = int(hashlib.sha256(email.encode('utf-8')).hexdigest(), 16) % self.m
            #if any the hashed indexes are not set to 1, the item is not in the DB
            if testBit(self.bloomArray, hashed) == 0:
                return "Not in the DB"
        #if all of the email's hashed indexes are set to 1, the email might be in the DB
        return "Probably in the DB"

def main():
    if len(sys.argv) > 1:
        #store the files passed to build and test our Bloom Filter
        initial = sys.argv[1]
        to_check = sys.argv[2]

        #initialize the filter
        with open(initial, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            
            #number of bits in the bloom array
            rows = list(reader)
            n = len(rows)
            bloom_filter = BloomFilter(n)

            #add the initial values to the filter
            for row in rows:
                bloom_filter.add(row[0])

        #check if the new emails are in the DB
        with open(to_check, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                print(f'{row[0]},{bloom_filter.check(row[0])}')

if __name__ == "__main__":
    main()
