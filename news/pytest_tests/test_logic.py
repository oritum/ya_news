from http import HTTPStatus

import pytest
from django.contrib.auth.models import AbstractBaseUser
from django.http import HttpResponse
from django.test import Client
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment, News
from news.pytest_tests.constants import AUTHOR_CLIENT, NOT_AUTHOR_CLIENT


def test_anonymous_user_cant_create_comment(
    client: Client,
    form_data: dict[str, str],
    news_detail_url: str,
) -> None:
    """Проверка невозможности отправки комментария анонимным пользователем."""
    client.post(news_detail_url, data=form_data)
    assert Comment.objects.count() == 0


@pytest.mark.parametrize('user', (NOT_AUTHOR_CLIENT,))
def test_user_can_create_comment(
    user: Client,
    not_author: AbstractBaseUser,
    news_detail_url: str,
    form_data: dict[str, str],
    comments_section_url: str,
    news: News
) -> None:
    """Проверка возможности отправки комментария аторизованным пользователем.
    """
    assertRedirects(user.post(news_detail_url, data=form_data),
                    comments_section_url)
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == form_data['text']
    assert comment.news == news
    assert comment.author == not_author


@pytest.mark.parametrize('user', (NOT_AUTHOR_CLIENT,))
@pytest.mark.parametrize('bad_word', BAD_WORDS)
def test_user_cant_use_bad_words(
    user: Client,
    news_detail_url: str,
    bad_word: str,
) -> None:
    """Проверка невозможности использования запрещённых слов в комментариях."""
    assertFormError(
        user.post(news_detail_url, data={'text': f'text, {bad_word}, text'}),
        form='form',
        field='text',
        errors=WARNING
    )
    assert Comment.objects.count() == 0


@pytest.mark.parametrize('user', (AUTHOR_CLIENT, NOT_AUTHOR_CLIENT))
def test_comment_delete_permission(
    user: Client,
    author_client: Client,
    comment_delete_response: HttpResponse,
    comments_section_url: str
 ) -> None:
    """Проверка доступности удаления комментариев:
    Автору комментария: доступно.
    Не автору: недоступно.
    """
    if user == author_client:
        assertRedirects(comment_delete_response, comments_section_url)
        assert Comment.objects.count() == 0
    else:
        assert comment_delete_response.status_code == HTTPStatus.NOT_FOUND
        assert Comment.objects.count() == 1


@pytest.mark.parametrize('user', (AUTHOR_CLIENT, NOT_AUTHOR_CLIENT))
def test_comment_edit_permission(
    user: Client,
    author_client: Client,
    comment: Comment,
    comment_edit_response: HttpResponse,
    comments_section_url: str,
    form_data: dict[str, str],
    form_data_new: dict[str, str],
 ) -> None:
    """Проверка доступности редактирования комментариев:
    Автору комментария: доступно.
    Не автору: недоступно.
    """
    if user == author_client:
        assertRedirects(comment_edit_response, comments_section_url)
        comment.refresh_from_db()
        assert comment.text == form_data_new['text']
    else:
        assert comment_edit_response.status_code == HTTPStatus.NOT_FOUND
        comment.refresh_from_db()
        assert comment.text == form_data['text']
