# a function to generate random fact files
gen_fact_file() {
    # Check if the correct number of arguments is provided
    if [ "$#" -lt 2 ]; then
        echo "Usage: gen_fact_file <file_name> <output_dir>"
        return 1
    fi
    
    file_name=$1
    output_dir=$2
    
    # Create the output directory if it doesn't exist
    mkdir -p "$output_dir"
    
    # Determine the directory of the script
    src_dir=$(dirname "${BASH_SOURCE[0]}")
    
    # Run the Ruby script and save the output to the specified directory
    ruby "$src_dir/random_fact_generator.rb" "${@:3}" > "$output_dir/$file_name.facts"
}

# set default benchmark size to small
TMP_SIZE=$1
SIZE=${TMP_SIZE:=$SIZE}
SIZE=${SIZE:=small}

echo "Generating facts of size: $SIZE"

# Example usage: gen_fact_file myfact /path/to/output $SIZE

