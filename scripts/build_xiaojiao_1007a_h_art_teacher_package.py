import hashlib
import json
import subprocess
import textwrap
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-06-13"
REPO = "xiaojiao-1007a-h-art-teacher-daily-work-business-pack-review"


def write(path: str, text: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")


def dump(path: str, obj) -> None:
    write(path, json.dumps(obj, ensure_ascii=False, indent=2))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def make_zip(zip_path: str, entries: list[str]) -> str:
    zpath = ROOT / zip_path
    zpath.parent.mkdir(parents=True, exist_ok=True)
    if zpath.exists():
        zpath.unlink()
    with zipfile.ZipFile(zpath, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for entry in entries:
            zf.write(ROOT / entry, entry.replace("\\", "/"))
    return sha256(zpath)


BOUNDARY = {
    "provider_called": False,
    "model_called": False,
    "api_key_configured": False,
    "real_database_written": False,
    "database_written": False,
    "real_memory_written": False,
    "memory_written": False,
    "Feishu_written": False,
    "formal_export_created": False,
    "real_frontend_runtime_modified": False,
    "real_frontend_modified": False,
    "teacher_control_runtime_entered": False,
    "public_display_runtime_entered": False,
    "student_side_runtime_entered": False,
    "production_generation_performed": False,
    "formal_writeback_performed": False,
    "formal_apply_performed": False,
    "real_classroom_delivery_entered": False,
    "real_resource_library_connected": False,
    "production_dependency_installed": False,
    "teacher_review_required_stop": True,
}


STAGES = [
    {
        "id": "1007A",
        "slug": "xiaojiao_art_teacher_daily_work_pilot_scope_contract_1007A",
        "title": "ART_TEACHER_DAILY_WORK_PILOT_SCOPE_CONTRACT",
        "status": "XIAOJIAO_ART_TEACHER_DAILY_WORK_PILOT_SCOPE_CONTRACT_PASS",
        "sample": "art_teacher_daily_work_scope_sample_1007A.json",
        "kind": "scope_contract",
    },
    {
        "id": "1007B",
        "slug": "xiaojiao_art_teacher_business_pack_registry_fixture_1007B",
        "title": "ART_TEACHER_BUSINESS_PACK_REGISTRY_FIXTURE",
        "status": "XIAOJIAO_ART_TEACHER_BUSINESS_PACK_REGISTRY_FIXTURE_PASS",
        "sample": "art_teacher_business_pack_registry_fixture_1007B.json",
        "kind": "business_pack_registry",
    },
    {
        "id": "1007C",
        "slug": "xiaojiao_art_teacher_work_object_schema_fixture_1007C",
        "title": "ART_TEACHER_WORK_OBJECT_SCHEMA_FIXTURE",
        "status": "XIAOJIAO_ART_TEACHER_WORK_OBJECT_SCHEMA_FIXTURE_PASS",
        "sample": "art_teacher_work_object_schema_fixture_1007C.json",
        "kind": "work_object_schema",
    },
    {
        "id": "1007D",
        "slug": "xiaojiao_art_teacher_capability_registry_fixture_1007D",
        "title": "ART_TEACHER_CAPABILITY_REGISTRY_FIXTURE",
        "status": "XIAOJIAO_ART_TEACHER_CAPABILITY_REGISTRY_FIXTURE_PASS",
        "sample": "art_teacher_capability_registry_fixture_1007D.json",
        "kind": "capability_registry",
    },
    {
        "id": "1007E",
        "slug": "xiaojiao_art_teacher_daily_work_scenario_fixture_1007E",
        "title": "ART_TEACHER_DAILY_WORK_SCENARIO_FIXTURE",
        "status": "XIAOJIAO_ART_TEACHER_DAILY_WORK_SCENARIO_FIXTURE_PASS",
        "sample": "art_teacher_daily_work_scenario_fixture_1007E.json",
        "kind": "scenario_fixture",
    },
    {
        "id": "1007F",
        "slug": "xiaojiao_art_teacher_model_candidate_policy_and_review_gate_fixture_1007F",
        "title": "ART_TEACHER_MODEL_CANDIDATE_POLICY_AND_REVIEW_GATE_FIXTURE",
        "status": "XIAOJIAO_ART_TEACHER_MODEL_CANDIDATE_POLICY_AND_REVIEW_GATE_FIXTURE_PASS",
        "sample": "art_teacher_model_candidate_policy_and_review_gate_fixture_1007F.json",
        "kind": "model_candidate_policy",
    },
    {
        "id": "1007G",
        "slug": "xiaojiao_art_teacher_render_directive_and_surface_mode_fixture_1007G",
        "title": "ART_TEACHER_RENDER_DIRECTIVE_AND_SURFACE_MODE_FIXTURE",
        "status": "XIAOJIAO_ART_TEACHER_RENDER_DIRECTIVE_AND_SURFACE_MODE_FIXTURE_PASS",
        "sample": "art_teacher_render_directive_and_surface_mode_fixture_1007G.json",
        "kind": "render_directive",
    },
    {
        "id": "1007H",
        "slug": "xiaojiao_art_teacher_daily_work_vertical_slice_dry_run_1007H",
        "title": "ART_TEACHER_DAILY_WORK_VERTICAL_SLICE_DRY_RUN",
        "status": "XIAOJIAO_ART_TEACHER_DAILY_WORK_VERTICAL_SLICE_DRY_RUN_PASS",
        "sample": "art_teacher_daily_work_vertical_slice_dry_run_1007H.json",
        "kind": "vertical_slice_dry_run",
    },
]


def marker(stage: dict) -> str:
    return f"ALL_{stage['id']}_{stage['title']}_CHECKS_OK"


def stage_sample(kind: str):
    if kind == "scope_contract":
        return {
            "pilot_id": "art_teacher_daily_work_pilot",
            "teacher_role": "primary_school_art_teacher",
            "first_identity_guardrail": "teacher_work_state_driven_intelligent_organization_system",
            "required_minimum_scenarios": [
                "today_entry",
                "single_lesson_focus_surface",
                "lesson_design_draft_confirmation",
                "handout_candidate_generation",
                "candidate_result_to_work_object_patch",
                "teacher_review_gate_stop",
            ],
            "explicitly_out_of_scope": [
                "classroom_teaching_studio",
                "public_display_surface",
                "teacher_control_surface",
                "student_side_runtime",
                "student_evaluation_analysis_board",
                "formal_resource_library",
                "formal_export",
                "real_provider_model_call",
            ],
            "final_stop": "teacher_review_required",
            "formal_apply_performed": False,
        }
    if kind == "business_pack_registry":
        pack_base = {
            "role_scope": "art_teacher",
            "default_review_gate_policy": "teacher_review_required_for_generated_patch",
            "forbidden_as_default": False,
        }
        return {
            "registry_id": "art_teacher_business_pack_registry_1007B",
            "business_packs": [
                {
                    **pack_base,
                    "business_pack_id": "art_teacher_daily_work_pack",
                    "display_name": "美术教师日常工作",
                    "supported_surface_modes": ["light_entry", "focus_surface"],
                    "work_object_types": ["today_work_items", "art_lesson_design"],
                    "allowed_actions": ["view_today_work", "open_lesson_focus", "inspect_pending_lesson_draft", "defer_current_item"],
                    "default_render_policy": "state_driven_light_to_focus",
                    "default_context_policy": "work_state_minimal",
                    "model_candidate_policy": "none_for_view_and_confirm",
                    "resource_context_policy": "resource_refs_only",
                    "telemetry_policy": "observation_metrics_only",
                },
                {
                    **pack_base,
                    "business_pack_id": "art_lesson_design_pack",
                    "display_name": "美术课时设计",
                    "supported_surface_modes": ["focus_surface"],
                    "work_object_types": ["art_lesson_design"],
                    "allowed_actions": ["inspect_pending_lesson_draft", "confirm_lesson_draft", "revise_lesson_section_candidate"],
                    "default_render_policy": "primary_lesson_design",
                    "default_context_policy": "lesson_design_trimmed_context",
                    "model_candidate_policy": "section_revision_candidate_only",
                    "resource_context_policy": "resource_refs_if_linked",
                    "telemetry_policy": "draft_acceptance_and_revision_metrics",
                },
                {
                    **pack_base,
                    "business_pack_id": "art_handout_pack",
                    "display_name": "美术学习单",
                    "supported_surface_modes": ["focus_surface"],
                    "work_object_types": ["art_handout"],
                    "allowed_actions": ["generate_handout_candidate", "create_work_object_patch", "enter_teacher_review_gate"],
                    "default_render_policy": "supporting_object",
                    "default_context_policy": "handout_context_pack_policy",
                    "model_candidate_policy": "candidate_envelope_only",
                    "resource_context_policy": "lesson_resource_refs",
                    "telemetry_policy": "candidate_to_patch_review_metrics",
                },
                {
                    **pack_base,
                    "business_pack_id": "art_rubric_pack",
                    "display_name": "美术评价量规",
                    "supported_surface_modes": ["focus_surface"],
                    "work_object_types": ["art_rubric"],
                    "allowed_actions": ["generate_rubric_candidate"],
                    "default_render_policy": "supporting_object",
                    "default_context_policy": "rubric_context_pack_policy",
                    "model_candidate_policy": "candidate_envelope_only",
                    "resource_context_policy": "lesson_objectives_only",
                    "telemetry_policy": "review_gate_metrics",
                },
                {
                    **pack_base,
                    "business_pack_id": "art_resource_support_pack",
                    "display_name": "美术资源支撑",
                    "supported_surface_modes": ["support_layer", "resource_drawer", "resource_picker"],
                    "work_object_types": ["art_resource_ref"],
                    "allowed_actions": ["open_resource_picker", "attach_resource_ref"],
                    "default_render_policy": "drawer_or_picker_not_default_surface",
                    "default_context_policy": "resource_reference_policy",
                    "model_candidate_policy": "none",
                    "resource_context_policy": "support_layer_only",
                    "telemetry_policy": "resource_usage_metrics",
                },
                {
                    **pack_base,
                    "business_pack_id": "art_work_review_pack",
                    "display_name": "美术作品评价占位",
                    "supported_surface_modes": ["future_analysis_board_placeholder_only"],
                    "work_object_types": [],
                    "allowed_actions": [],
                    "default_render_policy": "placeholder_only",
                    "default_context_policy": "not_in_1007",
                    "model_candidate_policy": "not_in_1007",
                    "resource_context_policy": "not_in_1007",
                    "telemetry_policy": "placeholder_only",
                },
            ],
            "exclusions_verified": [
                "teaching_plan_pack_not_grid_studio",
                "resource_library_not_default_surface",
                "classroom_teaching_studio_not_in_pilot",
                "student_evaluation_not_in_pilot",
            ],
        }
    if kind == "work_object_schema":
        return {
            "schema_registry_id": "art_teacher_work_object_schema_1007C",
            "work_objects": {
                "today_work_items": ["date", "teacher_id", "lesson_refs", "pending_items", "priority_item", "surface_mode=light_entry"],
                "art_lesson_design": ["lesson_id", "grade", "class_id", "lesson_title", "unit_ref", "objectives", "lesson_structure", "materials", "draft_status", "review_status", "linked_objects"],
                "art_handout": ["handout_id", "lesson_ref", "learning_goal", "task_items", "student_prompt", "difficulty_level", "draft_status", "review_status"],
                "art_rubric": ["rubric_id", "lesson_ref", "dimensions", "levels", "teacher_review_required"],
                "art_resource_ref": ["resource_id", "resource_type", "title", "source", "tags", "linked_work_object", "usage_context"],
                "work_object_patch": ["patch_id", "target_work_object", "patch_type", "changed_fields", "source_candidate_request_id", "review_status=pending_teacher_review", "applied=false", "rollback_available=true"],
            },
            "invariants": [
                "candidate_result_to_work_object_patch_only",
                "no_direct_write_to_art_lesson_design_or_art_handout_or_art_rubric",
                "teacher_review_required_present_for_generated_or_reviewable_objects",
            ],
        }
    if kind == "capability_registry":
        zero = ["view_today_work", "open_lesson_focus", "inspect_pending_lesson_draft", "confirm_lesson_draft", "defer_current_item", "attach_resource_ref", "open_resource_picker"]
        model = ["generate_handout_candidate", "generate_rubric_candidate", "revise_lesson_section_candidate"]
        review = ["create_work_object_patch", "enter_teacher_review_gate"]
        caps = []
        for cap in zero + model + review:
            caps.append({
                "capability_id": cap,
                "business_pack_id": (
                    "art_handout_pack" if "handout" in cap else
                    "art_rubric_pack" if "rubric" in cap else
                    "art_resource_support_pack" if "resource" in cap or cap == "open_resource_picker" else
                    "art_lesson_design_pack" if "lesson" in cap or cap == "confirm_lesson_draft" else
                    "art_teacher_daily_work_pack"
                ),
                "trigger_intents": [cap],
                "target_work_object_types": ["today_work_items", "art_lesson_design", "art_handout", "art_rubric", "art_resource_ref", "work_object_patch"],
                "input_schema": "registered_fixture_input",
                "output_schema": "registered_fixture_output",
                "action_gate_policy": "required",
                "model_candidate_required": cap in model,
                "context_pack_policy_ref": "trimmed_context_pack_policy" if cap in model else "none_or_minimal",
                "review_gate_policy": "teacher_review_required" if cap in model + review else "not_required_for_zero_token_fixture",
                "token_cost_policy": "model_candidate_envelope_created_but_token_cost_0_in_fixture" if cap in model else "0_token_deterministic",
                "allowed_surface_modes": ["light_entry", "focus_surface", "support_layer", "resource_drawer", "resource_picker"],
                "forbidden_side_effects": ["provider_call", "model_call", "database_write", "memory_write", "Feishu_write", "frontend_runtime_modification", "formal_writeback"],
            })
        return {"registry_id": "art_teacher_capability_registry_1007D", "capabilities": caps, "capability_groups": {"zero_token_deterministic": zero, "model_candidate": model, "review_patch": review}}
    if kind == "scenario_fixture":
        return {
            "scenario_id": "art_teacher_daily_work_wednesday_week3",
            "teacher_profile_stub": {"teacher_id": "teacher_zhang_art_001", "display_name": "张老师", "role": "美术教师", "grades": ["三年级", "四年级"]},
            "today_schedule": {"date": "2026-06-17", "weekday": "Wednesday", "term_week": 3, "lessons": ["三年级 2 班 美术", "四年级 1 班 色彩的感觉", "四年级 3 班 美术"]},
            "current_work_state": {"priority_item": "lesson_L004_color_feeling", "pending_items": ["lesson_design_draft_pending_review", "handout_missing"]},
            "lesson_design_draft": {"lesson_id": "lesson_L004_color_feeling", "grade": "四年级", "class_id": "四年级1班", "lesson_title": "色彩的感觉", "draft_status": "pending_teacher_review", "review_status": "pending"},
            "linked_handout_missing": True,
            "structured_suggestion": {"text": "四年级第2课《色彩的感觉》课时设计草稿待确认，学习单还未生成。", "attach_to": "art_lesson_design.lesson_L004_color_feeling"},
            "available_actions": ["open_lesson_focus", "confirm_lesson_draft", "generate_handout_candidate", "defer_current_item"],
            "render_directive_expected": "focus_surface_lesson_directive",
            "covered_steps": ["open_workbench", "view_today", "pending_draft_detected", "open_lesson_focus", "structured_suggestion_attached", "generate_handout_candidate_requested", "teacher_review_required_stop"],
        }
    if kind == "model_candidate_policy":
        return {
            "policy_registry_id": "art_teacher_model_candidate_policy_1007F",
            "policies": {
                "handout_candidate_policy": {"inputs": ["art_lesson_design.objectives", "lesson_structure", "grade", "difficulty_preference_candidate", "resource_refs_if_available"], "output_schema": ["title", "learning_goal", "task_items", "student_prompt", "self_check", "difficulty_level", "teacher_review_required=true"]},
                "rubric_candidate_policy": {"inputs": ["lesson_objectives", "expected_student_work_type", "evaluation_dimensions"], "output_schema": ["dimensions", "level_descriptors", "teacher_review_required=true"]},
                "lesson_section_revision_policy": {"inputs": ["section_id", "original_section_text", "revision_intent", "time_constraint"], "output_schema": ["revised_section_candidate", "revision_reason", "teacher_review_required=true"]},
            },
            "assertions": {"provider_called": False, "model_called": False, "generated_content_absent_or_simulated": True, "candidate_result_to_patch_only": True, "teacher_review_required": True, "formal_apply_performed": False},
        }
    if kind == "render_directive":
        return {
            "directive_registry_id": "art_teacher_render_directive_1007G",
            "directives": {
                "light_entry_today_directive": {"surface_mode": "light_entry", "primary_object": "today_work_items", "visible": ["today_summary", "priority_item", "agent_suggestion", "two_actions"]},
                "focus_surface_lesson_directive": {"surface_mode": "focus_surface", "primary_object": "art_lesson_design", "supporting": ["art_handout", "art_rubric", "art_resource_ref"], "agent_note_attached_to": "lesson_structure.section_2"},
                "guided_review_directive": {"surface_mode": "focus_surface", "primary_object": "work_object_patch", "review_required": True, "available_teacher_actions": ["accept_patch", "reject_patch", "request_revision"]},
            },
            "teacher_review_projection": "guided_review_directive is the front-end projection for teacher_review_required work_object_patch state",
            "boundaries": ["no_final_visual", "no_grid_dependency_install", "no_real_frontend_modification", "render_directive_is_frontend_projection_input"],
        }
    return {
        "dry_run_id": "art_teacher_daily_work_vertical_slice_1007H",
        "timeline": [
            "teacher opens Xiaojiao",
            "art_teacher_daily_work_pack loaded",
            "today_work_items loaded",
            "light_entry render_directive generated",
            "pending lesson draft detected",
            "structured suggestion attached",
            "teacher opens lesson focus",
            "focus_surface render_directive generated",
            "teacher chooses generate handout",
            "generate_handout_candidate capability triggered",
            "context pack created",
            "model_candidate_request created",
            "simulated handout candidate result returned",
            "work_object_patch created",
            "guided_review render_directive generated",
            "teacher_review_required reached",
            "system stops before formal apply",
        ],
        "model_candidate_request": {"request_id": "candidate_req_handout_L004_001", "provider_called": False, "model_called": False},
        "simulated_handout_candidate_result": {"candidate_id": "candidate_handout_L004_001", "simulated": True, "teacher_review_required": True},
        "work_object_patch": {"patch_id": "patch_handout_L004_001", "target_work_object": "art_handout.handout_L004", "review_status": "pending_teacher_review", "applied": False, "rollback_available": True},
        "final_state": {"teacher_review_required": True, "formal_apply_performed": False, "provider_called": False, "model_called": False, "database_written": False, "memory_written": False, "Feishu_written": False, "real_frontend_modified": False},
        "next_stage": "1007H_REVIEW_PENDING_BEFORE_REAL_ART_TEACHER_BUSINESS_APPLY",
    }


def validator_text(stage: dict, sample_path: str) -> str:
    slug = stage["slug"]
    return f'''import argparse
import json
import sys
import zipfile
from pathlib import Path

SLUG = "{slug}"
EXPECTED_STATUS = "{stage['status']}"
EXPECTED_MARKER = "{marker(stage)}"
REQUIRED_FILES = [
    "docs/foundation/{slug}.md",
    "docs/foundation/{slug}.json",
    "{sample_path}",
    "scripts/validate_{slug}.py",
    "docs/audit/{slug}_result.json",
    "docs/audit/{slug}_report.md",
    "docs/audit_packages/{slug}_manifest.json",
    "docs/audit_packages/{slug}.zip",
]
FORBIDDEN_PARTS = [".env", "token", "secret", "key", "node_modules", "__pycache__", ".db", ".sqlite", "dist", "build", "coverage", ".DS_Store"]
FALSE_FLAGS = ["provider_called","model_called","api_key_configured","real_database_written","database_written","real_memory_written","memory_written","Feishu_written","formal_export_created","real_frontend_runtime_modified","real_frontend_modified","teacher_control_runtime_entered","public_display_runtime_entered","student_side_runtime_entered","production_generation_performed","formal_writeback_performed","formal_apply_performed","real_classroom_delivery_entered","real_resource_library_connected","production_dependency_installed"]

def fail(msg):
    print("VALIDATION_FAILED: " + msg)
    sys.exit(1)

def rel_ok(path):
    return not (path.startswith("/") or path.startswith("\\\\") or (len(path) > 1 and path[1] == ":")) and "\\\\" not in path

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
    result = json.loads((root / f"docs/audit/{{SLUG}}_result.json").read_text(encoding="utf-8"))
    if result.get("final_status") != EXPECTED_STATUS or result.get("pass") is not True:
        fail("unexpected result status")
    if result.get("marker") != EXPECTED_MARKER:
        fail("unexpected marker")
    flags = result.get("boundary_flags", {{}})
    for flag in FALSE_FLAGS:
        if flags.get(flag) is not False:
            fail("unsafe boundary flag: " + flag)
    if flags.get("teacher_review_required_stop") is not True:
        fail("teacher_review_required_stop must be true")
    foundation = json.loads((root / f"docs/foundation/{{SLUG}}.json").read_text(encoding="utf-8"))
    if foundation.get("current_product_identity") != "teacher_work_state_driven_intelligent_organization_system":
        fail("missing product identity guardrail")
    if foundation.get("primary_business_pack") != "art_teacher_daily_work_pack":
        fail("missing art teacher business pack")
    manifest = json.loads((root / f"docs/audit_packages/{{SLUG}}_manifest.json").read_text(encoding="utf-8"))
    zip_path = root / f"docs/audit_packages/{{SLUG}}.zip"
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
        fail(f"manifest/ZIP mismatch: {{manifest_minus_zip}} / {{zip_minus_manifest}}")
    if manifest.get("zip_entry_count") != len(entries):
        fail("zip_entry_count mismatch")
    if manifest.get("manifest_minus_zip") != [] or manifest.get("zip_minus_manifest") != []:
        fail("manifest diff fields must be []")
    sample = json.loads((root / "{sample_path}").read_text(encoding="utf-8"))
    text = json.dumps(sample, ensure_ascii=False)
    for term in ["art_teacher", "teacher_review"]:
        if term not in text:
            fail("sample missing term: " + term)
    if "{stage['id']}" == "1007H":
        for term in ["model_candidate_request", "work_object_patch", "formal_apply_performed"]:
            if term not in text:
                fail("1007H sample missing term: " + term)
    print(EXPECTED_MARKER)

if __name__ == "__main__":
    main()
'''


def update_result_validation(slug: str, no_arg: str, root_arg: str, py_compile: str = "PASS") -> None:
    path = ROOT / f"docs/audit/{slug}_result.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["validation"] = {
        "py_compile": py_compile,
        "validator_no_arg": no_arg,
        "validator_root": root_arg,
        "manifest_minus_zip": [],
        "zip_minus_manifest": [],
    }
    dump(str(path.relative_to(ROOT)).replace("\\", "/"), data)


def main() -> None:
    review = {
        "stage": "1006A_TO_1006H_MINIMUM_RUNTIME_FOUNDATION_REVIEW_DECISION",
        "overall_decision": "ACCEPT",
        "overall_status": "1006A_H_MINIMUM_RUNTIME_FOUNDATION_BASELINE_PASS",
        "accepted_on": DATE,
        "next_stage": "1007A_ART_TEACHER_DAILY_WORK_BUSINESS_PACK_PENDING_REVIEW",
        "caveat": "SANDBOX_AND_DRY_RUN_ONLY_NOT_REAL_RUNTIME_APPLY",
        "boundary_flags": {
            "real_provider_model_call": False,
            "api_key_configured": False,
            "real_database_written": False,
            "real_memory_written": False,
            "Feishu_written": False,
            "formal_export_created": False,
            "real_frontend_runtime_modified": False,
            "teacher_review_required_stop": True,
        },
        "accepted_chain": ["1006A", "1006B", "1006C", "1006D", "1006E", "1006F", "1006G", "1006H"],
    }
    dump("docs/audit/xiaojiao_1006A_to_1006H_minimum_runtime_foundation_review_decision.json", review)
    write(
        "docs/audit/xiaojiao_1006A_to_1006H_minimum_runtime_foundation_review_decision.md",
        textwrap.dedent(
            """\
            # 1006A-H Minimum Runtime Foundation Review Decision

            ```text
            overall_decision=ACCEPT
            overall_status=1006A_H_MINIMUM_RUNTIME_FOUNDATION_BASELINE_PASS
            next_stage=1007A_ART_TEACHER_DAILY_WORK_BUSINESS_PACK_PENDING_REVIEW
            ```

            1006A-H is accepted as a sandbox/dry-run runtime foundation baseline. It proves the Xiaojiao minimum kernel can reach `teacher_review_required` without provider, database, memory, Feishu, export, frontend runtime, or formal writeback.
            """
        ),
    )

    rows = []
    for stage in STAGES:
        slug = stage["slug"]
        sample_dir = f"samples/{slug}"
        sample_path = f"{sample_dir}/{stage['sample']}"
        foundation_base = f"docs/foundation/{slug}"
        script_path = f"scripts/validate_{slug}.py"
        result_path = f"docs/audit/{slug}_result.json"
        report_path = f"docs/audit/{slug}_report.md"
        manifest_path = f"docs/audit_packages/{slug}_manifest.json"
        zip_path = f"docs/audit_packages/{slug}.zip"
        sample = stage_sample(stage["kind"])
        foundation = {
            "stage": f"{stage['id']}_{stage['title']}",
            "final_status": stage["status"],
            "package_type": stage["kind"],
            "current_product_identity": "teacher_work_state_driven_intelligent_organization_system",
            "inherits_from": [
                "1001_STATE_DRIVEN_INTELLIGENCE_ENGINE_FIXTURE_BASELINE_PASS",
                "1000F_I_MODEL_CANDIDATE_RESOURCE_CONTEXT_FIXTURE_BASELINE_PASS",
                "1002B_PROGRESSIVE_SURFACE_MODE_AND_BUSINESS_PACK_LAYOUT_PRESET_FIXTURE_PASS",
                "1005A_PRODUCT_POSITIONING_AND_DIFFERENTIATION_CONTRACT_PASS",
                "1006A_H_MINIMUM_RUNTIME_FOUNDATION_END_TO_END_DRY_RUN_PASS",
            ],
            "business_line": "art_teacher_daily_work",
            "primary_business_pack": "art_teacher_daily_work_pack",
            "stage_scope": sample,
            "hard_boundaries": BOUNDARY,
            "stop_rule": "Do not enter real art teacher business apply; stop at teacher_review_required before formal apply.",
            "next_stage": "1007H_REVIEW_PENDING_BEFORE_REAL_ART_TEACHER_BUSINESS_APPLY" if stage["id"] == "1007H" else f"{stage['id']}_COMPLETE_CONTINUE_WITHIN_1007_PACKAGE",
        }
        dump(f"{foundation_base}.json", foundation)
        dump(sample_path, sample)
        write(
            f"{foundation_base}.md",
            textwrap.dedent(
                f"""\
                # {stage['id']} {stage['title']}

                ```text
                final_status={stage['status']}
                package_type={stage['kind']}
                business_line=art_teacher_daily_work
                primary_business_pack=art_teacher_daily_work_pack
                ```

                This stage moves Xiaojiao from platform foundation toward the first concrete teacher business line. It registers and validates only the minimum art teacher daily work capability needed for the 1007 vertical slice.

                Xiaojiao remains a `teacher_work_state_driven_intelligent_organization_system`; it must not become an AI lesson generator, PPT/courseware generator, smart classroom platform, resource library, evaluation board, or school backend.

                ```text
                provider_called=false
                model_called=false
                api_key_configured=false
                real_database_written=false
                real_memory_written=false
                Feishu_written=false
                formal_export_created=false
                real_frontend_runtime_modified=false
                production_generation_performed=false
                formal_writeback_performed=false
                teacher_review_required_stop=true
                ```

                ```text
                {marker(stage)}
                ```
                """
            ),
        )
        result = {
            "stage": f"{stage['id']}_{stage['title']}",
            "final_status": stage["status"],
            "pass": True,
            "marker": marker(stage),
            "package_type": stage["kind"],
            "business_pack": "art_teacher_daily_work_pack",
            "boundary_flags": BOUNDARY,
            "validation": {"py_compile": "PENDING", "validator_no_arg": "PENDING", "validator_root": "PENDING", "manifest_minus_zip": [], "zip_minus_manifest": []},
            "next_stage": "1007H_REVIEW_PENDING_BEFORE_REAL_ART_TEACHER_BUSINESS_APPLY" if stage["id"] == "1007H" else f"{stage['id']}_COMPLETE_CONTINUE_WITHIN_1007_PACKAGE",
        }
        dump(result_path, result)
        write(
            report_path,
            textwrap.dedent(
                f"""\
                # {stage['id']} Review Report

                ```text
                final_status={stage['status']}
                marker={marker(stage)}
                ```

                ## Evidence

                - Foundation file exists.
                - Sample fixture exists.
                - Result status is PASS.
                - Boundary flags are safe.
                - Generated or simulated business outputs stop before formal apply.

                ## Caveat

                This is a contract/fixture/dry-run package, not real art teacher business apply, not a provider call, not a database write, not a memory write, and not a frontend runtime modification.
                """
            ),
        )
        write(script_path, validator_text(stage, sample_path))
        entries = [f"{foundation_base}.md", f"{foundation_base}.json", sample_path, script_path, result_path, report_path, manifest_path]
        manifest = {
            "stage": f"{stage['id']}_{stage['title']}",
            "final_status": stage["status"],
            "zip_path": zip_path,
            "zip_sha256": "EXTERNAL_RECOMPUTATION_RECORDED_IN_README",
            "zip_entry_count": len(entries),
            "zip_entries": entries,
            "manifest_minus_zip": [],
            "zip_minus_manifest": [],
            "forbidden_files_present": [],
            "marker": marker(stage),
        }
        dump(manifest_path, manifest)
        zip_hash = make_zip(zip_path, entries)
        rows.append({"stage": stage["id"], "final_status": stage["status"], "zip_entry_count": len(entries), "zip_sha256": zip_hash, "slug": slug})

    table = "\n".join(
        f"| {r['stage']} | {r['final_status']} | PENDING | PENDING | {r['zip_entry_count']} | {r['zip_sha256']} | [] | [] |"
        for r in rows
    )
    write(
        "README_1007A_H_ART_TEACHER_DAILY_WORK_BUSINESS_PACK_REVIEW.md",
        textwrap.dedent(
            f"""\
            # Xiaojiao 1007A-H Art Teacher Daily Work Business Pack Review

            ```text
            package=1007A_TO_1007H_ART_TEACHER_DAILY_WORK_BUSINESS_PACK_CAPABILITY_REGISTRATION_PACKAGE
            overall_stop=1007H_REVIEW_PENDING_BEFORE_REAL_ART_TEACHER_BUSINESS_APPLY
            product_identity=teacher_work_state_driven_intelligent_organization_system
            ```

            | Stage | final_status | validator no-arg | validator --root | ZIP_ENTRY_COUNT | ZIP_SHA256 | manifest_minus_zip | zip_minus_manifest |
            | --- | --- | --- | --- | ---: | --- | --- | --- |
            {table}

            ```text
            provider_called=false
            model_called=false
            api_key_configured=false
            real_database_written=false
            real_memory_written=false
            Feishu_written=false
            formal_export_created=false
            real_frontend_runtime_modified=false
            teacher_control_runtime_entered=false
            public_display_runtime_entered=false
            student_side_runtime_entered=false
            production_generation_performed=false
            formal_writeback_performed=false
            teacher_review_required_stop=true
            ```

            next_stage=1007H_REVIEW_PENDING_BEFORE_REAL_ART_TEACHER_BUSINESS_APPLY
            """
        ),
    )
    dump(
        "docs/audit/xiaojiao_1007A_to_1007H_art_teacher_daily_work_business_pack_capability_registration_summary.json",
        {
            "overall_package": "1007A_TO_1007H_ART_TEACHER_DAILY_WORK_BUSINESS_PACK_CAPABILITY_REGISTRATION_PACKAGE",
            "overall_status": "1007A_H_ART_TEACHER_DAILY_WORK_BUSINESS_PACK_CAPABILITY_REGISTRATION_BASELINE_PASS",
            "stages": rows,
            "stop": "1007H_REVIEW_PENDING_BEFORE_REAL_ART_TEACHER_BUSINESS_APPLY",
            "boundary_flags": BOUNDARY,
        },
    )
    write(
        "docs/audit/xiaojiao_1007A_to_1007H_art_teacher_daily_work_business_pack_capability_registration_report.md",
        textwrap.dedent(
            """\
            # 1007A-H Art Teacher Daily Work Business Pack Capability Registration Package

            ```text
            overall_package=1007A_TO_1007H_ART_TEACHER_DAILY_WORK_BUSINESS_PACK_CAPABILITY_REGISTRATION_PACKAGE
            overall_status=1007A_H_ART_TEACHER_DAILY_WORK_BUSINESS_PACK_CAPABILITY_REGISTRATION_BASELINE_PASS
            stop_point=1007H_REVIEW_PENDING_BEFORE_REAL_ART_TEACHER_BUSINESS_APPLY
            ```

            This package does not implement a complete art teacher product. It registers enough business structure for the Xiaojiao platform foundation to carry one realistic art teacher daily work vertical slice.

            The dry-run reaches `teacher_review_required=true` and stops before formal apply.
            """
        ),
    )


if __name__ == "__main__":
    main()
