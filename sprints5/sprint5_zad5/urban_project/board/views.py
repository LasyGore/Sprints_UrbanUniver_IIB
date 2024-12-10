from django.shortcuts import render, redirect
from .models import Advertisement
from .forms import AdvertisementForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from .forms import SignUpForm
from django.contrib.auth import login


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
    Обрабатывает регистрацию пользователя.

    Если метод запроса POST, функция обрабатывает форму регистрации.
    Если форма действительна, пользователь регистрируется и авторизуется.

    Аргументы:
        request: Объект HTTP-запроса.

    Возвращает:
        Отображает страницу регистрации или перенаправляет на доску после успешной регистрации.
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
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
        form = AdvertisementForm(request.POST, request.FILES)  # Обработка изображений
        if form.is_valid():
            advertisement = form.save(commit=False)
            advertisement.author = request.user
            advertisement.save()
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
       ображает подтверждение удаления объявления или перенаправляет на список объявлений после удаления.
    """
    advertisement = get_object_or_404(Advertisement, pk=pk, author=request.user)

    if request.method == "POST":
        advertisement.delete()  # Удаление объявления
        return redirect('board:advertisement_list')  # Перенаправление на список объявлений

    return render(request, 'board/delete_advertisement.html', {'advertisement': advertisement})



@login_required
def like_advertisement(request, pk):
    """
    Обрабатывает лайк к объявлению.
    Увеличивает счетчик лайков на 1.
    """
    advertisement = get_object_or_404(Advertisement, pk=pk)
    advertisement.likes += 1
    advertisement.save()
    return redirect('board:advertisement_detail', pk=pk)


@login_required
def dislike_advertisement(request, pk):
    """
    Обрабатывает дизлайк к объявлению.
    Увеличивает счетчик дизлайков на 1.
    """
    advertisement = get_object_or_404(Advertisement, pk=pk)
    advertisement.dislikes += 1
    advertisement.save()
    return redirect('board:advertisement_detail', pk=pk)

