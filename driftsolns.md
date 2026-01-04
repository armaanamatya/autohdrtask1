# Drift Solutions for Adjacent Frame Comparison

## Problem: Chain Effect Drift

When comparing only adjacent frames (i, i+1), you can get a "chain effect" problem:

- Frame A → Frame B: similar → B dropped
- Frame B → Frame C: similar → C dropped
- But Frame A → Frame C might be **very different**!

This happens because you're comparing against frames that get dropped, leading to "drift" where you lose good frames that should have been kept.

---

## Solution Options

### **Option 1: Compare against last KEPT frame (Recommended)**

Instead of comparing against the previous frame (which might get dropped), compare against the last frame you decided to **keep**. This prevents drift.

**Pros:**
- Prevents drift entirely
- Simple to implement
- Maintains semantic meaning (all kept frames are compared to each other)
- Most robust against edge cases

**Cons:**
- Slightly more complex logic
- May need to track "last kept index"

**Implementation approach:**
```python
last_kept_idx = 0
for i in range(1, len(groups)):
    # Compare groups[i] against groups[last_kept_idx]
    if not_duplicate:
        last_kept_idx = i  # Update reference
    else:
        drop(i)
```

---

### **Option 2: Temporal windowing**

Compare each frame against the next 2-3 frames, not just the immediate next one. This catches gradual transitions.

**Pros:**
- Catches gradual changes across multiple frames
- Good for detecting slow transitions
- Still relatively fast

**Cons:**
- Doesn't fully prevent drift (just reduces it)
- More comparisons needed (2-3x)
- Window size is a tuning parameter

**Implementation approach:**
```python
WINDOW_SIZE = 3
for i in range(len(groups)):
    for j in range(i+1, min(i+WINDOW_SIZE, len(groups))):
        # Compare groups[i] against groups[j]
```

---

### **Option 3: Reference frame with drift detection**

Keep a reference frame and compare all frames against it. When drift gets too large, update the reference to the current kept frame.

**Pros:**
- Adaptive to scene changes
- Can handle both similar and changing sequences
- Automatically resets reference on scene cuts

**Cons:**
- More complex logic
- Need to define "drift threshold"
- May miss duplicates if reference updates too frequently

**Implementation approach:**
```python
reference_idx = 0
for i in range(1, len(groups)):
    score = compare(groups[reference_idx], groups[i])

    if score >= duplicate_threshold:
        drop(i)
    else:
        # Check if we've drifted from reference
        if score < drift_threshold:
            reference_idx = i  # Update reference
```

---

### **Option 4: Hybrid approach**

Combine options 1 and 2: compare against last kept frame, but also check 1-2 frames ahead to catch near-duplicates that appear slightly later.

**Pros:**
- Best of both worlds
- Prevents drift AND catches delayed duplicates
- Most comprehensive

**Cons:**
- Most complex implementation
- More comparisons (but still fewer than full scan)

**Implementation approach:**
```python
last_kept_idx = 0
LOOKAHEAD = 2

for i in range(1, len(groups)):
    # Primary check: against last kept
    if is_duplicate(groups[last_kept_idx], groups[i]):
        drop(i)
        continue

    # Secondary check: lookahead for delayed duplicates
    for j in range(i+1, min(i+LOOKAHEAD+1, len(groups))):
        if is_duplicate(groups[i], groups[j]):
            drop(j)

    last_kept_idx = i  # Update reference
```

---

## Recommendation

**Start with Option 1** (compare against last kept frame). It's the simplest solution that completely eliminates drift and is easy to reason about.

If you still see issues with near-duplicates being kept, then upgrade to **Option 4** (hybrid) for maximum coverage.

Avoid Option 2 and 3 unless you have specific use cases:
- Option 2: Good for video frames with slow motion
- Option 3: Good for long sequences with distinct scenes

---

## Testing Strategy

After implementing the solution:

1. **Test on known problem cases** - Use the folders that dropped too much
2. **Compare metrics** - Count input vs output, verify no important frames lost
3. **Visual inspection** - Sample random kept frames to ensure quality
4. **Edge cases** - Test with all-similar and all-different sequences
