from keras.models import load_model
model = load_model("kitapyorum.h5")
def preprocessingg(column):
    column=column.apply(lambda x: " ".join(x.lower() for x in x.split()))
    column=column.str.replace("[^\w\s]","")
    column=column.str.replace("[\d]","")
    return column
yeni_yorumlar = pd.DataFrame(yeni_yorumlar,columns=["yeni yorumlar"])
yeni_yorumlar["yeni yorumlar"] = preprocessingg(yeni_yorumlar["yeni yorumlar"])
allDocs_sequences = tokenizer.texts_to_sequences(yeni_yorumlar["yeni yorumlar"])
word_index = tokenizer.word_index


train_padded = pad_sequences(allDocs_sequences, padding='post', truncating='post', maxlen=max_length)
predict = model.predict(train_padded)

yeni_yorumlar["predict"]=[1 if i[0]>0.5 else 0 for i in predict]