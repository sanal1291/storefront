from django.db import models
from django.contrib.contenttypes.models import ContentType 
from django.contrib.contenttypes.fields import GenericForeignKey

class TaggedItemManager(models.Manager):
    def get_tags_for(self,obj_type, obj_id):
        contentType = ContentType.objects.get_for_model(obj_type)
        result =TaggedItem.objects \
            .select_related('tag') \
            .filter(content_type= contentType,
                object_id = obj_id).all()

class Tag(models.Model):
    label = models.CharField(max_length=255)

class TaggedItem(models.Model):
    objects = TaggedItemManager()
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # Type (product,video,article)
    # ID
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField()
    content_object = GenericForeignKey()
