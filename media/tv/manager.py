#!  /usr/bin/env python
# -*- coding: utf-8 -*-
#   Title: manager.py
#   Package: Tv
#   Author: Romain Gigault
from media import media
from media.tv.model import TvModel

class TvManager(TvModel):
    """Called every time we need to access Tv Device"""

    def __init__(self):
        super(TvManager, self).__init__(host=media.config.get("TV_IP"))