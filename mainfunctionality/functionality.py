import paramiko
import textwrap
import json
import black
import os
import ast
path=os.getcwd() + "/mainfunctionality/kernelspace_scripts/kernel_functions.py"
##Extract function with arg
def extract_function_calls(file_path):
    with open(file_path, "r") as file:
        code = file.read()
    tree = ast.parse(code)
    function_calls = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):  
            if isinstance(node.func, ast.Name):
                func_name = node.func.id

            args = []
            for arg in node.args:
                args.append(ast.unparse(arg)) 
            function_call = f"{func_name}({', '.join(args)})"
            function_calls.append(function_call)
    return function_calls



class ConnetionMaker:
        
    def ssh_call(self,ip,command,content): 
            self.calls = []
            self.calls = extract_function_calls(path)
            for func_call in self.calls:
                    func_name_only = func_call.split('(')[0]

                    if command in func_name_only:
                        function_code = textwrap.dedent("""import subprocess\n{}\n{}""").format(content,func_call)     
                        exec_code =  textwrap.dedent("""{}\nprint(remote_function.{})""").format("import remote_function",func_call) 
                        hostname = "{}".format(ip).strip()
                        username = "terra"
                        password = "terra"
                        client = paramiko.SSHClient()
                        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        client.connect(hostname, username=username, password=password)

                        try:
                            sftp = client.open_sftp()
                            remote_file = "/tmp/remote_function.py"
                            with sftp.open(remote_file, "w") as f:
                                f.write(function_code)
                            exec_file = "/tmp/exec_file.py"
                            with sftp.open(exec_file, "w") as f:
                                f.write(exec_code)
                            sftp.close()
                            command = f"python3 {exec_file} "
                            stdin, stdout, stderr = client.exec_command(command)
                            result = stdout.read().decode().strip()
                            error = stderr.read().decode().strip()

                            if error:
                                print("Error:", error)
                            else:
                                #print("result",result)
                                return result
                        finally:
                            #client.exec_command(f"rm {remote_file} {exec_code}")
                            client.close()
