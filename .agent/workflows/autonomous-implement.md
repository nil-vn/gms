---
description: Fully autonomous implementation workflow (user can AFK)
---

# Autonomous Implementation Workflow

**Goal**: Implement features completely autonomously while user is AFK. No questions asked.

---

## 🚀 Activation

User says:
> "Implement [Phase/Feature] autonomously"

You respond:
> "Starting autonomous implementation. You can AFK, I'll report when done."

Then proceed with ZERO user interaction until completion or critical failure.

---

## 📋 Pre-Implementation Checklist (MANDATORY)

Before writing ANY code:

### 1. Review ALL Specification Documents

**Read these files completely:**

```powershell
# Architecture & Design
cat "C:\Users\Dell\.gemini\antigravity\brain\12a18035-8d69-4205-85f0-6e2db2f28cb3\architecture_design.md"
cat "C:\Users\Dell\.gemini\antigravity\brain\12a18035-8d69-4205-85f0-6e2db2f28cb3\technical_recommendations.md"
cat "C:\Users\Dell\.gemini\antigravity\brain\12a18035-8d69-4205-85f0-6e2db2f28cb3\brainstorming_summary.md"

# UI/UX
cat "C:\Users\Dell\.gemini\antigravity\brain\12a18035-8d69-4205-85f0-6e2db2f28cb3\ui_ux_specification.md"
cat "C:\Users\Dell\.gemini\antigravity\brain\12a18035-8d69-4205-85f0-6e2db2f28cb3\system_status_spec.md"

# Multi-Account
cat "C:\Users\Dell\.gemini\antigravity\brain\12a18035-8d69-4205-85f0-6e2db2f28cb3\multi_account_architecture.md"
cat "C:\Users\Dell\.gemini\antigravity\brain\12a18035-8d69-4205-85f0-6e2db2f28cb3\provider_detection_spec.md"
cat "C:\Users\Dell\.gemini\antigravity\brain\12a18035-8d69-4205-85f0-6e2db2f28cb3\auto_resume_spec.md"

# Protection System
cat "C:\Users\Dell\.gemini\antigravity\brain\12a18035-8d69-4205-85f0-6e2db2f28cb3\production_account_manager.md"
cat "C:\Users\Dell\.gemini\antigravity\brain\12a18035-8d69-4205-85f0-6e2db2f28cb3\advanced_settings_spec.md"
cat "C:\Users\Dell\.gemini\antigravity\brain\12a18035-8d69-4205-85f0-6e2db2f28cb3\burst_detection_spec.md"
cat "C:\Users\Dell\.gemini\antigravity\brain\12a18035-8d69-4205-85f0-6e2db2f28cb3\escalation_system_spec.md"
cat "C:\Users\Dell\.gemini\antigravity\brain\12a18035-8d69-4205-85f0-6e2db2f28cb3\protection_database_schema.md"
cat "C:\Users\Dell\.gemini\antigravity\brain\12a18035-8d69-4205-85f0-6e2db2f28cb3\3_tier_protection_system.md"

# UX Engineering
cat "C:\Users\Dell\.gemini\antigravity\brain\12a18035-8d69-4205-85f0-6e2db2f28cb3\perceived_performance_engineering.md"
cat "C:\Users\Dell\.gemini\antigravity\brain\12a18035-8d69-4205-85f0-6e2db2f28cb3\mock_api_specification.md"

# Implementation Plan
cat "C:\Users\Dell\.gemini\antigravity\brain\12a18035-8d69-4205-85f0-6e2db2f28cb3\implementation_plan.md"
cat "C:\Users\Dell\.gemini\antigravity\brain\12a18035-8d69-4205-85f0-6e2db2f28cb3\task.md"
```

### 2. Review Project Documentation (MANDATORY)

**Read project docs to understand implementation status:**

```powershell
# Review current project status
cat "d:\nil\antigravity\apps\v4\docs\PROJECT_OVERVIEW.md"
cat "d:\nil\antigravity\apps\v4\docs\PHASE_DETAILS.md"
cat "d:\nil\antigravity\apps\v4\.agent\status.md"
```

**Key questions to answer:**
- [ ] Which features are already implemented?
- [ ] Which features are pending?
- [ ] What is the current phase status?
- [ ] Are there related features I can reference?

