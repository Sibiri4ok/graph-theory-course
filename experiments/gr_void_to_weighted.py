#!/usr/bin/env python3
"""Convert Galois .gr (void/unweighted v1) to .gr with uint32 edge weight = 1."""
import struct
import sys


def convert(in_path, out_path, weight=1):
    with open(in_path, "rb") as f:
        ver, esz, nn, ne = struct.unpack("<4Q", f.read(32))
    if ver != 1:
        raise SystemExit(f"unsupported version {ver}")
    if esz != 0:
        raise SystemExit(f"expected void graph (edge size 0), got {esz}")

    with open(in_path, "rb") as f:
        raw = f.read()

    hdr = 32
    out_idx_bytes = (nn + 1) * 8
    dst_bytes = ne * 4
    if ne % 2:
        dst_bytes += 4
    expected = hdr + out_idx_bytes + dst_bytes
    if len(raw) < expected:
        # Galois v1 uses nn index entries in some builds
        out_idx_bytes = nn * 8
        expected = hdr + out_idx_bytes + dst_bytes
    if len(raw) < expected:
        raise SystemExit(f"file size mismatch: {len(raw)} vs expected ~{expected}")

    out_idx = raw[hdr : hdr + out_idx_bytes]
    dst_start = hdr + out_idx_bytes
    dst_end = dst_start + ne * 4
    dst = raw[dst_start:dst_end]
    weights = struct.pack(f"<{ne}I", *([weight] * ne))

    out_esz = 4
    header = struct.pack("<4Q", 1, out_esz, nn, ne)
    with open(out_path, "wb") as o:
        o.write(header)
        o.write(out_idx)
        o.write(dst)
        if ne % 2:
            o.write(b"\x00\x00\x00\x00")
        o.write(weights)

    print(f"{in_path} -> {out_path}: V={nn:,} E={ne:,} weight={weight}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} input.gr output-w.gr")
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2])
