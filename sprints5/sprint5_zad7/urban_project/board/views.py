from django.shortcuts import render, redirect
from .models import Advertisement
from .forms import AdvertisementForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from .forms import SignUpForm
from django.contrib.auth import login
from .models import UserProfile


def logout_view(request):
    """
    Обрабатывает выход пользователя из системы.

    Аргументы:
        request: Объект HTTP-запроса.

    Возвращает:
        Перенаправление на главную страницу после выхода.
    """
    logout(request)
    return redirect('home')


def signup(request):
    """
    Обрабатывает регистрацию нового пользователя.

    Если метод запроса POST, форма регистрации обрабатывается. Пользователь
    создаётся и автоматически авторизуется, а также создаётся профиль пользователя.

    Аргументы:
        request: Объект HTTP-запроса.

    Возвращает:
        Отображает страницу регистрации или перенаправляет на доску после успешной регистрации.
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)  # Создание профиля пользователя
            login(request, user)
            return redirect('/board')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def home(request):
    """
    Отображает главную страницу.

    Аргументы:
        request: Объект HTTP-запроса.

    Возвращает:
        Отображает шаблон главной страницы.
    """
    return render(request, 'home.html')


def advertisement_list(request):
    """
    Отображает список всех объявлений.

    Аргументы:
        request: Объект HTTP-запроса.

    Возвращает:
        Отображает шаблон списка объявлений со всеми объявлениями.
    """
    advertisements = Advertisement.objects.all()
    return render(request, 'board/advertisement_list.html', {'advertisements': advertisements})


def advertisement_detail(request, pk):
    """
    Отображает подробности конкретного объявления.

    Аргументы:
        request: Объект HTTP-запроса.
        pk: Первичный ключ объявления для получения.

    Возвращает:
        Отображает шаблон детализации объявления для указанного объявления.
    """
    advertisement = Advertisement.objects.get(pk=pk)
    return render(request, 'board/advertisement_detail.html', {'advertisement': advertisement})


@login_required
def add_advertisement(request):
    """
    Обрабатывает создание нового объявления.

    Если метод запроса POST, обрабатывает форму объявления.
    Если форма действительна, объявление сохраняется с текущим пользователем как автором.

    Аргументы:
        request: Объект HTTP-запроса.

    Возвращает:
        Отображает форму добавления объявления или перенаправляет на список объявлений после сохранения.
    """
    if request.method == "POST":
        form = AdvertisementForm(request.POST, request.FILES)
        if form.is_valid():
            advertisement = form.save(commit=False)
            advertisement.author = request.user
            advertisement.save()

            # Обновляем счетчик созданных объявлений у профиля пользователя
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            user_profile.created_ads_count += 1  # Увеличиваем счетчик созданных объявлений
            print(f"Объявление создано: {advertisement.title}, Автор: {request.user.username}")
            print(f"Обновлен счетчик созданных объявлений: {user_profile.created_ads_count}")
            user_profile.save()

            return redirect('board:advertisement_list')
    else:
        form = AdvertisementForm()

    return render(request, 'board/add_advertisement.html', {'form': form})


@login_required
def edit_advertisement(request, pk):
    """
    Обрабатывает редактирование существующего объявления.

    Убедитесь, что объявление принадлежит текущему пользователю.
    Если метод запроса POST, обрабатывает форму для объявления.

    Аргументы:
        request: Объект HTTP-запроса.
        pk: Первичный ключ объявления для редактирования.

    Возвращает:
        Отображает форму редактирования объявления или перенаправляет на список объявлений после сохранения.
    """
    advertisement = get_object_or_404(Advertisement, pk=pk, author=request.user)
    if request.method == "POST":
        form = AdvertisementForm(request.POST, request.FILES, instance=advertisement)  # Обработка изображений
        if form.is_valid():
            form.save()
            return redirect('board:advertisement_list')
    else:
        form = AdvertisementForm(instance=advertisement)
    return render(request, 'board/edit_advertisement.html', {'form': form, 'advertisement': advertisement})


@login_required
def delete_advertisement(request, pk):
    """
    Обрабатывает удаление объявления.

    Убедитесь, что объявление принадлежит текущему пользователю.
    Если метод запроса POST, объявление удаляется.

    Аргументы:
        request: Объект HTTP-запроса.
        pk: Первичный ключ объявления для удаления.

    Возвращает:
        отображает подтверждение удаления объявления или перенаправляет на список объявлений после удаления.
    """
    advertisement = get_object_or_404(Advertisement, pk=pk, author=request.user)

    if request.method == "POST":
        # Здесь обновляем счетчик удаленных объявлений у профиля пользователя
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        user_profile.deleted_ads_count += 1  # Увеличиваем счетчик удалённых объявлений
        user_profile.save()

        advertisement.delete()  # Удаление объявления
        return redirect('board:advertisement_list')  # Перенаправление на список объявлений

    return render(request, 'board/delete_advertisement.html', {'advertisement': advertisement})


@login_required
def like_advertisement(request, pk):
    """
    Обрабатывает лайк к объявлению.
    """
    advertisement = get_object_or_404(Advertisement, pk=pk)

    # Убедитесь, что профиль пользователя существует
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    # Обновляем количество лайков в объявлении
    advertisement.likes += 1
    advertisement.save()

    # Обновляем количество лайков у профиля пользователя
    user_profile.likes_count += 1
    user_profile.save()

    return redirect('board:advertisement_detail', pk=pk)


#@login_required
#def dislike_advertisement(request, pk):
#    """
#    Обрабатывает дизлайк к объявлению.
#   Увеличивает счетчик дизлайков на 1.
#    """
#    advertisement = get_object_or_404(Advertisement, pk=pk)
#    advertisement.dislikes += 1
#    advertisement.save()
#    return redirect('board:advertisement_detail', pk=pk)


#@login_required
#def like_advertisement(request, pk):
#    """
#    Обрабатывает действие лайка к объявлению.

#    Увеличивает счётчик лайков объявления и счётчик лайков пользователя.

#   Аргументы:
#        request: Объект HTTP-запроса.
#        pk: Первичный ключ объявления для лайка.

#    Возвращает:
#        Перенаправление на страницу детализации объявления.
#    """
#    advertisement = get_object_or_404(Advertisement, pk=pk)
#    advertisement.likes += 1
#    advertisement.save()

#    advertisement.author.userprofile.likes_count += 1
#    advertisement.author.userprofile.save()

#    return redirect('board:advertisement_detail', pk=pk)


@login_required
def dislike_advertisement(request, pk):
    """
    Обрабатывает действие дизлайка к объявлению.

    Увеличивает счётчик дизлайков объявления и счётчик дизлайков пользователя.

    Аргументы:
        request: Объект HTTP-запроса.
        pk: Первичный ключ объявления для дизлайка.

    Возвращает:
        Перенаправление на страницу детализации объявления.
    """
    advertisement = get_object_or_404(Advertisement, pk=pk)
    advertisement.dislikes += 1
    advertisement.save()

    advertisement.author.userprofile.dislikes_count += 1
    advertisement.author.userprofile.save()

    return redirect('board:advertisement_detail', pk=pk)

