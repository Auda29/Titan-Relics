# Beta 3 publication record

Beta 3 was published on 10 November 2026 at 13:01:09 UTC as
[GitHub Latest](https://github.com/Auda29/Titan-Relics/releases/tag/v1.0.0-beta.3).
The tag is fixed at `5bd9011902b1c123e561dc5e3b356c828be9fdf4`.
The release comes from the PR #2 branch, not a merge to main. The author explicitly
requested another beta playtest despite the documented acceptance findings.

The [release workflow](https://github.com/Auda29/Titan-Relics/actions/runs/42814577854)
completed successfully, including all eight target builds, required tests, GitHub
publication, and both platform upload jobs. The CurseForge job finished at
13:04:11 UTC. GitHub uses its normal release flag for the Latest badge; this is
still a testing beta and both mod platforms classify the files as Beta.

## Download verification

All eight player JARs, SHA256SUMS.txt and platform-upload-state.json were downloaded
from that existing release after publication. Each local JAR matches its listed
SHA-256, and the receipt binds the same tag, project IDs and all eight hashes.
Every platform entry is `verified`: eight Modrinth and eight CurseForge entries.
That phase means the CI uploader successfully downloaded and hash-checked the
known platform file, not merely that an upload POST was accepted.

The receipt SHA-256 is `b5c7f41475fbb9fbebb84690b5467aa481810aa7ccaeae7f26d563d4441b9e6c`.
Local verification files are under `dist/public-beta-3/` and remain untracked.

| GitHub filename | SHA-256 | Modrinth version | CurseForge file |
| --- | --- | --- | --- |
| `relics-1.0.0-beta.3+mc1.21.1-neoforge.jar` | `ee9e9e94361568e9964f49c5a40d2388dfe2666430cea516e69aa4e1b62df15c` | [qKkIg9gt](https://modrinth.com/mod/titan-relics/version/qKkIg9gt) | [9541130](https://www.curseforge.com/minecraft/mc-mods/titan-relics/files/9541130) |
| `relics-1.0.0-beta.3+mc1.21.1.jar` | `f7ca55d1a2ab2e472e4c98672dbba7403ca8f06d98f1d15d9714069d2dcb7398` | [yz8LAorG](https://modrinth.com/mod/titan-relics/version/yz8LAorG) | [9541129](https://www.curseforge.com/minecraft/mc-mods/titan-relics/files/9541129) |
| `relics-1.0.0-beta.3+mc1.21.11-neoforge.jar` | `942b18c22a3851b6155cc76db6c0bd805419812c231e98224f92ddda7543d591` | [wVn0KyuT](https://modrinth.com/mod/titan-relics/version/wVn0KyuT) | [9541137](https://www.curseforge.com/minecraft/mc-mods/titan-relics/files/9541137) |
| `relics-1.0.0-beta.3+mc1.21.11.jar` | `fc53a28c8c27eeaadd89c05aeeda3216326ca6389b24f7c09717f3c63abd4148` | [p4Xn284d](https://modrinth.com/mod/titan-relics/version/p4Xn284d) | [9541134](https://www.curseforge.com/minecraft/mc-mods/titan-relics/files/9541134) |
| `relics-1.0.0-beta.3+mc26.2-neoforge.jar` | `45725119ce20a3704ea3972e5b17733278e3b842bc5c129d763f840e68fd2298` | [KoNT7jOB](https://modrinth.com/mod/titan-relics/version/KoNT7jOB) | [9541133](https://www.curseforge.com/minecraft/mc-mods/titan-relics/files/9541133) |
| `relics-1.0.0-beta.3+mc26.2.jar` | `c5d3cf6618aeba5460caf0162f7a9e65809a122b08767eb921910c9b5ccb529c` | [rP44IG6Z](https://modrinth.com/mod/titan-relics/version/rP44IG6Z) | [9541125](https://www.curseforge.com/minecraft/mc-mods/titan-relics/files/9541125) |
| `relics-1.0.0-beta.3+mc26.3-neoforge.jar` | `9418f75ae03820fbf37966c03a3a1976efdd0ef5768b300396ee35d65778843f` | [catIZWyC](https://modrinth.com/mod/titan-relics/version/catIZWyC) | [9541141](https://www.curseforge.com/minecraft/mc-mods/titan-relics/files/9541141) |
| `relics-1.0.0-beta.3+mc26.3.jar` | `13f7504a541042d34ee593f27f397eaf5251e946595988dc23fb6dc72d60d11c` | [F2cOkEwX](https://modrinth.com/mod/titan-relics/version/F2cOkEwX) | [9541140](https://www.curseforge.com/minecraft/mc-mods/titan-relics/files/9541140) |

## Project approval and remaining testing

A separate authenticated read still returned Modrinth project status `processing`,
no approval timestamp and no moderator message. Verified version downloads do not
establish project moderation approval. No visibility, moderation setting or AI
content disclosure was changed. The CurseForge dashboard was not re-audited.
No files were re-uploaded and no existing release or tag was replaced.

PR #2 remains a draft. Its Sword Skull ground-contact findings, exact gameplay
marker normalization, second native density seed and redesigned-menu visual
acceptance are not marked as passed by successful release CI. See the
[Beta 3 release notes](1.0.0-beta.3.md). For distribution testing, create a new
world and explicitly select a new preset; existing worlds retain their rules.
