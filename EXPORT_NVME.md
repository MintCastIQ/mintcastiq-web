# Export an NVME drive using iSCSI# Export an NVME drive using iSCSI
## My use case
- I have an old HP Proliant server without NVME support that I have ProxMox hypervisor installed on.
- I am going to use it for a PostgreSQL server (dev) for a MintCastIQ
- I also have a couple of NVME drives installed on a machine running Ubuntu. 
- I want to use one of them on the Proliant server and attach it to the DB VM for WAL writes.
# 🧩 On the SOURCE machine
## Install targetcli (or tgt)
```bash
sudo apt update
sudo apt install targetcli-fb -y
```
## Create a backstore for the NVMe device
```bash
sudo targetcli
backstores/block create nvme0 /dev/nvme0n1
```
- nvme0 → friendly name for the backstore
- /dev/nvme0n1 → your NVMe device
## Create an iSCSI target
`iscsi/ create iqn.2025-11.local.lan:nvme0`
- **IQN format:** *iqn.YYYY-MM.domain:identifier*
## Add a LUN pointing to the NVMe backstore
`iscsi/iqn.2025-11.local.lan:nvme0/tpg1/luns create /backstores/block/nvme0`
## Allow network access
`iscsi/iqn.2025-11.local.lan:nvme0/tpg1/portals create 0.0.0.0 3260`
## **(Optional)** Add CHAP authentication
```bash
iscsi/iqn.2025-11.local.lan:nvme0/tpg1 set attribute authentication=1
iscsi/iqn.2025-11.local.lan:nvme0/tpg1 set auth userid=dbuser
iscsi/iqn.2025-11.local.lan:nvme0/tpg1 set auth password=strongpass
```
## Save config and exit
```bash
saveconfig
exit
```
# 🧩 On the TARGET machine
## Install open-iscsi
```bash
sudo apt update
sudo apt install open-iscsi -y
```
## Discover the target
`sudo iscsiadm -m discovery -t sendtargets -p $SOURCEIP
## Login to the target
`sudo iscsiadm -m node -T iqn.2025-11.local.lan:nvme0 -p $SOURCEIP:3260 --login`
## Verify the device appears
`lsblk`
You should see a new block device (e.g. /dev/sdb).
# 🧩 Attach to DB VM in Proxmox
## In the Proxmox UI:
-Go to your DB VM → Hardware → Add → Hard Disk.
-Select the new iSCSI storage or raw device.
-Or edit /etc/pve/qemu-server/<VMID>.conf:
`scsi1: /dev/sdb`
# 🧩 Inside the DB VM
## Format and mount
```bash
sudo mkfs.ext4 /dev/vdb
sudo mkdir -p /srv/postgres
sudo mount /dev/vdb /srv/postgres
```
## Update /etc/fstab
`/dev/vdb   /srv/postgres   ext4   defaults   0 2`

```
## My use case
- I have an old HP Proliant server without NVME support that I have ProxMox hypervisor installed on.
- I am going to use it for a PostgreSQL server (dev) for a webapp that I am working on.
- I also have a couple of NVME drives installed on a machine running Ubuntu. 
- I want to use one of them on the Proliant server and attach it to the DB VM for WAL writes.
# 🧩 On the SOURCE machine
## Install targetcli (or tgt)
```bash
sudo apt update
sudo apt install targetcli-fb -y
```
## Create a backstore for the NVMe device
```bash
sudo targetcli
backstores/block create nvme0 /dev/nvme0n1
```
- nvme0 → friendly name for the backstore
- /dev/nvme0n1 → your NVMe device
## Create an iSCSI target
`iscsi/ create iqn.2025-11.local.lan:nvme0`
- **IQN format:** *iqn.YYYY-MM.domain:identifier*
## Add a LUN pointing to the NVMe backstore
`iscsi/iqn.2025-11.local.lan:nvme0/tpg1/luns create /backstores/block/nvme0`
## Allow network access
`iscsi/iqn.2025-11.local.lan:nvme0/tpg1/portals create 0.0.0.0 3260`
## **(Optional)** Add CHAP authentication
```bash
iscsi/iqn.2025-11.local.lan:nvme0/tpg1 set attribute authentication=1
iscsi/iqn.2025-11.local.lan:nvme0/tpg1 set auth userid=dbuser
iscsi/iqn.2025-11.local.lan:nvme0/tpg1 set auth password=strongpass
```
## Save config and exit
```bash
saveconfig
exit
```
# 🧩 On the TARGET machine
## Install open-iscsi
```bash
sudo apt update
sudo apt install open-iscsi -y
```
## Discover the target
`sudo iscsiadm -m discovery -t sendtargets -p $SOURCEIP
## Login to the target
`sudo iscsiadm -m node -T iqn.2025-11.local.lan:nvme0 -p $SOURCEIP:3260 --login`
## Verify the device appears
`lsblk`
You should see a new block device (e.g. /dev/sdb).
# 🧩 Attach to DB VM in Proxmox
## In the Proxmox UI:
-Go to your DB VM → Hardware → Add → Hard Disk.
-Select the new iSCSI storage or raw device.
-Or edit /etc/pve/qemu-server/<VMID>.conf:
`scsi1: /dev/sdb`
# 🧩 Inside the DB VM
## Format and mount
```bash
sudo mkfs.ext4 /dev/vdb
sudo mkdir -p /srv/postgres
sudo mount /dev/vdb /srv/postgres
```
## Update /etc/fstab
`/dev/vdb   /srv/postgres   ext4   defaults   0 2`

```
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
