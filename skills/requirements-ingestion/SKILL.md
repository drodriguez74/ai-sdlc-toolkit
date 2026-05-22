---
name: requirements-ingestion
description: Parse BRD/PDF/DOCX/CSV requirements documents into structured form. Use when stakeholders provide requirements in business document form.
---

# Requirements Ingestion (Integration Skill)

## Overview

Requirements often arrive as PDFs, Word docs, or spreadsheets. This skill turns
them into structured form that subsequent agents can consume.

## When To Use

When stakeholders provide requirements in non-structured document form.

## Workflow

1. Identify the document format and structure (table of contents, sections).
2. Extract requirements as discrete statements with stable IDs.
3. Classify each: functional, non-functional, constraint, assumption, out-of-scope.
4. Capture source location (page number, section) for traceability.
5. Hand structured output to `requirements-analyst` for traceability mapping.

## Evidence And Verification

- Each requirement has a stable ID and source citation.
- Classification covers all requirements.
- Ambiguities are flagged, not silently resolved.

## Common Rationalizations

- "I'll just summarize the doc" — summary loses traceability.
- "Ambiguity is fine; I can fill the gap" — silent gap-filling is how scope creeps.

## Red Flags

- Requirements list without source citations.
- Ambiguous requirements rewritten to look clear without confirmation.

## Output Contract

Structured requirement list: ID, statement, classification, source location,
flags for ambiguity.

## Dependencies

This skill may require optional Python packages for parsing (e.g.,
`pdfplumber`, `python-docx`). Declare them in `requirements.txt` within this
skill directory. They are not core toolkit dependencies.
