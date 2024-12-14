import os
import importlib.util
import inspect

path=os.path.abspath("../mainfunctionality/kernelspace_scripts/kernel_functions.py")
file_name = path.split('/')[-1].replace('.py','')
print(file_name)
spec = importlib.util.spec_from_file_location(file_name, path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

# for name, obj in inspect.getmembers(mod):
#     if inspect.isfunction(obj):
#         print(name)

functions_dict={}
count=0
for name, obj in inspect.getmembers(mod):
        if inspect.isfunction(obj):
            count+=1
            curr_dict={f"{count}": f"{name}", "function_content": f"{inspect.getsource(obj)}" }
            functions_dict[name] = curr_dict

print (functions_dict)