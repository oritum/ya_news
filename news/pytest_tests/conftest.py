"""Фикстуры для Pytest."""

from typing import Type

import pytest
from django.contrib.auth.models import AbstractBaseUser
from django.test.client import Client
from django.urls import reverse
from datetime import datetime, timedelta
from news.models import Comment, News
from yanews.settings import NEWS_COUNT_ON_HOME_PAGE


@pytest.fixture(autouse=True)
def enable_db_access(db):
    pass


@pytest.fixture
def author(django_user_model: Type[AbstractBaseUser]) -> AbstractBaseUser:
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model: Type[AbstractBaseUser]) -> AbstractBaseUser:
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author: AbstractBaseUser) -> Client:
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author: AbstractBaseUser) -> Client:
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news() -> News:
    return News.objects.create(
        title='Заголовок',
        text='Текст новости',
    )


@pytest.fixture
def comment(news: News, author: AbstractBaseUser) -> Comment:
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария',
    )


@pytest.fixture
def news_home_list() -> list[News]:
    return News.objects.bulk_create(
        News(
            title=f'Заголовок {index}', 
            text='Текст новости.',
            date=datetime.today() - timedelta(days=index)
        )
        for index in range(NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def homepage_url() -> str:
    return reverse('news:home')


@pytest.fixture
def news_detail_url(news: News) -> str:
    return reverse('news:detail', args=(news.pk,))


@pytest.fixture
def comment_delete_url(comment: Comment) -> str:
    return reverse('news:delete', args=(comment.pk,))


@pytest.fixture
def comment_edit_url(comment: Comment) -> str:
    return reverse('news:edit', args=(comment.pk,))


@pytest.fixture
def login_url() -> str:
    return reverse('users:login')


@pytest.fixture
def logout_url() -> str:
    return reverse('users:logout')


@pytest.fixture
def signup_url() -> str:
    return reverse('users:signup')
