# Change Policy

This policy defines how changes should be categorized, reviewed, validated, and documented.

## Minor Change

A local change with low regression risk and no schema impact.

Examples:
- template wording changes
- small UI improvements
- documentation corrections
- harmless refactors inside a function

Required actions:
- local validation
- update documentation if behavior changed

## Moderate Change

A workflow-affecting change that touches behavior but not the overall architecture.

Examples:
- form logic changes
- route/view/template chain improvements
- new templates for existing flows
- import workflow refinements
- status handling changes without schema redesign

Required actions:
- targeted tests or test updates
- system check
- contract/workflow doc updates

## Major Change

A change with structural, architectural, or schema-level impact.

Examples:
- model field changes
- migrations that affect stable data contracts
- authentication model changes
- route renaming affecting external or internal contracts
- major directory restructuring

Required actions:
- explicit plan before implementation
- documentation updates across governance/contracts/workflows as needed
- validation plan
- baseline-freeze review if stable contracts were altered
