from hasty import hasty
import requests_mock


def test_bin():
    url = 'https://helloworld.com/'
    webbin = hasty.Hastebin(url)
    assert webbin.url == url


def test_paste():
    with requests_mock.Mocker() as mock_api:
        url = 'https://helloworld.com/'
        mock_response = 'hello111'
        mock_link = url + mock_response
        mock_api.post(url + 'documents', json={'key': mock_response})

        hastebin = hasty.Hastebin(url)
        link = hastebin.paste('hello world')
        assert link == mock_link


# TODO - test error handling


