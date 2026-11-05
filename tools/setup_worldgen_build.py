"""Explicit portable compilation-cache setup; does not launch Minecraft or edit profiles."""
import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen
import zipfile

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "build/worldgen-dependencies"
LITHOSTITCHED_SHA256 = "4d74a8ec2023657352ae051f1a6270bff474bf3cc46013100eff5f9ddbbdd024"
FABRIC_API_SHA256 = "e5b858ceb13290c274e31cb888ff5a1a40cb91067e7ffab0b5b775aec51e216a"


def fetch(url):
    request = Request(url, headers={"User-Agent": "Relic-Mod-build/0.1.0 (https://github.com/Auda29/Titan-Relics)"})
    with urlopen(request, timeout=120) as response:
        return response.read()


def checked_download(url, path, algorithm, expected):
    if path.is_file() and hashlib.new(algorithm, path.read_bytes()).hexdigest() == expected:
        return
    data = fetch(url)
    if hashlib.new(algorithm, data).hexdigest() != expected:
        raise ValueError(f"Download checksum mismatch: {url}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--accept-downloads", action="store_true", help="Download official Minecraft/Fabric and pinned Lithostitched compile dependencies")
    args = parser.parse_args()
    if not args.accept_downloads:
        parser.error("Pass --accept-downloads to prepare the isolated build dependency cache")
    manifest = json.loads(fetch("https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"))
    version = next(v for v in manifest["versions"] if v["id"] == "26.2")
    metadata_path = CACHE / "minecraft-version.json"
    checked_download(version["url"], metadata_path, "sha1", version["sha1"])
    metadata = json.loads(metadata_path.read_bytes())
    client = metadata["downloads"]["client"]
    checked_download(client["url"], CACHE / "minecraft-client.jar", "sha1", client["sha1"])
    menu=json.loads(fetch("https://api.modrinth.com/v2/project/modmenu/version/20.0.3"))
    menu_file=next(f for f in menu["files"] if f["primary"])
    checked_download(menu_file["url"],CACHE / "modmenu-api.jar","sha512",menu_file["hashes"]["sha512"])
    server = metadata["downloads"]["server"]
    bundler = CACHE / "minecraft-server-bundler.jar"
    checked_download(server["url"], bundler, "sha1", server["sha1"])
    classpath = []
    with zipfile.ZipFile(bundler) as archive:
        for kind in ("versions", "libraries"):
            for line in archive.read(f"META-INF/{kind}.list").decode().splitlines():
                checksum, _, relative = line.split("\t")
                path = CACHE / kind / relative
                if not path.resolve().is_relative_to(CACHE.resolve()):
                    raise ValueError("Bundled dependency escapes cache directory")
                data = archive.read(f"META-INF/{kind}/{relative}")
                if hashlib.sha256(data).hexdigest() != checksum:
                    raise ValueError("Bundled dependency checksum mismatch")
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
                classpath.append(path)
    loader_url = "https://maven.fabricmc.net/net/fabricmc/fabric-loader/0.19.5/fabric-loader-0.19.5.jar"
    loader = CACHE / "fabric-loader-0.19.5.jar"
    checked_download(loader_url, loader, "sha1", fetch(loader_url + ".sha1").decode().strip())
    classpath.append(loader)
    loader_meta = json.loads(fetch("https://meta.fabricmc.net/v2/versions/loader/26.2/0.19.5"))
    for entry in loader_meta["launcherMeta"]["libraries"]["common"]:
        group, name, version = entry["name"].split(":")
        relative = f"{group.replace('.', '/')}/{name}/{version}/{name}-{version}.jar"
        path = CACHE / "loader-libraries" / relative
        checked_download(entry["url"] + relative, path, "sha256", entry["sha256"])
        classpath.append(path)
    with zipfile.ZipFile(loader) as archive:
        mixinextras = CACHE / "mixinextras-fabric-0.5.5.jar"
        mixinextras.write_bytes(archive.read("META-INF/jars/mixinextras-fabric-0.5.5.jar"))
        classpath.append(mixinextras)
    versions = json.loads(fetch("https://api.modrinth.com/v2/project/fabric-api/version?game_versions=%5B%2226.2%22%5D&loaders=%5B%22fabric%22%5D"))
    release = next(v for v in versions if v["version_number"] == "0.161.0+26.2")
    file = next(f for f in release["files"] if f["primary"])
    fabric_api = CACHE / "fabric-api-0.161.0+26.2.jar"
    checked_download(file["url"], fabric_api, "sha256", FABRIC_API_SHA256)
    with zipfile.ZipFile(fabric_api) as archive:
        for name in archive.namelist():
            if name.startswith("META-INF/jars/") and name.endswith(".jar"):
                path = CACHE / Path(name).name
                path.write_bytes(archive.read(name))
                classpath.append(path)
    versions = json.loads(fetch("https://api.modrinth.com/v2/project/lithostitched/version?game_versions=%5B%2226.2%22%5D&loaders=%5B%22fabric%22%5D"))
    release = next(v for v in versions if v["version_number"] == "1.8.0-fabric-26.2")
    file = next(f for f in release["files"] if f["primary"])
    lithostitched = CACHE / "lithostitched-1.8.0-fabric-26.2.jar"
    checked_download(file["url"], lithostitched, "sha256", LITHOSTITCHED_SHA256)
    classpath.append(lithostitched)
    entries = [{"file": p.relative_to(CACHE).as_posix(), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
               for p in classpath]
    (CACHE / "classpath.json").write_text(json.dumps(entries, indent=2) + "\n", encoding="utf-8")
    print(f"Prepared {len(classpath)} checksum-verified compilation dependencies in {CACHE}")


if __name__ == "__main__":
    main()
