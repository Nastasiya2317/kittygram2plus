from rest_framework import viewsets, permissions

from .models import Achievement, Cat, User

from .serializers import AchievementSerializer, CatSerializer, UserSerializer
from .permissions import OwnerOrReadOnly, ReadOnly
# импортируем класс пользователя Anon
from rest_framework.throttling import AnonRateThrottle
# класс, нужный для создания своего троттлинга
from rest_framework.throttling import ScopedRateThrottle
from .throttling import WorkingHoursRateThrottle
# настроим пагинацию на уровне класса:
from rest_framework.pagination import PageNumberPagination
# пагинатор без предопределенного количества элементов на странице
from rest_framework.pagination import LimitOffsetPagination
from .pagination import CatsPagination
# импортируем для поиска по имени и сортировке
from rest_framework import filters


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    # Устанавливаем разрешение
    permission_classes = (OwnerOrReadOnly,)
    # Если кастомный тротлинг-класс вернёт True - запросы будут обработаны
    # Если он вернёт False - все запросы будут отклонены
    throttle_classes = (WorkingHoursRateThrottle, ScopedRateThrottle)
    # throttle_classes = (AnonRateThrottle,)  # Подключили класс AnonRateThrottle
    # Для любых пользователей установим кастомный лимит 1 запрос в минуту
    # throttle_scope - атрибут
    # low_request - придуманный нами лимит, записанный в settings
    throttle_scope = 'low_request'
    # pagination_class = PageNumberPagination
    # количество объектов на странице берется из settings из PAGE_SIZE
    # Если пагинация установлена на уровне проекта, то для отдельного класса её можно отключить, установив для атрибута pagination_class значение None
    # Даже если на уровне проекта установлен PageNumberPagination
    # Для котиков будет работать LimitOffsetPagination
    # pagination_class = LimitOffsetPagination 
    # pagination_class = CatsPagination

    # Указываем фильтрующий бэкенд DjangoFilterBackend
    # Из библиотеки django-filter
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # Временно отключим пагинацию на уровне вьюсета, 
    # так будет удобнее настраивать фильтрацию
    pagination_class = None
    # Фильтровать будем по полям color и birth_year модели Cat
    filterset_fields = ('color', 'birth_year')
    # будем делать поиск по имени
    search_fields = ('name',)
    # поиск по полям в связанных таблицах:
    # search_fields = ('achievements__name', 'owner__username')
    # проводим сортировку по полям
    ordering_fields = ('name', 'birth_year')
    # сортировка по умолчанию
    ordering = ('birth_year',)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
    # Если в GET-запросе требуется получить информацию об объекте
        if self.action == 'retrieve':
        # Вернем обновленный перечень используемых пермишенов
            return (ReadOnly(),)
        # Для остальных ситуаций оставим текущий перечень пермишенов без изменений
        return super().get_permissions() 


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
