def parse_image_filename_v2(filename):
    
    # Remove the file extension
    filename_without_ext = filename.split(".")[0]
    # Split the filename into parts
    parts = filename_without_ext.split("_")
    # Extract the date and time part
    date_part = parts[3]
    time_part = parts[4]
    # Correct the format for time
    formatted_time = time_part[:2] + ':' + time_part[3:5] + ':' + time_part[6:]
    # Extract and format the details
    details = {
        "camera_name": parts[0],
        "class_name": parts[1],
        "count": parts[2],
        "date_created": date_part,
        "time_created": formatted_time
    }
    return details



def split(name):
    split_text = name.split(',')
    Name = split_text[0]
    Employee_id = split_text[1]
    Company_id = split_text[2]
    print(Name,Employee_id,Company_id)
    return(Name,Employee_id,Company_id)

    
# Example usage
filename_v2 = "110a1_person_1_2023-12-12_20-51-35.jpg"
parsed_details_v2 = parse_image_filename_v2(filename_v2)