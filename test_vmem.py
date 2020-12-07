import psutil

TEMPLATE_VIRT_MEM = "Virtual Memory Statistics:\n\nTotal memory:{total}Mb\tUsed memory:{used}Mb\tFree memory:{free}Mb"

def virt_mem():
    memory = psutil.virtual_memory()
    a = 10 ** 6
    res = {"virtual":{'total': memory.total, 'used': memory.used, 'free': memory.free}}
    for keys,value in res["virtual"].items():
        res["virtual"][keys] = value / a

    return res

def show():
    virtual_mem = virt_mem()
    virtal_mem_info = TEMPLATE_VIRT_MEM.format(**virtual_mem["virtual"])
    print(virtal_mem_info)








if __name__ == "__main__":
    show()