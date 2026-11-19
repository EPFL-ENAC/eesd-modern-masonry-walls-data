"""Withdraw specimens from the dataset; their numbers stay retired.

Each Database row becomes a placeholder that holds only its N, so that the
next ingest does not give this N again. The curve files and the photos of
the specimen are deleted. All checks run before the first write.
"""

import argparse
import sys
from pathlib import Path

from enacit4r_contrib.ingest import IngestError, Plan, run

from mmw_data.validate import DATABASE_CSV, N, _parse

__all__ = ["IngestError", "main", "withdraw"]

CURVES = ("02_fd_curve", "03_envelope_Pavia", "04_envelope_EPFL")
CURVES += ("05_bilinear_curve_Pavia", "06_bilinear_curve_EPFL")
PHOTOS = ("07_fig_setup", "08_fig_failmode", "09_fig_materials", "10_fig_cracks")


def _files(data: Path, n: int) -> list[Path]:
    """Curves <prefix>_NNNN[_<suffix>].csv and photos fig_*_NNNN(.jpg|-512.webp|...)."""
    nnnn = f"{n:04d}"
    out = []
    for d in CURVES:
        out += (data / d).glob(f"*_{nnnn}.csv")
        out += (data / d).glob(f"*_{nnnn}_*.csv")
    for d in PHOTOS:
        out += (data / d).glob(f"fig_*_{nnnn}.*")
        out += (data / d).glob(f"fig_*_{nnnn}-*")
    return sorted(out)


def withdraw(numbers: list[int], data: Path) -> list[str]:
    """Retire each N in `data/`: placeholder row, files deleted."""
    db_path = data / DATABASE_CSV
    rows = _parse(db_path.read_bytes().decode("utf-8-sig"))[4:]
    by_n = {r[N].strip(): r for r in rows if r and r[N].strip()}
    for n in numbers:
        r = by_n.get(str(n))
        if r is None:
            raise IngestError(f"N={n} is not in the dataset")
        if not any(c.strip() for c in r[1:]):
            raise IngestError(f"N={n} is already withdrawn")
    plan = Plan()
    done = []
    for n in numbers:
        key = str(n)
        plan.rewrite_rows(
            db_path,
            lambda r, key=key: (
                [key] + [""] * (len(r) - 1) if r[N].strip() == key else r
            ),
            header_rows=4,
        )
        files = _files(data, n)
        for f in files:
            plan.delete(f)
        done.append(f"withdrew N={n} ({len(files)} files), the number stays retired")
    plan.apply()
    return done


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("numbers", nargs="+", type=int)
    ap.add_argument("--data", type=Path, default=Path(__file__).parents[2] / "data")
    a = ap.parse_args(argv)
    # run() takes one argument: give it the numbers as one text.
    joined = " ".join(map(str, a.numbers))
    return run(lambda t: withdraw([int(x) for x in str(t).split()], a.data), [joined])


if __name__ == "__main__":
    sys.exit(main())
