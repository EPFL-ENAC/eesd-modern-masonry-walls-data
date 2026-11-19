import pytest
from enacit4r_contrib.ingest import next_number

from mmw_data.ingest import ingest
from mmw_data.validate import DATABASE_CSV, N_ID, N, _parse, check_submission
from mmw_data.withdraw import IngestError, main, withdraw
from tests.test_ingest import _max_n, _tree, _write
from tests.test_validate import DATASET, NAME, _with

PHOTOS = ("07_fig_setup/fig_setup", "10_fig_cracks/fig_cracks")


def _lines(data) -> list[bytes]:
    return (data / DATABASE_CSV).read_bytes().splitlines(keepends=True)


def _add_photos(data, *numbers: int) -> None:
    for n in numbers:
        for p in PHOTOS:
            for tail in (".jpg", "-512.webp", "-1920.webp"):
                f = data / f"{p}_{n:04d}{tail}"
                f.parent.mkdir(exist_ok=True)
                f.write_bytes(b"photo")


def _files(data, n: int) -> list[str]:
    return sorted(p.name for p in data.rglob(f"*_{n:04d}[._-]*"))


def _check(data, numbers: list[int]) -> None:
    before = _lines(data)
    assert all(_files(data, n) for n in numbers)
    gone = tuple(f"_{n:04d}" for n in numbers)
    keep = {p: h for p, h in _tree(data).items() if not any(g in p for g in gone)}
    out = withdraw(numbers, data)
    assert len(out) == len(numbers)
    after = _lines(data)
    assert len(after) == len(before)
    for i, (b, a) in enumerate(zip(before, after)):
        n = b.split(b",")[0].decode()
        if i >= 4 and n.isdigit() and int(n) in numbers:
            width = len(_parse(b.decode())[0])
            assert a == (n + "," * (width - 1) + "\n").encode()
        else:
            assert a == b  # every other line keeps its bytes
    for n in numbers:
        assert _files(data, n) == []
    tree = _tree(data)
    del tree[DATABASE_CSV]
    del keep[DATABASE_CSV]
    assert tree == keep


def test_withdraw_one(data):
    _add_photos(data, 226, 227)
    _check(data, [227])
    assert _files(data, 226)


def test_withdraw_two(data):
    _add_photos(data, 226, 227)
    _check(data, [226, 227])


@pytest.mark.parametrize("numbers", [[999], [227, 999], [237]])
def test_unknown_or_placeholder_writes_nothing(data, numbers):
    _add_photos(data, 227)
    before = _tree(data)
    with pytest.raises(IngestError):
        withdraw(numbers, data)
    assert _tree(data) == before


def test_placeholder_is_ignored_and_retired(tmp_path, data):
    withdraw([227], data)
    db = (data / DATABASE_CSV).read_bytes()
    row = next(r for r in _parse(db.decode("utf-8-sig"))[4:] if r[N] == "227")
    assert row[N_ID] == "" and not any(row[1:])
    # SW0.1 is gone: a new submission of it is no longer a duplicate.
    sw01 = _with("Specimen name", "SW0.1")
    assert any("as N=227" in i.message for i in check_submission(sw01, DATASET))
    again = check_submission(sw01, db)
    assert not any("already in the database" in i.message for i in again)
    rows = _parse(db.decode("utf-8-sig"))[4:]
    assert next_number(r[j] for r in rows for j in (N, N_ID) if j < len(r)) > 227
    n = _max_n(data) + 1
    assert ingest(_write(tmp_path), data) == [(NAME, n)]
    withdraw([n], data)
    assert ingest(_write(tmp_path, NAME + "2"), data) == [(NAME + "2", n + 1)]


def test_cli(data, capsys):
    assert main(["227", "--data", str(data)]) == 0
    assert "withdrew N=227" in capsys.readouterr().out
    assert main(["227", "--data", str(data)]) == 1
    assert "already withdrawn" in capsys.readouterr().out
