# MindForgeAI Industry Project — Master Workspace

This repository is the official Chatake Innoworks template for every Internship 1.0 industry project. The Program Office creates one company-owned repository per active project from this template. Students clone their assigned project repository—not this master template—and preserve the standard structure.

## First setup

1. Open the project repository assigned to your group under the `Chatake-Innoworks` GitHub organization.
2. Clone that assigned repository and open it in VS Code.
3. Read `00_project_governance/WORKING_RULES.md` and `00_project_governance/OWNERSHIP_AND_ACCESS.md` with the complete team.
4. Run `scripts/create_member_workspace.ps1 STUDENT_ID` on Windows PowerShell or `bash scripts/create_member_workspace.sh STUDENT_ID` on macOS/Linux.
5. Each member copies their existing current working folder into their generated folder under `04_active_workspaces/`.
6. Create a branch named `member/STUDENT-ID/short-task-name` before making project changes.
7. Move only reviewed, team-approved work into `05_shared_integration/` and then the relevant production folder through a pull request.
8. Record sources, decisions, tasks and diary entries as the work happens.

## Repository map

| Folder | Purpose |
|---|---|
| `00_project_governance` | team charter, roles, working rules and quality gates |
| `01_project_definition` | title, structured abstract, scope, requirements and architecture |
| `02_research_and_sources` | literature, web research log, citations and source assessments |
| `03_data_and_resources` | data documentation, licences, resource inventory and non-secret setup notes |
| `04_active_workspaces` | one isolated current working folder per student |
| `05_shared_integration` | reviewed work waiting for integration into the common solution |
| `06_code` | stable source, notebooks, tests, configuration and reusable scripts |
| `07_models_and_artifacts` | versioned model metadata and reproducible output manifests; avoid huge binaries in Git |
| `08_project_report` | chapter-wise report, drafts, figures, tables and references |
| `09_project_diaries` | separate group and individual daily project diaries |
| `10_management` | tasks, meeting records, decisions, risks and change notes |
| `11_deployment` | container, cloud, monitoring, rollback and runbook assets |
| `12_presentation_and_demo` | slides, demo script, screenshots, rehearsal and backup demo |
| `13_release_and_handover` | final release, checksums, installation, user guide and handover |
| `14_publication_and_portfolio` | approved public project profile, publication checklist and showcase assets |
| `study_material` | approved learning material relevant to this project |

## Branch and review model

- `main`: reviewed and demonstrable group state.
- `develop`: integrated work for the next stable checkpoint.
- `member/<student-id>/<task>`: individual task branch.
- No member pushes experimental code directly to `main`.
- A merge requires a pull request, meaningful commit message, evidence of testing and team awareness.
- Student Codex/AI agents may push only through the authenticated student's branch and permissions.
- Company credentials, owner tokens and shared access tokens must never be given to a student or an AI agent.

## Security

Never commit passwords, API keys, AWS credentials, private student data, `.env` files, service-account JSON, raw identity documents or proprietary datasets. Commit `.env.example` with placeholder names only.

## Portal relationship

The online Project Portal is the shared operational record. This repository is the technical and document workspace. Update both deliberately:

- Portal: tasks, daily diary, abstract/report working text, notes and links.
- Repository: code, notebooks, tests, formal report source, diagrams, deployment assets and evidence.
- Printed diary: signed physical group record.

## Publication relationship

The repository remains the technical source of truth. Only reviewed material is published through `projects.chatakeinnoworks.com`. Public project pages must use the approved content in `14_publication_and_portfolio/` and must not expose private data, secrets, restricted datasets or unapproved company material.
