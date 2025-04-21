#!/bin/bash
# 
# Build the various components needed for the ET artifact

set -o pipefail -o errexit

source "$(dirname ${0})/common.sh"

install_kernel() {
	if [[ "${TYPE}" == "vm" ]]; then
		fail "Please run scripts/install.sh inside the VM or manually copy / install the VM kernel"
	fi

	if [[ "${KERNEL}" == "mthp" ]]; then
  		pushd src/linux-mthp
  		ok "Installing 6.9rc-mthp kernel..."
  		cp configs/config.mthp .config
  	elif [[ "${KERNEL}" == "mthp.pftrace.4k" ]]; then
  		pushd src/linux-mthp
  		ok "Installing 6.9rc-mthp kernel..."
  		cp configs/config.mthp.pftrace.4k .config
  	elif [[ "${KERNEL}" == "mthp.pftrace.64k" ]]; then
    		pushd src/linux-mthp
    		ok "Installing 6.9rc-mthp kernel..."
    		cp configs/config.mthp.pftrace.64k .config
	elif [[ "${KERNEL}" == "trident" ]]; then
		pushd src/trident-linux

		ok "Installing 4.17-trident kernel..."
	else
		pushd src/et-linux
		ok "Installing ${KERNEL}..."
	fi

	ok "Installing kernel modules..."
	make modules_install

	ok "Installing kernel..."
	sed -i.bak -E "s/^kernel=.*\\.img/kernel=kernel_${KERNEL}.img/" /boot/firmware/config.txt
	sudo cp arch/arm64/boot/Image.gz /boot/firmware/kernel_${KERNEL}.img
  sudo cp arch/arm64/boot/dts/broadcom/*.dtb /boot/firmware/
  sudo cp arch/arm64/boot/dts/overlays/*.dtb* /boot/firmware/overlays/
  sudo cp arch/arm64/boot/dts/overlays/README /boot/firmware/overlays/

	ok "Installing the kernel image..."
	make install

	ok "Installing perf..."
	cp tools/perf/perf "${BASE}/bin"

	popd
}

install_qemu() {
	pushd src/et-qemu
	ok "Installing Qemu..."
	cp build/qemu-system-aarch64 ${BASE}/bin/vm/
	cp build/pc-bios/efi-virtio.rom ${BASE}/bin/
	popd
}

install_utils() {
	pushd src/etutils-rs
	ok "Installing ET userspace utilities..."
	find ./target/release/ -maxdepth 1 -perm /ugo+x -type f | xargs -I '{}' cp '{}' "${BASE}/bin/"
	popd
}

install_benchmarks() {
	pushd src/benchmarks

	pushd hashjoin
	ok "Installing hashjoin..."
	cp hashjoin "${BASE}/benchmarks"
	popd

	pushd btree
	ok "Installing btree..."
	cp BTree "${BASE}/benchmarks"
	popd

	pushd gapbs
	ok "Installing bfs..."
	cp bfs converter "${BASE}/benchmarks"
	popd

	pushd svm
	ok "Installing svm..."
	cp train "${BASE}/benchmarks"
	popd

	pushd gups
	ok "Installing gups..."
	cp gups "${BASE}/benchmarks"
	popd

	popd
}

install_kernel
install_qemu
install_utils
install_benchmarks
