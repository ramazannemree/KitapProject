from products.models import Product
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
#from django.db.models.signals import post_save
#from keras.models import load_model
#import pandas as pd
#from keras.preprocessing.text import Tokenizer
#from keras.preprocessing.sequence import pad_sequences
#import os
from django.conf import settings

def comment_validator(value):
    if len(value) < 5 or len(value) > 200:
        raise ValidationError('Yorum 5 karakterden kısa, 200 karakterden uzun olamaz.')

def rate_validator(value):
    if not isinstance(value,int) or (value < 1 or value > 5):
        raise ValidationError('Lütfen geçerli bir puan verin')

class Comment (models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE) 
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    comment = models.TextField(max_length=200,validators=[comment_validator])
    rate = models.IntegerField(validators=[rate_validator])
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    prediction = models.BooleanField(default=True)

    class Meta():
        ordering = ['-create_at']


    def __str__(self):
        return self.user.username

    def save (self,*args,**kwargs):
        if not self.id:
            self.create_at = timezone.now()
        self.update_at = timezone.now()
        return super(Comment, self).save(*args,**kwargs)

def preprocessingg(column):
    column=column.apply(lambda x: " ".join(x.lower() for x in x.split()))
    column=column.str.replace("[^\w\s]","")
    column=column.str.replace("[\d]","")
    return column

def comment_predict(sender,instance,**kwargs):
    # file_ = os.path.join(settings.BASE_DIR, 'comment/kitapyorum.h5')
    # model = load_model(file_)
    # yorum = instance.comment
    # tokenizer = Tokenizer()
    # yeni_yorumlar = pd.DataFrame(list(yorum),columns=["yeni yorumlar"])
    # tokenizer.fit_on_texts(yeni_yorumlar["yeni yorumlar"])
    # yeni_yorumlar["yeni yorumlar"] = preprocessingg(yeni_yorumlar["yeni yorumlar"])
    # allDocs_sequences = tokenizer.texts_to_sequences(yeni_yorumlar["yeni yorumlar"])
    # word_index = tokenizer.word_index   

    # train_padded = pad_sequences(allDocs_sequences, padding='post', truncating='post', maxlen=257)
    #predict = model.predict(train_padded)
    predict = 0.7
    if predict>0.5:
        instance.prediction = True
    else:
        instance.prediction = False
    
    instance.save()

#post_save.connect(comment_predict,sender=Comment)
#pre_save.connect(user_check_mail_exists,sender = User)