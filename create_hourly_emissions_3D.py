#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 16:15:43 2020

@author: bruine
"""

from ruisdael_functions import reademisoptions, writereademission_3d

# === Read options ====================================================================       
domainbounds, tstart, tend, tracers, sources, categos = reademisoptions("emisoptions_large_domain.txt", show_log=True)


# === Read/write emissions ============================================================
writereademission_3d(domainbounds, tstart, tend, tracers, sources, categos, show_log=True)
