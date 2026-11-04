# CI: Markdown filter and updated server fixture

Validated locally on November 4, 2026. CI correction commit: `c0287ef`.

## Reported failures

The normal Build alpha runs for the 5.0.5 code commit and the following roadmap
commit failed at the same assertion in `tools/test_alpha5_port_server.py`:

- [Code commit run 41671361730](https://github.com/Auda29/Relic-Mod/actions/runs/41671361730).
- [Documentation commit run 41677181101](https://github.com/Auda29/Relic-Mod/actions/runs/41677181101).

The stored settings include `colossusMinDistance` since 5.0.5, but the expected
settings fixture omitted it. The full dictionary comparison therefore failed.
The release workflow used a different invocation without that preset assertion
and passed; this does not turn the failed normal-build checks into successes.

## Correction

The server fixture now explicitly supplies and expects the current preset
minimum: Expedition 30,000, Balanced 15,000, Discoveries 8,000 and the test-only
tower profile 8,000. A failed comparison prints both actual and expected values.
The restart assertion still requires the complete frozen settings and target
to remain unchanged when installation defaults are changed.

`build.yml` excludes `**/*.md` for branch pushes and pull requests. The full
build is skipped only when all changed files match. JSON files, manifests,
assets, scripts, workflow configuration and mixed changes continue to trigger
the build. This deliberately does not exclude the whole `docs/` directory,
which also contains technical inputs and provenance data. Manual builds remain
available. `release.yml` and release-tag publication are unchanged.

GitHub's path-filter semantics are documented in
[Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#onpushpull_requestpull_request_targetpathspaths-ignore).

## Local verification

- actionlint 1.7.12 passed for both `build.yml` and `release.yml`.
- Python compilation passed for the changed test runner.
- The previously failing native Fabric 26.2 suite passed with the published
  5.0.5 JAR, Discoveries settings and Expedition installation defaults on reload.
- Both server boot cycles passed; stored `colossusMinDistance` remained 8,000,
  and the destination, original spawn and complete saved settings stayed equal.
- Recipe network checks, core/recipe checks, Trial/Vault presentation, magnet
  behavior, Tree aura, natural animals and restart checks passed.

Reproduction:

```text
actionlint .github/workflows/build.yml .github/workflows/release.yml
python tools/build_fabric26_checks.py --java-home <jdk25> --artifact <published-5.0.5-fabric-26.2-jar>
python tools/test_alpha5_port_server.py --loader fabric --minecraft 26.2 --accept-eula --java <jdk25-java> --artifact <published-5.0.5-fabric-26.2-jar> --test-mod build/fabric26-checks/relics-alpha5-port-checks+mc26.2.jar --suite --distribution-preset discovery --reload-preset expedition
```

Local evidence: `build/alpha5-ports-20261028/fabric-26.2-084927-576314/evidence.json`.
Its player-JAR SHA-256 is
`85fe1f13f03c95deca2d41dba0093cc1b95a53bb0ad058c5b0357b84799afff1`.
The diagnostic test JAR must be rebuilt against 5.0.5 before this command; a
stale 5.0.3 test JAR is rejected by the loader before the suite can run.

The CI correction itself changes non-Markdown files and should trigger one
normal build. This report and the accompanying release-CI documentation are
pushed separately as a real Markdown-only change to verify the filter.
The full remote build remains a separate result from the successful local suite.
No new release or runtime change is part of this correction.
