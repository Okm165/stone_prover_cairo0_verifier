import subprocess
from colorama import Fore, Style

def log_and_run(commands, description, cwd=None):
    full_command = " && ".join(commands)
    try:
        print(f"{Fore.YELLOW}Starting: {description}...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Command: {full_command}{Style.RESET_ALL}")
        result = subprocess.run(full_command, shell=True, check=True, cwd=cwd, text=True)
        print(f"{Fore.GREEN}Success: {description} completed!\n{Style.RESET_ALL}")
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error running command '{full_command}': {e}\n{Style.RESET_ALL}")

log_and_run([
    "time cairo-run \
    --program=zerosync_compiled.json \
    --layout=starknet_with_keccak \
    --program_input=zerosync_input.json \
    --air_public_input=zerosync_public_input.json \
    --air_private_input=zerosync_private_input.json \
    --trace_file=zerosync_trace.bin \
    --memory_file=zerosync_memory.bin \
    --print_output \
    --print_info \
    --proof_mode", 
], "Running zerosync program", cwd="stone-prover/e2e_test")

log_and_run([
    "time ./cpu_air_prover \
    --out_file=zerosync_proof.json \
    --public_input_file=zerosync_public_input.json \
    --private_input_file=zerosync_private_input.json \
    --prover_config_file=cpu_air_prover_config.json \
    --parameter_file=cpu_air_params.json \
    -generate_annotations", 
], "Proving zerosync program", cwd="stone-prover/e2e_test")