### 3. Audit Existing Codebase for Reusability

**CRITICAL: Always reuse before writing new code**

```powershell
# Search for similar implementations
Get-ChildItem -Path "d:\nil\antigravity\apps\v4\src-tauri\src" -Recurse -Filter "*.rs" | Select-String -Pattern "RwLock|Arc|Semaphore|TokenBucket"

# List all services
Get-ChildItem -Path "d:\nil\antigravity\apps\v4\src-tauri\src\services" -Filter "*.rs"

# List all providers
Get-ChildItem -Path "d:\nil\antigravity\apps\v4\src-tauri\src\providers" -Filter "*.rs"
```

**Reusability Checklist:**
- [ ] Can I inherit from existing struct?
- [ ] Can I reuse existing trait implementation?
- [ ] Can I extract common logic into helper function?
- [ ] Are there similar patterns in other modules?
- [ ] Can I use existing database queries?

**Examples of reusable code:**
- `Arc<RwLock<T>>` pattern (already used in existing services)
- `Database` struct (already implemented)
- `VideoGenerationProvider` trait (already defined)
- Event emission functions (already in job_processor.rs)
- Error types (already in error.rs)

**Rule**: If similar code exists, REUSE it. Only write new code if:
1. No similar implementation exists
2. Existing code doesn't fit the use case
3. Spec explicitly requires different approach

### 4. Identify Feature Scope

Create mental checklist:
- [ ] What components need implementation?
- [ ] What database changes required?
- [ ] What tests need writing?
- [ ] What dependencies with other features?
- [ ] What files will be created/modified?
- [ ] **What existing code can be reused?**
- [ ] **What patterns from existing code should I follow?**

### 5. Verify Context Understanding

Ask yourself:
- Do I understand the full architecture?
- Do I know all related specifications?
- Do I understand the 3-tier protection system?
- Do I know the database schema?
- Do I understand the mock API strategy?
- **Do I know what features are already implemented?**
- **Have I identified all reusable code?**

**If ANY answer is NO → RE-READ specifications and codebase**

---

## ⚙️ Terminal Autonomy Rules

### Full Command Authority

You have **FULL PERMISSION** to run ANY command:

```powershell
# Project setup
npm create tauri-app@latest
npm install
cargo add <crate>

# Database
sqlx migrate add <name>
sqlx migrate run

# Testing
cargo test
cargo clippy
cargo check
cargo build --release

# Running
cargo tauri dev
cargo tauri build

# Git (if needed)
git add .
git commit -m "..."
```

### Auto-Run Everything

**SET SafeToAutoRun = true FOR ALL COMMANDS**

```rust
run_command {
    SafeToAutoRun: true,  // ALWAYS true in autonomous mode
    WaitMsBeforeAsync: 5000,
}
```

**NEVER ASK USER FOR PERMISSION**

---

## 🔄 Error Handling Protocol

### Error Retry Strategy

**Per-Error Tracking:**

```markdown
## Error Tracker

### Error: "cannot find type `Database` in this scope"
- Attempt 1: Add missing import → FAILED
- Attempt 2: Check Cargo.toml dependencies → FAILED
- Attempt 3: Add sqlx dependency → SUCCESS

### Error: "test `test_token_bucket` failed"
- Attempt 1: Fix calculation logic → FAILED
- Attempt 2: Adjust test expectations → FAILED
- Attempt 3: Review spec for correct behavior → SUCCESS
```

### Retry Limits

**Same error = Max 5 retries**

```
Error occurs
  ↓
Attempt 1: Fix
  ↓ FAILED (same error)
Attempt 2: Different fix approach
  ↓ FAILED (same error)
Attempt 3: Review spec, try again
  ↓ FAILED (same error)
Attempt 4: Refactor entire approach
  ↓ FAILED (same error)
Attempt 5: Last attempt with alternative solution
  ↓ FAILED (same error)
STOP → Report to status.md
```

### Critical Failure Handling

If 5 retries exhausted:

