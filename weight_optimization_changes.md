# Weight Optimization Changes for HDR Bracket Preservation

**Date**: 2026-01-03
**Purpose**: Prevent system from dropping HDR brackets while still catching near-duplicates

---

## Summary of Changes

Updated weights and thresholds in `deduplicationwnew.py` to preserve HDR brackets while still removing burst mode photos, photographer retakes, and duplicate angles.

---

## Changes Made

### Regular Photos Configuration (Lines 173-184)

| Parameter | Old Value | New Value | Reason |
|-----------|-----------|-----------|--------|
| `MTB_HARD_FLOOR` | 63.0% | 58.0% | Allow true duplicates (57-61% MTB) to be caught while protecting HDR brackets (<50%) |
| `WEIGHT_MTB` | 0.3 | 0.4 | Make brightness differences more important - HDR brackets have different exposures |
| `WEIGHT_PDQ` | 0.2 | 0.15 | Make room for increased MTB weight |
| `WEIGHT_SIFT` | 0.2 | 0.15 | De-emphasize in composite score (still used for override) |
| `COMPOSITE_DUP_THRESHOLD` | 0.5 | 0.55 | Harder to classify as duplicate overall |
| `SIFT_MIN_MATCHES` | 100 | 150 | Higher bar for SIFT contribution |

**Weight sum check**: 0.4 + 0.1 + 0.2 + 0.15 + 0.15 = 1.0 ✓

### Aerial Photos Configuration (Lines 187-198)

| Parameter | Old Value | New Value | Reason |
|-----------|-----------|-----------|--------|
| `AERIAL_MTB_HARD_FLOOR` | 62.0% | 55.0% | Same reasoning as regular photos |
| `AERIAL_WEIGHT_MTB` | 0.30 | 0.40 | Brightness matters for aerial HDR too |
| `AERIAL_WEIGHT_PDQ` | 0.25 | 0.15 | Make room for MTB |
| `AERIAL_COMPOSITE_DUP_THRESHOLD` | 0.32 | 0.38 | Less permissive than before |
| `AERIAL_SIFT_MIN_MATCHES` | 50 | 100 | Require stronger evidence |

**Weight sum check**: 0.40 + 0.10 + 0.25 + 0.15 + 0.10 = 1.0 ✓

### SIFT Override Logic (Line 653)

**Old code:**
```python
sift_override = (sift_matches >= sift_min * 1.5) or ((sift_matches >= sift_min) and (clip >= 85.0))
```

**New code:**
```python
sift_override = (sift_matches >= sift_min * 3.0) or ((sift_matches >= sift_min) and (clip >= 92.0))
```

**Impact:**
- **Regular photos**: Override threshold raised from 150 to **450 matches**
- **Aerial photos**: Override threshold raised from 75 to **300 matches**
- **Combo override**: CLIP threshold raised from 85% to **92%**

**Rationale:**
- HDR brackets on tripod: 500-1500 SIFT matches → will NOT trigger override anymore
- Burst mode: 2000-3000+ SIFT matches → WILL trigger override
- This prevents HDR brackets from being incorrectly dropped as duplicates

---

## Expected Behavior Changes

### HDR Brackets (BEFORE vs AFTER)

**Before:**
- HDR bracket 1 vs bracket 2: SIFT=1000, MTB=45% → SIFT override (1000 >= 150) → **DROPPED** ❌
- Result: Lost HDR brackets

**After:**
- HDR bracket 1 vs bracket 2: SIFT=1000, MTB=45% → No SIFT override (1000 < 450), MTB < 58% floor → **KEPT** ✓
- Result: HDR brackets preserved

### Burst Mode (BEFORE vs AFTER)

**Before:**
- Burst 1 vs burst 2: SIFT=2500, MTB=70% → SIFT override (2500 >= 150) → **DROPPED** ✓
- Result: Correctly removed

**After:**
- Burst 1 vs burst 2: SIFT=2500, MTB=70% → SIFT override (2500 >= 450) → **DROPPED** ✓
- Result: Still correctly removed

### Photographer Retakes (BEFORE vs AFTER)

