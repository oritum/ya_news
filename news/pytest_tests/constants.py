"""Константы для Pytest."""
import pytest
from django.urls import reverse


HOME_PAGE: str = 'news:home'
NEWS_DETAIL_PAGE: str = 'news:detail'
COMMENT_DELETE_PAGE: str = 'news:delete'
COMMENT_EDIT_PAGE: str = 'news:edit'
LOGIN_PAGE: str = 'users:login'
LOGOUT_PAGE: str = 'users:logout'
SIGNUP_PAGE: str = 'users:signup'
