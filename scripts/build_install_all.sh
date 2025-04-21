#!/bin/bash

set -o pipefail -o errexit

source "$(dirname ${0})/common.sh"

# KERNELS="vanilla vanilla.pftrace.4k vanilla.pftrace.16k et et.pftrace hwk"
KERNELS="mthp mthp.pftrace.4k mthp.pftrace.64k"
# KERNELS="vanilla vanilla.pftrace.4k vanilla.pftrace.16k et et.pftrace hwk mthp mthp.pftrace.4k mthp.pftrace.64k"

build_kernel() {
	CONFIG="./configs"

  if [[ "${KERNEL}" == "mthp" ]]; then
		pushd src/linux-mthp
		ok "Building 6.8rc-mthp kernel..."
		cp configs/config.mthp .config
	elif [[ "${KERNEL}" == "mthp.pftrace.4k" ]]; then
		pushd src/linux-mthp
		ok "Building 6.8rc-mthp kernel..."
		cp configs/config.mthp.pftrace.4k .config
	elif [[ "${KERNEL}" == "mthp.pftrace.64k" ]]; then
  		pushd src/linux-mthp
  		ok "Building 6.8rc-mthp kernel..."
  		cp configs/config.mthp.pftrace.64k .config
	elif [[ "${KERNEL}" == "trident" ]]; then
		pushd src/

		ok "Building 4.17-trident kernel..."

		cp configs/* .config
		if [[ ! -z "${VM}" ]]; then
			CONFIG="${CONFIG}/config.vm"
		else
			CONFIG="${CONFIG}/config.altra"
		fi

		ok "Using config ${CONFIG}..."
		cp ${CONFIG} .config
	else
		pushd src/et-linux

		if [[ ! -z "${VM}" ]]; then
			CONFIG="${CONFIG}/vm/config.${KERNEL}"
		else
			CONFIG="${CONFIG}/native/config.${KERNEL}"
		fi

		ok "Using config ${CONFIG}..."
		cp ${CONFIG} .config
	fi

	ok "Building ${KERNEL} kernel..."
	make olddefconfig
	make prepare
	make -j$(nproc) Image.gz modules dtbs

	ok "Building perf..."
	make -j$(nproc) -C tools/perf WERROR=0

	popd
}

install_kernel() {
	if [[ "${TYPE}" == "vm" ]]; then
		fail "Please run scripts/install.sh inside the VM or manually copy / install the VM kernel"
	fi

	if [[ "${KERNEL}" == "mthp" ]]; then
  		pushd src/linux-mthp
  		ok "Installing 6.8rc-mthp kernel..."
  		cp configs/config.mthp .config
  	elif [[ "${KERNEL}" == "mthp.pftrace.4k" ]]; then
  		pushd src/linux-mthp
  		ok "Installing 6.8rc-mthp kernel..."
  		cp configs/config.mthp.pftrace.4k .config
  	elif [[ "${KERNEL}" == "mthp.pftrace.64k" ]]; then
    		pushd src/linux-mthp
    		ok "Installing 6.8rc-mthp kernel..."
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

for ker in ${KERNELS}; do
  KERNEL=${ker} build_kernel
  KERNEL=${ker} install_kernel
done
