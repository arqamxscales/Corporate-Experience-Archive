# Task 2: Immutability Ledger — Block Hashing Simulation

## Objective
A local cryptographic console model demonstrating the core blockchain
link-security property: each block cryptographically commits to the one
before it, so history can't be silently rewritten.

## Files
- `blockchain_simulation.py` — the full simulation, runnable standalone
  with no external dependencies (pure Python 3 standard library).

## How it works
1. **`Block`** holds an index, timestamp, list of transactions, the
   previous block's hash, a nonce, and its own hash.
2. **`compute_hash()`** serializes the block's fields deterministically
   (`json.dumps(..., sort_keys=True)`) and runs SHA-256 over it — this is
   the block's "fingerprint."
3. **`Blockchain._mine()`** implements a tiny proof-of-work: it keeps
   incrementing the nonce until the hash starts with `DIFFICULTY` leading
   zeros. This is a simplified stand-in for how real miners have to do
   real computational work to add a block.
4. **`add_block()`** always sets `previous_hash` to the *actual* hash of
   the current last block — this is the "link" in blockchain.
5. **`is_chain_valid()`** walks the whole chain and checks two things for
   every block:
   - Recomputing the block's hash from its current data still matches the
     stored hash (catches direct tampering).
   - The block's `previous_hash` still matches the prior block's real
     hash (catches broken links / reordering / deleted blocks).

## Run it
```bash
python3 blockchain_simulation.py
```

Expected behavior:
- The script mines a genesis block plus 3 transaction blocks and prints
  each one.
- It validates the untouched chain → `✅ Chain is valid`.
- It then simulates an attacker editing Block #2's transaction data
  *without* redoing the proof-of-work, and re-validates → the script
  correctly reports `❌ Block 2 data has been tampered with.`

## Report notes
For your submission, include:
- A screenshot of the console output (both the "valid" and "tampered"
  validation results).
- One paragraph explaining, in your own words, why changing one block
  breaks every block after it in a real blockchain (hint: each
  subsequent block's `previous_hash` would also need to be recomputed
  and re-mined — this is what makes rewriting history expensive).
