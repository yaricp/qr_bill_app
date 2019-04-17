# -*- coding: utf-8 -*-
import os
REQUEST_KWARGS={
    'proxy_url': 'socks5://80.211.38.123:1080',
    # Optional, if you need authentication:
    'urllib3_proxy_kwargs': {
        'username': 'user123321',
        'password': '123qweasdzxc',
    }
}

allowed_users = ['yaricp','yaricp_dev']
development = int(os.getenv('DEVEL', 1))

if development:
    from config.development import *
else:
    from config.production import *
