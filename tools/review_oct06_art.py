"""Actual-NBT before/after review with an oblique side-wall view of the tower."""
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import review_screenshot_revisions as review

review.WORK=ROOT/'.work/oct06-art-review'
review.OUTPUT=ROOT/'docs/project/reviews/ground-weathering-20261006.png'
review.TITLE='OCTOBER 6 / GROUND AND WEATHERING'
review.PAIRS=[('Small Colossus','colossus','small-colossus',('v6','v7'),
              'Surface-hugging moss / weathered plates / buried body retained'),
             ('Ruined Tower / side elevation','ruined-tower','ruined-tower',('v4','v5'),
              'Broken side walls / exposed courses / low meadow-soil foot'),
             ('World Tree / ground only','world-tree','world-tree',('v4','v4-1'),
              'Accepted V4 tree / narrow soil toes at root contact edges')]


def render():
    import review_relic_v2 as comparison
    for title,relic,stem,versions,note in review.PAIRS:
        if '--tree-only' in sys.argv and stem!='world-tree':continue
        comparison.WORK=review.WORK/stem
        comparison.PAIRS=[(title,relic,stem,note)]
        comparison.render(versions,yaw=68 if stem=='ruined-tower' else 22)


if __name__=='__main__':
    if '--render' in sys.argv:render()
    elif '--compose-only' in sys.argv:review.compose()
    else:
        subprocess.run([r'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe','--background','--threads','6',
                        '--python-exit-code','1','--python',str(Path(__file__).resolve()),'--','--render',
                        *(['--tree-only'] if '--tree-only' in sys.argv else [])],cwd=ROOT,check=True)
        review.compose()
