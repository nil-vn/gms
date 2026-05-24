---
description: Complete feature implementation workflow with PM, Dev, and QA roles
---

# Feature Implementation Workflow

This workflow ensures high-quality, specification-compliant implementation.

## Prerequisites

- All specification documents reviewed
- Feature defined in implementation plan
- Dependencies identified

## Phase 1: Planning (PM Role)

### 1. Review Specifications

**Read these documents:**
- Architecture Design: `C:\Users\Dell\.gemini\antigravity\brain\12a18035-8d69-4205-85f0-6e2db2f28cb3\architecture_design.md`
- Technical Recommendations: `C:\Users\Dell\.gemini\antigravity\brain\12a18035-8d69-4205-85f0-6e2db2f28cb3\technical_recommendations.md`
- Related feature specs in brain directory

### 2. Define Scope

```markdown
## Feature: [Name]

**Specification**: [path/to/spec.md]
**Section**: [specific section in spec]

**In Scope**:
- [ ] Item 1 from spec
- [ ] Item 2 from spec

**Out of Scope**:
- Not in specification
- Future enhancements
```

### 3. Identify Dependencies

- Database schema changes
- Related components
- External libraries
- UI components

### 5. Audit Existing Code for Reusability (MANDATORY)

**Before writing ANY new code, check what exists:**

```powershell
# Review project status
cat "d:\nil\antigravity\apps\v4\docs\PROJECT_OVERVIEW.md"
cat "d:\nil\antigravity\apps\v4\docs\PHASE_DETAILS.md"
cat "d:\nil\antigravity\apps\v4\.agent\status.md"

# Search for similar patterns
Get-ChildItem -Path "d:\nil\antigravity\apps\v4\src-tauri\src" -Recurse -Filter "*.rs" | Select-String -Pattern "[search_term]"

# List existing services
Get-ChildItem -Path "d:\nil\antigravity\apps\v4\src-tauri\src\services" -Filter "*.rs"
```

**Reusability Questions:**
- [ ] Is there similar code I can inherit/extend?
- [ ] Can I reuse existing traits?
- [ ] Are there helper functions I can use?
- [ ] What patterns are already established?
- [ ] Can I extract common logic from existing code?

**Common Reusable Patterns:**
- `Arc<RwLock<T>>` for thread-safe state
- `Database` struct for queries
- `VideoGenerationProvider` trait
- Event emission helpers
- Error types from `error.rs`

**Rule**: Reuse > Refactor > Write New

### 6. Create Feature Branch

```powershell
git checkout -b feature/[feature-name]
```

## Phase 2: Development (Senior Rust Dev Role)

### 1. Write Tests First (TDD)

```rust
#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_feature_behavior() {
        // Arrange
        let input = /* test data */;
        
        // Act
        let result = feature_function(input);
        
        // Assert
        assert_eq!(result, expected);
    }
}
```

### 2. Run Tests (Should Fail)

```powershell
cargo test test_feature_behavior
```

Expected: ❌ Test fails (not implemented yet)

### 3. Implement Minimum Code

Follow performance rules from `senior-rust-dev.md`:
- Avoid unnecessary allocations
- Use references when possible
- Pre-allocate collections
- Keep lock scopes minimal

### 4. Run Tests (Should Pass)

```powershell
cargo test test_feature_behavior
```

Expected: ✅ Test passes

### 5. Refactor

Improve code while keeping tests green:
- Extract functions
- Improve naming
- Add documentation
- Optimize performance

## Phase 3: Quality Assurance (QA Role)

### Gate 1: Unit Tests

```powershell
cargo test
```

**Pass Criteria**: All tests pass
**If Failed**: Report to senior-rust-dev

### Gate 2: Cargo Check

```powershell
cargo check
```

**Pass Criteria**: No compilation errors
**If Failed**: Review and fix type errors

### Gate 3: Clippy

```powershell
cargo clippy -- -D warnings
```

**Pass Criteria**: Zero warnings
**If Failed**: Fix all clippy suggestions

### Gate 4: Build

```powershell
cargo build --release
```

**Pass Criteria**: Build succeeds
**If Failed**: Fix build errors

### Gate 5: Integration Tests

```powershell
cargo test --test '*'
```

**Pass Criteria**: All integration tests pass
**If Failed**: Fix integration issues

### Gate 6: Runtime Verification

```powershell
cargo tauri dev
```

**Manual Checks**:
- Feature works as specified
- No runtime errors
- UI displays correctly
- Performance acceptable

## Phase 4: Documentation (PM Role)

### 1. Update Status Log

Edit `.agent/status.md`:

```markdown
## [Date] - [Feature Name]

**Specification**: [spec_file.md]
**Status**: ✅ Completed

**Implementation**:
- Implemented X according to spec section Y
- Added tests for all public functions
- Verified performance requirements

**Tests Added**:
- Unit tests: 5
- Integration tests: 2
- All passing

**QA Results**:
- [x] Unit tests pass
- [x] Cargo check pass
- [x] Clippy clean
- [x] Build success
- [x] Integration tests pass
- [x] Runtime verified

**Performance**:
- Test suite: +1.2s
- Build time: +5s
- Binary size: +150 KB
```

### 2. Update Task Checklist

Edit `C:\Users\Dell\.gemini\antigravity\brain\12a18035-8d69-4205-85f0-6e2db2f28cb3\task.md`:

```markdown
### Phase [N]: [Phase Name]
- [x] Feature implemented  # Mark complete
- [ ] Next feature
```

### 3. Commit Changes

```powershell
git add .
git commit -m "feat: implement [feature] per spec

- Implemented [component] from [spec.md]
- Added unit tests with 100% coverage
- Verified performance requirements
- All QA gates passed

Refs: [spec.md#section]"
```

## Phase 5: Integration (All Roles)

### PM: Verify Scope

- [ ] Only specified features implemented
- [ ] No feature creep
- [ ] Matches specification exactly

### Dev: Code Review Checklist

- [ ] All public functions documented
- [ ] Performance rules followed
- [ ] No unsafe without justification
- [ ] Error handling complete

### QA: Final Validation

- [ ] All 6 gates passed
- [ ] No regressions
- [ ] Manual testing complete

## Example: Implementing Token Bucket

### PM Phase

**Specification**: `production_account_manager.md` - Token Bucket Algorithm
**Scope**: 
- Token capacity
- Refill rate
- Acquire method
- Thread-safe implementation

### Dev Phase

```rust
// Test first
#[test]
fn test_token_bucket_refill() {
    let bucket = TokenBucket::new(10.0, 0.5);
    // Test implementation...
}

// Implementation
pub struct TokenBucket {
    capacity: f64,
    refill_rate: f64,
    tokens: Arc<RwLock<f64>>,
    last_refill: Arc<RwLock<Instant>>,
}
```

### QA Phase

```powershell
cargo test  # ✅ Pass
cargo clippy  # ✅ Zero warnings
cargo build --release  # ✅ Success
```

### Documentation

```markdown
## 2026-02-13 - Token Bucket Rate Limiter

**Specification**: production_account_manager.md (Layer 2)
**Status**: ✅ Completed

**Implementation**:
- Thread-safe token bucket with RwLock
- Configurable capacity and refill rate
- Automatic refill on acquire

**Tests**: 3 unit tests, all passing
**Performance**: <1μs per acquire operation
```

---

**Follow this workflow for EVERY feature implementation**
