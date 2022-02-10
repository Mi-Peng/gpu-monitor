# Gpu-Monitor
A Python function for Slurm, where I couldn't use `nvidia-smi` to monitor the GPU information.

**whole repo is not finish**

## Installation
TODO




## Monitor the GPU information in Model Training

```python
from showGPU import showGPUinfo
...
for batch_id, (x, y) in enumerate(dataloader):
    ...
    showGPUinfo()
    ...
```


## Ref
- [GPUtils](https://github.com/anderskm/gputil)
- [nvidia-smi](https://nvidia.custhelp.com/app/answers/detail/a_id/3751/~/useful-nvidia-smi-queries)