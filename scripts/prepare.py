#!/usr/bin/env python3
"""Pair the provided audio/transcripts without changing their spoken wording."""
from pathlib import Path
import csv, re, sys
import soundfile as sf
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'data' / 'original' / 'Assignment 2a'
CORPUS = ROOT / 'data' / 'corpus'

def files_by_stem(folder, ext):
    result = {}
    for p in folder.iterdir():
        if p.is_file() and p.suffix.lower() == ext:
            k = p.stem.casefold()
            if k in result: raise ValueError(f'Duplicate stem: {p.stem}')
            result[k] = p
    return result

def main():
    if not SOURCE.exists(): raise FileNotFoundError(f'Missing provided dataset: {SOURCE}')
    audio = files_by_stem(SOURCE / 'wav', '.wav')
    text = files_by_stem(SOURCE / 'transcripts', '.txt')
    if set(audio) != set(text):
        raise ValueError(f'Unmatched audio: {sorted(audio.keys()-text.keys())}; unmatched transcripts: {sorted(text.keys()-audio.keys())}')
    if not audio: raise ValueError('No pairs found')
    rows = []
    for key, wav in sorted(audio.items()):
        transcript = text[key].read_text(encoding='utf-8-sig').strip()
        if not transcript: raise ValueError(f'Empty transcript: {text[key]}')
        # Merge line breaks only. MFA itself handles case and punctuation.
        transcript = re.sub(r'\s+', ' ', transcript)
        # Two sets clearly correspond to distinct recordings; never pool them as a single speaker.
        speaker = 'F2BJRLP' if wav.stem.startswith('F2BJRLP') else 'ISLE_SESS0131'
        out = CORPUS / speaker
        out.mkdir(parents=True, exist_ok=True)
        # Three files have a WAV extension but contain NIST Sphere audio.
        # Decode and losslessly write 16-bit PCM RIFF WAV for MFA/Praat.
        samples, rate = sf.read(str(wav), dtype='int16', always_2d=True)
        sf.write(str(out / wav.name), samples, rate, format='WAV', subtype='PCM_16')
        (out / (wav.stem + '.lab')).write_text(transcript + '\n', encoding='utf-8')
        info = sf.info(str(wav))
        rows.append([speaker, wav.name, text[key].name, info.channels, info.samplerate, round(info.duration,3), info.format, info.subtype])
    with (ROOT/'data'/'manifest.csv').open('w', encoding='utf-8', newline='') as f:
        writer=csv.writer(f); writer.writerow(['speaker_group','audio','original_transcript','channels','sample_rate_hz','duration_seconds','original_container','original_encoding']); writer.writerows(rows)
    print(f'Prepared {len(rows)} pairs in {CORPUS}. Manifest: data/manifest.csv')
    print('Review transcripts against audio, especially abbreviations and hyphens; original wording was not silently rewritten.')
if __name__ == '__main__':
    try: main()
    except Exception as e: print(f'ERROR: {e}', file=sys.stderr); sys.exit(1)
