from django.db import models
from datetime import date
#from django.core.urlresolvers import reverse
from django.urls import reverse


class Category(models.Model):
    '''Категория'''
    name = models.CharField(max_length=150, verbose_name='Категория')
    description = models.TextField('Описания')
    url = models.SlugField(max_length=160, unique=True) #принемает только цифры, буквы, диффис

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name
    

class Actor(models.Model):
    '''Актеры и режиссеры'''
    name = models.CharField(max_length=100, verbose_name='Имя')
    age = models.PositiveSmallIntegerField(default=0, verbose_name='Возраст') #разрешает цифры 0-2000
    description = models.TextField('Описания')
    image = models.ImageField('Изображение', upload_to='actors/')

    class Meta:
        verbose_name = 'Актеры и режиссеры'
        verbose_name_plural = 'Актеры и режиссеры'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('actor_detail', kwargs={"slug": self.name})


class Genre(models.Model):
    '''Жанры'''
    name = models.CharField(max_length=150, verbose_name='Категория')
    description = models.TextField('Описания')
    url = models.SlugField(max_length=160, unique=True) #принемает только цифры, буквы, диффис

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    tagline = models.CharField(max_length=100, default='', verbose_name='Слоган')
    description = models.TextField('Описания', blank=True, null=True)
    poster = models.ImageField('Постер', upload_to='movies/')
    year = models.PositiveIntegerField(default=2019, verbose_name='Дата выхода')
    country = models.CharField(max_length=30, verbose_name='Страна')
    directors = models.ManyToManyField('Actor', verbose_name='режиссер', related_name='film_direcor')
    actor = models.ManyToManyField('Actor', verbose_name='актер', related_name='film_actor')
    genre = models.ManyToManyField('Genre', verbose_name='жанры')
    world_premier = models.DateField(default=date.today, verbose_name='Примьера в мире')
    budget = models.PositiveIntegerField(default=0, help_text='указывать сумму в долларах', verbose_name='Бюджет')
    fees_in_usa = models.PositiveIntegerField(default=0, help_text='указывать сумму в долларах', verbose_name='Сборы в США')
    fees_in_world = models.PositiveIntegerField(default=0, help_text='указывать сумму в долларах', verbose_name='Сборы в мире')
    category = models.ForeignKey('Category', verbose_name='Категория', on_delete=models.SET_NULL, null=True, related_name='category_movie')
    #category = models.CharField(max_length=100, verbose_name='Категория')
    url = models.SlugField(max_length=100, unique=True)
    draft = models.BooleanField(default=False, verbose_name='Черновик')
    
    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"slug": self.url})
    
    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)
    

class MovieShots(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описания')
    image = models.ImageField('Изображение', upload_to='movie_shots/')
    movie = models.ForeignKey(Movie, verbose_name='Фильм', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Кадр из фильма'
        verbose_name_plural = 'Кадры из фильма'

    def __str__(self):
        return self.title


class RatingStar(models.Model):
    value = models.PositiveSmallIntegerField(default=0, verbose_name='Значение')

    class Meta:
        verbose_name = 'Звезда рейтинга фильма'
        verbose_name_plural = 'Звезды рейтинга фильма'
        ordering = ["-value"]

    def __str__(self):
        return f'{self.value}'


class Rating(models.Model):
    ip = models.CharField(max_length=15, verbose_name='Ip aдрес')
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='звезда')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='фильм', related_name='rating')

    class Meta:
        verbose_name = 'Звезда рейтинга актера'
        verbose_name_plural = 'Звезды рейтинга актера'

    def __str__(self):
        return f'{self.star} - {self.movie}'


class Review(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=100, verbose_name='Имя')
    text = models.TextField('Описание')
    parent = models.ForeignKey('self', verbose_name='Родители', on_delete=models.SET_NULL, blank=True, null=True, related_name='children')
    movie = models.ForeignKey(Movie, verbose_name='фильм', on_delete=models.CASCADE, related_name='review')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'{self.movie} -> {self.name}'

        