"""Фикстуры для Pytest."""

import pytest
from typing import Type
from django.test.client import Client
from django.contrib.auth.models import AbstractBaseUser
from news.models import News, Comment


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
def pk_for_args(news: News) -> tuple:
    return (news.pk,)


@pytest.fixture
def comment(news: News, author: AbstractBaseUser) -> Comment:
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария',
    )

@pytest.fixture
def pk_for_comment(comment: Comment) -> tuple:
    return (comment.pk,)


@pytest.fixture
def form_data():
    return {
        'title': 'Новый заголовок',
        'text': 'Новый текст',
        'slug': 'new-slug'
    } 