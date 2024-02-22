# Stone-Prover-Cairo0-Verifier

## Overview
This repository demonstrates how proofs generated by StoneProver can be verified using the Cairo0 verifier. It includes two submodules:
- [cairo-lang](https://github.com/Okm165/cairo-lang)
- [stone-prover](https://github.com/Okm165/stone-prover)

## Getting Started

### Clone the Repository
To get started, clone this repository and initialize its submodules:

```bash
git clone https://github.com/Okm165/stone-prover-cairo0-verifier.git
cd stone-prover-cairo0-verifier
git submodule update --init --recursive
```

### Install Cairo Lang
Install the Cairo language by executing the following commands:

```bash
cd cairo-lang
pip install --upgrade pip
zip -r cairo-lang-0.12.0.zip cairo-lang-0.12.0
pip install cairo-lang-0.12.0.zip
cd ../
```

### Build Stone-Prover
Build the StoneProver tool using Docker:

```bash
cd stone-prover
docker build --tag prover .
container_id=$(docker create prover)
docker cp -L ${container_id}:/bin/cpu_air_prover ./e2e_test
docker cp -L ${container_id}:/bin/cpu_air_verifier ./e2e_test
cd ../
```

### Install Hyperfine
```bash
cargo install hyperfine
```

### Running Benchmarks
To run the benchmarks first ensure you are on the correct branch with the corresponding layout for the program (this is needed the cairo verifier changes dependent on the layout).

-	keccak_builtin_bench.sh -> origin/master
-	keccak_bench.sh -> origin/recursive_layout
-	SOON! sha256_bench.sh -> origin/recursive_layout

Input options indicate the number of bytes being hashed:
```bash
{INPUT} = { 32, 320, 3200, 32000 }
```

Keccak (In cairo)
```bash
chmod +x keccak_bench.sh
./keccak_bench.sh {INPUT}
```

Keccak Builtin
```bash
chmod +x keccak_builtin_bench.sh
./keccak_builtin_bench.sh {INPUT}
```
## Usage

### Generate Proof
To generate a proof, follow these steps:

```bash
cd stone-prover/e2e_test
cairo-compile fibonacci.cairo --output fibonacci_compiled.json --proof_mode
cairo-run \
    --program=fibonacci_compiled.json \
    --layout=starknet_with_keccak \
    --program_input=fibonacci_input.json \
    --air_public_input=fibonacci_public_input.json \
    --air_private_input=fibonacci_private_input.json \
    --trace_file=fibonacci_trace.json \
    --memory_file=fibonacci_memory.json \
    --print_output \
    --proof_mode
./cpu_air_prover \
    --out_file=fibonacci_proof.json \
    --private_input_file=fibonacci_private_input.json \
    --public_input_file=fibonacci_public_input.json \
    --prover_config_file=cpu_air_prover_config.json \
    --parameter_file=cpu_air_params.json \
    -generate_annotations
cd ../../
```

### Verify Proof
To verify the generated proof, use the following steps:

```bash
cd cairo-lang
jq '{ proof: . }' ../stone-prover/e2e_test/fibonacci_proof.json > cairo_verifier_input.json
cairo-compile --cairo_path=./src src/starkware/cairo/cairo_verifier/layouts/all_cairo/cairo_verifier.cairo --output cairo_verifier.json --no_debug_info
cairo-run \
    --program=cairo_verifier.json \
    --layout=starknet_with_keccak \
    --program_input=cairo_verifier_input.json \
    --trace_file=cairo_verifier_trace.json \
    --memory_file=cairo_verifier_memory.json \
    --print_output
cd ../
```

### Future Work and Enhancements

#### Version Compatibility:
An essential future direction is to ensure compatibility with newer versions of Cairo Lang and Cairo Verifier. This involves analyzing the changes between different versions and updating the repository to accommodate these changes.

#### Continuous Maintenance:
To remain a reliable reference, the repository will be regularly updated. This maintenance includes fixing bugs, improving documentation, and incorporating community feedback.
