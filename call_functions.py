from google.genai import types
from functions.get_files_info import *
from functions.get_file_content import *
from functions.write_file import *
from functions.run_python_file import *

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info, 
        schema_get_file_content, 
        schema_write_file, 
        schema_run_python_file
        ],
)

# function_call is a types.FunctionCall object. It has a name (str) and args (dict of str)
def call_function(function_call, verbose=False):
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    
    print(f" - Calling function: {function_call.name}")

    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file
    }

    function_name = function_call.name or ""
    
    # Error in case the function call is not one of the available ones.
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    args = dict(function_call.args) if function_call.args else {}

    args["working_directory"] = "./calculator"
    
    function_result = function_map[function_name](**args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                # from_function_response requires a dictionary for response.
                response={"result": function_result},
            )
        ],
    )