#!/bin/bash -u

main(){
    echo -e "discoverable on\npairable on\nexit\n" | bluetoothctl
    python cornholio_main.py
}

if [[ "${0}" == "${BASH_SOURCE[0]}" ]]; then
    main "$@"
fi
