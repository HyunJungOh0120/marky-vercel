from django.db import models
from django.conf import settings
# Create your models here.


CATEGORY_CHOICES = [
    ('Life', (
        ('Daily', 'Daily',),
        ('RelationShip', 'RelationShip',),
        ('Family', 'Family',),
        ('Pets', 'Pets',),
        ('Hobby', 'Hobby',),
        ('Photography', 'Photography',),
        ('Cook', 'Cook',),
        ('Car', 'Car',),
        ('Interior', 'Interior',),
        ('Fashion/Beauty', 'Fashion/Beauty',),
        ('Health', 'Health',),
    )),
    ('Travel/Restaurants', (
        ('Domestic', 'Domestic',),
        ('Oversea', 'Oversea',),
        ('Camping/Hiking', 'Camping/Hiking',),
        ('Restaurants', 'Restaurants',),
        ('Cafe', 'Cafe',),
    )),
    ('Entertainment', (
        ('Tv', 'Tv',),
        ('Star', 'Star'),
        ('Movie', 'Movie'),
        ('Music', 'Music'),
        ('Book', 'Book'),
        ('Animation', 'Animation'),
        ('Exhibition', 'Exhibition'),
        ('Show', 'Show'),
        ('Craft', 'Craft'),
    )),
    ('IT', (
        ('IT Internet', 'IT Internet'),
        ('Mobile', 'Mobile'),
        ('Game', 'Game'),
        ('Science', 'Science'),
        ('IT Product', 'IT Product'),
    )),
    ('Sports', (
        ('Sports', 'Sports'),
        ('Soccer', 'Soccer'),
        ('Volleyball', 'Volleyball'),
        ('Baseball', 'Baseball'),
        ('Basketball', 'Basketball'),
        ('Golf', 'Golf'),
    )),
    ('Current', (
        ('Government', 'Government'),
        ('Society', 'Society'),
        ('Education', 'Education'),
        ('International', 'International'),
        ('Business', 'Business'),
        ('Economy', 'Economy'),
        ('Job', 'Job'),
    )),
    ('Event', (
        ('Event', 'Event'),
    ))
]


class Category(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    topic = models.CharField(max_length=40, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=40, blank=False)
    slug = models.SlugField(blank=True, max_length=100)

    def __str__(self) -> str:
        return f'{self.name}-{self.topic}'

    class Meta:
        db_table = 'category'
