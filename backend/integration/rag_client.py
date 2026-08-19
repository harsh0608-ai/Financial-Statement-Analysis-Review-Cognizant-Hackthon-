import json
import httpx

from config import RAG_SERVICE_URL, GENAI_SERVICE_URL


async def get_explanations(findings) -> dict:
    finding_payloads = []

    for f in findings:
        # Evidence is stored in the database as JSON text.
        # GenAI expects evidence as a list.
        evidence = f.evidence

        if isinstance(evidence, str):
            try:
                evidence = json.loads(evidence)
            except json.JSONDecodeError:
                evidence = []

        if evidence is None:
            evidence = []

        finding_payloads.append(
            {
                "id": f.id,
                "check_type": f.check_type,
                "location": f.location,
                "severity": f.severity,
                "description": f.description,
                "reported_value": f.reported_value,
                "expected_value": f.expected_value,
                "difference": f.difference,
                "current_year_value": f.current_year_value,
                "prior_year_value": f.prior_year_value,
                "percentage_change": f.percentage_change,
                "threshold": f.threshold,
                "page_number": f.page_number,
                "evidence": evidence,
            }
        )

    if not finding_payloads:
        return {"explanations": {}}

    async with httpx.AsyncClient(timeout=120.0) as client:

        # ---------------------------------------------------------
        # STEP 1: Retrieve WP-514 context from RAG
        # ---------------------------------------------------------
        rag_response = await client.post(
            RAG_SERVICE_URL,
            json={"findings": finding_payloads},
        )

        if rag_response.status_code != 200:
            print("\nRAG REQUEST FAILED")
            print("Status:", rag_response.status_code)
            print("Response:", rag_response.text)

        rag_response.raise_for_status()

        rag_data = rag_response.json()

        explanations = {}

        # ---------------------------------------------------------
        # STEP 2: Send each finding + retrieved context to GenAI
        # ---------------------------------------------------------
        for result in rag_data.get("results", []):

            finding_id = result.get("finding_id")
            contexts = result.get("contexts", [])

            finding = next(
                (
                    f
                    for f in finding_payloads
                    if f["id"] == finding_id
                ),
                None,
            )

            if finding is None:
                print(f"Skipping unknown finding ID: {finding_id}")
                continue

            genai_payload = {
                "finding": finding,
                "contexts": contexts,
            }

            try:
                genai_response = await client.post(
                    GENAI_SERVICE_URL,
                    json=genai_payload,
                )

                # -------------------------------------------------
                # Do NOT abort the entire batch if one finding fails
                # -------------------------------------------------
                if genai_response.status_code != 200:
                    print("\n" + "=" * 70)
                    print("GENAI REQUEST FAILED")
                    print("=" * 70)
                    print("Finding ID:", finding_id)
                    print("Status:", genai_response.status_code)
                    print("Response:", genai_response.text)
                    print("=" * 70 + "\n")

                    continue

                genai_data = genai_response.json()

                explanation = genai_data.get("explanation")

                if explanation:
                    explanations[str(finding_id)] = explanation

            except httpx.RequestError as exc:
                print(
                    f"GenAI connection failed for finding "
                    f"{finding_id}: {exc}"
                )
                continue

            except Exception as exc:
                print(
                    f"GenAI processing failed for finding "
                    f"{finding_id}: {exc}"
                )
                continue

        # ---------------------------------------------------------
        # STEP 3: Return all successfully generated explanations
        # ---------------------------------------------------------
        return {
            "explanations": explanations
        }