#-*- conding:utf-8 -*-
# sentence_extractor.py
# Single sentence extractor from compound, complex sentence
# 191211 gl2een

from collections import OrderedDict
import pdb

test = """1	보험	보험	_	NNG	_	2	NP	_	_
2	약관	약관	_	NNG	_	3	NP	_	_
3	대출	대출	_	NNG	_	4	NP_OBJ	_	_
4	받으려고	받 으려고	_	VV+EC	_	5	VP	_	_
5	하는데	하 는데	_	VV+EC	_	7	VP	_	_
6	얼마나	얼마나	_	MAG	_	7	AP	_	_
7	받을	받 을	_	VV+ETM	_	8	VP_MOD	_	_
8	수	수	_	NNB	_	9	NP_SBJ	_	_
9	있나요?	있 나요 ?	_	VV+EF+SF	_	0	VP	_	_"""

def find_row_by_head_deprel(conllu_data, head, deprel):
    """
    Find a row in the sentence with head id, deprel(dependency relation)
    :param conllu_data: pasred sentence
    :param head: head id to find
    :param deprel: dependency relation to find
    :returns: row id or -1
    """
    for row in conllu_data:
        if deprel == row["deprel"] and head == row["head"]:
            return row["id"]
            break
    return -1
    
def find_nnb_soo_root(conllu_data, vp_id):
    """
    Find a row with row['form']='수/NNB', whith is tail of 'VP' row.
    :param conllu_data: pasred sentence
    :param vp_id: row id with row["xpostag"] == 'VP'
    :returns: row id or -1
    """
    for row in conllu_data:
        if row["head"] == vp_id and row["form"] == '수' and row["xpostag"] == 'NNB':
            return row["id"]
            break
    return -1

def get_vp_with_root(conllu_data):
    """
    Find a row with head is 0 & 'VP'.
    :param conllu_data: pasred sentence
    :returns: root id or -1
    """
    rootVP = -1

    for row in conllu_data:
        if row["head"] == '0' and row["deprel"] == 'VP':
            rootVP = row["id"]

            nnb_soo = find_nnb_soo_root(conllu_data, rootVP)
            if nnb_soo != -1:
                rootVP = find_row_by_head_deprel(conllu_data, nnb_soo, 'VP_MOD')
                
            vpmod = find_row_by_head_deprel(conllu_data, rootVP, 'VP_MOD')
            if vpmod != -1:
                rootVP = vpmod
            
            break
    
    return rootVP
    
def get_all_vp_with_root(conllu_data, root, negative=None):
    """
    Get all rows with dependency.
    :param conllu_data: list of dictionary
        pasred sentence
    :param root: int
        root row id
    :param negative: str list
        ignore if dependency relation is in this 'negative' list
    :returns: list of row id
    """
    result = []

    neg = negative
    if negative is None:
        neg = []

    for row in conllu_data:
        if row["head"] == root and row["deprel"] == 'VP':
            #partial_result = get_all_vp_with_root(conllu_data, row["id"])
            result.append(row["id"])
            result += get_all_vp_with_root(conllu_data, row["id"])
        #if row["id"] == root:
        #    result.append(row["id"])
    return result

def get_tail(conllu_data, head):
    """
    Get all rows with dependency.
    :param conllu_data: pasred sentence
    :param root: root row id
    :returns: list of row id
    """
    result = []
    for row in conllu_data:
        if row["head"] == head:
            #if row["deprel"] == 'NP_SBJ' or row["deprel"] == 'NP_OBJ':
            if row["deprel"] != 'VP':
                result += get_tail(conllu_data, row["id"])
                result.append(row)
    #result.append(conllu_data[int(head)-1])
    return result

def isInEC(conllu_data):
    for row in conllu_data:
        pos = row["xpostag"].split('+')
        if 'EC' in pos:
            print(row)
            return row["id"]
            
    return -1

def separateSentence(conllu_result): 
    conll_u_lines = [line for line in conllu_result if line[0].isnumeric()]

    conllu_data = []

    for tabbed_line in conll_u_lines:
        word_line = OrderedDict()
        word_line["id"], word_line["form"], word_line["lemma"], \
        word_line["upostag"], word_line["xpostag"], word_line["feats"], \
        word_line["head"], word_line["deprel"], word_line["deps"], \
        word_line["misc"] = tabbed_line.split("\t")
        conllu_data.append(word_line)

    #pdb.set_trace() 

    ec_position = isInEC(conllu_data)
    rootVP = get_vp_with_root(conllu_data)

    if ec_position == -1 or rootVP == -1:
        return

    vps = get_all_vp_with_root(conllu_data, rootVP)
    vps.append(rootVP)

    count = 1
    for vp in vps:
        single_snt = get_tail(conllu_data, vp)
        single_snt.append(conllu_data[int(vp)-1])
        snt = ' '.join([w["form"] for w in single_snt])
        print('=====')
        print('%d sentence : %s' % (count, snt ))
        print('')
        count += 1


if __name__ == '__main__':
    
    test_data = test.split('\n')


