# Assignment: forced alignment with Montreal Forced Aligner

This package is for the **forced-alignment portion (Assignment 2a)** in `data/original/Assignment 2a/Assignment_2a.pdf`; It prepares the six provided audio/transcript pairs, validates them, aligns them with Montreal Forced Aligner (MFA), and writes Praat-compatible TextGrids. 

## Quick start (Windows, Miniforge Prompt)

1. Extract the supplied project ZIP. In Miniforge Prompt, `cd /d "C:\path\to\MFA_Assignment"` (replace with your real folder).
2. Run:

```bat
conda env create -f environment.yml
conda activate mfa-assignment
python scripts\run_pipeline.py
python scripts\create_report.py
```

The initial environment and model downloads require internet. On subsequent runs, `python scripts\run_pipeline.py --skip-download` uses already downloaded models. This package includes results from a Linux run with MFA 3.4.3; the Windows instructions and environment have not been executed on a Windows machine.

## Project structure

- `data/original/Assignment 2a/`: the supplied recordings, transcripts and assignment PDF in this local package. `.gitignore` excludes the source dataset and prepared audio/transcripts from Git by default; publish them only if redistribution is permitted.
- `data/corpus/`: prepared WAV + `.lab` pairs, grouped by recording set for MFA.
- `data/manifest.csv`: original audio format, durations, and pairing summary.
- `scripts/prepare.py`: checks matching stems and writes RIFF PCM WAV and `.lab` files.
- `scripts/run_pipeline.py`: model download, preparation, validation, and alignment.
- `scripts/create_report.py`: regenerates the waveform/TextGrid plot and the report PDF from the current outputs.
- `scripts/build_assignment_report.py`: renders `REPORT.md` to `outputs/Assignment_2a_Alignment_Report.pdf`.
- `REPORT.md`: full draft report with actual run details, output summary, OOV observations, and manual-review caveats.
- `outputs/textgrids/`: six actual TextGrids, with word and phone tiers.
- `outputs/validation/`: MFA's OOV reports; important limitations are described in the guide.
- `outputs/sample_alignment.png`: programmatic waveform/TextGrid visualization.
- `outputs/praat_manual_inspection_sample.png`: Praat Editor screenshot supplied by the student.
- `REPORT.md` and `outputs/Assignment_2a_Alignment_Report.pdf`: report draft/source and generated PDF. The report records the student's observation that the six transcript sequences and file durations matched during Praat review; it does not claim a numerical boundary-accuracy score.
- `logs/`: run logs. Linux paths in included logs identify the original execution environment; rerunning replaces these logs.

## Reproducible commands

```bat
mfa model download acoustic english_us_arpa
mfa model download dictionary english_us_arpa
python scripts\prepare.py
mfa validate data\corpus english_us_arpa --ignore_acoustics --output_directory outputs\validation --clean -j 1
mfa align_one data\corpus\ISLE_SESS0131\ISLE_SESS0131_BLOCKD02_01_sprt1.wav data\corpus\ISLE_SESS0131\ISLE_SESS0131_BLOCKD02_01_sprt1.lab english_us_arpa english_us_arpa outputs\textgrids\ISLE_SESS0131\ISLE_SESS0131_BLOCKD02_01_sprt1.TextGrid --clean --overwrite
```

The pipeline invokes `align_one` for every pair. Optional corpus-level speaker-adapted alignment: `python scripts\run_pipeline.py --skip-download --mode corpus --jobs 1`. It may need more memory and generates a different alignment; do not mix the outputs without noting the method. The included outputs use `align_one`.

** warning:** the dictionary lacks `dukakis`, `wbur`, `melnicove`, `politicize`, and `maffy`, resulting in `<unk>` labels in two news TextGrids. 



## Source documentation

- MFA installation: https://montreal-forced-aligner.readthedocs.io/en/latest/installation.html
- MFA alignment: https://montreal-forced-aligner.readthedocs.io/en/stable/user_guide/workflows/alignment.html
- MFA validation: https://montreal-forced-aligner.readthedocs.io/en/v3.1.1/user_guide/data_validation.html
- Praat: https://www.praat.org/

