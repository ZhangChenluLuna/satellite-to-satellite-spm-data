"""Calculate validation metrics from stored predictions."""
from pathlib import Path
import csv,gzip,math,statistics,json
root=Path(__file__).resolve().parents[1]
def numeric(text):
 try:
  value=float(text);return value if math.isfinite(value) else None
 except (ValueError,TypeError):return None
def metrics(pairs):
 y=[math.log10(a) for a,b in pairs];p=[math.log10(b) for a,b in pairs]
 ym=statistics.mean(y);pm=statistics.mean(p)
 yy=sum((v-ym)**2 for v in y);pp=sum((v-pm)**2 for v in p)
 yp=sum((a-ym)*(b-pm) for a,b in zip(y,p))
 return dict(n=len(pairs),RMSD_log10=math.sqrt(statistics.mean((a-b)**2 for a,b in zip(y,p))),MdAPD_pct=statistics.median(100*abs(b-a)/a for a,b in pairs),multiplicative_bias=10**statistics.mean(b-a for a,b in zip(y,p)),slope_log10=yp/yy,R2_log_correlation=yp**2/yy/pp)
expected={'S2':(721,39.93327617645265),'L7':(427,56.27493858337402),'L8':(347,46.93808328537714),'L9':(117,49.21195109685261)}
for sensor,(n,mdapd) in expected.items():
 with gzip.open(root/f'data/dataset_iii/{sensor}_field_validation.csv.gz','rt',encoding='utf8') as f:rows=list(csv.DictReader(f))
 pairs=[]
 for r in rows:
  y=numeric(r['SS2']);p=numeric(r['pred_spm'])
  if y is not None and y>=1 and p is not None and p>0:pairs.append((y,p))
 result=metrics(pairs)
 assert result['n']==n
 assert abs(result['MdAPD_pct']-mdapd)<1e-8
 print(sensor,json.dumps(result))
with gzip.open(root/'data/dataset_i/field_olci_matchups.csv.gz','rt',encoding='utf8') as f:rows=list(csv.DictReader(f))
pairs=[(float(r['SPM']),float(r['mai'])) for r in rows]
result=metrics(pairs);assert result['n']==348
print('OLCI',json.dumps(result))
