import argparse
import json
import sys
import zipfile
from pathlib import Path

SLUG = "xiaojiao_art_teacher_capability_registry_fixture_1007D"
EXPECTED_STATUS = "XIAOJIAO_ART_TEACHER_CAPABILITY_REGISTRY_FIXTURE_PASS"
EXPECTED_MARKER = "ALL_1007D_ART_TEACHER_CAPABILITY_REGISTRY_FIXTURE_CHECKS_OK"
REQUIRED_FILES = [
    "docs/foundation/xiaojiao_art_teacher_capability_registry_fixture_1007D.md",
    "docs/foundation/xiaojiao_art_teacher_capability_registry_fixture_1007D.json",
    "samples/xiaojiao_art_teacher_capability_registry_fixture_1007D/art_teacher_capability_registry_fixture_1007D.json",
    "scripts/validate_xiaojiao_art_teacher_capability_registry_fixture_1007D.py",
    "docs/audit/xiaojiao_art_teacher_capability_registry_fixture_1007D_result.json",
    "docs/audit/xiaojiao_art_teacher_capability_registry_fixture_1007D_report.md",
    "docs/audit_packages/xiaojiao_art_teacher_capability_registry_fixture_1007D_manifest.json",
    "docs/audit_packages/xiaojiao_art_teacher_capability_registry_fixture_1007D.zip",
]
FORBIDDEN_PARTS = [".env", "token", "secret", "key", "node_modules", "__pycache__", ".db", ".sqlite", "dist", "build", "coverage", ".DS_Store"]
FALSE_FLAGS = ["provider_called","model_called","api_key_configured","real_database_written","database_written","real_memory_written","memory_written","Feishu_written","formal_export_created","real_frontend_runtime_modified","real_frontend_modified","teacher_control_runtime_entered","public_display_runtime_entered","student_side_runtime_entered","production_generation_performed","formal_writeback_performed","formal_apply_performed","real_classroom_delivery_entered","real_resource_library_connected","production_dependency_installed"]

def fail(msg):
    print("VALIDATION_FAILED: " + msg)
    sys.exit(1)

def rel_ok(path):
    return not (path.startswith("/") or path.startswith("\\") or (len(path) > 1 and path[1] == ":")) and "\\" not in path

def forbidden(path):
    low = path.lower()
    return any(part.lower() in low for part in FORBIDDEN_PARTS)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    for rel in REQUIRED_FILES:
        if not rel_ok(rel):
            fail("bad required path: " + rel)
        if forbidden(rel):
            fail("forbidden required path: " + rel)
        if not (root / rel).exists():
            fail("missing required file: " + rel)
    result = json.loads((root / f"docs/audit/{SLUG}_result.json").read_text(encoding="utf-8"))
    if result.get("final_status") != EXPECTED_STATUS or result.get("pass") is not True:
        fail("unexpected result status")
    if result.get("marker") != EXPECTED_MARKER:
        fail("unexpected marker")
    flags = result.get("boundary_flags", {})
    for flag in FALSE_FLAGS:
        if flags.get(flag) is not False:
            fail("unsafe boundary flag: " + flag)
    if flags.get("teacher_review_required_stop") is not True:
        fail("teacher_review_required_stop must be true")
    foundation = json.loads((root / f"docs/foundation/{SLUG}.json").read_text(encoding="utf-8"))
    if foundation.get("current_product_identity") != "teacher_work_state_driven_intelligent_organization_system":
        fail("missing product identity guardrail")
    if foundation.get("primary_business_pack") != "art_teacher_daily_work_pack":
        fail("missing art teacher business pack")
    manifest = json.loads((root / f"docs/audit_packages/{SLUG}_manifest.json").read_text(encoding="utf-8"))
    zip_path = root / f"docs/audit_packages/{SLUG}.zip"
    with zipfile.ZipFile(zip_path, "r") as zf:
        entries = sorted(zf.namelist())
    for entry in entries:
        if not rel_ok(entry):
            fail("bad ZIP entry path: " + entry)
        if forbidden(entry):
            fail("forbidden ZIP entry: " + entry)
    expected = sorted(manifest.get("zip_entries", []))
    manifest_minus_zip = sorted(set(expected) - set(entries))
    zip_minus_manifest = sorted(set(entries) - set(expected))
    if manifest_minus_zip or zip_minus_manifest:
        fail(f"manifest/ZIP mismatch: {manifest_minus_zip} / {zip_minus_manifest}")
    if manifest.get("zip_entry_count") != len(entries):
        fail("zip_entry_count mismatch")
    if manifest.get("manifest_minus_zip") != [] or manifest.get("zip_minus_manifest") != []:
        fail("manifest diff fields must be []")
    sample = json.loads((root / "samples/xiaojiao_art_teacher_capability_registry_fixture_1007D/art_teacher_capability_registry_fixture_1007D.json").read_text(encoding="utf-8"))
    text = json.dumps(sample, ensure_ascii=False)
    for term in ["art_teacher", "teacher_review"]:
        if term not in text:
            fail("sample missing term: " + term)
    if "1007D" == "1007H":
        for term in ["model_candidate_request", "work_object_patch", "formal_apply_performed"]:
            if term not in text:
                fail("1007H sample missing term: " + term)
    print(EXPECTED_MARKER)

if __name__ == "__main__":
    main()
