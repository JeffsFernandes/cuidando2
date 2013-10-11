#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from .models import (
    BdJogador,
    )

CACHE = {}


def groupfinder(nome, request):
    grupos = []

    # jogador
    tempo = CACHE.get(nome)
    if not tempo or (time.time()-tempo) > 60:
        jog = request.db.query(BdJogador).filter_by(nome=nome).first()
        if jog:
            CACHE[nome] = time.time()
    else:
        jog = True
    if jog:
        grupos.append('g:jogador')

        # desafio
        if jog is True:
            jog = request.db.query(BdJogador).filter_by(nome=nome).first()
        tipo = request.matchdict.get('tipo')
        if tipo:
            tipos_destravados = jog.desafios_destravados.split(",")
            if tipo in tipos_destravados:
                grupos.append("g:desafio")

    request.jogador = jog

    try:
        if nome in ['a']:
            grupos.append("g:analise")
    except:
        pass

    return grupos
