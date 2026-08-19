import os
from datetime import datetime
from config import REPORT_DIR

SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2, "info": 3}


def _fmt(value):
    return "-" if value is None else value


def build_report_html(statement, findings: list) -> str:
    sorted_findings = sorted(findings, key=lambda f: SEVERITY_ORDER.get(f.severity, 4))

    rows = "\n".join(
        f"""
        <tr>
            <td>{f.check_type}</td>
            <td>{f.location or '-'}</td>
            <td>{f.severity}</td>
            <td>{f.description}</td>
            <td>{_fmt(f.reported_value)}</td>
            <td>{_fmt(f.expected_value)}</td>
            <td>{_fmt(f.difference)}</td>
            <td>{f.explanation or '-'}</td>
        </tr>
        """
        for f in sorted_findings
    )

    html = f"""
    <html>
    <head>
        <title>Audit Report - {statement.filename}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; vertical-align: top; }}
            th {{ background-color: #f0f0f0; }}
        </style>
    </head>
    <body>
        <h1>Financial Statement Audit Report</h1>
        <p><strong>Statement:</strong> {statement.filename}</p>
        <p><strong>Generated:</strong> {datetime.utcnow().isoformat()}</p>
        <p><strong>Total Findings:</strong> {len(findings)}</p>
        <table>
            <tr>
                <th>Check Type</th>
                <th>Location</th>
                <th>Severity</th>
                <th>Description</th>
                <th>Reported</th>
                <th>Expected</th>
                <th>Difference</th>
                <th>Explanation</th>
            </tr>
            {rows}
        </table>
    </body>
    </html>
    """

    output_path = os.path.join(REPORT_DIR, f"report_{statement.id}.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    return output_path
