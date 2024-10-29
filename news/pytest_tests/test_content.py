# """Тесты контента YaNews."""

# import pytest
# from django.http import HttpResponse
# from django.test import Client

# from news.forms import CommentForm
# from news.models import Comment, News
# from news.pytest_tests.constants import (AUTHOR_CLIENT, NOT_AUTHOR_CLIENT,
#                                          NOT_AUTHORIZED_CLIENT)
# from yanews.settings import NEWS_COUNT_ON_HOME_PAGE


# def test_count_of_news(
#     news_home_list: list[News],
#     homepage_response,
# ) -> None:
#     """Проверка количества новостей на главной странице - не более 10."""
#     assert (
#         len(homepage_response.context['object_list'])
#         == NEWS_COUNT_ON_HOME_PAGE
#     )


# def test_news_order(
#     news_home_list: list[News],
#     homepage_response: HttpResponse
# ) -> None:
#     """"Проверка корректности сортировки новостей - от новых к старым."""
#     all_dates = [
#         news.date for news in homepage_response.context['object_list']
#     ]
#     assert all_dates == sorted(all_dates, reverse=True)


# @pytest.mark.parametrize('user', (AUTHOR_CLIENT,))
# def test_comments_order(
#         comments_list: list[Comment],
#         news_detail_response: HttpResponse
# ) -> None:
#     """"Проверка корректности сортировки комментариев - от старых к новым."""
#     assert 'news' in news_detail_response.context
#     all_timestamps = [
#         comment.created for comment in news_detail_response
#         .context['news'].comment_set.all()
#     ]
#     assert all_timestamps == sorted(all_timestamps)


# @pytest.mark.parametrize(
#     'user, has_form',
#     (
#         (NOT_AUTHORIZED_CLIENT, False),
#         (NOT_AUTHOR_CLIENT, True),
#     ),
# )
# def test_client_form_visibility(
#     user: Client,
#     has_form: bool,
#     news_detail_response: HttpResponse
# ) -> None:
#     """Проверка доступности формы отправки комментария.
#     Анонимному пользователю: недоcтупна.
#     Авторизованному пользователю: доступна."""
#     assert ('form' in news_detail_response.context) is has_form
#     if has_form:
#         assert isinstance(news_detail_response.context['form'], CommentForm)
