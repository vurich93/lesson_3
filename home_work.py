import psutil
import time


HEAD_START = "{:^150}"
TEMPLATE_VIRT_MEM = "Virtual Memory Statistics:\nTotal memory:{total}Mb\tUsed memory:{used}Mb\tFree memory:{free}Mb"
SWAP_MEM = "Swap Memory Statistics:\nTotal memory:{total}Mb\tUsed memory:{used}Mb\tFree memory:{free}Mb"
TEMPL_DISK_HEAD = "|{:_^150}|"
TEMPL_DISK = "Mountpoint -> {:<30}\tTotal(Gb):{:<30}\tUsed(Gb):{:<30}\tFree(Gb):{:<30}"
HEAD_PROCES = "{name:<25}\t{pid:<5}\t{username:<10}\t"
TEMPLATE_PROCES = "{:<25}\t{:<5}\t{:<10}\t"
ТEMPLATE_NETWORK = "interface:{interface:<10}\naddress:{address:<10}\tnetmask:{netmask:}\tbroadcast:{broadcast:}\n"
ТEMPLATE_TEMP = "Name:{Name:}\ncurrent(℃ ):{current:}\thigh(℃ ):{high:}\tcritical(℃ ):{critical:}\n"
ТEMPLATE_TEMP_Core = "Name:{Name:}\nlabel:{label:<10}\tcurrent(℃ ):{current:<10}\thigh(℃ ):{high:<10}\tcritical(℃ ):{critical:<10}\n"
# TEMPLATE_SEN_BAT = "Percent:{percent}%\tPower-plugged:{power_plugged}"


def virt_mem():
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    a = 10 ** 6
    res = {
        "virtual":
        {'total': memory.total, 'used': memory.used, 'free': memory.free},
        "swap":
        {'total': swap.total, 'used': swap.used, 'free':swap.free}
        
        }
    for keys,value in res["virtual"].items():
        res["virtual"][keys] = value / a 
    for keys,value in res["swap"].items():
        res["swap"][keys] = value / a 
    return res

def disk_dev():
    disk = psutil.disk_partitions()
    device = []
    for i in disk:
        device.append(i.device)
    
    return device


def disk_part():
    disk_1 = psutil.disk_partitions()
    part = []
    for i in disk_1:
        part.append(i.mountpoint)
    return part


def run_proc():
    proces = []
    for proc in psutil.process_iter(['name','pid','username']):
        proces.append(proc.info)

    return proces


def sensor_batery():
    baterry = psutil.sensors_battery()
    res = {
        "sbatery": 
    {"percent": baterry.percent, "power_plugged": baterry.power_plugged}
        }
    return res

def show():
    virtual_mem = virt_mem()
    virtal_mem_info = TEMPLATE_VIRT_MEM.format(**virtual_mem["virtual"])
    swap_mem_info = SWAP_MEM.format(**virtual_mem["swap"])
    start_mem = HEAD_START.format("Обработка памяти компьютера")
    print(start_mem, end="\n\n")
    print(virtal_mem_info, end='\n\n')
    print(swap_mem_info, end='\n\n')
    time.sleep(3)

    dev = disk_dev()
    par = disk_part()
    num = 10**9
    start_disk = HEAD_START.format("Обработка дискового пространства компьютера")
    print(start_disk, end = '\n\n')
    for i,j in zip(dev,par):
        d_u = psutil.disk_usage(j)
        disk_head = TEMPL_DISK_HEAD.format("Device:"+i)
        
        disk_inf = TEMPL_DISK.format(j,(d_u.total/num),(d_u.used/num),(d_u.free/num))

        print(disk_head,end='\n\n')
        print(disk_inf, end='\n\n')
        time.sleep(0.5)


    start_proc = HEAD_START.format("Запущенные процессы")
    print(start_proc, end = '\n\n')
    proces_run = run_proc()
    for i in proces_run:
        procs_dict = i
        info = HEAD_PROCES.format(**procs_dict)
        head = TEMPLATE_PROCES.format("Name","Pid","Username")
        print(head)
        print(info, end='\n\n')
        time.sleep(0.005)


    start_network = HEAD_START.format("Сетевые интерфейсы")
    print(start_network,end='\n\n')
    for keys,values in psutil.net_if_addrs().items():
        net_inf = {
              "interface": keys,
              "address": values[0].address ,
              "netmask": values[0].netmask ,
              "broadcast":values[0].broadcast
            }
        network_info = ТEMPLATE_NETWORK.format(**net_inf)
        print(network_info)
        time.sleep(0.5)


    start_sensor = HEAD_START.format("Датчики температуры")
    # print(start_sensor,end='\n\n')
    # sen_bat = sensor_batery()
    # batery_info = TEMPLATE_SEN_BAT.format(**sen_bat["sbatery"])
    # print(batery_info)
    for keys,values in psutil.sensors_temperatures().items():
        if keys == 'coretemp':
            for i in psutil.sensors_temperatures()['coretemp']:
                res = {
                "Name": keys,
                "label": i.label,
                "current": i.current,
                "high": i.high,
                "critical": i.critical

                    }
                res_if = ТEMPLATE_TEMP_Core.format(**res)
                print(res_if)
                time.sleep(0.5)

        else:
            res = {
              "Name": keys,
              "current": values[0].current,
              "high": values[0].high,
              "critical":values[0].critical
                }
 
            res_if = ТEMPLATE_TEMP.format(**res)
            print(res_if, end='\n\n')
            time.sleep(0.5)


if __name__ == "__main__":
    show()