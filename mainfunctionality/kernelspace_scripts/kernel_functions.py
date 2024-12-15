import subprocess
def func1(a,b):
        result = subprocess.run(['uname', '-r'], capture_output=True, text=True)
        return {"kernel_version":result.stdout.strip()}

def func2():
        result = subprocess.run(['uptime'], capture_output=True, text=True)
        return {"uptime":result.stdout.strip()}

def func3():
        pass


func1(2,3)
func2()
func3()



