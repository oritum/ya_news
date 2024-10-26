"""Тесты маршрутов YaNews."""

from http import HTTPStatus

import pytest
from django.test import Client
from pytest_django.asserts import assertRedirects

from news.pytest_tests.constants import (AUTHOR_CLIENT, COMMENT_DELETE_PAGE,
                                         COMMENT_EDIT_PAGE, HOME_PAGE,
                                         LOGIN_PAGE, LOGOUT_PAGE,
                                         NEWS_DETAIL_PAGE, NOT_AUTHOR_CLIENT,
                                         NOT_AUTHORIZED_CLIENT, SIGNUP_PAGE)


@pytest.mark.parametrize(
    'url, user, expected_status',
    (
        (HOME_PAGE, NOT_AUTHORIZED_CLIENT, HTTPStatus.OK),
        (NEWS_DETAIL_PAGE, NOT_AUTHORIZED_CLIENT, HTTPStatus.OK),
        (COMMENT_DELETE_PAGE, AUTHOR_CLIENT, HTTPStatus.OK),
        (COMMENT_DELETE_PAGE, NOT_AUTHOR_CLIENT, HTTPStatus.NOT_FOUND),
        (COMMENT_EDIT_PAGE, AUTHOR_CLIENT, HTTPStatus.OK),
        (COMMENT_EDIT_PAGE, NOT_AUTHOR_CLIENT, HTTPStatus.NOT_FOUND),
        (LOGIN_PAGE, NOT_AUTHOR_CLIENT, HTTPStatus.OK),
        (LOGOUT_PAGE, NOT_AUTHOR_CLIENT, HTTPStatus.OK),
        (SIGNUP_PAGE, NOT_AUTHOR_CLIENT, HTTPStatus.OK),
    ),
)
def test_pages_availability(
        url: str, user: Client, expected_status: HTTPStatus) -> None:
    """Проверка доступности страниц.
    Главная: доступна всем.
    Отдельная новость: доступна всем.
    Удаление и редактирование комментариев: доступны только автору.
    Регистрация, вход в учётную запись, выход из учётной записи: доступны всем.
    """
    assert user.get(url).status_code == expected_status


@pytest.mark.parametrize(
    'url, user',
    (
        (COMMENT_DELETE_PAGE, NOT_AUTHORIZED_CLIENT),
        (COMMENT_EDIT_PAGE, NOT_AUTHORIZED_CLIENT),
    ),
)
def test_redirects(url: str, user: Client, login_url: str) -> None:
    """Проверка перенаправления анонимного пользователя со страниц
    удаления и редактирования комментария на страницу авторизации."""
    assertRedirects(user.get(url), f'{login_url}?next={url}')
