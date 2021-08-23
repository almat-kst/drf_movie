from django.contrib import admin
from .models import * 
from django.utils.safestring import mark_safe

from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


# @admin.register(Movie)
# class MovieAdmin(admin.ModelAdmin):
#     class Meta:
#         model = Movie
#         fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url")
    list_display_links = ("name",)


class ReviewInvine(admin.ModelAdmin):
    model = Review
    extra = 1
    readonly_fields = ("name", "email")


class MovieShotsInline(admin.ModelAdmin):
    model = MovieShots
    extra = 1
    readonly_fields = ("get_image", )

    def get_image(self, obj):
        return mark_safe(f'<img scr={obj.image.url} width="100" height="110"')

    get_image.short_description = 'Изображение'



@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "url", "draft")
    list_filter = ("category", "year")
    search_fields = ("title", "category__name")
    # inlines = [MovieShotsInline, ReviewInvine]
    save_on_top = True
    save_as = True
    list_editable = ("draft",)
    actions = ["publish", "unpublish"]
    # form = MovieAdminForm
    readonly_fields = ("get_image", )
    fieldsets = (
        (None, {
            "fields": (("title", "tagline"), )
        }),

        (None, {
            "fields": ("description", ("poster", "get_image"), )
        }),

        (None, {
            "fields": (("year", "world_premier", "country"), )
        }),

        ("Actors", {
            "classes": ("collapse", ),
            "fields": (("actor", "directors", "genre"), )
        }),

        (None, {
            "fields": (("category", "budget", "fees_in_usa", "fees_in_world"), )
        }),

        ("Options", {
            "fields": (("url", "draft"), )
        }),
    )

    def get_image(self, obj):
        return mark_safe(f'<img scr={obj.poster.url} width="100" height="110"')


    def unpublish(self, request, queryset):
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")


    def publish(self, request, queryset):
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")


    publish.short_description = 'Опубликовать'
    publish.allowed_permissions = ('change', )

    unpublish.short_description = 'Снять с публикации'
    unpublish.allowed_permissions = ('change', )
    #get_image.short_description = 'Изображение'

    get_image.short_description = 'Постер'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Отзывы к фильму"""
    list_display = ("name", "email", "parent", "movie", "id")
    readonly_fields = ("name", "email")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры"""
    list_display = ("name", "url")


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """Актеры"""
    list_display = ("name", "age", "get_image")
    readonly_fields = ("get_image", )

    def get_image(self, obj):
        return mark_safe(f'<img scr={obj.image.url} width="50" height="60"')

    get_image.short_description = 'Изображение'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("star", "movie", "ip")


@admin.register(MovieShots)
class MovieShots(admin.ModelAdmin):
    list_display = ("title", "movie", "get_image")
    readonly_fields = ("get_image", )

    def get_image(self, obj):
        return mark_safe(f'<img scr={obj.image.url} width="50" height="60"')

    get_image.short_description = 'Изображение'


admin.site.register(RatingStar)

admin.site.site_title = "Django Movie"
admin.site.site_header = "Django Movie"