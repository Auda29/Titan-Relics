"""Compare the art visible in Alpha 4.2 screenshots with the next visual candidates."""
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import review_screenshot_revisions as review

review.WORK=ROOT/'.work/alpha42-art-review'
review.OUTPUT=ROOT/'docs/project/reviews/alpha42-art-followup-20261005.png'
review.TITLE='ALPHA 4.2 SCREENSHOTS / ART FOLLOW-UP'
review.PAIRS=[('World Tree','world-tree','world-tree',('v3','v4'),
              'Spreading forks / open foliage fans / lower root deposits'),
             ('Small Colossus','colossus','small-colossus',('v5','v6'),
              'Overlapping forged plates / settled upper body / darker pincers'),
             ('Ruined Tower','ruined-tower','ruined-tower',('v3','v4'),
              'Staggered skyline fractures / broken lower flight / masonry relief')]


if __name__=='__main__':
    if '--render' in sys.argv:review.render()
    elif '--compose-only' in sys.argv:review.compose()
    else:
        subprocess.run([r'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe','--background','--threads','8',
                        '--python-exit-code','1','--python',str(Path(__file__).resolve()),'--','--render'],cwd=ROOT,check=True)
        review.compose()
