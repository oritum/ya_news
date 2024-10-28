"""Фикстуры для Pytest."""

from datetime import timedelta
from typing import Type

import pytest
from django.contrib.auth.models import AbstractBaseUser
from django.http import HttpResponse
from django.test.client import Client
from django.urls import reverse

from news.models import Comment, News
from news.pytest_tests.constants import NOW
from yanews.settings import NEWS_COUNT_ON_HOME_PAGE


@pytest.fixture(autouse=True)
def enable_db_access(db):
    """Автоматически включает доступ к базе данных для всех тестов."""


@pytest.fixture
def author(django_user_model: Type[AbstractBaseUser]) -> AbstractBaseUser:
    """Создаёт пользователя, выступающего автором."""
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model: Type[AbstractBaseUser]) -> AbstractBaseUser:
    """Создаёт пользователя, не являющегося автором."""
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author: AbstractBaseUser) -> Client:
    """Создаёт клиента с залогиненным автором."""
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author: AbstractBaseUser) -> Client:
    """Создаёт клиента с залогиненным пользователем, не являющимся автором."""
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news() -> News:
    """Создаёт объект News."""
    return News.objects.create(
        title='Заголовок',
        text='Текст новости',
    )


@pytest.fixture
def comment(news: News, author: AbstractBaseUser) -> Comment:
    """Создаёт комментарий."""
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария',
    )


@pytest.fixture
def form_data():
    return {'text': 'Текст комментария'}

@pytest.fixture
def comments_list(news: News, author: AbstractBaseUser) -> list[Comment]:
    """Создаёт список комментариев с разными датами создания."""
    comments: list = []
    for index in range(2):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Текст комментария {index}'
        )
        comment.created = NOW + timedelta(days=index)
        comment.save()
        comments.append(comment)
    return comments


@pytest.fixture
def news_home_list() -> list[News]:
    """Создаёт список новостей."""
    return News.objects.bulk_create(
        News(
            title=f'Заголовок {index}',
            text='Текст новости.',
            date=NOW - timedelta(days=index)
        )
        for index in range(NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def homepage_url() -> str:
    """Возвращает URL главной страницы."""
    return reverse('news:home')


@pytest.fixture
def news_detail_url(news: News) -> str:
    """Возвращает URL страницы новости."""
    return reverse('news:detail', args=(news.pk,))


@pytest.fixture
def comment_delete_url(comment: Comment) -> str:
    """Возвращает URL для удаления комментария."""
    return reverse('news:delete', args=(comment.pk,))


@pytest.fixture
def comment_edit_url(comment: Comment) -> str:
    """Возвращает URL для редактирования комментария."""
    return reverse('news:edit', args=(comment.pk,))


@pytest.fixture
def login_url() -> str:
    """Возвращает URL страницы логина пользователя."""
    return reverse('users:login')


@pytest.fixture
def logout_url() -> str:
    """Возвращает URL страницы выхода пользователя."""
    return reverse('users:logout')


@pytest.fixture
def signup_url() -> str:
    """Возвращает URL страницы регистрации нового пользователя."""
    return reverse('users:signup')


@pytest.fixture
def homepage_response(client: Client, homepage_url: str) -> HttpResponse:
    """Возвращает ответ на запрос к главной странице."""
    return client.get(homepage_url)


@pytest.fixture
def news_detail_response(user: Client, news_detail_url: str):
    """Возвращает ответ на запрос к странице новости."""
    return user.get(news_detail_url)
