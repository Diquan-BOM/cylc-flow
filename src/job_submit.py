#!/usr/bin/python

import os
import re
import config

# TO DO: EXTERNAL PROGRAMS AND MODULE LOCATIONS
# path = config.task_launch_dir

def run( owner, task_name, ref_time, task, extra_vars=[] ):

    #external_task = path + '/' + task
    external_task = task
    if config.dummy_mode or task_name in config.dummy_out:
        # RUN AN EXTERNAL DUMMY TASK
        external_task = "dummy_task.py"

        if config.dummy_job_launch == "direct":
            command =  'export REFERENCE_TIME=' + ref_time + '; '
            command += 'export TASK_NAME=' + task_name + '; '
            command += external_task + ' ' + task_name + ' ' + ref_time + ' ' + config.pyro_ns_group + ' ' + str( config.dummy_mode ) + ' ' + str( config.dummy_clock_rate ) + ' ' + str( config.dummy_clock_offset ) + ' &' 

            if os.system( command ) != 0:
                raise Exception( 'dummy_task.py failed: ' + task_name + ' ' + ref_time )
            return

    # ECOCONNECT: modify owner if we're running on /test or /dvel
    sequenz_owner = os.environ[ 'USER' ]
    if re.search( '_test$', sequenz_owner) or re.search( '_dvel$', sequenz_owner ): 
            system = re.split( '_', sequenz_owner )[-1]
            owner = re.sub( '_oper$', '_' + system, owner )

    #====================================
    print "!!!!!!!!job_submit.py: DISABLING QSUB"

    command = ''
    for entry in extra_vars:
        [ var_name, value ] = entry
        command += 'export ' + var_name + '=' + value + '; '

    command += 'export REFERENCE_TIME=' + ref_time + '; export TASK_NAME=' + task_name + '; ' + external_task + '&'
    print command
    if os.system( command ) != 0:
        raise Exception( 'job launch failed' )

    return
    #====================================

    if owner == sequenz_owner: 
        command = ''
    else:
        command  = 'sudo -u ' + owner 

    print "job_submit.py: TEMPORARILY using topnet_test queue"
    # command += ' qsub -q ' + system + ' -z'
    command += ' qsub -q topnet_test -z'

    command += ' -v REFERENCE_TIME=' + ref_time
    command += ',TASK_NAME=' + task_name

    for entry in extra_vars:
        [ var_name, value ] = entry
        command += ',' + var_name + '=' + value

    command += ' -k oe ' + external_task

    if os.system( command ) != 0:
        raise Exception( 'job launch failed: ' + task_name + ' ' + ref_time )
