"""Константы для Pytest."""
import pytest
from django.utils import timezone

# Константы разных типов клиентов:
NOT_AUTHORIZED_CLIENT = pytest.lazy_fixture('client')
NOT_AUTHOR_CLIENT = pytest.lazy_fixture('not_author_client')
AUTHOR_CLIENT = pytest.lazy_fixture('author_client')

# Константы разных страниц проекта:
HOME_PAGE: str = pytest.lazy_fixture('homepage_url')
NEWS_DETAIL_PAGE: str = pytest.lazy_fixture('news_detail_url')
COMMENT_DELETE_PAGE: str = pytest.lazy_fixture('comment_delete_url')
COMMENT_EDIT_PAGE: str = pytest.lazy_fixture('comment_edit_url')
LOGIN_PAGE: str = pytest.lazy_fixture('login_url')
LOGOUT_PAGE: str = pytest.lazy_fixture('logout_url')
SIGNUP_PAGE: str = pytest.lazy_fixture('signup_url')


NOW = timezone.now()  # Текущие дата и время.