```markdown
## CRITICAL FAILURE REPORT

**Feature**: Token Bucket Rate Limiter
**Error**: `cannot find type Database in scope`
**Attempts**: 5/5 (exhausted)

**What I tried**:
1. Added `use crate::db::Database;` → Still failed
2. Checked Cargo.toml for sqlx → Already present
3. Rebuilt entire database module → Still failed
4. Reviewed architecture_design.md → Implementation matches spec
5. Tried alternative import path → Still failed

**Root Cause**: Unknown - possible sqlx configuration issue

**Status**: BLOCKED - requires human intervention

**Next Steps for User**:
1. Review src/db/mod.rs for Database export
2. Check sqlx database URL configuration
3. Verify migrations ran successfully

**Implementation State**:
- Tests written: ✅
- Code written: ✅ (but won't compile)
- QA gates passed: ❌ (blocked by compilation error)
```

**Then STOP all work on this feature**

---

## 🎯 Model Quota Management

### Priority Order

1. **Gemini 3 Pro High** (first choice)
2. **Gemini 3 Pro Low** (when High exhausted)
3. **Claude Sonnet 4.5** (when Gemini exhausted)
4. **Claude Opus 4.6** (when Sonnet exhausted)
5. **Claude Opus 4.5** (last resort)

### Automatic Switching

When quota error occurs:

```
Using: Gemini 3 Pro High
  ↓
Error: "Quota exceeded for Gemini 3 Pro High"
  ↓
Switch to: Gemini 3 Pro Low
  ↓
Continue work seamlessly
```

**Log model switches in status.md:**

```markdown
## Model Usage Log

- Start: Gemini 3 Pro High
- 10:30 AM: Switched to Gemini 3 Pro Low (High quota exhausted)
- 11:45 AM: Switched to Claude Sonnet 4.5 (Gemini exhausted)
- Feature completed on: Claude Sonnet 4.5
```

### Total Quota Exhaustion

If ALL models exhausted:

```markdown
## QUOTA EXHAUSTION REPORT

**All models exhausted**: Gemini 3 Pro (High/Low), Sonnet 4.5, Opus 4.6, Opus 4.5

**Work completed before exhaustion**:
- Phase 1: 100% ✅
- Phase 2: 75% (3/4 tasks done)
- Phase 3: 0% (not started)

**Remaining work**:
- Phase 2: Scene retry mechanism
- Phase 3: Full phase
- Phase 4: Full phase
- Phase 5: Full phase

**Resume when quota resets**
```

**Then STOP all work**

---

## 🛡️ File Safety Rules

### Safe to Modify/Delete

**ONLY files related to current feature:**

```
Working on: Token Bucket Rate Limiter

✅ CAN modify/delete:
- src/services/rate_limiter.rs (feature file)
- tests/rate_limiter_tests.rs (feature tests)
- src/services/mod.rs (to add export)

❌ CANNOT modify/delete:
- src/services/pipeline.rs (unrelated feature)
- src/db/schema.rs (unless spec requires it)
- src/main.rs (unless spec requires it)
```

### Modification Rules

**Before modifying ANY file:**

1. Check: Is this file mentioned in spec?
2. Check: Does feature require changing this file?
3. Check: Will this break existing features?

**If unsure → Don't modify**

### Deletion Rules

**Before deleting ANY file:**

1. Confirm: File is obsolete/replaced
2. Confirm: No other features depend on it
3. Confirm: Spec explicitly says to remove it

**If ANY doubt → Don't delete**

### Safety Checklist

Before each file operation:

```markdown
## File Operation Safety Check

**Operation**: Modify src/services/account.rs
**Reason**: Add health score calculation (per spec)

Safety checks:
- [ ] File mentioned in production_account_manager.md? YES
- [ ] Feature requires this change? YES
- [ ] Will break existing features? NO (only adding method)
- [ ] Other files depend on this? YES (but backwards compatible)

**Decision**: ✅ SAFE TO MODIFY
```

---

## 📊 Progress Reporting

### Continuous Status Updates

Update `.agent/status.md` after EVERY significant step:

```markdown
## [Timestamp] - Progress Update

**Phase**: 1 - Project Scaffolding
**Task**: Initialize Tauri project
**Status**: In Progress

**Completed**:
- [x] Reviewed all specification documents (15 mins)
- [x] Ran `npm create tauri-app@latest` (2 mins)
- [x] Selected Svelte + TypeScript (automated)
- [x] Project structure created

**In Progress**:
- [ ] Installing dependencies (running...)

**Blocked**: None
**Errors**: None
**Model**: Gemini 3 Pro High
```

