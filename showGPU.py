import os
from subprocess import Popen, PIPE

'''
    determinate attribute to show in terminal
    key: the string, which will be shown in terminal as title.
    value: the name of variable in class `GPU`, which will be used as `getattr(value)`.
'''
NORMAL_ATTR_TO_SHOW = {
    'ID': 'id',
    'GPU Name': 'gpu_name',
    'GPU Utilization': 'gpu_utilization',
    'Memory(Total)': 'memoryTotal',
    'Memory(Used)': 'memoryUsed',
    'Memory(Avail)': 'memoryAvailable',
    'temperature': 'temp_gpu',
    'driver version': 'driver_version',
}
CLEAN_ATTR_TO_SHOW = {
    'ID': 'id',
    'GPU Name': 'gpu_name',
    'MemoryInfo': 'memoryAll',
}
DEFAULT_ATTR_TO_SHOW = CLEAN_ATTR_TO_SHOW


class GPU:
    def __init__(
        self, 
        id,
        uuid,
        gpu_utilization,
        memoryTotal,
        memoryUsed,
        memoryAvailable,
        driver_version,
        gpu_name,
        serial,
        display_mode,
        display_active,
        temp_gpu) -> None:
        self.id = id
        self.uuid = uuid
        self.gpu_utilization = str(gpu_utilization * 100) + '%'
        self.memoryTotal = str(memoryTotal) + 'Mb'
        self.memoryUsed = str(memoryUsed) + 'Mb'
        self.memoryAvailable = str(memoryAvailable) + 'Mb'
        self.memoryPercent = '{:.2f}'.format(float(memoryUsed)/float(memoryTotal) * 100) + '%'
        self.memoryAll = '{}Mb / {}Mb ({:.2f}%)'.format(memoryUsed, memoryTotal, float(memoryUsed)/float(memoryTotal) * 100)
        self.driver_version = driver_version
        self.gpu_name = gpu_name
        self.serial = serial
        self.display_mode = display_mode
        self.display_active = display_active
        self.temp_gpu = str(temp_gpu) + 'C'

        self.setAttrToShow()

    def setAttrToShow(self, attr_to_show=DEFAULT_ATTR_TO_SHOW):
        self.attr_to_show = attr_to_show

    def __str__(self) -> str:
        Str = '|'
        for k, v in self.attr_to_show.items():
            Str += ' {}: {} |'.format(k, getattr(self, v))
        return Str

def safeFloatTransform(strNumber):
    try:
        number = float(strNumber)
    except ValueError:
        number = float('nan')
    return number


def getGPUs():
    # Windows is not supported
    p = Popen(["nvidia-smi","--query-gpu=index,uuid,utilization.gpu,memory.total,memory.used,memory.free,driver_version,name,gpu_serial,display_active,display_mode,temperature.gpu", "--format=csv,noheader,nounits"], stdout=PIPE)
    stdout, stderror = p.communicate() # get output of command line(See more in *.md file)
    stdout_utf8 = stdout.decode('UTF-8') # bytes -> UTF-8
    gpu_list = stdout_utf8.split(os.linesep) # os.linesep: line terminator used by the current platform
    numGPUs = len(gpu_list) - 1 # exists a blank string in the end
    GPUs = []
    for i in range(numGPUs):
        gpu = gpu_list[i] # gpu: 'xxx, xxxx, xx, xxx'
        values = gpu.split(', ')
        gpu_info = {
            'id': int(values[0]),
            'uuid': values[1],
            'gpu_utilization': safeFloatTransform(values[2])/100,
            'memoryTotal': safeFloatTransform(values[3]),
            'memoryUsed': safeFloatTransform(values[4]),
            'memoryAvailable': safeFloatTransform(values[5]),
            'driver_version': values[6],
            'gpu_name': values[7],
            'serial': values[8],
            'display_active': values[9],
            'display_mode': values[10],
            'temp_gpu': safeFloatTransform(values[11])
        }
        print(gpu_info)
        GPUs.append(GPU(**gpu_info))
    return GPUs

def showGPUinfo(attr_to_show=DEFAULT_ATTR_TO_SHOW):
    GPUs = getGPUs()
    try:
        from tabulate import tabulate
        header = list(attr_to_show.keys())
        rows = []
        for gpu in GPUs:
            gpu_info = (getattr(gpu, v) for v in attr_to_show.values())
            rows.append(gpu_info)
        shows = tabulate(rows, headers=header, stralign='center')

    except:
        print('[Warning] Fail to `import tabulate`, Please `pip install tabulate`.')
        shows = ''
        for gpu in GPUs:
            shows += str(gpu) + '\n'
        shows = shows[:-2] # remove final `\n`
    finally:
        print(shows)

# showGPUinfo()