from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Avg, Count, Max
from drf_spectacular.utils import (extend_schema, OpenApiParameter,
                                   OpenApiResponse,OpenApiExample)

from .serializers import HabitSerializer, MoodSerializer
from .models import Habit, Mood


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['frequency']
    search_fields = ['name', 'description']
    ordering_fields = ['streak', 'created_at']

    def get_queryset(self):
        return Habit.objects.filter(
            user=self.request.user, is_deleted=False).order_by("streak")


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    def perform_destroy(self, instance):
        instance.soft_delete()


    @extend_schema(
        summary='List all habits', tags=['Habits'],
        description='Returns all habits for the logged-in user ordered by streak.',
        responses={200: HabitSerializer(many=True),
                   401: OpenApiResponse(description='Authentication required!')},
        parameters=[
            OpenApiParameter(
                name='search',
                description='Filter habits by name or description',
                required=False,
                type=str,
                location=OpenApiParameter.QUERY,
                examples=[OpenApiExample('Search exercise', 'exercise')]
            ),
            OpenApiParameter(
                name='frequency',
                description='Filter by frequency',
                enum=['daily', 'weekly', 'monthly'],
                required=False,
                type=str,
                location=OpenApiParameter.QUERY
            ),
            OpenApiParameter(
                name='ordering',
                description='Sort results',
                enum = ['-streak', 'streak', '-created_at', 'created_at'],
                default='-streak',
                required=False,
                type=str,
                location=OpenApiParameter.QUERY
            )
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


    @extend_schema(
        summary='Create a habit',
        description='Creates a new habit for the logged-in user.',
        tags=['Habits'],
        request=HabitSerializer,
        responses={
            201: HabitSerializer,
            400: OpenApiResponse(
                description='Validation error',
                examples=[
                    OpenApiExample(
                        'Missing name',
                        value={'name': ['This field is required.']}
                    )
                ]
            ),
        },
        examples=[
            OpenApiExample(
                'Daily habit',
                value={
                    'name': 'Exercise',
                    'frequency': 'daily',
                    'description': '30 min a day'
                },
                request_only=True,
            ),
        ],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


    @extend_schema(
        summary='Get one habit', tags=['Habits'],
        responses={200: HabitSerializer,
                   404: OpenApiResponse(description='Not found')},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


    @extend_schema(
        summary='Update habit', tags=['Habits'],
        request=HabitSerializer,
        responses={200: HabitSerializer,
                   400: OpenApiResponse(description='Validation error')},
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


    @extend_schema(
        summary='Partially update habit', tags=['Habits'],
        request=HabitSerializer,
        responses={200: HabitSerializer,
                   400: OpenApiResponse(description='Validation error')}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


    @extend_schema(
        summary='Delete habit', tags=['Habits'],
        responses={204: None}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


    @extend_schema(
        summary='Complete habit',
        description='Marks habit as completed today and add +1 to streak',
        tags=['Habits'],
        responses={
            200: OpenApiResponse(
                description='Habit completed',
                examples=OpenApiExample(
                    'Success',
                    value={'streak': 6, 'last_completed': '2026-06-03'}
                )
            ),
            400: OpenApiResponse(description='Habit not found!')
        }
    )
    @action(detail=True, methods=['post'], url_path='complete')
    def complete(self, request, pk=None):
        habit = self.get_object()
        habit.complete()
        serializer = self.get_serializer(habit)
        return Response(serializer.data)

    @extend_schema(
        summary='Get habit stats', tags=['Habits'],
        description='Returns aggregated stats for all user habits.',
        responses={
            200: OpenApiResponse(
                description='Success',
                examples=[OpenApiExample(
                    'Stats response',
                    value={
                        'total_habits': 5,
                        'avg_streak': 4.5,
                        'best_streak': 21,
                        'daily_habits': 3,
                        'weekly_habits': 2,
                        'monthly_habits': 1
                    }
                )]
            )
        }
    )
    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        qs = self.get_queryset()
        data = {
            'total_habits': qs.count(),
            'avg_streak': round(qs.aggregate(average=Avg('streak'))['average'] or 0, 1),
            'best_streak': qs.aggregate(best=Max('streak'))['best'] or 0,
            'daily_habits': qs.filter(frequency='daily').count(),
            'weekly_habits': qs.filter(frequency='weekly').count(),
            'monthly_habits': qs.filter(frequency='monthly').count()
        }
        return Response(data)



class MoodViewSet(viewsets.ModelViewSet):
    serializer_class = MoodSerializer
    permission_classes = [IsAuthenticated]
    ordering_fields = ['date', 'created_at']

    def get_queryset(self):
        return Mood.objects.filter(user=self.request.user)


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    @extend_schema(
        summary='List all moods', tags=['Mood'],
        description='Returns all moods for the logged-in user',
        responses={200: MoodSerializer(many=True),
                   401: OpenApiResponse(description='Authentication required!')}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, *kwargs)


    @extend_schema(
        summary='Log mood', tags=['Mood'],
        description='Creates a new mood for the logged-in user.',
        request=MoodSerializer
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


    @extend_schema(summary='Get mood', tags=['Mood'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


    @extend_schema(
        summary='Update mood', tags=['Mood'],
        request=MoodSerializer
    )
    def update(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


    @extend_schema(
        summary='Partially update mood', tags=['Mood'],
        request=MoodSerializer,
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


    @extend_schema(
        summary='Delete mood', tags=['Mood'],
        responses={204: None}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)