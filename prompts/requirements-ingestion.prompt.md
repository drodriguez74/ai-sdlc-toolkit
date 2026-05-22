---
name: requirements-ingestion
description: Parse a stakeholder document (BRD/PDF/DOCX/CSV) into structured requirements.
skills:
  - using-agent-skills
  - requirements-ingestion
agent: requirements-analyst
---

# /requirements-ingestion — Parse Requirements Document

## Goal

Turn an unstructured stakeholder document into a structured requirements list
with stable IDs.

## Instructions

1. Load `skills/using-agent-skills/SKILL.md`.
2. Follow `skills/requirements-ingestion/SKILL.md`.
3. Adopt `requirements-analyst` perspective.

## Output

Structured requirement list: ID, statement, classification, source location,
ambiguity flags.
