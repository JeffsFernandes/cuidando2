#!/usr/bin/env python
# -*- coding: utf-8 -*-


def groupfinder(identificador, request):
    grupos = []

    cid = request.db['usrTree'].get(identificador)
    request.cidadao = cid
    if cid is not None:
        grupos.append('g:cidadao')
    else:
        cid = request.db['twtTree'].get(identificador)
        request.cidadao = cid	
        if cid is not None:
            grupos.append('g:cidadao')
    return grupos
