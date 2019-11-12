import mecab
#from neuronlp2.io.logger import get_logger
import pdb
import sys


class CoNLLUConverter(object):
    def __init__(self, source_path, output_path=None):
        self.__source_file = None
        self.__conll_file = None
        self.__source_path = source_path
        if output_path == None:
            self.__conll_path = source_path + '_converted.conll'
        else:
            self.__conll_path = output_path 
        self.__mecab = mecab.MeCab().tagger
        self.__ma_list = []

    def open(self):
        self.__source_file = open(self.__source_path, 'r', encoding='utf-8')
        self.__conll_file = open(self.__conll_path, 'w', encoding='utf-8')

    def close(self):
        self.__source_file.close()
        self.__conll_file.close()

    def convert(self):
        #logger = get_logger("CoNLL-u Converter")
        #logger.info("Converting the original file to CoNLL-u formatted file")

        if self.__source_file is None:
            self.open()

        snt_id = 0
        for line in self.__source_file:
            snt_id += 1
            if snt_id % 10000 == 0:
                print("Converting data: %d" % snt_id)

            origin_snt = line.strip()
            #morph, pos = self.__wisekma.dep_pos(origin_snt, nbest=5)

            ## 형태소 분석 & 어절 정보 맵핑 Start
            # MeCab의 형태소 분석 결과는 어절(띄어쓰기)정보를 유지할 수 없기 때문에
            # 원문 텍스트의 어절별 음절 수로 형태소 분석 결과를 맵핑
            # gl2een 191112

            # Index of MeCab parse() result
            # 0: 품사 태그
            # 1: 의미 부류
            # 2: 종성 유무
            # 3: 읽기
            # 4: 타입
            #    Inflect(활용)
            #    Compound(복합명사)
            #    Preanalysis(기분석)
            # 5: 첫번째 품사
            # 6: 마지막 품사
            # 7: 표현(활용, 복합명사, 기분석이 어떻게 구성되는지 알려주는 필드)
            analyzed_list = self.__mecab.parse(origin_snt).split('\n')

            # 원문 어절별 음절 길이
            origin_eojeol_count = [len(e) for e in origin_snt.split()]

            morph = []
            pos = []
            m_buf = []
            p_buf = []
            cur_eojeol = 0
            cur_eojeol_len = origin_eojeol_count[cur_eojeol]
            len_buf = 0

            #pdb.set_trace()

            for row in analyzed_list:
                if cur_eojeol_len == len_buf:
                    morph.append(m_buf)
                    pos.append(p_buf)

                    cur_eojeol += 1
                    if cur_eojeol == len(origin_eojeol_count):
                        break
                    cur_eojeol_len = origin_eojeol_count[cur_eojeol]
                    len_buf = 0
                    m_buf = []
                    p_buf = []

                if row == 'EOS':
                    break

                origin, analyzed = row.split('\t')
                analyzed =  analyzed.split(',')

                p_buf.append(analyzed[0])

                if analyzed[4] == 'inflected':
                    m_buf.append([a.split('/')[0] for a in analyzed[7].split('+')])
                else:
                    m_buf.append(origin)

                len_buf += len(m_buf[-1])
            
            print(morph)
            print(pos)

            self.__conll_file.write('#SENTID:%d\n' % snt_id)
            self.__conll_file.write('#ORGSENT:%s\n' % origin_snt)

            origin_eojeols = origin_snt.split(' ')

            for i in range(len(morph)):
                self.__conll_file.write('%d\t%s\t%s\t-\t%s\t-\t-\t-\t-\t-\n' % (i+1, origin_eojeols[i], ' '.join(morph[i]), '+'.join(pos[i])))

            self.__conll_file.write('\n')

        self.close()

        #logger.info('Converted data : %d' % snt_id)

        return self.__conll_path


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: origin2conllu.py [INPUT_FILE] [OUTPUT_FILE]')
        exit(-1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    converter = CoNLLUConverter(input_file, output_file)
    converter.convert()

    print('Successfully Finished!')
