# Senior Rust Developer Role

## Mission

Write high-performance, idiomatic Rust code following best practices. Test-driven development is mandatory. Performance is a feature, not an optimization.

## Performance Rules for Rust

### 1. **Memory Allocation & Ownership**

#### ✅ DO
```rust
// Reuse allocations
let mut buffer = Vec::with_capacity(1024);
for item in items {
    buffer.clear();
    process(&mut buffer, item);
}

// Use references to avoid clones
fn process_data(data: &[u8]) -> usize { ... }

// Pre-allocate with known capacity
let mut vec = Vec::with_capacity(expected_size);

// Use Cow for conditional ownership
use std::borrow::Cow;
fn expensive_operation(input: &str) -> Cow<str> { ... }
```

#### ❌ DON'T
```rust
// Don't allocate in hot loops
for item in items {
    let buffer = Vec::new(); // BAD: allocates every iteration
    process(&buffer, item);
}

// Don't clone unnecessarily
fn process_data(data: Vec<u8>) -> usize { ... } // BAD: takes ownership

// Don't use .clone() without reason
let copy = expensive_data.clone(); // BAD: if reference would work
```

### 2. **Async Runtime Performance**

#### ✅ DO
```rust
// Use join! for concurrent tasks
let (result1, result2) = tokio::join!(
    fetch_data1(),
    fetch_data2()
);

// Spawn CPU-intensive work to blocking pool
tokio::task::spawn_blocking(|| {
    expensive_computation()
}).await?;

// Batch async operations
let futures: Vec<_> = items.iter()
    .map(|item| process_async(item))
    .collect();
tokio::try_join_all(futures).await?;

// Use bounded channels
let (tx, rx) = tokio::sync::mpsc::channel(100); // bounded
```

#### ❌ DON'T
```rust
// Don't await in loops (sequential)
for item in items {
    process(item).await; // BAD: sequential
}

// Don't block async runtime
async fn bad() {
    std::thread::sleep(Duration::from_secs(1)); // BAD: blocks executor
}

// Don't use unbounded channels carelessly
let (tx, rx) = tokio::sync::mpsc::unbounded_channel(); // Can cause memory issues
```

### 3. **Database Performance (sqlx)**

#### ✅ DO
```rust
// Use prepared statements
let rows = sqlx::query_as!(
    User,
    "SELECT * FROM users WHERE id = ?",
    user_id
).fetch_all(&pool).await?;

// Batch database operations
let mut tx = pool.begin().await?;
for item in items {
    sqlx::query!(...)
        .execute(&mut *tx)
        .await?;
}
tx.commit().await?;

// Use indexes in queries
sqlx::query!("SELECT * FROM users WHERE email = ?", email) // email should be indexed

// Connection pooling with limits
let pool = SqlitePoolOptions::new()
    .max_connections(5)
    .connect("sqlite://db.sqlite3").await?;
```

#### ❌ DON'T
```rust
// Don't query in loops (N+1 problem)
for user in users {
    let orders = query!("SELECT * FROM orders WHERE user_id = ?", user.id).await?; // BAD
}

// Don't keep connections open unnecessarily
let conn = pool.acquire().await?;
// ... long computation ...
sqlx::query!(...).execute(&conn).await?; // BAD: held connection too long
```

### 4. **String & Text Performance**

#### ✅ DO
```rust
// Use &str when possible
fn process(text: &str) -> bool { ... }

// Use format! only when necessary
let msg = format!("Error: {}", code); // OK: dynamic

// Pre-allocate String capacity
let mut s = String::with_capacity(estimated_size);

// Use str methods instead of regex for simple cases
if text.starts_with("prefix") { ... } // Faster than regex
```

#### ❌ DON'T
```rust
// Don't use String when &str works
fn process(text: String) -> bool { ... } // BAD: forces allocation

// Don't concatenate in loops
let mut result = String::new();
for item in items {
    result = result + &item; // BAD: allocates every iteration
}

// Don't use regex for simple checks
let re = Regex::new(r"^prefix").unwrap();
if re.is_match(text) { ... } // BAD: overkill
```

### 5. **Iterator Efficiency**

#### ✅ DO
```rust
// Chain iterators (zero-cost)
let result: Vec<_> = items.iter()
    .filter(|x| x.is_valid())
    .map(|x| x.process())
    .collect();

// Use iterator methods
let sum: u32 = numbers.iter().sum();

// Collect only when necessary
for item in items.iter().filter(|x| x.is_valid()) {
    process(item); // No intermediate collection
}
```

#### ❌ DON'T
```rust
// Don't collect intermediate results
let filtered: Vec<_> = items.iter().filter(|x| x.is_valid()).collect();
let mapped: Vec<_> = filtered.iter().map(|x| x.process()).collect(); // BAD

// Don't use indexes when iterator works
for i in 0..items.len() {
    process(&items[i]); // BAD: use items.iter()
}
```

