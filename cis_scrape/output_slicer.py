# Capable of slicing output_url.txt files into smaller chunks if needed
def split_file(input_file, output_prefix, num_parts):
    with open(input_file, 'r') as file:
        lines = file.readlines()
    total_lines = len(lines)
    lines_per_part = total_lines // num_parts
    for i in range(num_parts):
        start_index = i * lines_per_part
        end_index = (i + 1) * lines_per_part if i < num_parts - 1 else total_lines
        output_file = f"{output_prefix}_{i + 1}.txt"
        with open(output_file, 'w') as out_file:
            out_file.writelines(lines[start_index:end_index])
    print(f"Split into {num_parts} parts successfully.")
split_file('output_urls.txt', 'output_part', 10)
