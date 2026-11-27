# Pick the best continuous window of LEN seconds from a clip: loud (music peaks) + visually lively, avoiding the very start/end.
import sys, subprocess, json, numpy as np, re
clip=sys.argv[1]; LEN=float(sys.argv[2]) if len(sys.argv)>2 else 40
dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',clip]).decode().strip())
if dur<=LEN+2: print(json.dumps({"start":0,"len":round(min(dur,LEN),2)})); sys.exit()
# loudness per 0.5s
a=subprocess.run(['ffmpeg','-v','error','-i',clip,'-ac','1','-ar','8000','-f','f32le','-'],capture_output=True).stdout
x=np.frombuffer(a,dtype=np.float32); step=4000
rms=np.array([np.sqrt(np.mean(x[i:i+step]**2)+1e-12) for i in range(0,len(x)-step,step)]); db=20*np.log10(rms)
# visual change per 0.5s via scene scores
out=subprocess.run(['ffmpeg','-i',clip,'-vf','fps=2,scale=160:-1,select=gte(scene\\,0),metadata=print','-an','-f','null','-'],capture_output=True,text=True).stderr
sc=np.array([float(v) for v in re.findall(r'lavfi.scene_score=([0-9.]+)',out)] or [0])
n=min(len(db),len(sc)) if len(sc)>1 else len(db)
db=db[:n]; sc=(sc[:n] if len(sc)>1 else np.zeros(n))
dbn=(db-np.median(db))/ (np.std(db)+1e-6); scn=np.clip(sc,0,0.4)/0.4
score=dbn+0.6*scn
W=int(LEN*2); margin=int(min(6,dur*0.08)*2)
best=None
for s in range(margin, n-W-margin+1):
    v=score[s:s+W].mean()-0.5*np.clip(-dbn[s:s+W],0,None).mean()
    if best is None or v>best[0]: best=(v,s)
start=best[1]/2 if best else 0
print(json.dumps({"start":round(start,2),"len":LEN,"duration":round(dur,2)}))
