import subprocess
import itertools

wr_list = [0, 25, 50, 75, 100]
qdep_list = [1, 4, 16, 64]
wrsize_list = [1, 4, 16, 64, 256]
rdsize_list = [1, 4, 16, 64, 256]

counter = 0
subprocess.call("rm -rf seq_result.log".split())

cmd_list = "fitness --device=/dev/sda --wr x --qdep x --wrsz x --rdsz x --wrnd 0 --rrnd 0 --wr_stride 0 --rd_stride 0 --warm 5 --test 5 --direct".split()

with open("seq_result.txt", 'w') as f_seq:
    f_seq.write("wr_ratio,qdep,wrsz,rdsz,wrnd,rrnd,wr_stride,rd_stride,lat,bw,iops\n")
    for para in itertools.product(wr_list, qdep_list, wrsize_list, rdsize_list):

        cmd_list[3] = str(para[0])
        cmd_list[5] = str(para[1])
        cmd_list[7] = str(para[2])
        cmd_list[9] = str(para[3])

        lines = subprocess.call(cmd_list)
        results = line.split('\n')[1]
        xarr = results.split()
        
        f_seq.write(','.join([str(x) for x in para]+["0" for i in xrange(4)]+[xarr[-1],xarr[-3],xarr[-2]])+'\n')
        counter += 1
    f_seq.write(str(counter)+' tests done.\n')
