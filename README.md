
# Korean Dependency Parser using Stack-Pointer Networks
Stack-Pointer Network를 이용한 한국어 의존 구문 파서 

이 코드는 NeruoNLP2(https://github.com/XuezheMax/NeuroNLP2) 코드에서
한국어 의존 구문 파서에 맞게 변경된 KoreanDependencyParserusingStackPointer(https://github.com/yseokchoi/KoreanDependencyParserusingStackPointer) 코드를 수정/개발 함.

### Requirement
- python 3.6
- gensim
- numpy
- Pytorch >= 0.4

### Train

------

python StackPointerParser.py  --pos --char --eojul --batch_size *"batch_size"* --word_embedding *random* --char_embedding *random* --pos_embedding *random* --train *"train_path"* --dev *"dev_path"* --test *"test_path"* --model_path *"model_path"* --model_name *"model_name"* --grandPar --sibling --skipConnect --prior_order *inside_out*

- CoNLL-u 형식의 train, dev, test data를 이용하여 model 생성

### Test

------

python StackPointerParser_test.py --model_path *"model_path"* --model_name *"model_name"* --output_path *"output_file_path"* --test *"test_file"* --batch_size *"batch_size"*

- CoNLL-u 형식의 test data를 읽어 model을 테스트

### Predict

------


python StackPointerParser_predict.py --model_path *%PROJECT_PATH%/sejong_conll_model/181108* --model_name *94ea90_sejong_ppos2.model* --output_path *"output_file_path"* --test *"test_file_path"* --batch_size *"batch_size"*

- raw text를 입력받아 형태소 분석 후 CoNLL-u 포맷으로 만들어 의존 구문 분석된 파일을 출력
- 테스트 파일은 한 라인당 한 문장으로 구성되어 있어야 함
- mecab 형태소 분석기 사용 
