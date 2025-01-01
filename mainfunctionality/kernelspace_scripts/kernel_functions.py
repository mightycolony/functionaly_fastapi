import subprocess
def boot_parameters():
        result = subprocess.run("cat /proc/cmdline", shell=True, capture_output=True, text=True)
        return {"kernel_version":result.stdout.strip()}

def func2():
        result = subprocess.run(['uptime'], capture_output=True, text=True)
        return {"uptime":result.stdout.strip()}

def func3():
        pass


boot_parameters()
func2()
func3()



