#!/usr/bin/env python
import sys, os
import build_context

build_context.inside_do_script_guard()
bc = build_context.init(os.environ, *sys.argv)

from log import err

if len(sys.argv) < 3:
    err('%s: at least 2 arguments expected.\n' % sys.argv[0])
    sys.exit(1)

target, deps = sys.argv[1], sys.argv[2:]

if target in deps:
    err('%s: circular dependency.\n' % target)
    sys.exit(1)

# Build the known dependencies of our primary target.  This *does* require
# grabbing locks.
bc.set_no_oob()
argv = ['redo-ifchange'] + deps
rv = os.spawnvp(os.P_WAIT, argv[0], argv)
if rv:
    sys.exit(rv)

# We know our caller already owns the lock on target, so we don't have to
# acquire another one; tell redo-ifchange about that.  Also, REDO_NO_OOB
# persists from up above, because we don't want to do OOB now either.
# (Actually it's most important for the primary target, since it's the one
# who initiated the OOB in the first place.)
bc.set_unlocked()
argv = ['redo-ifchange', target]
sys.exit(os.spawnvp(os.P_WAIT, argv[0], argv))
