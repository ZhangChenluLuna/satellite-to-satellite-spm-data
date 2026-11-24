from pathlib import Path
import csv, hashlib, sys
root=Path(__file__).resolve().parents[1]
bad=[];count=0
with (root/'checksums.csv').open(encoding='utf-8-sig',newline='') as stream:
 for row in csv.DictReader(stream):
  p=root/row['file'];h=hashlib.sha256()
  if not p.exists():bad.append(row['file']);continue
  with p.open('rb') as f:
   for b in iter(lambda:f.read(1048576),b''):h.update(b)
  if h.hexdigest()!=row['sha256']:bad.append(row['file'])
  count+=1
print('Checked',count,'files. Mismatches:',len(bad))
for name in bad:print(name)
sys.exit(bool(bad))
