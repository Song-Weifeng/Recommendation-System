import spacy

nlp = spacy.load("zh_core_web_lg")
doc1 = nlp('你好')
doc2 = nlp('早上好')
# 获取doc1和doc2的相似度
print(doc1.similarity(doc2))
