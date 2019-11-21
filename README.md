
# Korean Dependency Parser using Stack-Pointer Networks
Stack-Pointer Network를 이용한 한국어 의존 구문 파서 

이 코드는 NeruoNLP2(https://github.com/XuezheMax/NeuroNLP2) 코드에서
한국어 의존 구문 파서에 맞게 변경된 KoreanDependencyParserusingStackPointer(https://github.com/yseokchoi/KoreanDependencyParserusingStackPointer) 코드를 수정/개발 함.

### Requirement
- python 3.6
- gensim
- numpy
- Pytorch >= 0.4
- MeCab 0.996

------
### Train
python StackPointerParser.py  --pos --char --eojul --batch_size *"batch_size"* --word_embedding *random* --char_embedding *random* --pos_embedding *random* --train *"train_path"* --dev *"dev_path"* --test *"test_path"* --model_path *"model_path"* --model_name *"model_name"* --grandPar --sibling --skipConnect --prior_order *left2right*

- CoNLL-u 형식의 train, dev, test data를 이용하여 model 생성

------
### Test
python StackPointerParser_test.py --model_path *"model_path"* --model_name *"model_name"* --output_path *"output_file_path"* --test *"test_file"* --batch_size *"batch_size"*

- CoNLL-u 형식의 test data를 읽어 model을 테스트

------
### Predict
python StackPointerParser_predict.py --model_path *"MODEL_PATH"* --model_name *"MODEL_NAME"* --predcit_data *"PREDICT_FILE_PATH"* --output_path *"OUTPUT_FILE_PATH"* (--use_gpu --use_stdio)

- raw text를 입력받아 형태소 분석 후 CoNLL-u 포맷으로 만들어 의존 구문 분석
- 테스트 파일은 한 라인당 한 문장으로 구성되어 있어야 함
- use_stdio 사용 시 STDIN으로 받은 문장을 STDOUT으로 결과 출력
- use_stdio를 사용하지 않으면 파일 입출력 사용
- MeCab 형태소 분석기 사용 
*- mecab-ko-dic.tar.gz 압축 해제 필요*

------
### mecab-ko-dic for Stack Pointer Network Dependency Parsing
- 세종 말뭉치 <-> mecab 형식 통일을 위한 사전 커스텀화
- Inflect.csv에서 호환형이 아닌 자음(초성, 종성)을 호환형(일반적인 자음)으로 변환
- 형태소 태그 통일
 - MeCab 형태소 태그 변경
  : SSO  -> SS
  : SSC  -> SS
  : SC   -> SP
  : NNBC -> NNB
 - 세종 의존 구문 분석 말뭉치 형태소 태그 변경
  : SO   -> SY
  : SW   -> SY

------
### TODO
~~- 세종<->mecab 형태소 태그 통일 필요~~
~~- mecab 형태소 분석 결과 형태와 세종 말뭉치 포맷 통일~~
 ~~: mecab 분석 결과가 종성으로 나오는 것 수정(dic을 고쳐야할듯)~~
- 였(mecab)<->았(세종) 형태소 분석 결과 처리 필요
- 음절, 형태소, 형태소 태그 임베딩 결합