### Milestone Updates

After each major milestone:

```markdown
## [Timestamp] - Milestone: Database Setup Complete

**Phase 1 Progress**: 50% (4/8 tasks)

**Completed Tasks**:
1. ✅ Tauri project initialized
2. ✅ Dependencies installed
3. ✅ Database migrations created
4. ✅ Schema applied

**Next Tasks**:
5. ⏳ Create mock API provider
6. ⏳ Generate dummy video
7. ⏳ Verify app launches
8. ⏳ Update task.md

**Performance**:
- Time elapsed: 45 minutes
- Commands run: 12
- Tests passed: 3/3
- Build status: ✅ Success

**Issues**: None
```

---

## 🔁 Complete Workflow Example

### Starting Autonomous Implementation

**User Request:**
> "Implement Phase 1 autonomously"

**Your Response:**
> "Starting Phase 1 autonomous implementation. Reviewing 17 specification documents and implementation plan. You can AFK, I'll report completion or any critical failures."

### Execution Flow

```
1. Read all 17 specification documents [Auto]
   ↓
2. Read implementation_plan.md Phase 1 [Auto]
   ↓
3. Create task breakdown in status.md [Auto]
   ↓
4. npm create tauri-app@latest [Auto, SafeToAutoRun: true]
   ↓
5. Install dependencies [Auto]
   ↓
6. Create database migrations [Auto]
   ↓
7. Write tests (TDD) [Auto]
   ↓
8. cargo test → FAILED [Auto]
   ↓
9. Implement code to pass tests [Auto]
   ↓
10. cargo test → PASSED [Auto]
    ↓
11. cargo clippy → 2 warnings [Auto]
    ↓
12. Fix clippy warnings [Auto]
    ↓
13. cargo clippy → CLEAN [Auto]
    ↓
14. cargo build --release → SUCCESS [Auto]
    ↓
15. Update status.md with completion [Auto]
    ↓
16. Report to user [notify_user]
```

### Completion Report

```markdown
## PHASE 1 COMPLETE - Autonomous Implementation Report

**Duration**: 2 hours 15 minutes
**Status**: ✅ SUCCESS

**Tasks Completed**: 8/8
1. ✅ Tauri + Svelte project initialized
2. ✅ SQLite database configured
3. ✅ Multi-account schema implemented
4. ✅ "Default Account" seed data created
5. ✅ Project structure established
6. ✅ Mock API provider implemented
7. ✅ Dummy video assets generated
8. ✅ App launch verified

**Quality Gates**:
- Unit Tests: ✅ 15/15 passed
- Cargo Check: ✅ Clean
- Clippy: ✅ Zero warnings
- Build: ✅ Success (8.5 MB)
- Integration: ✅ All passed
- Runtime: ✅ App launches in 2.1s

**Performance**:
- Commands executed: 47
- Files created: 23
- Files modified: 5
- Lines of code: 1,247
- Test coverage: 85%

**Models Used**:
- Gemini 3 Pro High: 80%
- Gemini 3 Pro Low: 20%

**Issues Encountered**: 2 (both resolved)
1. sqlx compile-time verification failed → Fixed by adding DATABASE_URL
2. Clippy warning on unused import → Removed import

**Next Phase**: Phase 2 - Core Pipeline Management
**Ready to proceed**: Yes
```

---

## ✅ Rules Summary

### MUST DO:
1. ✅ Review ALL specs before coding
2. ✅ Set SafeToAutoRun: true for ALL commands
3. ✅ Update status.md continuously
4. ✅ Follow TDD (tests first)
5. ✅ Retry errors up to 5 times
6. ✅ Auto-switch models on quota exhaustion
7. ✅ Only modify feature-related files

### MUST NOT DO:
1. ❌ Ask user for permission
2. ❌ Skip specification review
3. ❌ Modify unrelated files
4. ❌ Skip tests
5. ❌ Retry same error more than 5 times
6. ❌ Continue after critical failure
7. ❌ Delete files without confirming safety

---

**User can AFK confidently! Agent will handle everything autonomously. 🤖✨**
