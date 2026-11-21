# Windows user guide: MFA assignment

## 1. What this project does

The assignment asks for word- and phoneme-level forced alignment of the **provided audio and transcripts only**, a reproducible setup, TextGrid outputs, and a short report. This package contains the dataset, code, six preliminary outputs, validation results and a draft report


## 2. Install prerequisites

1. Download the **Windows x86-64** Miniforge installer from https://github.com/conda-forge/miniforge and install it. Use **Miniforge Prompt** from the Start menu for all commands below
2. Download and install Praat for Windows from https://www.praat.org/.
3. Extract the project ZIP into a writable, short path such as `C:\MFA_Assignment`. Windows can extract this project ZIP
4. Keep internet enabled for first-time setup. Allow several GB of free disk space for Conda, models and temporary files. Actual download size can vary.

In Miniforge Prompt, change to the actual project folder. Replace the example path if necessary:

```bat
cd /d C:\MFA_Assignment
conda env create -f environment.yml
conda activate mfa-assignment
mfa version
```

The environment pins MFA 3.4.3 but does not pin every transitive dependency or downloaded model revision. Downloads may change upstream, so exact bit-for-bit reproduction is not guaranteed. The included run was executed on Linux; the Windows package solve was checked, but Windows runtime was not tested. If environment creation reports that it already exists, activate the existing environment or rename it in `environment.yml` before creating a fresh one.

## 3. Run the automated pipeline

With the environment activated and the current directory set to the project root:

```bat
python scripts\run_pipeline.py
```

It will prepare the six pairs, download the `english_us_arpa` acoustic model and compatible dictionary, validate text and pairings, then align each recording individually. It stops on a failed command and records logs in `logs`. `mfa validate --ignore_acoustics` checks corpus and dictionary coverage but **does not** evaluate acoustic features or test alignments. The alignment step itself processes the audio. Completion checks that six expected TextGrid filenames exist; this is not an accuracy check.

For repeat runs after models are already available:

```bat
python scripts\run_pipeline.py --skip-download
python scripts\create_report.py
```

The second command recreates the sample plot and PDF draft. The per-file default is low-memory and does not perform corpus-level speaker adaptation. Optionally try `python scripts\run_pipeline.py --skip-download --mode corpus --jobs 1` for corpus alignment with the acoustic model's default speaker adaptation; this can use substantially more memory. 


## 4. Find and inspect the results in Praat

1. Find a matching audio/TextGrid pair. For example:
   - `data\corpus\ISLE_SESS0131\ISLE_SESS0131_BLOCKD02_01_sprt1.wav`
   - `outputs\textgrids\ISLE_SESS0131\ISLE_SESS0131_BLOCKD02_01_sprt1.TextGrid`
2. Open Praat. In the Objects window, use **Open > Read from file...** to load the WAV and the TextGrid. Select both objects together (Ctrl-click), then choose **View & Edit**. Interface wording can vary by Praat version.
3. Zoom into a few words. Play the audio, compare the word intervals and phone intervals with the waveform and spectrogram, and note any questionable boundaries, skipped sounds, unexpected silence or transcript mismatches. Do not assume model boundaries are ground truth.
4. Repeat on the longer news recordings and check the OOV locations. Take a Praat screenshot for your report .

In the included sample `I SAID WHITE NOT BAIT`, the predicted word interval for `white` is 0.92–1.49 seconds and the recording duration is 4.125 seconds. `outputs\sample_alignment.png` is generated from the actual TextGrid and WAV; the separate `outputs\praat_manual_inspection_sample.png’ Praat screenshot.

## 5. Known issues and what to investigate

- The OOV frequency file `outputs\validation\oov_counts_english_us_arpa.txt` lists five missing types: `dukakis` (2 occurrences), `wbur`, `melnicove`, `politicize` and `maffy` (1 each). The validation log in MFA 3.4.3 also reports larger character-like totals; rely on the word frequency file for the above word list and investigate the OOV reporting discrepancy if needed. In the generated grids unknown words appear as `<unk>`; their alignment and phone labels are not reliable.
- The transcript `S.J.C.'s` is tokenized into separate pieces in the first news TextGrid. Hyphenated words are also split by normalization. Check actual pronunciation in the recordings before changing text or a dictionary. Do not silently replace names or words just to eliminate warnings.
- MFA 3.4.3 corpus-wide collection was killed in the sandbox, even with one job; per-file alignment succeeded. On a memory-constrained computer, use the default mode and close other applications. For missing `mfa`, check `conda activate mfa-assignment`; ## 6. Complete the submission

1. Review `REPORT.md` and `outputs\Assignment_2a_Alignment_Report.pdf`. Regenerate the sample plot and PDF from the current TextGrids with `python scripts\create_report.py`. The current draft includes the student's reported Praat observations and supplied screenshot; revise it if your own inspection differs or if you add dictionary pronunciations.

