from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.db.models import Q
from .models import Competition, Participant
from .forms import CompetitionForm, LoginForm, SearchForm


def competition_list(request):
    competitions = Competition.objects.all()
    form = SearchForm(request.GET or None)

    if form.is_valid():
        query = form.cleaned_data.get('query')
        sport_type = form.cleaned_data.get('sport_type')
        status = form.cleaned_data.get('status')

        if query:
            competitions = competitions.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(location__icontains=query)
            )

        if sport_type:
            competitions = competitions.filter(sport_type=sport_type)

        if status:
            competitions = competitions.filter(status=status)

    # Для обычных пользователей показываем только публичные соревнования
    if not request.user.has_perm('competitions.can_view_all'):
        competitions = competitions.filter(is_public=True)

    context = {
        'competitions': competitions,
        'form': form,
        'can_create': request.user.has_perm('competitions.can_create_competition'),
    }
    return render(request, 'competitions/competition_list.html', context)


def competition_detail(request, pk):
    competition = get_object_or_404(Competition, pk=pk)

    # Проверка доступа
    if not competition.is_public and not request.user.has_perm('competitions.can_view_all'):
        messages.error(request, "У вас нет доступа к этому соревнованию")
        return redirect('competition_list')

    is_participant = False
    if request.user.is_authenticated:
        is_participant = Participant.objects.filter(
            competition=competition,
            user=request.user
        ).exists()

    context = {
        'competition': competition,
        'is_participant': is_participant,
        'can_edit': request.user.has_perm('competitions.can_edit_competition') or
                    request.user == competition.created_by,
        'can_delete': request.user.has_perm('competitions.can_delete_competition') or
                      request.user == competition.created_by,
        'can_register': request.user.has_perm('competitions.can_register_participant'),
    }
    return render(request, 'competitions/competition_detail.html', context)


@login_required
@permission_required('competitions.can_create_competition', raise_exception=True)
def competition_create(request):
    if request.method == 'POST':
        form = CompetitionForm(request.POST)
        if form.is_valid():
            competition = form.save(commit=False)
            competition.created_by = request.user
            competition.save()
            messages.success(request, 'Соревнование успешно создано!')
            return redirect('competition_detail', pk=competition.pk)
    else:
        form = CompetitionForm()

    context = {'form': form}
    return render(request, 'competitions/competition_form.html', context)


@login_required
def competition_edit(request, pk):
    competition = get_object_or_404(Competition, pk=pk)

    # Проверка прав на редактирование
    if not (request.user.has_perm('competitions.can_edit_competition') or
            request.user == competition.created_by):
        messages.error(request, "У вас нет прав на редактирование этого соревнования")
        return redirect('competition_detail', pk=pk)

    if request.method == 'POST':
        form = CompetitionForm(request.POST, instance=competition)
        if form.is_valid():
            form.save()
            messages.success(request, 'Соревнование успешно обновлено!')
            return redirect('competition_detail', pk=competition.pk)
    else:
        form = CompetitionForm(instance=competition)

    context = {
        'form': form,
        'competition': competition,
    }
    return render(request, 'competitions/competition_form.html', context)


@login_required
def competition_delete(request, pk):
    competition = get_object_or_404(Competition, pk=pk)

    # Проверка прав на удаление
    if not (request.user.has_perm('competitions.can_delete_competition') or
            request.user == competition.created_by):
        messages.error(request, "У вас нет прав на удаление этого соревнования")
        return redirect('competition_detail', pk=pk)

    if request.method == 'POST':
        competition.delete()
        messages.success(request, 'Соревнование успешно удалено!')
        return redirect('competition_list')

    context = {'competition': competition}
    return render(request, 'competitions/competition_confirm_delete.html', context)


@login_required
def register_participant(request, pk):
    competition = get_object_or_404(Competition, pk=pk)

    if not request.user.has_perm('competitions.can_register_participant'):
        messages.error(request, "У вас нет прав на регистрацию участников")
        return redirect('competition_detail', pk=pk)

    if not competition.is_registration_open:
        messages.error(request, "Регистрация на это соревнование закрыта")
        return redirect('competition_detail', pk=pk)

    if competition.available_slots <= 0:
        messages.error(request, "Нет свободных мест для регистрации")
        return redirect('competition_detail', pk=pk)

    # Проверяем, не зарегистрирован ли уже пользователь
    if Participant.objects.filter(competition=competition, user=request.user).exists():
        messages.warning(request, "Вы уже зарегистрированы на это соревнование")
        return redirect('competition_detail', pk=pk)

    # Регистрируем участника
    Participant.objects.create(
        competition=competition,
        user=request.user,
        is_confirmed=True
    )

    # Обновляем счетчик участников
    competition.current_participants += 1
    competition.save()

    messages.success(request, "Вы успешно зарегистрировались на соревнование!")
    return redirect('competition_detail', pk=pk)


def custom_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Добро пожаловать, {user.username}!")
            return redirect('competition_list')
    else:
        form = LoginForm()

    return render(request, 'competitions/login.html', {'form': form})


def custom_logout(request):
    logout(request)
    messages.info(request, "Вы успешно вышли из системы")
    return redirect('competition_list')