import socket
import struct
import xml.etree.ElementTree as ET

option = None


def check_children(root, option_id):
    global option
    for child in root:
        if int(child.attrib['id']) == option_id:
            option = child
        check_children(child, option_id)


def get_next_question_id(option_id):
    tree = ET.parse("Resources/resourcesradio/ArtifactD.xml")
    root = tree.getroot()
    check_children(root, option_id)
    global option
    if len(list(option)) == 0:
        return 0
    question = list(option)[0]
    return int(question.attrib['id'])


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 6969
    s.bind(('', port))
    print("socket binded to %s" % port)
    s.listen(5)
    print("socket is listening")
    while True:
        c, addr = s.accept()
        print('Got connection from', addr)

        nr = c.recv(4)
        nr = struct.unpack('!i', nr)[0]
        print(nr)
        cnt = get_next_question_id(nr)
        print(cnt)
        res = c.send(struct.pack('!i', cnt))
        c.close()
        if cnt == 0:
            break
    s.close()
