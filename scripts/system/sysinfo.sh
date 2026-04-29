#!/bin/bash
# Admin-Meta: Title: System Information
# Admin-Meta: Description: Similar to Neofetch, but with no dependencies!
#

#!/usr/bin/env bash
# sysinfo.sh — minimal neofetch-like system info, no nonstandard deps


# --- Gather info ---

USER_HOST="${USER}@$(hostname)"

# OS
if [[ -f /etc/os-release ]]; then
    . /etc/os-release
    OS_NAME="${PRETTY_NAME:-$NAME}"
else
    OS_NAME="Unknown"
fi

# Kernel
KERNEL=$(uname -r)

# Uptime from /proc/uptime
read -r up_sec _ < /proc/uptime
up_sec=${up_sec%.*}
UP_DAYS=$(( up_sec / 86400 ))
UP_HRS=$(( (up_sec % 86400) / 3600 ))
UP_MIN=$(( (up_sec % 3600) / 60 ))
UPTIME=""
(( UP_DAYS > 0 )) && UPTIME+="${UP_DAYS}d "
(( UP_HRS  > 0 )) && UPTIME+="${UP_HRS}h "
UPTIME+="${UP_MIN}m"

# Shell
SHELL_NAME=$(basename "$SHELL")

# Terminal
TERM_NAME=${TERM:-unknown}

# CPU
CPU=$(grep -m1 'model name' /proc/cpuinfo | cut -d: -f2 | sed 's/^ *//')
CPU_CORES=$(grep -c '^processor' /proc/cpuinfo)

# CPU usage % (sample over 0.2s from /proc/stat)
read_cpu_stat() {
    read -ra f < /proc/stat
    echo "${f[@]:1:7}"
}
cpu1=( $(read_cpu_stat) )
sleep 0.2
cpu2=( $(read_cpu_stat) )
idle1=${cpu1[3]}; idle2=${cpu2[3]}
total1=0; total2=0
for v in "${cpu1[@]}"; do (( total1 += v )); done
for v in "${cpu2[@]}"; do (( total2 += v )); done
d_total=$(( total2 - total1 ))
d_idle=$(( idle2 - idle1 ))
if (( d_total > 0 )); then
    CPU_USAGE=$(( 100 * (d_total - d_idle) / d_total ))
else
    CPU_USAGE=0
fi

# RAM from /proc/meminfo
mem_total=$(awk '/^MemTotal:/{print $2}' /proc/meminfo)
mem_avail=$(awk '/^MemAvailable:/{print $2}' /proc/meminfo)
mem_used=$(( mem_total - mem_avail ))
mem_total_mb=$(( mem_total / 1024 ))
mem_used_mb=$(( mem_used / 1024 ))

# Disk usage for /
read -r disk_used disk_total disk_pct <<< \
    "$(df -BM / | awk 'NR==2{gsub(/M/,"",$3); gsub(/M/,"",$2); printf "%s %s %s", $3, $2, $5}')"

# GPU (best-effort, no drivers required)
GPU="unknown"
if [[ -d /sys/class/drm ]]; then
    for card in /sys/class/drm/card*/device/; do
        vendor_id=$(cat "${card}vendor" 2>/dev/null)
        device_id=$(cat "${card}device" 2>/dev/null)
        if [[ -n $vendor_id ]]; then
            # Try to resolve via modalias
            modalias=$(cat "${card}modalias" 2>/dev/null)
            # Fallback: use label if uevent has it
            label=$(grep -i 'pci_id\|gpu\|vga' "${card}uevent" 2>/dev/null | head -1)
            GPU="${vendor_id}:${device_id}"
            break
        fi
    done
    # Nicer: check /sys/class/drm/card0/device/label or hwmon name
    for f in /sys/class/drm/card*/device/hwmon/hwmon*/name; do
        [[ -f $f ]] && GPU=$(cat "$f") && break
    done
fi

# Local IP
LOCAL_IP=$(ip -4 route get 1.1.1.1 2>/dev/null | awk '/src/{for(i=1;i<=NF;i++) if($i=="src") print $(i+1)}')
LOCAL_IP=${LOCAL_IP:-"unavailable"}

# Battery (if present)
BATTERY=""
for bat in /sys/class/power_supply/BAT*; do
    [[ -f "$bat/capacity" ]] || continue
    cap=$(< "$bat/capacity")
    status=$(< "$bat/status" 2>/dev/null)
    BATTERY="${cap}% (${status})"
    break
done

# --- Print ---

line() { printf "  ${B}%-12s${R} %s\n" "$1" "$2"; }

echo
printf "  ${C}%s${R}\n" "$USER_HOST"
printf "  %s\n" "$(printf '─%.0s' {1..30})"
line "OS"       "${OS_NAME}"
line "Kernel"   "${KERNEL}"
line "Shell"    "${SHELL_NAME}"
line "Terminal" "${TERM_NAME}"
line "Uptime"   "${UPTIME}"
line "CPU"      "${CPU} (${CPU_CORES}c, ${CPU_USAGE}% load)"
line "Memory"   "${mem_used_mb}MB / ${mem_total_mb}MB"
line "Disk (/)" "${disk_used}MB / ${disk_total}MB (${disk_pct})"
line "GPU"      "${GPU}"
line "Local IP" "${LOCAL_IP}"
[[ -n $BATTERY ]] && line "Battery" "${BATTERY}"
echo
