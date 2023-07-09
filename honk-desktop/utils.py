"""
Utility functions and classes
"""
import json
import os
import requests


def get_or_create_directory(path):
    """
    Get or create a directory
    """
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as e:
            raise SystemError(f"Could not create directory: {path} - {e}")
    return path


class Config:
    """
    Credentials class
    """

    def __init__(self):
        self.config_path = self._get_config_path()
        self.api_credentials = self._get_api_credentials()

    def _get_api_credentials(self):
        config_path = self.config_path
        configfile = self._get_config_file(config_path)
        with open(configfile, "r") as f:
            config_file = json.load(f)
        api_credentials = config_file.get("api_credentials")
        if not api_credentials:
            api_credentials = self._ask_user_for_api_credentials()
            self._save_api_credentials(configfile, api_credentials)
        return api_credentials

    @staticmethod
    def _save_api_credentials(configfile, api_credentials):
        with open(configfile, "w") as f:
            json.dump({"api_credentials": api_credentials}, f)

    @staticmethod
    def _ask_user_for_api_credentials():
        print('Please enter your API credentials:')
        api_credentials = input('API key: ')
        if not api_credentials:
            raise UserWarning('No API key provided')
        return api_credentials

    @staticmethod
    def _get_config_file(config_path):
        configfile = os.path.join(config_path, "config.json")
        if not os.path.exists(configfile):
            try:
                with open(configfile, "w") as f:
                    f.write("{}")
            except OSError as e:
                raise SystemError(
                    f"Could not create config file: {configfile} - {e}"
                )
        return configfile

    @staticmethod
    def _get_config_path():
        config_path = os.path.join(
            os.environ.get('APPDATA') or
            os.environ.get('XDG_CONFIG_HOME') or
            os.path.join(os.environ['HOME'], '.config'),
            "honk"
        )
        return get_or_create_directory(config_path)


class Api:
    """
    Api class
    """
    BASE_URL = 'https://honk.rafaelmc.net/api'

    def __init__(self, api_token, file_cache):
        self.api_token = api_token
        self.file_cache = file_cache
        self.headers = {'Authorization': f'Token {self.api_token}'}
        self.client = requests
        self.honks = {}

    def fetch_honks(self) -> None:
        """
        Fetch honks from the API and assign them to the honks dict.
        """

        response = self.client.get(
            f"{self.BASE_URL}/honks/", headers=self.headers
        )
        honks = response.json()

        if not honks:
            return

        for honk in honks:
            if honk['id'] not in self.honks:
                self.add_honk(honk)

    def add_honk(self, honk) -> None:
        """
        Add a honk to the honks dict
        """

        self.honks[honk['id']] = honk
        self.honks[honk['id']]['image_path'] = self.file_cache.download_images(
            honk_id=honk['id'],
            url=honk['clown_url']
        )
        print(f'New honk: {honk["id"]}\n')


class FileCache:
    """
    FileCache class
    """

    def __init__(self, config_singleton):
        self.config = config_singleton
        self.cache_path = self._get_cache_path()

    def _get_cache_path(self):
        cache_path = os.path.join(self.config.config_path, "cache")
        return get_or_create_directory(cache_path)

    def download_images(self, honk_id, url) -> os.path:
        """
        Download images from the API
        """

        if os.path.exists(os.path.join(self.cache_path, f'{honk_id}.gif')):
            return os.path.join(self.cache_path, f'{honk_id}.gif')

        response = requests.get(url)
        img_data = response.content
        with open(os.path.join(self.cache_path, f'{honk_id}.gif'), 'wb') as f:
            f.write(img_data)

        return os.path.join(self.cache_path, f'{honk_id}.gif')
