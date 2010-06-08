# get unsigned bits
def _getUBits(bitList, bitPos, nr):
    valD = 0
    for runD in xrange(bitPos, bitPos+nr):
        valD = valD*2 + bitList[runD]
    return valD

# get signed bits
def _getSBits(bitList, bitPos, nr):
    valD = 0
    for runD in xrange(bitPos+1, bitPos+nr): #skip the first bit -> it is the sign
        valD = valD*2 + bitList[runD]
    if bitList[bitPos]: valD = -valD
    return valD


def analyseContent(data):
    """ Analyzes content of (possible compressed) swf file
        and returns header's data as a dictionary
    """
    if len(data)<=(8+17):
        raise "Content error","data too small!"
    # Uncompressed flash file
    if str(data[:3]) == 'FWS':
        compressed=0
    # Version 6 or greater ZLIB compressed flash file
    elif ((str(data[:3]) == 'CWS') or (str(data[:3]) == 'FWC')):
    	compressed=1
    else:
        raise "Content error","This does not appear to be an SWF file!"

    version = str(ord(data[3]))
    uncompressed_size = ord(data[4]) + ord(data[5])*256 + ord(data[6])*256*256 + ord(data[7])*256*256*256

    data=data[8:1024]
    if compressed:
        from zlib import decompressobj
        do = decompressobj()
        data=do.decompress(data)
        do.flush()

    bitList = []
    for runD in xrange(0, 17):
        byteD = ord(data[runD])
        bitList.append( (byteD&128)/128 )
        bitList.append( (byteD&64)/64 )
        bitList.append( (byteD&32)/32 )
        bitList.append( (byteD&16)/16 )
        bitList.append( (byteD&8)/8 )
        bitList.append( (byteD&4)/4 )
        bitList.append( (byteD&2)/2 )
        bitList.append( (byteD&1)/1 )
    bitPos = 0
    fieldSize = _getUBits(bitList, bitPos, 5); bitPos=bitPos + 5
    x1 = _getSBits(bitList, bitPos, fieldSize); bitPos=bitPos + fieldSize
    x2 = _getSBits(bitList, bitPos, fieldSize); bitPos=bitPos + fieldSize
    y1 = _getSBits(bitList, bitPos, fieldSize); bitPos=bitPos + fieldSize
    y2 = _getSBits(bitList, bitPos, fieldSize); bitPos=bitPos + fieldSize
    p=(bitPos/8+1)
    frameRateMinor=ord(data[p]); p+=1
    frameRateMajor=ord(data[p]); p+=1
    framesTotal=ord(data[p])+ord(data[p+1])*254
    return {'flashversion':version
           , 'compressed':compressed
           , 'width': int(x2)/20
           , 'height':int(y2)/20
           , 'uncompressed_size':uncompressed_size
           , 'frame_rate':'%s.%s' % (frameRateMajor, frameRateMinor)
           , 'frames_total':framesTotal
           }

