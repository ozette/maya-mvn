Python 3.x

# Below some struct notes
import struct 

# Unpack to float, requires 4 bytes (single-precision) 32 bits
struct.unpack('f', 4BYTES)


# During the test phase, we'd encountered a problem.
# As soon as the size of one character is more than 1 byte i.e. Unicode, unpacking
# to a float will not work. e.g. the int value 197 was rendered as character 'Å' which
# has a size of 2 bytes. unpacking to a float requires a total of 4 bytes.
# which will give you some error like: "struct.error: unpack requires a bytes object of length 4"
# whenever you try a struct.unpack('f', floatcontainer)

# Solution given below:

# 1. first pack each character to a byte
floatcontainer = struct.pack('=B', 65)+struct.pack('=B', 95)+struct.pack('=B', 195)+struct.pack('=B', 5)

# 2. then unpack each to a float (4 byte single precision) in a variable.
# we chose the name "floatcontainer"

struct.unpack('f', floatcontainer)

>> this will give us a float value

# NOTE: please take note of the byte order, experiment if you must. python offers reading
# values in either way but only one way is the correct way.
# example: struct.unpack('>i', containerwith4bytes)
# it all depends on the order in which you fill your "floatcontainer" variable.
# NOTE: the float value will probably end with a "," character, but this can be omitted.
