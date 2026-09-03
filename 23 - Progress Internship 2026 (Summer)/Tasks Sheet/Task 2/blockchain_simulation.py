"""
Immutability Ledger — Block Hashing Simulation
------------------------------------------------
A simplified, local blockchain model demonstrating the core security
property of a blockchain: each block's hash depends on its own content
AND the previous block's hash, so tampering with any historical block
breaks the chain and is immediately detectable.

Run:
    python blockchain_simulation.py
"""

import hashlib
import json
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class Block:
    """A single block in the chain."""

    index: int
    timestamp: float
    transactions: List[Dict[str, Any]]
    previous_hash: str
    nonce: int = 0
    hash: str = field(default="", init=False)

    def compute_hash(self) -> str:
        """
        Deterministically serialize the block's contents and return its
        SHA-256 fingerprint. sort_keys=True guarantees the same dict
        always produces the same string -> same hash.
        """
        block_content = {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
        }
        block_string = json.dumps(block_content, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()


class Blockchain:
    """A minimal chain of blocks with proof-of-work style mining and
    validation."""

    DIFFICULTY = 4  # number of leading zeros required in a mined hash

    def __init__(self) -> None:
        self.chain: List[Block] = []
        self._create_genesis_block()

    def _create_genesis_block(self) -> None:
        genesis = Block(
            index=0,
            timestamp=time.time(),
            transactions=[{"note": "Genesis Block"}],
            previous_hash="0" * 64,
        )
        genesis.hash = self._mine(genesis)
        self.chain.append(genesis)

    @property
    def last_block(self) -> Block:
        return self.chain[-1]

    def _mine(self, block: Block) -> str:
        """
        Simple proof-of-work: increment nonce until the hash has the
        required number of leading zeros. This simulates the "work"
        miners do and shows why altering history is computationally
        expensive on a real chain.
        """
        computed_hash = block.compute_hash()
        while not computed_hash.startswith("0" * self.DIFFICULTY):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def add_block(self, transactions: List[Dict[str, Any]]) -> Block:
        new_block = Block(
            index=self.last_block.index + 1,
            timestamp=time.time(),
            transactions=transactions,
            previous_hash=self.last_block.hash,
        )
        new_block.hash = self._mine(new_block)
        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self) -> bool:
        """
        Walk the chain and verify:
        1. Each block's stored hash matches a fresh recomputation
           (detects tampering with that block's own data).
        2. Each block's previous_hash correctly links to the prior
           block's actual hash (detects broken links / reordering).
        """
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.compute_hash():
                print(f"❌ Block {current.index} data has been tampered with.")
                return False

            if current.previous_hash != previous.hash:
                print(f"❌ Block {current.index} is not correctly linked to block {previous.index}.")
                return False

        print("✅ Chain is valid — no tampering detected.")
        return True


def print_chain(blockchain: Blockchain) -> None:
    for block in blockchain.chain:
        print(f"\nBlock #{block.index}")
        print(f"  Timestamp:     {block.timestamp}")
        print(f"  Transactions:  {block.transactions}")
        print(f"  Previous Hash: {block.previous_hash}")
        print(f"  Nonce:         {block.nonce}")
        print(f"  Hash:          {block.hash}")


if __name__ == "__main__":
    print("=== Building the chain ===")
    chain = Blockchain()
    chain.add_block([{"from": "Alice", "to": "Bob", "amount": 25}])
    chain.add_block([{"from": "Bob", "to": "Charlie", "amount": 10}])
    chain.add_block([{"from": "Charlie", "to": "Dave", "amount": 5}])

    print_chain(chain)

    print("\n=== Validating the untouched chain ===")
    chain.is_chain_valid()

    print("\n=== Simulating an attack: tampering with Block #2 ===")
    chain.chain[2].transactions = [{"from": "Bob", "to": "Charlie", "amount": 10000}]
    # Note: hash is deliberately NOT recomputed here — this is the point.
    # A real attacker who only edits the data (without redoing the work
    # for every following block) gets caught immediately below.

    print("\n=== Re-validating after tampering ===")
    chain.is_chain_valid()
