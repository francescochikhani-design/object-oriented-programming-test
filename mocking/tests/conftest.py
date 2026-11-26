from unittest.mock import Mock

import pytest

from src.app import OrderService, ProductRepository


@pytest.fixture
def repository():
    return ProductRepository()


@pytest.fixture
def service(repository):
    return OrderService(repository)


@pytest.fixture
def client():
    return Mock()
