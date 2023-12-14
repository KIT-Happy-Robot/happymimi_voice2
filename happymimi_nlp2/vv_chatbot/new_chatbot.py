from transformers import AutoTokenizer, MBartForConditionalGeneration
tokenizer = AutoTokenizer.from_pretrained('ku-nlp/bart-base-japanese')
model = MBartForConditionalGeneration.from_pretrained('ku-nlp/bart-base-japanese')
sentence = '京都 大学 で 自然 言語 処理 を 専攻 する 。'  # input should be segmented into words by Juman++ in advance
encoding = tokenizer(sentence, return_tensors='pt')

print(encoding)