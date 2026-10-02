"""Compare the warm V4.2 NBT and its actual missing chunks against V4.1."""
from pathlib import Path
import json

from review_v4_1 import sheet

ROOT=Path(__file__).resolve().parents[1]


def main():
    base=ROOT/"relics/obelisk/design/generated"
    out=base/"obelisk-v4-2"
    metadata=json.loads((out/"obelisk-v4-2.design.json").read_text())
    removed=metadata["obelisk_v4"]["volume_removed_percent"]
    sheet("OBELISK V4.2 / WARM OCHRE & MISSING STONE",
          "Consistent ochre/clay facets / same stone on cut faces / genuine missing pieces",
          [(base/"obelisk-v4-1/02-blocks-front.png","V4.1 / Pale stone and dark crack lining","Previous version, retained for comparison"),
           (out/"02-blocks-front.png","V4.2 / Warm ochre and clay","Recesses read through missing geometry and shadows"),
           (out/"11-missing-chunk-1.png","V4.2 / Missing edge piece","Actual NBT crop: open notch, no contrasting repair material"),
           (out/"10-crack-1.png","V4.2 / Unpainted crack","Same side material continues into the recessed stone")],
          f"Two extra edge chunks removed; {removed:.3f}% total source volume loss. Monolith remains solid and upright.",
          out/"obelisk-v4-2-changes-review.png")


if __name__=="__main__": main()
