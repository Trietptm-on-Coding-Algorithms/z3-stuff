from z3 import *
def getIndex(x,i,length):
    return (LShR(x,  (length-i-1)*8) & 0xff)
def isAscii(s,x,length):
    for i in range(length):
        s.add( And(32 <= getIndex(x,i,length),getIndex(x,i,length) < 128))
def intToText(x,length):
    return hex(x)[2:].strip('L').ljust(2*length,'0').decode('hex')
def z3crc64(data,length):
    crc = 0xFFFFFFFFFFFFFFFF
    for block in range((length-1)*8, -1, -8):
        crc ^= LShR(data, block) & 0xFF
        for i in range(8):
            crc = If(crc & 1 == BitVecVal(1, 8*length), LShR(crc, 1) ^ 0xC96C5795D7870F42, LShR(crc, 1))
    return crc ^ 0xFFFFFFFFFFFFFFFF
def Breakcrc64(_crc,length):
    s = Solver()
    data = BitVec('data',8*length)
    crc = z3crc64(data,length)
    isAscii(s,data,length)
    s.add(crc == _crc)
    print  s.check()
    #find all solution, However, In this case, there is only one souution
    while s.check() == sat:
      m = s.model()
      print intToText(m.eval(data).as_long(),length)
      s.add(data != m[data])

Breakcrc64(0x5C8B80482BAC7809,10)
print "End"
