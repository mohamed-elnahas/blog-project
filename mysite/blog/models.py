from django.conf import settings
from django.db import models
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager




class PublishedManager(models.Manager):
      def get_queryset(self):
          return (
                  super().get_queryset().filter(status=Post.Status.published)
                 )

class Post (models.Model):

    class Status (models.TextChoices):
        DRAFT='DF','Draft'
        published='PB','Published'

    title=models.CharField(max_length=50)
    tags = TaggableManager()
    slug=models.SlugField(max_length=30,unique_for_date='publish')
    body=models.TextField()
    author=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts'

    )
    publish=models.DateTimeField(default=timezone.now)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    status=models.CharField(
        max_length=2,
        choices=Status,
        default=Status.DRAFT
                            )
    
    objects = models.Manager() 
    published = PublishedManager()



    class Meta :
        ordering=['-publish']
        indexes=[
            models.Index(fields=['-publish'])
        ]



    def __str__(self):
        return self.title
    
    
    
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[
                                    self.publish.year,
                                    self.publish.month,
                                    self.publish.day,
                                    self.slug
                            ])

    




class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name=models.CharField(max_length=80)
    email=models.EmailField()
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    update=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)


    class Meta :
        ordering = ['created']
        indexes = [models.Index(fields=['created']),]


    def __int__ (self):
        return f"commented by {self.name} on {self.post}"
        

