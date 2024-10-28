import pytest
from pytest_django.asserts import assertRedirects

from django.urls import reverse


from pytest_django.asserts import assertRedirects, assertFormError

from pytils.translit import slugify
from news.models import Comment, News


from http import HTTPStatus
from news.pytest_tests.constants import NOT_AUTHORIZED_CLIENT, AUTHOR_CLIENT

@pytest.mark.parametrize('user', (NOT_AUTHORIZED_CLIENT,))
def test_anonymous_user_cant_create_comment(user, form_data, news_detail_url):
    # Совершаем запрос от анонимного клиента, в POST-запросе отправляем
    # предварительно подготовленные данные формы с текстом комментария.     
    user.post(news_detail_url, data=form_data)
    # Считаем количество комментариев.
    comments_count = Comment.objects.count()
    # Ожидаем, что комментариев в базе нет - сравниваем с нулём.
    assert comments_count == 0

@pytest.mark.parametrize('user', (AUTHOR_CLIENT,))
def test_user_can_create_comment(user, news_detail_url, form_data, news):
    response = user.post(news_detail_url, data=form_data)
    assert response.status_code == HTTPStatus.FOUND
    assert response['Location'] == f'{news_detail_url}#comments'
    
    comments_count = Comment.objects.count()
    assert comments_count == 1
    
    comment = Comment.objects.get()
    assert comment.text == form_data['text']
    assert comment.news == news
    assert comment.author == user