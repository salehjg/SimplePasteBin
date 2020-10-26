import requests


class SimplePasteBin:
    def __init__(self, username, password, api_key, is_verbose=True):
        self.username = username
        self.password = password
        self.key_api = api_key
        self.key_user = ''
        self.is_verbose = is_verbose

    def login(self):
        response = self.__send_a_post_req(
            'https://pastebin.com/api/api_login.php',
            {
                'api_dev_key': self.key_api,
                'api_user_name': self.username,
                'api_user_password': self.password,

            }
        )

        if response.reason == 'OK' and response.text.find('Bad') == -1:
            self.key_user = response.text
        else:
            if self.is_verbose:
                print("Failed to login and acquire a user key.")
            if self.is_verbose:
                print("Response: ", response.reason, ", Text: ", response.text)
            return 1
        return 0

    def create_paste(self, title, content, expire_in='N', permission='private'):
        assert permission == 'public' or permission == 'private' or permission == 'unlisted'
        assert expire_in == 'N' or \
               expire_in == '10M' or \
               expire_in == '1H' or \
               expire_in == '1D' or \
               expire_in == '1W' or \
               expire_in == '2W' or \
               expire_in == '1M' or \
               expire_in == '6M' or \
               expire_in == '1Y'
        assert title != ''
        assert content != ''

        if self.key_user == '':
            if self.is_verbose:
                print('Error: Have not logged in yet.')
            return 2

        if permission == 'public':
            api_paste_private = '0'
        else:
            if permission  == 'unlisted':
                api_paste_private = '1'
            else:
                api_paste_private = '2'

        response = self.__send_a_post_req(
            'https://pastebin.com/api/api_post.php',
            {
                'api_option': 'paste',
                'api_dev_key': self.key_api,
                'api_user_key': self.key_user,
                'api_paste_private': api_paste_private,
                'api_paste_name': title,
                'api_paste_expire_date': expire_in,
                # 'api_paste_format': api_paste_format,
                'api_paste_code': content,

            }
        )

        if response.reason == 'OK' and response.text.find('Bad') == -1:
            if self.is_verbose:
                print("The paste has been created.")
            return 0
        else:
            if self.is_verbose:
                print("Failed to post the log file.")
                print("Response: ", response.reason, ", Text: ", response.text)
            return 3

    def __send_a_post_req(self, url, dict_fields):
        return requests.post(url, data=dict_fields)