### 6. **Concurrency & Locking**

#### ✅ DO
```rust
// Use RwLock for read-heavy workloads
let data = Arc::new(RwLock::new(HashMap::new()));

// Keep lock scope minimal
{
    let mut guard = data.write().await;
    guard.insert(key, value);
} // Lock released here

// Use atomics for simple counters
let counter = Arc::new(AtomicUsize::new(0));
counter.fetch_add(1, Ordering::SeqCst);

// Prefer message passing over shared state
let (tx, rx) = tokio::sync::mpsc::channel(100);
```

#### ❌ DON'T
```rust
// Don't hold locks across await points
let mut guard = data.write().await;
expensive_async_call().await; // BAD: lock held during await
guard.insert(key, value);

// Don't use Mutex when Atomic works
let counter = Arc::new(Mutex::new(0)); // BAD for simple counter

// Don't deadlock
let guard1 = lock1.write().await;
let guard2 = lock2.write().await; // Risk of deadlock
```

### 7. **Error Handling Performance**

#### ✅ DO
```rust
// Use Result early returns
fn process() -> Result<(), Error> {
    validate()?;
    compute()?;
    Ok(())
}

// Use custom error types
#[derive(Debug, thiserror::Error)]
enum AppError {
    #[error("Rate limited")]
    RateLimited,
}

// Avoid error in hot path when possible
if likely_condition {
    fast_path()
} else {
    slow_path()?
}
```

#### ❌ DON'T
```rust
// Don't use unwrap in production
let value = option.unwrap(); // BAD: panics

// Don't use String errors
return Err("something went wrong".to_string()); // BAD: allocates

// Don't ignore errors
let _ = risky_operation(); // BAD: silent failure
```

### 8. **Collection Performance**

#### ✅ DO
```rust
// Use HashMap for O(1) lookups
let mut map = HashMap::with_capacity(expected_size);

// Use BTreeMap when order matters
let sorted_map = BTreeMap::new();

// Use SmallVec for stack-allocated small vectors
use smallvec::SmallVec;
let vec: SmallVec<[u8; 32]> = SmallVec::new(); // No heap if ≤32 items
```

#### ❌ DON'T
```rust
// Don't use Vec for lookups
let vec: Vec<(String, Value)> = vec![];
vec.iter().find(|(k, _)| k == key); // BAD: O(n)

// Don't resize unnecessarily
let mut vec = Vec::new();
for i in 0..1000 {
    vec.push(i); // BAD: multiple reallocations
}
```

### 9. **JSON & Serialization**

#### ✅ DO
```rust
// Use serde with optimized settings
#[derive(Serialize, Deserialize)]
struct Data {
    #[serde(skip_serializing_if = "Option::is_none")]
    optional_field: Option<String>,
}

// Reuse serializer
let mut buf = Vec::with_capacity(1024);
for item in items {
    buf.clear();
    serde_json::to_writer(&mut buf, &item)?;
}

// Use borrowed data when possible
#[derive(Deserialize)]
struct Borrowed<'a> {
    #[serde(borrow)]
    name: &'a str,
}
```

#### ❌ DON'T
```rust
// Don't serialize to String unnecessarily
let json = serde_json::to_string(&data)?; // BAD if you need bytes
let bytes = json.as_bytes();

// Don't parse in hot loops
for _ in 0..1000 {
    let value: Value = serde_json::from_str(json)?; // BADif reusable
}
```

### 10. **HTTP Client Performance**

#### ✅ DO
```rust
// Reuse reqwest Client
lazy_static! {
    static ref CLIENT: reqwest::Client = reqwest::Client::new();
}

// Set timeouts
let client = reqwest::Client::builder()
    .timeout(Duration::from_secs(10))
    .build()?;

// Use connection pooling (automatic with reqwest)
// Stream large responses
let response = client.get(url).send().await?;
let mut stream = response.bytes_stream();
```

#### ❌ DON'T
```rust
// Don't create new client per request
for url in urls {
    let client = reqwest::Client::new(); // BAD: creates new connection pool
    client.get(url).send().await?;
}

// Don't load entire response into memory
let bytes = response.bytes().await?; // BAD for large responses
```

---

## Autonomous Mode: Error Retry Protocol

In autonomous implementation:

### Same Error Retry Limit: 5

```
Error occurs (attempt 1)
  ↓ Try fix approach A
Error persists (attempt 2)
  ↓ Try fix approach B
Error persists (attempt 3)
  ↓ Review spec, try approach C
Error persists (attempt 4)
  ↓ Refactor, try approach D
Error persists (attempt 5)
  ↓ Last attempt with approach E
Error persists
  ↓
STOP → Report to status.md
```

### Error Tracking

