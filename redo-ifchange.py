#!/usr/bin/env python
import sys, os

import build_context
bc = build_context.init(os.environ, *sys.argv)

import vars, state, builder, jwack
from helpers import unlink
from log import debug, debug2, err

def should_build(t):
    f = state.File(name=t)
    if f.is_failed():
        raise builder.ImmediateReturn(32)
    dirty = f.is_dirty(max_changed=vars.RUNID)
    return dirty==[f] and state.DIRTY or dirty


rv = 202
try:
    if vars.TARGET and not vars.UNLOCKED:
        f = state.File(name=bc.target_name())
        debug2('TARGET: %r %r %r\n' % (vars.STARTDIR, vars.PWD, vars.TARGET))
    else:
        f = me = None
        debug2('redo-ifchange: not adding depends.\n')
    try:
        targets = sys.argv[1:]
        if f:
            for t in targets:
                f.add_dep('m', t)
            f.save()
        rv = builder.main(targets, should_build)
    finally:
        jwack.force_return_tokens()
except KeyboardInterrupt:
    sys.exit(200)
state.commit()
sys.exit(rv)