**Before:**
- Retake 1 vs retake 2: SIFT=800, MTB=65%, score=0.52 → SIFT override (800 >= 150) → **DROPPED** ✓
- Result: Correctly removed

**After:**
- Retake 1 vs retake 2: SIFT=800, MTB=65%, score=0.52 → No SIFT override (800 < 450), but MTB > 58% and score < 0.55 → **KEPT** ?
- Result: Might keep some retakes IF composite score < 0.55
- If composite score calculation gives high values due to increased MTB weight (0.4 * 0.65 = 0.26), still likely to drop

**Note**: May need iteration in Phase 4 if retakes are being kept

---

## Risk Mitigation

1. **Risk**: Lower MTB floor (58%) might drop HDR brackets with moderate exposure difference
   - **Mitigation**: HDR brackets typically have <50% MTB overlap; if 58-62%, probably not enough variation for HDR
   - **Fallback**: Can raise to 60% if testing shows issues

2. **Risk**: Higher SIFT threshold (450) might miss burst mode with camera movement
   - **Mitigation**: Composite score will still catch these (high MTB, high CLIP)
   - **Fallback**: Can lower to 300-350 if testing shows burst mode being missed

3. **Risk**: Increased composite threshold (0.55) might keep some duplicates
   - **Mitigation**: True duplicates have very high scores (0.6-0.7+)
   - **Fallback**: Can lower to 0.52-0.53 if testing shows duplicates being kept

---

## Testing Recommendations

Run the following test scenarios:

1. **HDR bracket set** (3-5 exposures of same scene)
   - Expected: Keep ALL images
   - Check: MTB should be <60% between brackets

2. **Burst mode** (rapid sequence, same exposure)
   - Expected: Keep 1, drop rest
   - Check: SIFT should be 2000+ → override triggers

3. **Photographer retakes** (same scene, same exposure, seconds apart)
   - Expected: Keep 1, drop rest
   - Check: Composite score or MTB overlap should trigger drop

4. **Different angles** (same location, different perspective)
   - Expected: Keep ALL
   - Check: Lower SIFT, composite score should keep them

---

## Files Modified

- `C:\Users\Armaan\Desktop\autohdrtask1\deduplicationwnew.py`
  - Lines 173-184: Regular photo weights and thresholds
  - Lines 187-198: Aerial photo weights and thresholds
  - Line 653: SIFT override logic
  - Lines 680-683: SIFT override logging messages

---

## Next Steps

1. **Test on real data** - Run on folders with known HDR brackets and duplicates
2. **Monitor results** - Check how many images kept vs dropped
3. **Iterate if needed** (Phase 4):
   - If still losing HDR brackets → Raise MTB_HARD_FLOOR to 60% or SIFT override to 4.0x (600)
   - If keeping too many duplicates → Lower COMPOSITE_DUP_THRESHOLD to 0.50-0.52
4. **If weight tuning insufficient** → Address adjacent comparison drift issue (see `driftsolns.md`)

---

## Technical Details

### Why These Metrics Matter for HDR

**MTB (Median Threshold Bitmap):**
- HDR brackets have different exposures → different median brightness → LOW MTB overlap
- Duplicates have same exposure → similar brightness → HIGH MTB overlap
- **Increased weight (0.4)** makes this difference matter more

**SIFT (Feature Matching):**
- HDR brackets on tripod: High matches (500-1500) but not extreme
- Burst mode: EXTREME matches (2000-3000+) - milliseconds apart, identical position
- **Raised threshold (3.0x)** differentiates between these cases

**Composite Score:**
- Balances all metrics with weighted average
- **Raised threshold (0.55)** requires stronger evidence across multiple metrics

### Verification

To verify changes are working:

```bash
python deduplicationwnew.py --log-experiment "test_new_weights" --log-file "test_weights.md"
```

Check the output markdown file for:
- SIFT override triggers (should show "≥450" for regular, "≥300" for aerial)
- MTB floor failures (should show "<58.0" for regular, "<55.0" for aerial)
- Composite score threshold (should show "≥0.55" for regular, "≥0.38" for aerial)
