import json
from datetime import datetime, timezone
from pathlib import Path


def before_scenario(context, scenario):
    context.run_started = datetime.now(timezone.utc).isoformat()
    context.steps = []
    context.report_path = Path(__file__).resolve().parent.parent / "artifacts" / "cucumber_report.json"


def after_step(context, step):
    status = step.status.name.lower()
    exception = getattr(step, "exception", None)
    step_error = getattr(step, "error_message", None)
    item = {"name": step.name, "status": status}
    if exception or step_error:
        item["error"] = str(exception or step_error)
        context.failure = item["error"]
    context.steps.append(item)


def after_scenario(context, scenario):
    if getattr(context, "page", None) and scenario.status.name.lower() in {"failed", "error"}:
        try:
            context.page.screenshot(path=str(context.report_path.parent / "failure.png"), full_page=True)
        except Exception:
            pass

    report = {
        "scenario": scenario.name,
        "status": scenario.status.name.lower(),
        "started_at_utc": context.run_started,
        "finished_at_utc": datetime.now(timezone.utc).isoformat(),
        "steps": context.steps,
        "route": getattr(context, "route", None),
        "selected_flight_price": getattr(context, "flight_price", None),
        "confirmation": getattr(context, "confirmation", None),
        "order_id": getattr(context, "order_id", None),
        "customer_data_source": "Cohere LLM",
        "error": getattr(context, "failure", None),
    }

    context.report_path.parent.mkdir(parents=True, exist_ok=True)
    context.report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    lines = [
        "# BlazeDemo BDD Cucumber Execution Report",
        "",
        f"- Scenario: {report['scenario']}",
        f"- Status: {report['status'].upper()}",
        f"- Started (UTC): {report['started_at_utc']}",
        f"- Finished (UTC): {report['finished_at_utc']}",
        f"- Route: {report['route']}",
        f"- Selected Price: ${report['selected_flight_price']}",
        f"- Confirmation: {report['confirmation']}",
        f"- Order ID: {report['order_id']}",
        "",
        "## Step Results",
        ""
    ]
    lines += [f"- **{s['status'].upper()}**: {s['name']}" + (f" - *Error: {s['error']}*" if s.get("error") else "") for s in report["steps"]]
    if report["error"] and not any(s.get("error") for s in report["steps"]):
        lines += ["", "## Failure Diagnostics", "", report["error"]]

    (context.report_path.parent / "cucumber_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    if getattr(context, "browser", None):
        context.browser.close()
    if getattr(context, "playwright", None):
        context.playwright.stop()
