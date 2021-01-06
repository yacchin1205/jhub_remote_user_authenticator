import string


def check_valid_organization(headers):
    return True

def normalize_quoted_printable(srcstr):
    unreserved  = string.ascii_letters + string.digits + '-._~'
    pchar = (unreserved + ':@').encode('latin-1')
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
