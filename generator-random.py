import subprocess
import itertools

wr_list = [0, 25, 50, 75, 100]
qdep_list = [1, 4, 16, 64]
wrsize_list = [1, 4, 16, 64, 256]
rdsize_list = [1, 4, 16, 64, 256]
wrnd_list = [0, 50, 100]
rrnd_list = [0, 50, 100]

counter = 0
subprocess.call("rm -rf random_result.log".split())

cmd_list = "fitness --device=/dev/sda --wr x --qdep x --wrsz x --rdsz x --wrnd 0 --rrnd 0 --wr_stride 0 --rd_stride 0 --warm 5 --test 5 --direct --outfile test.log".split()

with open("random_result.txt", 'w') as f_random:
    f_random.write("wr_ratio,qdep,wrsz,rdsz,wrnd,rrnd,wr_stride,rd_stride,lat,bw,iops\n")
    for para in itertools.product(wr_list, qdep_list, wrsize_list, rdsize_list, wrnd_list, rrnd_list):
        if para[4] == 0 and para[5] == 0:
            continue

        cmd_list[3] = str(para[0])
        cmd_list[5] = str(para[1])
        cmd_list[7] = str(para[2])
        cmd_list[9] = str(para[3])
        cmd_list[11] = str(para[4])
        cmd_list[13] = str(para[5])

        subprocess.call(cmd_list)
        line = subprocess.check_output("tail -n 1 test.log".split())
        line = line.strip()
        xarr = line.split()

        
        f_random.write(','.join([str(x) for x in para]+["0", "0"]+[xarr[-1],xarr[-3],xarr[-2]])+'\n')
    	counter += 1
    f_random.write(str(counter)+' tests done.\n')
