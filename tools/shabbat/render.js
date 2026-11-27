const p=require('puppeteer-core');const {spawn}=require('child_process');const fs=require('fs');
const T=+process.argv[2]||12,FPS=30,OUT=process.argv[3]||'video.mp4';
(async()=>{const b=await p.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox','--allow-file-access-from-files']});
const pg=await b.newPage();await pg.setViewport({width:1080,height:1920});await pg.goto('file://'+__dirname+'/frame.html');await pg.evaluate(()=>document.fonts.ready);await new Promise(r=>setTimeout(r,400));
const tmp=OUT.replace(/\.mp4$/,'.tmp.mp4');
const ff=spawn('ffmpeg',['-y','-v','error','-f','image2pipe','-framerate',String(FPS),'-c:v','mjpeg','-i','-','-c:v','libx264','-crf','18','-preset','veryfast','-pix_fmt','yuv420p','-r',String(FPS),tmp]);
for(let f=0;f<Math.round(T*FPS);f++){await pg.evaluate(t=>render(t),f/FPS);const buf=await pg.screenshot({type:'jpeg',quality:92});if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));}
ff.stdin.end();const code=await new Promise(r=>ff.on('close',r));if(code===0)fs.renameSync(tmp,OUT);console.log('render',code);await b.close();})();
