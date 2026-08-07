# Aethera v0.1.0 release lock

**Release class:** internship prototype / non-operational demonstration  
**Locked on:** 2026-08-07  
**Purpose:** preserve the reviewed baseline before data and ML development begins.

## Locked delivery artifact

- Archive: `06_code/dist/aethera-deployment-0.1.0.zip`
- SHA-256: `B8A4400AD34363070979FE515C18A8BA66BAA4C04767E3F676691BB3F71588D3`
- Validation: application test suite passed (`3 tests`) before lock.

## What this lock means

The archive is the immutable reference copy of the prototype as delivered. Do not edit it. New development happens on a new Git branch and is released under a new version/archive only after review. This is a release lock, not a claim that the software is production-ready.

## Change control

1. Create an issue and Git branch for every change.
2. Record data/model versions for any new intelligence feature.
3. Require teammate review and passing tests before merge.
4. Update `CHANGELOG.md`, test evidence and deployment manifest.
5. Create a new archive and SHA-256 checksum; never overwrite the historical lock.

## Immediate next release goal

`v0.2.0-data-foundation`: one documented pilot dataset powering at least one dashboard view, with no unsupported operational claims.
