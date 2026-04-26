SHELL := /bin/sh
PY := PYTHONPATH=./src python3

.PHONY: init check screen screen-valid screen-bad-request screen-bad-contract eval skills package pipeline evidence state orchestrate clean submission-surface

init:
	$(PY) -m bioguard init

check:
	$(PY) -m bioguard check

screen-valid:
	$(PY) -m bioguard screen --request artifacts/requests/seed_request.json --out artifacts/records/seed_screen.jsonl

screen-bad-request:
	-$(PY) -m bioguard screen --request artifacts/requests/bad_request.json --out artifacts/records/screen_bad_request.jsonl

screen-bad-contract:
	-$(PY) -m bioguard screen --request artifacts/requests/bad_contract.json --out artifacts/records/screen_bad_contract.jsonl

screen: screen-valid screen-bad-request screen-bad-contract

eval:
	$(PY) -m bioguard evaluate --manifest spec/benchmark_manifest_v1.0.json --seed 1 --splits test --out artifacts/metrics --include-ablations

eval-primary:
	$(PY) -m bioguard evaluate --manifest spec/benchmark_manifest_v1.0.json --seed 1 --splits test --out artifacts/metrics

skills:
	$(PY) scripts/bioguard_skill_proxy.py --mode bkt-scoring --input artifacts/requests/skill_bkt_request.json --out artifacts/records/skill_bkt_scoring.json
	$(PY) scripts/bioguard_skill_proxy.py --mode bio-trace --input artifacts/requests/seed_request.json --out artifacts/records/skill_bio_trace.json
	$(PY) scripts/bioguard_skill_proxy.py --mode bio-guard --input artifacts/requests/seed_request.json --out artifacts/records/skill_bio_guard.json
	$(PY) scripts/bioguard_skill_proxy.py --mode bio-seq --input artifacts/requests/skill_bio_seq_request.json --out artifacts/records/skill_bio_seq.json

package:
	$(PY) -m bioguard check
	$(PY) -m bioguard screen --request artifacts/requests/seed_request.json --out artifacts/records/seed_screen.jsonl
	-$(PY) -m bioguard screen --request artifacts/requests/bad_request.json --out artifacts/records/screen_bad_request.jsonl
	-$(PY) -m bioguard screen --request artifacts/requests/bad_contract.json --out artifacts/records/screen_bad_contract.jsonl
	$(MAKE) skills
	$(MAKE) eval
	$(PY) -m bioguard state --state artifacts/checks/execution_state.json
	ls -1 artifacts/records artifacts/metrics

pipeline:
	$(PY) -m bioguard init --force-seed
	$(PY) -m bioguard check
	$(PY) -m bioguard screen --request artifacts/requests/seed_request.json --out artifacts/records/seed_screen.jsonl
	-$(PY) -m bioguard screen --request artifacts/requests/bad_request.json --out artifacts/records/screen_bad_request.jsonl
	-$(PY) -m bioguard screen --request artifacts/requests/bad_contract.json --out artifacts/records/screen_bad_contract.jsonl
	$(MAKE) skills
	$(MAKE) eval
	$(PY) -m bioguard state --state artifacts/checks/execution_state.json --complete-task protocol-engine --note "protocol-engine validated in automated pipeline"
	$(PY) -m bioguard state --state artifacts/checks/execution_state.json --complete-task core-implementation --note "runtime and skill smoke artifacts refreshed"
	$(PY) -m bioguard state --state artifacts/checks/execution_state.json --complete-task eval-engine --note "evaluation matrix and error taxonomy refreshed"
	$(PY) -m bioguard state --state artifacts/checks/execution_state.json --complete-task report-engine --note "submission report package refreshed"
	$(PY) -m bioguard state --state artifacts/checks/execution_state.json --note "pipeline complete"
	$(PY) scripts/build_evidence_manifest.py

evidence:
	$(PY) scripts/build_evidence_manifest.py

submission-surface:
	$(PY) scripts/build_submission_surface.py --out artifacts/submission_surface

state:
	$(PY) -m bioguard state --state artifacts/checks/execution_state.json

orchestrate:
	$(PY) -m bioguard orchestrate --state artifacts/checks/execution_state.json

clean:
	rm -f artifacts/records/*.jsonl artifacts/metrics/*.json artifacts/metrics/*.csv artifacts/metrics/*.md
	rm -rf .pytest_cache
