import os
import sys
import begin
import subprocess

''' IDEA: we can create an Alltoall superclass for other alltoall 
	implementations (Intel Micro Benchmark (IMB) etc.)
'''

class OSU_Alltoall():
    def __init__(self, params):
        self.source_code = "./osu_alltoall.c"
        self.binary      = "./osu_alltoall"
        self.run_args    = "-f"

        self.__compile(params)

    def add_run_args(self, params):
	    if "message_sizes" in params:
	        self.run_args =  self.run_args + " -m " + params["message_sizes"]
	    if "iterations" in params:
	        self.run_args =  self.run_args + " -x " + params["iterations"]

    def run_command(self, params=None):
    	return self.binary + " " + self.run_args

    def execute(self, mpirun, mpi_args):
		cmd  = " ".join([mpirun, mpi_args, self.run_command()])
		proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		stdout, stderr = proc.communicate()

		if len(stderr) == 0:
    		return self.__parse_output(stdout.splitlines()[3:])
    	else:
    		print "ERROR: \n" + stderr
    		exit(1) 

    def __compile(self, params=None):
        pass

    def __parse_output(self, output):
    	results = {}

    	for line in output:
    		size, t_avg, t_min, t_max, iterations = line.split()
    		results[size] = {}
    		results[size]["avg"] = t_avg
    		results[size]["min"] = t_min
			results[size]["max"] = t_max
			results[size]["iterations"] = iterations

		return results

''' In principle, we should be able to get a binary that has been compiled using the 
	MPI library that we are benchmarking (Open MPI, MVAPICH, MPICH, etc)
'''
def get_app(params=None):
	app = OSU_Alltoall(params)

	return app

@begin.start
def main():
    app = get_app(None)
    print (app.run_command(None))

