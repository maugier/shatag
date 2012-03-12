#!/usr/bin/env python3
# Copyright 2011 Maxime Augier
# Distributed under the terms of the GNU General Public License

import http.client
import shatag.base

class Store(shatag.base.IStore):
    def __init__(self,url):
        super().__init__(url, name)


    def fetch(self,hash):
    	pass
