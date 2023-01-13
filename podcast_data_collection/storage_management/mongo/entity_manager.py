from enum import Enum
import mongoengine as me

#### Entities ####


class MedicalArticle(me.Document):
    
    title = me.StringField()
    description = me.StringField()
    link = me.StringField()
    date = me.DateTimeField()
    data_source = me.StringField()

