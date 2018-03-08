#
# Generate templates with variables for send emails with laravel
#
import os
import re

#
# Get list of file with specific extension in defined path
#
def list_filesext(directory, extension):
    return (f for f in os.listdir(directory) if f.endswith('.' + extension))

#
# Read document and get data
#
def get_html(url_file):
    fp = open(url_file, 'r')
    str_fp = fp.read()
    return str_fp

#
# Search laravel variables
#
def get_variables(full_document):
    variables = []
    regex_expression = r"\{\!\! .* \!\!\}"
    regex_var_expression = r"\$\S*"
    matches = re.findall(regex_expression, full_document)
    for match in matches:
        # Find first match to extract variables
        vari = re.findall(regex_var_expression, match)[0]
        # Add variables to main array
        variables.append(vari)
    return variables

#
# Add variables to initial full_document
#
def write_variables(file_str, file_variables):
    new_file_str = "{{-- -----------------------------------------------------\n"
    new_file_str = new_file_str + "\n      LARAVEL VARIABLES\n\n"
    for fvar in file_variables:
        new_file_str = new_file_str + "      " + fvar + '\n'
    new_file_str = new_file_str + "----------------------------------------------------- --}}\n"
    new_file_str = new_file_str + file_str
    return new_file_str

#
# Execute
#
# Alist dist dir
directory = "./dist/laravel/dist/"
if not os.path.exists(directory):
    os.makedirs(directory)
# Html Files in directory
source_path = "./dist/"
files = list_filesext(source_path, "html")
# Genarate each new template
dest_path = "./dist/laravel/dist/"
for ifile in files:
    # Determine file path
    file_path = source_path + ifile
    # Get contet of file
    file_str = get_html(file_path)
    # Get PHP variables in the content of file
    file_variables = get_variables(file_str)
    # Asign new content for the blade files
    if(len(file_variables)):
        new_file_str = write_variables(file_str, file_variables)
    else:
        new_file_str = file_str
    # Determinate amd write the new file for blade template
    new_file_path = dest_path + ifile.replace(".html", ".blade.php")
    new_file = open(new_file_path, "w+")
    new_file.write(new_file_str)
