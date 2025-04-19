#!/bin/bash
# Fault latency with different sizes. Requires pftrace (CONFIG_PFTRACE)
# enabled kernel.

set -o pipefail -o errexit

ok() {
        echo -e "[\033[0;32mOK\033[0m] ${@}"
}

fail() {
        echo -e "[\033[0;31mFAILED\033[0m] ${@}"
        exit 1
}

cleanup() {
	FAILED=0
	[ $? -ne 0 ] && FAILED=1
	while popd &>/dev/null; do true; done
	[ ${FAILED} -eq 1 ] && fail "${0} failed, exiting..."
	ok "${0} finished, exiting..."
}
trap cleanup EXIT

# init env
export BASE="${BASE:-/root/elastic-translations-MICRO2024}"
source "${BASE}/env/base.env"
pushd "${BASE}"

# FIXME: Create a proper CLI arg parser
# pflag <VMA size in bytes> <nr of VMAs> <nr of threads> <THP-flag> <shuffle-flag (fault VMA randomly, not sequentially)> <nr of faults> <VMA # drop-flag (count VMA unmapping / flushing in the tracing)>

if [ $(uname -r) == "6.8.12-v8+" ] \
  || [ $(uname -r) == "6.8.12-v8+64k+" ]; then
  # 4KiB (for 64KiB boot a kernel with a 64KiB granule -- CONFIG_ARM64_64K_PAGES)
  if [ $(uname -r) == "6.8.12-v8+" ]; then
    ok "Running pflat 4KiB..."
  else
    ok "Running pflat 64KiB..."
  fi
  pflat $(( 100 << 30 )) 1 1 false true 100000 false
  pflat.sh show
  pflat.sh clear
elif [ $(uname -r) == "5.18.19-et+pftrace+" ]; then
  # 64KiB ET faults
  ok "Running pflat 64KiB ET..."
  MODE=etheap ETHEAP=1 prctl.sh pflat $(( 100 << 30 )) 1 1 false true 100000 false
  pflat.sh show
  pflat.sh clear
  # 32MiB ET faults
  ok "Running pflat 32MiB ET..."
  MODE=etheap ETHEAP=1 prctl.sh prctl --ca --et -- pflat $(( 100 << 30 )) 1 1 true true 100000 false
  pflat.sh show
  pflat.sh clear
elif [ $(uname -r) == "5.18.19-vanilla+pftrace+4k+" ] \
  || [ $(uname -r) == "5.18.19-vanilla+pftrace+16k+" ]; then
  # 2MiB (for 32MiB boot a kernel with a 16KiB granule -- CONFIG_ARM64_16K_PAGES)
  if [ $(uname -r) == "5.18.19-vanilla+pftrace+4k+" ]; then
    ok "Running pflat 2MiB..."
  else
    ok "Running pflat 32MiB..."
  fi
  pflat $(( 100 << 30 )) 1 1 true true 100000 false
  pflat.sh show
  pflat.sh clear
else
  echo "ERROR: kernel $(uname -r) is not valid"
fi
