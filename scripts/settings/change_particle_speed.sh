#!/bin/bash

# stonemeta: title: Change Particle Speed
# stonemeta: description: Modifies the particle movement speed cap for the background animation.
# stonemeta: command: Settings
#

set -e

SHELL_JSON="$(dirname "$(dirname "$(dirname "$(readlink -f "$0")")")")/shell.json"

show_current() {
    if [ -f "$SHELL_JSON" ]; then
        current=$(jq '.PARTICLE_SPEED_CAP' "$SHELL_JSON")
        echo "Current particle speed cap: $current ($(echo "$current * 100" | bc)%)"
        echo "  (1.0 = full speed, 0.3 = 30% speed, 0.1 = 10% speed)"
    else
        echo "Error: shell.json not found at $SHELL_JSON"
        exit 1
    fi
}

validate_input() {
    local value="$1"
    if ! [[ "$value" =~ ^[0-9]*\.?[0-9]+$ ]]; then
        echo "Error: Please enter a valid number (e.g., 0.3, 0.5, 1.0)."
        return 1
    fi
    if jq -e --arg v "$value" '($v | tonumber) < 0.05' > /dev/null 2>&1; then
        echo "Warning: Speed below 0.05 may make particles nearly stationary."
    fi
    if jq -e --arg v "$value" '($v | tonumber) > 1.0' > /dev/null 2>&1; then
        echo "Warning: Speed above 1.0 will exceed the original maximum speed."
    fi
    return 0
}

show_current
echo ""

if [ -n "$1" ]; then
    new_speed="$1"
    echo "Using provided value: $new_speed"
else
    echo "Enter new particle speed cap (recommended: 0.2 to 0.5):"
    read -r new_speed
fi

if validate_input "$new_speed"; then
    jq ".PARTICLE_SPEED_CAP = $new_speed" "$SHELL_JSON" > "${SHELL_JSON}.tmp" && \
        mv "${SHELL_JSON}.tmp" "$SHELL_JSON"

    echo ""
    echo "Success: Particle speed cap updated to $new_speed ($(echo "$new_speed * 100" | bc)%)"
    show_current
    echo ""
    echo "Restart shellstone to apply changes."
else
    echo ""
    echo "Operation cancelled."
    exit 1
fi
