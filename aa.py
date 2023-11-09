def format_cuadruplas(input_file_path, output_file_path):
    formatted_code = ""
    with open(input_file_path, 'r') as file:
        cuadruplas = file.read().splitlines()
    
    current_class = None
    
    for line in cuadruplas:
        tokens = line.split(',')
        keyword = tokens[0]
        if keyword == "CLASS":
            class_name = tokens[1]
            formatted_code += f"CLASS {class_name}\n"
            current_class = class_name
        elif keyword == "END_CLASS":
            formatted_code += f"END_CLASS {current_class}\n"
            current_class = None
        elif current_class:
            if keyword == "DECLARE" or keyword == "DECLARE_VAR":
                variable_name = tokens[1]
                formatted_code += f"    DECLARE {variable_name}\n"
            elif keyword == "PARAM":
                param_name = tokens[1]
                formatted_code += f"    PARAM {param_name}\n"
            elif keyword == "END_FUNCTION":
                function_name = tokens[1]
                formatted_code += f"    END_FUNCTION {function_name}\n"
            elif keyword == "LABEL":
                label_name = tokens[1]
                formatted_code += f"    LABEL {label_name}\n"
            elif keyword == "GOTO":
                label_name = tokens[1]
                formatted_code += f"    GOTO {label_name}\n"
            elif keyword in ("+", "-", "*", "/", "<", ">", "<=", ">=", "=", "NOT", "ISVOID", "~"):
                target = tokens[3]
                operand1 = tokens[2]
                operand2 = tokens[1]
                formatted_code += f"        {target} = {operand1} {keyword} {operand2}\n"
            elif keyword == "NEW":
                target = tokens[1]
                class_name = tokens[2]
                formatted_code += f"        {target} = NEW {class_name}\n"
            elif keyword == "LET":
                target = tokens[1]
                variable = tokens[2]
                formatted_code += f"        {target} = LET {variable}\n"
            elif keyword == "PUT":
                target = tokens[1]
                value = tokens[3]
                formatted_code += f"        {value} = {target}\n"
                
    with open(output_file_path, 'w') as output_file:
        output_file.write(formatted_code)
