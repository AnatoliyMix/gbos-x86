#!/usr/bin/env python3
"""make_initramfs.py MODULES_ROOT OUT.cpio: stage0 initramfs (busybox + init + kernel modules)."""
import pathlib, sys
here = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(here.parent / 'lapis/qemu'))
from cpio_tree import pack
bb_candidates = [
    here.parent / 'kernel/out/busybox',
    pathlib.Path('/build/out/busybox'),
    pathlib.Path('/bin/busybox'),
    pathlib.Path('/usr/bin/busybox'),
]
busybox = None
for bb in bb_candidates:
    if bb.is_file():
        busybox = bb.read_bytes()
        break
if busybox is None:
    raise FileNotFoundError("busybox binary not found in any of: " + ", ".join(str(p) for p in bb_candidates))

init = (here / 'stage0_init.sh').read_bytes()
files = [(d, 0o40755, b'', 0, 0) for d in ('dev', 'proc', 'sys', 'bin', 'new', 'gbos')]
files += [('dev/console', 0o20600, b'', 5, 1), ('bin/busybox', 0o100755, busybox, 0, 0), ('init', 0o100755, init, 0, 0)]
open(sys.argv[2], 'wb').write(pack(sys.argv[1], extra=files))
