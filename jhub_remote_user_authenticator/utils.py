import string


def normalize_quoted_printable(srcstr):
    unreserved  = string.ascii_letters + string.digits + '-._~'
    sub_delims = '!$&\'()*+,;='
    pchar = (unreserved + sub_delims + ':@').encode('latin-1')
    if isinstance(srcstr, str):
        src = srcstr.encode('utf8')
    else:
        src = srcstr

    encoded = b''
    for index in range(len(src)):
        if src[index] in pchar:
            encoded += src[index:index + 1]
            continue
        encoded += '={0:02x}'.format(src[index]).upper().encode('latin-1')
    return encoded.decode('latin-1')
