# -*- coding: utf-8 
#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2

from webapp2_extras import sessions

confighandler = {}
confighandler['webapp2_extras.sessions'] = {
    'secret_key': 'ujkljlksdfu9890','cookie_name':'proxylogin'
}

class BaseHandler(webapp2.RequestHandler):

    def renderTemplate(self,template_name,template_vars):
        jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.abspath('.')))
        template = jinja_environment.get_template(template_name)
        self.response.out.write(template.render(template_vars))

    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session(backend='datastore')
