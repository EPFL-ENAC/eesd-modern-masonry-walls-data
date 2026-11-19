# EESD Modern Masonry Walls data

This repository holds the dataset of the Modern Masonry Database: in-plane
shear-compression tests on modern unreinforced masonry walls, collected by
EPFL's Earthquake Engineering and Structural Dynamics lab (EESD).
[eesd-modern-masonry-walls-db](https://github.com/EPFL-ENAC/eesd-modern-masonry-walls-db)
is the site that shows it. The data has its own repository for two reasons.
A data release does not need a code release. Tests on the dev site never
touch the real data
([#62](https://github.com/EPFL-ENAC/eesd-modern-masonry-walls-db/issues/62)).

## Layout

| Path | Content |
| --- | --- |
| `data/ModernMasonryDatabase_EIA_Database.csv` | One row per test. The 4 header rows give the column number, the category, the number in the category and the name. |
| `data/ModernMasonryDatabase_EIA_Fields.csv` | The definition and the unit of each column. |
| `data/01_references/` | The references, as CSV and BibTeX. |
| `data/02_fd_curve/` … `data/06_bilinear_curve_EPFL/` | The curves of each test, named after its number N. |
| `data/07_fig_setup/` … `data/10_fig_cracks/` | The photos, as git-lfs objects. |
| `submissions/` | Contributions that wait for their ingest. |

The CSV files are UTF-8 with a BOM, so that Excel on Windows shows σ, δ and μ.

## Branches

- `main` holds the real data. The prod site shows it.
- `dev` holds the test data that the dev site shows. After the tests, a
  maintainer resets it to `main`.

## Get the data

The photos are on the ENAC-IT git-lfs server (`.lfsconfig`). From outside the
EPFL network, you need its credentials.

```bash
git config --global http.https://enac-it-git-lfs.epfl.ch/.version HTTP/1.1
git clone git@github.com:EPFL-ENAC/eesd-modern-masonry-walls-data.git
```

## Change the data

- New tests come from the Submit page of the site. Each one opens a pull
  request that adds `submissions/<id>/`. When a curator merges it, the ingest
  gives the next free N to each new test and moves its files into `data/`.
- A correction is a pull request that edits the files in `data/`. A test keeps
  its N forever, and the number of a removed test is not used again.

## License

EESD has not chosen the license of the data yet. Until then, cite the
publication that is listed for each test
([#35](https://github.com/EPFL-ENAC/eesd-modern-masonry-walls-db/issues/35)).
