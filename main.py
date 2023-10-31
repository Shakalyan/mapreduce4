import os, pyhdfs, math

base_dir = "/user/shakalyan/"
dpnds = "./utils.py"

def load_input():
    os.system(f"hadoop fs -rm -r {base_dir}/input4")
    os.system(f"hadoop fs -mkdir {base_dir}/input4")
    os.system(f"hadoop fs -put input.txt {base_dir}/input4")


def run_hadoop(indir, oudir, script, map_params, cmb_params, rdc_params):
    os.system(f"hadoop fs -rm -r {base_dir}{oudir}")
    cmd =   f"yarn jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar"\
            f" -files {script},{dpnds}"\
            f" -input {base_dir}{indir}"\
            f" -output {base_dir}{oudir}"
    
    if map_params != None:
        cmd += f" -mapper '{script} map {map_params}'"
    if cmb_params != None:
        cmd += f" -combiner '{script} combine {cmb_params}'"
    if rdc_params != None:
        cmd += f" -reducer '{script} reduce {rdc_params}'"
    
    os.system(cmd)


def get_norm_coeff(outpath):
    client = pyhdfs.HdfsClient()
    with client.open(f"/user/shakalyan/{outpath}/part-00000") as f:
        sum = float(f.read().decode('utf-8').split('\n')[0])        
    return 1 / math.sqrt(sum)


def authority_update():
    run_hadoop("input4", "aupdate_out", "./authority_update.py", "", None, "")

def authority_sum():
    run_hadoop("aupdate_out", "a_sum", "./authority_sum.py", "", None, "")

def authority_norm(coeff):
    run_hadoop("aupdate_out", "a_norm", "./authority_norm.py", str(coeff), None, None)


def hub_update():
    run_hadoop("a_norm", "hupdate_out", "./hub_update.py", "", None, "")

def hub_sum():
    run_hadoop("hupdate_out", "h_sum", "./hub_sum.py", "", None, "")

def hub_norm(coeff):
    run_hadoop("hupdate_out", "input4", "./hub_norm.py", str(coeff), None, None)


def main():
    iterations = 1
    load_input()
    for i in range(iterations):
        authority_update()
        authority_sum()
        a_coeff = get_norm_coeff("a_sum")
        authority_norm(a_coeff)
        hub_update()
        hub_sum()
        h_coeff = get_norm_coeff("h_sum")
        hub_norm(h_coeff)
    

main()