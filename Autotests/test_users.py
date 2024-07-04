import json
import time

import pytest
import requests

import urllib3

from utils import check_valid_email
from conftest import BACKEND_URL

http = urllib3.PoolManager()


class TestUsers:

    def test_status_code(self, page_users):
        """Status code is 200"""
        assert page_users.status == 200

    def test_quantity_pages(self, page_users):
        """Quantity pages == 2"""
        json_data = page_users.json()
        assert json_data['total_pages'] == 2

    def test_current_page_1(self):
        """Current page is 1"""
        request = http.request("GET", BACKEND_URL + '?page=1')
        json_data = request.json()
        assert json_data['page'] == 1

    def test_current_page_2(self):
        """Current page is 2"""
        request = http.request("GET", BACKEND_URL + '?page=2')
        json_data = request.json()
        assert json_data['page'] == 2

    def test_current_page_3(self):
        """Page 3 is empty"""
        request = http.request("GET", BACKEND_URL + '?page=3')
        json_data = request.json()
        assert json_data['page'] == 3 and json_data['data'] == []

    def test_response_time(self):
        """Response time is less than 500ms"""
        start_time = time.time()
        http.request("GET", BACKEND_URL + '?page=2')
        end_time = time.time()
        response_time = end_time - start_time
        assert response_time < 0.500

    def test_body_contains_person_id(self, page_users):
        """Body contains person id"""
        page = page_users.json()
        assert page['data'][0]['id'] == 1

    def test_body_person_by_id(self):
        """Data contains info about users ID"""
        request = requests.get(BACKEND_URL + '/3')
        json_data = request.json()
        assert json_data['data']['id'] == 3

    def test_several_elements_for_test(self, page_users):
        """Several elements test"""
        json_data = page_users.json()
        assert len(json_data['data'][0]) >= 1
        assert json_data['data'][0]['id'] == 1

    def test_content_type(self, page_users):
        """Content-Type header is application/json"""
        assert page_users.headers['Content-Type'].startswith('application/json')

    def test_email_validate(self, current_page):
        """Check 'email' is valid"""
        json_data = current_page.json()
        for d in json_data['data']:
            email = d['email']
            assert check_valid_email(email)

    def test_avatar_is_valid(self, current_page):
        """Check 'avatar' is valid url"""
        json_data = current_page.json()
        for d in json_data['data']:
            avatar_url = d['avatar']
            r = requests.get(avatar_url)
            assert r.status_code == 200

    def test_first_name_validate(self, current_page):
        """Check 'first_name' contains only a-zA-Z letters"""
        json_data = current_page.json()
        for d in json_data['data']:
            first_name = d['first_name']
            assert first_name.isalpha()

    def test_last_name_validate(self, current_page):
        """Check 'last_name' contains only a-zA-Z letters"""
        json_data = current_page.json()
        for d in json_data['data']:
            last_name = d['last_name']
            assert last_name.isalpha()

    @pytest.mark.xfail(reason="Method POST do not create row without body. Return status 201")
    def test_post_without_body(self):
        """Check create row in DB without body"""
        request_post = http.request(method="POST", url=BACKEND_URL)
        post_data = request_post.json()
        assert request_post.status == 201
        request_get = http.request(method="GET", url=BACKEND_URL + f"/{post_data['id']}")
        assert request_get.status == 200  # Wrong

    @pytest.mark.xfail(reason="Method POST do not create row with body. Return status 201")
    def test_post_with_body(self):
        """Check create row in DB with body"""
        data = {'email': 'test.fields@reqres.in', 'first_name': 'Test', 'last_name': 'Fortest',
                'avatar': 'https://reqres.in/img/faces/10-image.jpg'}
        request_post = http.request(method="POST", url=BACKEND_URL, body=json.dumps(data))
        post_data = request_post.json()
        assert request_post.status == 201
        request_get = http.request(method="GET", url=BACKEND_URL + f"/{post_data['id']}")
        assert request_get.status == 200  # Wrong

    @pytest.mark.xfail(reason="Method PATCH not work")
    def test_patch_data(self):
        """Check data changes by PATCH request"""
        request_get = http.request(method="GET", url=BACKEND_URL + "/2")
        last_name_before = request_get.json()['data']['last_name']
        patch_name = "Fortest"
        assert last_name_before != patch_name

        request_opt = http.request(method="PATCH", url=BACKEND_URL + "/2", body=json.dumps({'last_name': patch_name}))
        assert request_opt.status == 200

        updated_get = http.request(method="GET", url=BACKEND_URL + "/2")
        last_name_after = updated_get.json()['data']['last_name']
        assert patch_name == last_name_after  # Wrong

    @pytest.mark.xfail(reason="Method DELETE not work")
    def test_delete_data(self):
        """Check DELETE row by DELETE request"""
        request_get = http.request(method="GET", url=BACKEND_URL + "/3")
        data_before = request_get.json()['data']
        assert data_before != {}

        request_del = http.request(method="DELETE", url=BACKEND_URL + "/3")
        assert request_del.status == 204

        updated_get = http.request(method="GET", url=BACKEND_URL + "/3")
        assert updated_get.status == 404  # Wrong
