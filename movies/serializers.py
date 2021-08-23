from .service import *
from rest_framework import fields, serializers

from .models import *


class ActorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ("id", "name", "image")


class ActorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = "__all__"


class MovieListSerializres(serializers.ModelSerializer):

    rating_user = serializers.BooleanField()
    middle_star = serializers.IntegerField()

    class Meta:
        model = Movie 
        fields = ("id", "title", "tagline", "category", "rating_user", "middle_star")



class FilterReviewListSerializres(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ReviewSerializres(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewListSerializres
        model = Review
        fields = ("name", "text", "parent")


class ReviewCreateSerializers(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'


class MovieDetailSerializres(serializers.ModelSerializer):
    
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    actor = ActorListSerializer(read_only=True, many=True)
    directors = ActorListSerializer(read_only=True, many=True)
    genre = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    review = ReviewCreateSerializers(many=True)

    class Meta:
        model = Movie 
        exclude = ("draft",)


class CreateRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ("star", "movie")

    def create(self, validated_data):
        rating, _ = Rating.objects.update_or_create(
            ip = validated_data.get("ip", None),
            movie = validated_data.get("movie", None),
            defaults={'star': validated_data.get("star")}
        )
        return rating



