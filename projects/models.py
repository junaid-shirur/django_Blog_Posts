from django.db import models
import uuid
# Create your models here.

class BaseModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4,unique=True, primary_key=True, editable=False)
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Project(BaseModel):
    title = models.CharField(max_length=200)
    desc = models.TextField(null=True, blank=True)
    source_link = models.CharField(max_length=2000)
    tags = models.ManyToManyField('Tag', blank=True)
    up_votes = models.IntegerField(default=0, blank=True, null=True)
    up_votes_ratio = models.IntegerField(default=0, blank=True, null=True)
    
    def __str__(self):
        return self.title


class Review(BaseModel):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    # owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)


class Tag(BaseModel):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
