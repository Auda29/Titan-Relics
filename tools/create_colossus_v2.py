"""Generate Colossus v2, the original reference study before the buried hip."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from create_colossus_v3 import main


if __name__ == "__main__":
    main(version=2)
