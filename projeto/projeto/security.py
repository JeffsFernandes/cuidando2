#!/usr/bin/env python
# -*- coding: utf-8 -*-


def groupfinder(identificador, request):
    grupos = []

    cid = request.db['cidadaos'].get(identificador)
    request.cidadao = cid
    if cid:
        grupos.append('g:cidadao')

    return grupos
