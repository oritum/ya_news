"""Тесты контента YaNews."""

from http import HTTPStatus

import pytest
from django.test import Client
from yanews.settings import NEWS_COUNT_ON_HOME_PAGE
from news.models import Comment, News

from news.pytest_tests.constants import (AUTHOR_CLIENT, COMMENT_DELETE_PAGE,
                                         COMMENT_EDIT_PAGE, HOME_PAGE,
                                         LOGIN_PAGE, LOGOUT_PAGE,
                                         NEWS_DETAIL_PAGE, NOT_AUTHOR_CLIENT,
                                         NOT_AUTHORIZED_CLIENT, SIGNUP_PAGE)


@pytest.mark.parametrize('user', (NOT_AUTHORIZED_CLIENT,))
def test_count_of_news(
    news_home_list: list[News],
    user: Client,
    homepage_url: str
) -> None:
    """Проверка количества новостей на главной странице - не более 10."""
    assert (
        len(user.get(homepage_url).context['object_list'])
        == NEWS_COUNT_ON_HOME_PAGE
    )

@pytest.mark.parametrize('user', (NOT_AUTHORIZED_CLIENT,))
def test_news_order(
    news_home_list: list[News],
    user: Client,
    homepage_url: str
) -> None:
    """"Проверка корректности сортировки новостей - от новых к старым."""
    all_dates = [
        news.date for news in user.get(homepage_url).context['object_list']
    ]
    assert all_dates == sorted(all_dates, reverse=True)
