# -*- coding: utf-8 -*-

#
# Copyright (c) 2012 Virtual Cable S.L.
# All rights reservem.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.
#    * Neither the name of Virtual Cable S.L. nor the names of its contributors
#      may be used to endorse or promote products derived from this software
#      without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''
@author: Adolfo Gómez, dkmaster at dkmon dot com
'''

from django.utils.translation import ugettext_noop as _
from uds.core.managers.UserPrefsManager import CommonPrefs
from uds.core.util import OsDetector
from uds.core.util import tools
from .BaseSPICETransport import BaseSpiceTransport

import logging

logger = logging.getLogger(__name__)

READY_CACHE_TIMEOUT = 30


class SPICETransport(BaseSpiceTransport):
    '''
    Provides access via SPICE to service.
    This transport can use an domain. If username processed by authenticator contains '@', it will split it and left-@-part will be username, and right password
    '''
    typeName = _('SPICE Transport (direct)')
    typeType = 'SPICETransport'
    typeDescription = _('SPICE Transport for direct connection')

    useEmptyCreds = BaseSpiceTransport.useEmptyCreds
    fixedName = BaseSpiceTransport.fixedName
    fixedPassword = BaseSpiceTransport.fixedPassword
    serverCertificate = BaseSpiceTransport.serverCertificate

    def getUDSTransportScript(self, userService, transport, ip, os, user, password, request):
        # We use helper to keep this clean
        prefs = user.prefs('rdp')

        ci = self.getConnectionInfo(userService, user, password)
        username, password, domain = ci['username'], ci['password'], ci['domain']

        width, height = CommonPrefs.getWidthHeight(prefs)
        depth = CommonPrefs.getDepth(prefs)

#         r = SPICEFile(width == -1 or height == -1, width, height, depth, target=os['OS'])
#         r.address = '{}:{}'.format(ip, 3389)
#         r.username = username
#         r.password = password
#         r.domain = domain
#         r.redirectPrinters = self.allowPrinters.isTrue()
#         r.redirectSmartcards = self.allowSmartcards.isTrue()
#         r.redirectDrives = self.allowDrives.isTrue()
#         r.redirectSerials = self.allowSerials.isTrue()
#         r.showWallpaper = self.wallpaper.isTrue()
#         r.multimon = self.multimon.isTrue()
#
#         # data
#         data = {
#             'os': os['OS'],
#             'ip': ip,
#             'port': 3389,
#             'username': username,
#             'password': password,
#             'hasCredentials': username != '' and password != '',
#             'domain': domain,
#             'width': width,
#             'height': height,
#             'depth': depth,
#             'printers': self.allowPrinters.isTrue(),
#             'smartcards': self.allowSmartcards.isTrue(),
#             'drives': self.allowDrives.isTrue(),
#             'serials': self.allowSerials.isTrue(),
#             'compression': True,
#             'wallpaper': self.wallpaper.isTrue(),
#             'multimon': self.multimon.isTrue(),
#             'fullScreen': width == -1 or height == -1,
#             'this_server': request.build_absolute_uri('/'),
#             'r': r,
#         }
#
#         m = tools.DictAsObj(data)
#
#         if m.domain != '':
#             m.usernameWithDomain = '{}\\\\{}'.format(m.domain, m.username)
#         else:
#             m.usernameWithDomain = m.username
#
#         if m.os == OsDetector.Windows:
#             m.r.password = '{password}'
#
#         os = {
#             OsDetector.Windows: 'windows',
#             OsDetector.Linux: 'linux',
#             OsDetector.Macintosh: 'macosx'
#
#         }.get(m.os)
#
#         if os is None:
#             return super(SPICETransport, self).getUDSTransportScript(self, userService, transport, ip, os, user, password, request)
#
#         return self.getScript('scripts/{}/direct.py'.format(os)).format(m=m)
