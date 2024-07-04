import pytest
from dotenv import load_dotenv, find_dotenv
import os
import urllib3

load_dotenv(find_dotenv())  # Load .env to environment

BACKEND_URL = os.getenv('BACKEND_ENDPOINT')

http = urllib3.PoolManager()

pages = []
pages_name = []


def total_pages():
    """Get total pages counts"""
    request = http.request("GET", BACKEND_URL)
    json_data = request.json()
    count = json_data['total_pages']
    for i in range(0, count):
        pages.append(i + 1)
        pages_name.append(f"page_{i + 1}")


total_pages()


@pytest.fixture(params=pages, ids=pages_name)
def current_page(request):
    page = http.request("GET", f"{BACKEND_URL}?page={request.param}")
    return page


@pytest.fixture(scope='class')
def page_users():
    """Get page"""
    return http.request("GET", BACKEND_URL)
