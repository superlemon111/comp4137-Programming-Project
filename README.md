# COMP4137/COMP7200 Programming Project

## Project Info

- Title: MiniChain
- Phase: Phase I, Task 1
- Group Number: `2`
- Group Members:
  - `Wong Wing Fung (23213477)`
  - `Cheung Yeung Tai (22233903)`
  - `Student Name 3 (Student ID 3)`

Replace the placeholders above with your actual group information before submission.

## Project Overview

The system supports:

- creation of blockchain accounts using a public/private key pair
- generation of signed single-input single-output (SISO) transactions
- computation of a transaction ID using SHA-256
- verification of transaction integrity and digital signatures
- detection of tampering by re-validating the transaction after data modification

The implementation is written in Python and uses modern public-key cryptography through the `cryptography` library.

## Implemented Components

### 1. Account Creation

Each user account is created with an `Ed25519` private key and public key.

- The private key is used to sign transaction data.
- The public key is serialized in PEM format and used as the blockchain address.

### 2. Transaction Structure

Each transaction contains the following fields:

- `transaction_id`: SHA-256 hash of the canonical transaction content
- `data`:
  - `amount`: number of virtual coins
  - `amount_hash`: SHA-256 hash of the amount
- `input`: sender address
- `output`: receiver address
- `signature`: sender's digital signature over the transaction payload

### 3. Verification

The verification logic checks:

- the amount hash matches the amount value
- the digital signature is valid for the sender's public key
- the stored transaction ID matches the recomputed transaction ID

If any field is changed after signing, verification fails.

## Folder Structure

```text
COMP4137/
├── README.md
├── requirements.txt
├── task1_demo.py
└── minichain/
    ├── __init__.py
    ├── account.py
    └── transaction.py
```

## Hardware and Software Requirements

- Operating System: macOS, Linux, or Windows
- Python Version: Python 3.11 or above
- Memory: 4 GB RAM or above is sufficient
- Disk Space: less than 100 MB required for this task

## Dependencies

Required Python package:

- `cryptography==46.0.6`

Install all dependencies with:

```bash
pip install -r requirements.txt
```

## Installation and Deployment

### Step 1. Create a virtual environment

```bash
python3 -m venv .venv
```

### Step 2. Activate the virtual environment

On macOS/Linux:

```bash
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### Step 3. Install required libraries

```bash
pip install -r requirements.txt
```

Estimated setup time: less than 3 minutes on a normal laptop with internet access.

## How to Run

Run the Task 1 demonstration program:

```bash
python task1_demo.py
```

## Execution Guide

The program performs the following workflow:

1. Create two accounts named `Alice` and `Bob`.
2. Generate a signed SISO transaction from Alice to Bob with amount `25`.
3. Print the generated transaction data in JSON format.
4. Verify the transaction and print the result.
5. Simulate tampering by changing the transaction amount.
6. Re-verify the modified transaction and show that it becomes invalid.

Estimated execution time: less than 5 seconds.

## Expected Output

The exact public keys, signatures, and transaction ID will be different in each run because the cryptographic keys are generated dynamically. However, the output format should look like this:

```text
=== Accounts ===
Alice address: ...
Bob address:   ...

=== Signed Transaction ===
{
  "transaction_id": "...",
  "data": {
    "amount": 25,
    "amount_hash": "..."
  },
  "input": "-----BEGIN PUBLIC KEY----- ...",
  "output": "-----BEGIN PUBLIC KEY----- ...",
  "signature": "..."
}

=== Verification ===
Valid transaction: True
Transaction ID: ...

=== Tampering Simulation ===
Valid after changing amount: False
```

The key correctness conditions are:

- `Valid transaction: True` for the original transaction
- `Valid after changing amount: False` after tampering

These results demonstrate that the transaction is properly signed and that any modification breaks its integrity.

## Source File Description

- `task1_demo.py`: demo script for Task 1
- `minichain/account.py`: account generation and digital signature functions
- `minichain/transaction.py`: transaction data model, transaction creation, transaction ID generation, and verification
- `requirements.txt`: dependency list

