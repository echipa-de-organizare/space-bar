import xml.etree.ElementTree as ET

question = None


def check_children(root, qid):
    global question
    for child in root:
        if int(child.attrib['id']) == qid:
            question = child
        check_children(child, qid)


def get_data_by_qid(qid):
    tree = ET.parse("resources/story.xml")
    root = tree.getroot()
    check_children(root, qid)
    global question
    # print(question.tag, question.attrib)
    options_list = []
    option_ids = []
    for option in question:
        options_list.append(option.attrib['text'])
        option_ids.append(int(option.attrib['id']))
        # print(option.tag, option.attrib)

    return question.attrib['text'], options_list,option_ids
