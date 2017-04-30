import subprocess
import itertools

wr_list = [0, 25, 50, 75, 100]
qdep_list = [1, 4, 16, 64]
wrsize_list = [1, 4, 16, 64, 256]
rdsize_list = [1, 4, 16, 64, 256]
wrstride_list = [0, 64, 128, 256]
rdstride_list = [0, 64, 128, 256]

counter = 0
subprocess.call("rm -rf stride_result.log".split())

cmd_list = "fitness --device=/dev/sda --wr x --qdep x --wrsz x --rdsz x --wrnd 0 --rrnd 0 --wr_stride 0 --rd_stride 0 --warm 5 --test 5 --direct".split()

with open("stride_result.txt", 'w') as f_stride:
    f_stride.write("wr_ratio,qdep,wrsz,rdsz,wrnd,rrnd,wr_stride,rd_stride,lat,bw,iops\n")
    for para in itertools.product(wr_list, qdep_list, wrsize_list, rdsize_list, wrstride_list, rdstride_list):
        if para[4] == 0 and para[5] == 0:
            continue

        cmd_list[3] = str(para[0])
        cmd_list[5] = str(para[1])
        cmd_list[7] = str(para[2])
        cmd_list[9] = str(para[3])
        cmd_list[15] = str(para[4])
        cmd_list[17] = str(para[5])

        lines = subprocess.check_output(cmd_list)
        results = lines.split('\n')[1]
        xarr = results.split()
        
        f_stride.write(','.join([str(x) for x in para[:4]]+["0", "0"]+[str(x) for x in para[4:]]+[xarr[-1],xarr[-3],xarr[-2]])+'\n')
        counter += 1
    f_stride.write(str(counter)+' tests done.\n')
