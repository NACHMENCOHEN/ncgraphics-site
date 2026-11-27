import numpy as np, soundfile as sf, sys
T=float(sys.argv[1]);sr=48000;n=int(T*sr);t=np.arange(n)/sr
note=lambda f:440*2**((f-69)/12)
ch=[[60,64,67,72],[57,60,64,69],[53,57,60,65],[55,59,62,67]]  # C Am F G
bar=T/4;m=np.zeros(n)
for i,c in enumerate(ch):
    s0=i*bar;sg=(t>=s0)&(t<s0+bar+1.2);x=t[sg]-s0
    env=np.minimum(1,x/0.9)*np.exp(-np.maximum(0,x-bar)/0.7)
    for f in c:
        fr=note(f);m[sg]+=(np.sin(2*np.pi*fr*x)+.25*np.sin(2*np.pi*fr*2.002*x))*env*.05
    for j in range(6):
        bs=s0+j*bar/6;sg2=(t>=bs)&(t<bs+1.2);x2=t[sg2]-bs;f=note([c[0]+12,c[1]+12,c[2]+12,c[3]+12,c[2]+12,c[1]+12][j])
        m[sg2]+=np.sin(2*np.pi*f*x2)*np.exp(-x2*3.5)*.05+np.sin(2*np.pi*f*2*x2)*np.exp(-x2*6)*.015
m=np.convolve(m,np.ones(5)/5,'same');m=m/np.max(np.abs(m))*.5*np.minimum(1,t/1)*np.minimum(1,(T-t)/1.5)
sf.write('music.wav',np.stack([m,m],1),sr)
