"""Тесты маршрутов YaNews."""

import pytest

from http import HTTPStatus

from django.urls import reverse
from django.test import Client
from pytest_django.asserts import assertRedirects

from news.pytest_tests.constants import (
    HOME_PAGE, LOGIN_PAGE, LOGOUT_PAGE, SIGNUP_PAGE, NEWS_DETAIL_PAGE,
    COMMENT_DELETE_PAGE, COMMENT_EDIT_PAGE
)
from news.models import News



@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args',
    (
        (HOME_PAGE, None),
        (LOGIN_PAGE, None),
        (LOGOUT_PAGE, None),
        (SIGNUP_PAGE, None),
        (NEWS_DETAIL_PAGE, pytest.lazy_fixture('pk_for_args')),
    ),
)
def test_pages_availability_for_anonymous_user(
        client: Client, name: str, args: tuple) -> None:
    """Проверка доступности главной страницы, страницы отдельной новости, 
    страниц регистрации, входа в учётную запись и выхода из неё анонимному 
    пользователю."""
    assert client.get(reverse(name, args=args)).status_code == HTTPStatus.OK

@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK)
    )
)
@pytest.mark.parametrize('name', (COMMENT_DELETE_PAGE, COMMENT_EDIT_PAGE))
def test_pages_availability_for_different_users(
    parametrized_client, name, comment, expected_status
):
    """Проверка доступности страницы удаления и редактирования комментария
    автору комментария."""
    assert (parametrized_client.get(
        reverse(name, args=(comment.pk,))).status_code == expected_status)


# @pytest.mark.parametrize(
#     'name',  # Имя параметра функции.
#     # Значения, которые будут передаваться в name.
#     ('notes:home', 'users:login', 'users:logout', 'users:signup')
# )
# # Указываем имя изменяемого параметра в сигнатуре теста.
# def test_pages_availability_for_anonymous_user(client, name):
#     url = reverse(name)  # Получаем ссылку на нужный адрес.
#     response = client.get(url)  # Выполняем запрос.
#     assert response.status_code == HTTPStatus.OK


# @pytest.mark.parametrize(
#     'name',
#     ('notes:list', 'notes:add', 'notes:success')
# )
# def test_pages_availability_for_auth_user(not_author_client, name):
#     url = reverse(name)
#     response = not_author_client.get(url)
#     assert response.status_code == HTTPStatus.OK


# @pytest.mark.parametrize(
#     'parametrized_client, expected_status',
#     # Предварительно оборачиваем имена фикстур 
#     # в вызов функции pytest.lazy_fixture().
#     (
#         (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND),
#         (pytest.lazy_fixture('author_client'), HTTPStatus.OK)
#     ),
# )
# @pytest.mark.parametrize(
#     'name',
#     ('notes:detail', 'notes:edit', 'notes:delete'),
# )
# def test_pages_availability_for_different_users(
#         parametrized_client, name, note, expected_status
# ):
#     url = reverse(name, args=(note.slug,))
#     response = parametrized_client.get(url)
#     assert response.status_code == expected_status


# @pytest.mark.parametrize(
#     'name, args',
#     (
#         ('notes:detail', pytest.lazy_fixture('slug_for_args')),
#         ('notes:edit', pytest.lazy_fixture('slug_for_args')),
#         ('notes:delete', pytest.lazy_fixture('slug_for_args')),
#         ('notes:add', None),
#         ('notes:success', None),
#         ('notes:list', None),
#     ),
# )
# # Передаём в тест анонимный клиент, name проверяемых страниц и args:
# def test_redirects(client, name, args):
#     login_url = reverse('users:login')
#     # Теперь не надо писать никаких if и можно обойтись одним выражением.
#     url = reverse(name, args=args)
#     expected_url = f'{login_url}?next={url}'
#     response = client.get(url)
#     assertRedirects(response, expected_url) 
