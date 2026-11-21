#!/usr/bin/env python3
"""Download MFA models, prepare, validate, align, and preserve process logs."""
from pathlib import Path
import argparse, datetime, shutil, subprocess, sys
ROOT = Path(__file__).resolve().parents[1]
MODEL = 'english_us_arpa'

def run(cmd, log):
    print('\n> ' + ' '.join(map(str, cmd)), flush=True)
    with log.open('w', encoding='utf-8') as f:
        f.write('Command: ' + ' '.join(map(str, cmd)) + '\n\n'); f.flush()
        process = subprocess.Popen([str(x) for x in cmd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace', bufsize=1)
        for line in process.stdout:
            print(line, end='', flush=True); f.write(line); f.flush()
        code = process.wait()
    if code: raise RuntimeError(f'Command failed (exit {code}); see {log}')

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--jobs', type=int, default=1)
    ap.add_argument('--skip-download', action='store_true', help='Use models already in MFA cache')
    ap.add_argument('--mode', choices=['single','corpus'], default='single', help='single: low-memory per-file alignment; corpus: speaker-adapted multi-file alignment')
    a=ap.parse_args()
    if a.jobs < 1: ap.error('--jobs must be positive')
    mfa=shutil.which('mfa')
    if not mfa: raise RuntimeError('mfa not found; activate the conda environment first.')
    (ROOT/'logs').mkdir(exist_ok=True); (ROOT/'outputs'/'textgrids').mkdir(parents=True, exist_ok=True)
    run([sys.executable, ROOT/'scripts'/'prepare.py'], ROOT/'logs'/'prepare.log')
    run([mfa, 'version'], ROOT/'logs'/'version.log')
    if not a.skip_download:
        for typ in ('acoustic','dictionary'):
            run([mfa,'model','download',typ,MODEL], ROOT/'logs'/f'download_{typ}.log')
    corpus=ROOT/'data'/'corpus'; out=ROOT/'outputs'/'textgrids'
    run([mfa,'validate', corpus, MODEL, '--ignore_acoustics', '--output_directory', ROOT/'outputs'/'validation', '--clean','-j',str(a.jobs)], ROOT/'logs'/'validate.log')
    if a.mode == 'corpus':
        run([mfa,'align', corpus, MODEL, MODEL, out, '--clean','--overwrite','-j',str(a.jobs)], ROOT/'logs'/'align.log')
    else:
        for wav in sorted(corpus.rglob('*.wav')):
            target=out/wav.parent.name/(wav.stem+'.TextGrid')
            target.parent.mkdir(parents=True, exist_ok=True)
            run([mfa,'align_one',wav,wav.with_suffix('.lab'),MODEL,MODEL,target,'--clean','--overwrite'], ROOT/'logs'/('align_'+wav.stem+'.log'))
    expected = {p.stem.casefold() for p in corpus.rglob('*.wav')}
    grids = {p.stem.casefold() for p in out.rglob('*.TextGrid')}
    missing = expected - grids
    if missing: raise RuntimeError(f'No TextGrid for: {sorted(missing)}. Check logs and MFA validation reports.')
    print(f'\nSUCCESS: {len(expected)} expected TextGrids found in {out}. Inspect them in Praat; validation warnings can still matter.')
if __name__ == '__main__':
    try: main()
    except (OSError, RuntimeError) as e: print(f'\nERROR: {e}',file=sys.stderr); sys.exit(1)
