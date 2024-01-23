#!/bin/bash
container="psql_contain"
image="psql:v001"


# Re-Build Container with New Configuration
function update_container {
    winpty docker rm $container
    winpty docker rmi $image

    winpty docker build -t $image .
    winpty docker run -it \
	--name=$container \
	--network=docker_sql_default \
	$image 
}

# Run Dockerised Python Ingestion Script
function run_script {
    winpty docker start -i $container
}

declare -A container_options=(
    [1]="1 - Update Container/Image with New Configuration" 
    [2]="2 - Run psql" 
)
keys_sorted=($(echo ${!container_options[@]} | tr ' ' '\n' | sort -n))

while true; do
    echo "=============================================="
    echo "Please Select An Action (Enter Integer Value):"
    echo "=============================================="
    for key in "${keys_sorted[@]}"; do
        echo "  ${container_options[$key]}"
    done
    read num
    case $num in
        1) update_container ;;
        2) run_script ;;
        *) 
            clear
            echo "-------------------------------------------------"
            echo "---  Invalid Selection - Enter Value on List  ---"
            echo "-------------------------------------------------
            "
            continue ;;
    esac
    break
done
