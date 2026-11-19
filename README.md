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
- A withdrawal removes tests from the dataset. Each row becomes a placeholder
  that holds only its N, and the curves and photos of the test are deleted.
  The withdrawn numbers stay retired: the ingest never gives them again.

## Tools

The tools are a Python package in `tools/` (`mmw_data`). You need
[uv](https://docs.astral.sh/uv/). Run the targets from the repository root.

| Target | What it does |
| --- | --- |
| `make install` | Installs the tools. |
| `make test` | Runs the tests. |
| `make lint` | Checks the style of the code with ruff. |
| `make check SUBMISSION=submissions/<id>` | Checks a submission. It shows each problem. It fails if there is an error. |
| `make ingest SUBMISSION=submissions/<id>` | Gives the next free N to each test of the submission, moves its files into `data/` and deletes the submission. |
| `make withdraw N="238 239"` | Withdraws the tests 238 and 239. |

An ingest or a withdrawal checks all the changes first. If one change fails,
it writes nothing.

## Workflows

| Workflow | Who starts it | What it does |
| --- | --- | --- |
| `ci.yml` | Each pull request and each push to `main` or `dev`. | Runs ruff and the tests. In a pull request, it checks each changed submission. |
| `ingest.yml` | The merge of a `contrib/*` pull request into `main` or `dev`. | Ingests the submissions of the pull request and pushes the result to the same branch. |
| `withdraw.yml` | A maintainer, by hand, on `main` or `dev`. The inputs are the numbers and the reason. | Withdraws the numbers and pushes one commit. The reason goes into the commit message. |
| `changed.yml` | A push to `main` or `dev`, or the ingest and withdraw workflows. | Only shows the branch and the commit for now. Later, it will start the deploy of the site. |
| `reset-dev.yml` | A maintainer, by hand. The maintainer must type `reset`. | Resets `dev` to `main`. |

An ingest and a withdrawal on the same branch never run at the same time.

## License

EESD has not chosen the license of the data yet. Until then, cite the
publication that is listed for each test
([#35](https://github.com/EPFL-ENAC/eesd-modern-masonry-walls-db/issues/35)).
