#-*- conding:utf-8 -*-

from collections import OrderedDict
from spacy import displacy

test = """1	보험	보험	_	NNG	_	2	NP	_	_
2	약관	약관	_	NNG	_	3	NP	_	_
3	대출	대출	_	NNG	_	4	NP_OBJ	_	_
4	받으려고	받 으려고	_	VV+EC	_	5	VP	_	_
5	하는데	하 는데	_	VV+EC	_	7	VP	_	_
6	얼마나	얼마나	_	MAG	_	7	AP	_	_
7	받을	받 을	_	VV+ETM	_	8	VP_MOD	_	_
8	수	수	_	NNB	_	9	NP_SBJ	_	_
9	있나요?	있 나요 ?	_	VV+EF+SF	_	0	VP	_	_"""


def set_arrow_direction(word_line):
    """
    Sets the orientation of the arrow that notes the directon of the dependency
    between the two units.
    
    """
    if int(word_line["id"]) > int(word_line["head"]):
        word_line["dir"] = "right"
    elif int(word_line["id"]) < int(word_line["head"]):
        word_line["dir"] = "left"
    return word_line

def convert2zero_based_numbering(word_line_field):
    "CONLL-U numbering starts at 1, displaCy's at 0..."
    if word_line_field == '0':
        word_line_field = '_'
    else: 
        word_line_field = str(int(word_line_field) - 1)
    return word_line_field

def get_start_and_end(word_line):
    """
    Displacy's 'start' value is the lowest value amongst the ID and HEAD values,
    and the 'end' is always the highest. 'Start' and 'End' have nothing to do
    with dependency which is indicated by the arrow direction, not the line
    direction.
    """
    word_line["start"] = min([int(word_line["id"]), int(word_line["head"])])
    word_line["end"] = max([int(word_line["id"]), int(word_line["head"])])
    return word_line

def conllu_to_displacy_dict(conllu_result):
    """
    convert CoNLL-u result to dispalcy dict format 
    :params conllu_result: dependency parsed result with CoNLL-u format
    :return: converted dict 
    """
    conll_u_lines = [line for line in conllu_result if line[0].isnumeric()]

    displacy_dict = {"arcs": [], "words": []}
    for tabbed_line in conll_u_lines:
        word_line = OrderedDict()
        word_line["id"], word_line["form"], word_line["lemma"], \
        word_line["upostag"], word_line["xpostag"], word_line["feats"], \
        word_line["head"], word_line["deprel"], word_line["deps"], \
        word_line["misc"] = tabbed_line.split("\t")

        word_line["id"] = convert2zero_based_numbering(word_line["id"])
        if word_line["head"] != "_":
            word_line["head"] = convert2zero_based_numbering(word_line["head"])       

        if word_line["deprel"] != "root" and word_line["head"] != "_":
            word_line = get_start_and_end(word_line)
            word_line = set_arrow_direction(word_line)
            displacy_dict["arcs"].append({"dir": word_line["dir"],
                                          "end": word_line["end"],
                                        #"label": word_line["deprel"],
                                        "label": '',
                                        "start": word_line["start"]})

        displacy_dict["words"].append({"tag": word_line["deprel"], "text": word_line["form"]})

    return displacy_dict

def render(conllu_result):
    options = {"compact": True, "bg": "#09a3d5",
        "color": "white", "font": "Source Sans Pro", 
        "word_spacing": 25, "arrow_spacing": 10,
        "distance": 90}

    result = conllu_to_displacy_dict(conllu_result)
    displacy.render(result, manual=True, options=options)


if __name__ == '__main__':
    
    test_data = test.split('\n')

    displacy_dict = conllu_to_displacy_dict(test_data)
    print(displacy_dict)

    render(test_data)