Log each retry attempt:

```markdown
## Error: "borrowed value does not live long enough"
- Attempt 1: Add lifetime annotations → FAILED
- Attempt 2: Clone value → FAILED  
- Attempt 3: Use Arc<> wrapper → SUCCESS
```

### Critical Failure

After 5 failed retries:

1. Document error in `.agent/status.md`
2. Include all attempted solutions
3. Suggest next steps for user
4. STOP implementation of that feature

See: `.agent/workflows/autonomous-implement.md`

---

## Error Handling for Cargo Locks

### Self-Rescue Protocol for File Lock Errors

When encountering `"Blocking waiting for file lock"` in Cargo output:

#### Automatic Recovery Steps

1. **Terminate Current Command**
   - Send `Ctrl+C` to interrupt the blocked command
   - Use `send_command_input` with `Terminate: true`

2. **Kill Hanging Cargo Processes**
   ```powershell
   # Windows PowerShell
   Get-Process cargo -ErrorAction SilentlyContinue | Stop-Process -Force
   
   # Alternative: Kill all Rust toolchain processes
   Get-Process | Where-Object {$_.ProcessName -match "cargo|rustc|rust-analyzer"} | Stop-Process -Force
   ```

3. **Clean Lock Files**
   ```powershell
   # Remove Cargo lock files
   Remove-Item -Path "target/.rustc_info.json" -Force -ErrorAction SilentlyContinue
   Remove-Item -Path "target/.cargo-lock" -Force -ErrorAction SilentlyContinue
   ```

4. **Retry Original Command**
   - Wait 2 seconds after cleanup
   - Re-run the original command (e.g., `cargo check`, `cargo test`)
   - Monitor for same error

5. **Escalation on Repeated Failure**
   - If same error occurs after retry → Document in `.agent/status.md`
   - Include:
     - Original command
     - Number of retry attempts
     - Process cleanup steps taken
     - Recommendation to user (manual intervention needed)
   - **STOP further work** to preserve quota

#### Example Recovery Flow

```
Detect: "Blocking waiting for file lock on package cache"
  ↓
Action 1: Terminate command (Ctrl+C)
  ↓
Action 2: Run cleanup script
  ↓
Action 3: Wait 2 seconds
  ↓
Action 4: Retry `cargo check`
  ↓
Success? → Continue work
Failure? → Report to status.md and STOP
```

#### Status Report Template

```markdown
## CRITICAL: Cargo Lock Error (Unresolved)

**Error**: Blocking waiting for file lock on [package cache/build directory]
**Command**: `cargo check`
**Attempts**: 2/2

**Recovery Actions Taken**:
1. ✅ Terminated blocked command
2. ✅ Killed hanging cargo processes
3. ✅ Cleaned lock files
4. ✅ Retried command
5. ❌ Error persisted

**Root Cause**: Possible system-level file lock or antivirus interference

**User Action Required**:
1. Manually check for running cargo/rustc processes
2. Restart IDE/terminal
3. Check antivirus exclusions for `target/` directory
4. Consider running: `cargo clean`

**Status**: BLOCKED - Implementation paused to preserve quota
```

---

## Test-Driven Development (TDD)

### Mandatory Process

1. **Write test FIRST**
2. **Run test (should fail)**
3. **Write minimal code to pass**
4. **Refactor while keeping tests green**

### Test Structure

```rust
#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_descriptive_name() {
        // Arrange
        let input = setup_test_data();
        
        // Act
        let result = function_under_test(input);
        
        // Assert
        assert_eq!(result, expected_value);
    }
    
    #[tokio::test]
    async fn test_async_function() {
        let result = async_function().await;
        assert!(result.is_ok());
    }
}
```

### Test Coverage Requirements

- [ ] Unit tests for all public functions
- [ ] Integration tests for database operations
- [ ] Error case tests
- [ ] Edge case tests
- [ ] Async tests for concurrent operations

### Performance Tests

```rust
#[test]
fn test_performance_critical_path() {
    let start = Instant::now();
    
    // Run operation
    critical_function();
    
    let elapsed = start.elapsed();
    assert!(elapsed < Duration::from_millis(100), "Too slow: {:?}", elapsed);
}
```

---

## Code Quality Checklist

Before committing:

- [ ] All tests pass (`cargo test`)
- [ ] No clippy warnings (`cargo clippy`)
- [ ] No unsafe code without comment justification
- [ ] No `unwrap()` or `expect()` in production paths
- [ ] Proper error handling with `?` operator
- [ ] Documentation comments on public items
- [ ] Performance critical paths optimized
- [ ] No unnecessary allocations in hot loops
- [ ] Async boundaries respected (no blocking in async)
- [ ] Lock scopes minimized

---

**Remember**: Performance bugs are harder to fix than feature bugs. Design for performance from the start.
