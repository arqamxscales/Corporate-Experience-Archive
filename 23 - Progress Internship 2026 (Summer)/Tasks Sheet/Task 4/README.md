# Task 4: Multi-Party Escrow Decentralized Application (DApp)

## Objective
An end-to-end Web3 DApp: a smart contract coordinating multi-party funding
with a real frontend that connects a crypto wallet and drives the
contract on-chain.

## Files
```
contracts/
  Escrow.sol        — the MultiPartyEscrow smart contract
frontend/
  index.html         — page structure
  styles.css          — styling
  app.js              — wallet connection + contract calls (ethers.js v5)
```

## Contract design (`Escrow.sol`)
`MultiPartyEscrow` is a crowdfunding-style escrow with a goal and a
deadline:

- **`contribute()`** — anyone can send ETH before the deadline; tracked
  per-address in `contributions`.
- **Conditional payout** — after the deadline:
  - If `totalRaised >= goal`, the **beneficiary** can call `withdraw()`
    once to collect everything.
  - If the goal wasn't met, every contributor can call `claimRefund()`
    to pull back exactly what they put in.
- **Reentrancy protection**: a custom `nonReentrant` modifier guards both
  `withdraw()` and `claimRefund()`, and both functions follow
  Checks-Effects-Interactions — state is updated (`fundsWithdrawn = true`,
  `contributions[msg.sender] = 0`) **before** the external `.call{value:}`
  transfer, so a malicious contract on the receiving end can't re-enter
  and drain funds twice.
- **Pull-payment refunds** — refunds are claimed individually by each
  contributor rather than pushed out in a loop, avoiding gas-limit and
  denial-of-service issues that come with paying many addresses in one
  transaction.

## Frontend (`frontend/`)
A single-page interface, no build step required — open `index.html`
directly or serve the folder with any static server.

1. **Connect wallet** — connects MetaMask via `window.ethereum` and
   shows the connected address + network.
2. **Load campaign** — paste in your deployed contract address to read
   the beneficiary, goal, amount raised, time remaining, and your own
   contribution, with a live progress bar and countdown.
3. **Contribute** — enter an ETH amount and send a `contribute()`
   transaction.
4. **Withdraw / Refund** — the relevant panel appears automatically once
   the deadline has passed, based on whether the goal was met and
   whether you're the beneficiary or a contributor.

## Deploying and running it yourself
This needs your own wallet + testnet ETH, so run these steps yourself:

1. **Deploy the contract** in Remix (same flow as Task 3):
   - Paste `Escrow.sol` into Remix, compile with Solidity `0.8.20`+.
   - In "Deploy & Run Transactions," connect **Injected Provider -
     MetaMask** on Sepolia.
   - Fill constructor args: `_beneficiary` (an address to receive funds),
     `_goalInWei` (e.g. `100000000000000000` for 0.1 ETH), and
     `_durationInSeconds` (e.g. `3600` for a 1-hour campaign).
   - Deploy and copy the resulting contract address.
2. **Run the frontend**:
   - Open `frontend/index.html` in a browser with MetaMask installed
     (or serve the folder locally, e.g. `python3 -m http.server` from
     inside `frontend/`, then visit `http://localhost:8000`).
   - Click **Connect wallet**, paste the deployed address, click **Load
     campaign**.
   - Try contributing from one or more MetaMask accounts to see the
     progress bar update.
   - After the deadline passes, reload the campaign to see either the
     withdraw panel (if goal met) or refund panel (if not) appear.

## Report notes
For your submission, include:
- The deployed contract address on Sepolia + Etherscan link.
- Screenshots of: a successful contribution, the progress bar updating,
  and either a successful withdrawal or refund after the deadline.
- A short paragraph on how the `nonReentrant` modifier + Checks-Effects-
  Interactions ordering together prevent a reentrancy attack on
  `withdraw()`/`claimRefund()`.
