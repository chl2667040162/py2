from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Competition(models.Model):
    STATUS_CHOICES = [
        ('planned', 'Запланировано'),
        ('ongoing', 'В процессе'),
        ('completed', 'Завершено'),
        ('cancelled', 'Отменено'),
    ]

    SPORT_TYPES = [
        ('football', 'Футбол'),
        ('basketball', 'Баскетбол'),
        ('volleyball', 'Волейбол'),
        ('tennis', 'Теннис'),
        ('swimming', 'Плавание'),
        ('athletics', 'Легкая атлетика'),
        ('chess', 'Шахматы'),
    ]

    name = models.CharField(max_length=200, verbose_name="Название соревнования")
    description = models.TextField(verbose_name="Описание")
    sport_type = models.CharField(
        max_length=50,
        choices=SPORT_TYPES,
        verbose_name="Вид спорта"
    )
    location = models.CharField(max_length=200, verbose_name="Место проведения")
    start_date = models.DateTimeField(verbose_name="Дата начала")
    end_date = models.DateTimeField(verbose_name="Дата окончания")
    max_participants = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(1000)],
        verbose_name="Максимальное количество участников",
        default=100
    )
    current_participants = models.IntegerField(
        default=0,
        verbose_name="Текущее количество участников"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='planned',
        verbose_name="Статус"
    )
    is_public = models.BooleanField(default=True, verbose_name="Публичное соревнование")
    registration_deadline = models.DateTimeField(
        verbose_name="Срок регистрации",
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_competitions',
        verbose_name="Создатель"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Соревнование"
        verbose_name_plural = "Соревнования"
        permissions = [
            ("can_view_all", "Может просматривать все соревнования"),
            ("can_edit_competition", "Может редактировать соревнование"),
            ("can_delete_competition", "Может удалять соревнование"),
            ("can_create_competition", "Может создавать соревнование"),
            ("can_register_participant", "Может регистрировать участников"),
        ]
        ordering = ['-start_date']

    def __str__(self):
        return self.name

    @property
    def is_registration_open(self):
        if self.registration_deadline:
            return timezone.now() <= self.registration_deadline
        return True

    @property
    def available_slots(self):
        return self.max_participants - self.current_participants


class Participant(models.Model):
    competition = models.ForeignKey(
        Competition,
        on_delete=models.CASCADE,
        related_name='participants'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='participations'
    )
    registration_date = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)

    class Meta:
        unique_together = ['competition', 'user']
        verbose_name = "Участник"
        verbose_name_plural = "Участники"

    def __str__(self):
        return f"{self.user.username} - {self.competition.name}"