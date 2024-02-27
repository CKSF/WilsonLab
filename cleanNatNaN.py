def clean_data(file_path, new_file_path):
    with open(file_path, 'r') as original_file:
        lines = original_file.readlines()

    with open(new_file_path, 'w') as cleaned_file:
        # Write the header to the new file
        cleaned_file.write(lines[0])

        for line in lines[1:]:
            # Check if the line contains 'NaT' or 'NaN'
            if 'NaT' in line or 'NaN' in line:
                continue  
            
            cleaned_file.write(line)


original_file_path = '/Users/fengtianning/Desktop/Wilson lab/cleaned data/Data-2021-10-24.txt'
new_file_path = '/Users/fengtianning/Desktop/Wilson lab/cleaned data/Cleaned_Data-2021-10-24.txt'
clean_data(original_file_path, new_file_path)

print(f"Cleaned data has been written to {new_file_path}.")
