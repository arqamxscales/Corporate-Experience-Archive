# Task 3: ERC-20 Standard Token Contract

## Objective
Author and deploy a compliant ERC-20 token on an Ethereum testnet.

## Files
- `ERC20Token.sol` — the full contract, `ProgreeToken` (symbol `PIT`),
  implementing `totalSupply`, `balanceOf`, `transfer`, `approve`,
  `allowance`, `transferFrom`, and the `Transfer`/`Approval` events per
  the ERC-20 standard.

## What the contract does
- **Constructor** mints an initial supply to whoever deploys it.
- **`transfer` / `transferFrom`** move tokens, with `require` checks
  guarding against zero-address transfers and insufficient balances.
- **`approve` / `allowance`** implement the standard delegated-spending
  pattern (e.g. what a DEX uses to move tokens on your behalf).
- All state changes emit the standard events so wallets/explorers can
  track balances correctly.

## Deploying it yourself (Remix + Sepolia)
This part needs your own MetaMask wallet and testnet ETH, so it has to be
done in your browser — here's exactly how:

1. **Get testnet ETH**: open a Sepolia faucet (e.g.
   `sepoliafaucet.com` or Alchemy's/Infura's faucet) and request funds to
   your MetaMask address.
2. **Open Remix**: go to `https://remix.ethereum.org`.
3. **Create the file**: in the File Explorer, create `ERC20Token.sol` and
   paste in the contract from this folder.
4. **Compile**: open the "Solidity Compiler" tab, select a `0.8.20`+
   compiler version, and click **Compile ERC20Token.sol**.
5. **Connect MetaMask**: in the "Deploy & Run Transactions" tab, set
   **Environment** to `Injected Provider - MetaMask`, and make sure
   MetaMask is switched to the **Sepolia** network.
6. **Deploy**: enter a constructor argument for `initialSupply_` (e.g.
   `1000000` for 1,000,000 whole tokens), then click **Deploy** and
   confirm the transaction in MetaMask.
7. **Log the address**: once mined, copy the deployed contract address
   from Remix's "Deployed Contracts" panel — this is your "active
   deployment address variable."
8. **Verify it works**: call `balanceOf(<your address>)` in Remix to
   confirm you received the initial supply, then try `transfer` to a
   second address to confirm events fire correctly.

## Report notes
For your submission, include:
- The deployed contract address on Sepolia.
- A link to the contract on Sepolia Etherscan
  (`https://sepolia.etherscan.io/address/<your address>`).
- A screenshot of a successful `transfer` call and the resulting
  `Transfer` event.

## Optional: OpenZeppelin version
If you'd rather build on an audited base instead of the from-scratch
version here, the equivalent using OpenZeppelin is:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract ProgreeToken is ERC20 {
    constructor(uint256 initialSupply) ERC20("Progree Internship Token", "PIT") {
        _mint(msg.sender, initialSupply * (10 ** decimals()));
    }
}
```
In Remix, use the "OpenZeppelin" import path directly — Remix resolves it
automatically from GitHub.
