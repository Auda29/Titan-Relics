"""Extract timestamped local reference frames/contact sheets for the Small Colossus V4 brief."""
import argparse
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import subprocess

from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[1]
FOLDER=ROOT/'.work/references/small-colossus-v4'
VIDEO=FOLDER/'Da-s0zqi7OQ.mp4'
URL='https://www.instagram.com/reel/Da-s0zqi7OQ/'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--times',type=float,nargs='+',default=list(range(0,112,6)))
    parser.add_argument('--label',default='overview')
    args=parser.parse_args();FOLDER.mkdir(parents=True,exist_ok=True)
    frames=[]
    for t in args.times:
        target=FOLDER/f'frame-{t:06.2f}.png'
        if not target.exists():
            subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-ss',str(t),'-i',str(VIDEO),
                            '-frames:v','1','-update','1',str(target)],check=True)
        frames.append({'time_seconds':t,'file':target.name,'sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
    cols=min(5,len(frames));cellw,cellh=306,585
    sheet=Image.new('RGB',(cols*cellw,((len(frames)+cols-1)//cols)*cellh),'#e9e4d8')
    draw=ImageDraw.Draw(sheet);font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf',22)
    for i,row in enumerate(frames):
        x,y=i%cols*cellw,i//cols*cellh
        image=Image.open(FOLDER/row['file']).convert('RGB');image.thumbnail((300,540),Image.Resampling.LANCZOS)
        sheet.paste(image,(x+(cellw-image.width)//2,y+36))
        draw.text((x+8,y+5),f"{row['time_seconds']:05.1f} s",fill='#293934',font=font)
    sheet.save(FOLDER/f'{args.label}-contact.png')
    path=FOLDER/'study-manifest.json'
    manifest=json.loads(path.read_text()) if path.exists() else {}
    manifest.update(source_url=URL,video_sha256=hashlib.sha256(VIDEO.read_bytes()).hexdigest(),
                    last_extraction_utc=datetime.now(timezone.utc).isoformat())
    manifest.setdefault('extractions',{})[args.label]=frames
    path.write_text(json.dumps(manifest,indent=2)+'\n')
    print(FOLDER/f'{args.label}-contact.png')


if __name__=='__main__':main()
