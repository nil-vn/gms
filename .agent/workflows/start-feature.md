---
description: How to start implementing a new feature from specifications
---

# Start Feature Implementation

Use this workflow when beginning work on a new feature.

## Step 1: Identify Feature

From `implementation_plan.md` or `task.md`, identify the feature to implement.

Example: "Token Bucket Rate Limiter"

## Step 2: Locate Specification

// turbo
Search for the specification document:

```powershell
# Find spec file
Get-ChildItem -Path "C:\Users\Dell\.gemini\antigravity\brain\12a18035-8d69-4205-85f0-6e2db2f28cb3" -Filter "*.md" | Select-String -Pattern "Token Bucket"
```

## Step 3: Read Specification (PM)

Open and review the specification document completely:

**Key sections to review**:
- Feature description
- Database schema requirements
- API interfaces
- Performance requirements
- Dependencies

**Questions to answer**:
- What exactly needs to be implemented?
- What are the inputs/outputs?
- What are the constraints?
- What components does this interact with?

## Step 4: Audit Existing Codebase (MANDATORY)

**Check what's already implemented:**

// turbo
```powershell
# Review project documentation
cat "d:\nil\antigravity\apps\v4\docs\PROJECT_OVERVIEW.md"
cat "d:\nil\antigravity\apps\v4\docs\PHASE_DETAILS.md"
cat "d:\nil\antigravity\apps\v4\.agent\status.md"
```

**Search for reusable code:**

// turbo
```powershell
# Find similar implementations
Get-ChildItem -Path "d:\nil\antigravity\apps\v4\src-tauri\src" -Recurse -Filter "*.rs" | Select-String -Pattern "RwLock|Semaphore|Arc"

# List all services
Get-ChildItem -Path "d:\nil\antigravity\apps\v4\src-tauri\src\services" -Filter "*.rs"
```

**Reusability Checklist:**
- [ ] What features are already implemented?
- [ ] Are there similar patterns I can follow?
- [ ] Can I reuse existing structs/traits?
- [ ] Are there helper functions I can use?
- [ ] What database queries already exist?

**Examples to look for:**
- Thread-safe patterns (`Arc<RwLock<T>>`)
- Database access patterns
- Event emission patterns
- Error handling patterns
- Async/await patterns

## Step 5: Create Implementation Notes

Create a markdown file: `.agent/notes/[feature-name].md`

```markdown
# [Feature Name] Implementation Notes

**Specification**: [path/to/spec.md]
**Section**: [specific section]

## Scope

### Must Implement:
- [ ] Component A
- [ ] Component B
- [ ] Tests for all components

### Must Not:
- Anything not in specification
- Performance optimizations beyond spec

## Dependencies

**Files to modify**:
- `src/services/[module].rs`
- `src/db/schema.rs`

**Database changes**:
- Add table X
- Add index Y

**External crates**:
- tokio = "1.x"
- sqlx = "0.7"

## Test Plan

### Unit Tests:
- Test behavior A
- Test behavior B
- Test edge case C

### Integration Tests:
- Test with database
- Test with mock API

## Performance Requirements

From spec:
- Operation must complete in < 1ms
- Memory usage < 10 MB
- Zero allocations in hot path
```

## Step 5: Create Feature Branch

// turbo
```powershell
git checkout -b feature/[feature-name]
```

## Step 6: Begin TDD Cycle

Follow the TDD workflow from `implement-feature.md`:

1. Write test
2. Run test (fails)
3. Implement code
4. Run test (passes)
5. Refactor

## Step 7: Reference Implementation

When implementing, add spec reference in code:

```rust
// Specification: production_account_manager.md - Token Bucket Algorithm
// Implements rate limiting layer from 3-tier protection system
pub struct TokenBucket {
    // ...
}
```

---

**Now proceed to implement-feature.md workflow**
