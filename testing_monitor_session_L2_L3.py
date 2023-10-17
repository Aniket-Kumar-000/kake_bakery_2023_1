from ats import tcl
from ats import aetest
from ats.log.utils import banner
import time
import logging
import os
import sys
import re
import pdb
import json
import pprint
import socket
import struct
import inspect

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
global uut1           
global uut1_intf1, uut1_intf2

def L3_intf(intf1,intf2,dev):
        log.info("No Switch Ports")
        cmd = """interface %s
                 no switchport
                 no shut
                 interface %s
                 switchport
                 switchport monitor
                 no shut
                 """%(intf1,intf2)
        status = True        
        try:
            dev.configure(cmd)
        except:
            log.error('Invalid CLI given: %s' % (cmd))
            status = False
        return status         



def L2_intf(intf1,intf2,dev):
        log.info("Switch Ports")
        cmd = """interface %s
                 switchport
                 no shut
                 interface %s
                 switchport
                 switchport monitor
                 no shut
                 """%(intf1,intf2)
        status = True         
        try:
            dev.configure(cmd)
        except:
            log.error('Invalid CLI given: %s' % (cmd))
            status = False
        return status



def SnD_ports(num,intf1,intf2,num2,dev):
        log.info(f"Creating Monitor Session {num} Source and Destination and filtering the VLAN 3 traffic...")
        cmd = """monitor session %s
                 no shut
                 source int %s
                 destination int %s
                 filter vlan %s
                 exit
                 """%(num,intf1,intf2,num2)
        status = True
        try:
            dev.configure(cmd)
        except:
            log.error('Invalid CLI given: %s' % (cmd))
            status = False
        return status



def swi_mon(intf,dev):
        log.info("Making Destination port as a Switchport Monitor...")
        cmd = """interface %s
                 switchport
                 switchport monitor
                 no shut
                 exit
                 """%(intf)
        status = True
        try:
            dev.configure(cmd)
        except:
            log.error('Invalid CLI given: %s' % (cmd))
            status = False
        return status      



def run_conf(num,dev):
    
        log.info("Checking running-configs of monitor session")
        cmd = """monitor session %s
                 sh running-config monitor
                 """%(num)
        status = True
        try:
            output = dev.configure(cmd)
            return output
        except:
            log.error('Invalid CLI given: %s' % (cmd))
            status = False
        return status



def run_conf_check(intf1,intf2,Out):
        put = ()
        if "monitor session 2" in Out:
            m = (("source interface Ethernet {0} both").format(intf1))
            
            if m in Out:
                n = (("destination interface Ethernet {1}").format(intf2))
                
                if n in Out:
                    
                    if "filter vlan 3" in Out:
                        
                        if "no shut" in Out:
                            put = "pass"
        else:
            put = "fail"
        return put       



def consis_check(num,dev):
        cmd = """show consistency-checker monitor session %s
              """%(num)
        status = True
        try:
            output = dev.configure(cmd)
            return output
        except:
            log.error('Invalid CLI given: %s' % (cmd))
            status = False
        return status
        
    
    
def mon_sess(intf1,intf2,num,dev):
        cmd = """int %s
                 no shut
                 int %s
                 no shut
                 show monitor session %s
              """%(intf1,intf2,num)
        status = True
        try:
            output = dev.configure(cmd)
            return output
        except:
            log.error('Invalid CLI given: %s' % (cmd))
            status = False
        return status



class Span_config(aetest.Testcase):
    
    @aetest.test
    def basic(self):
        log.info("Collecting internal build version...")
        
        cmd = """sh version internal build-identifier"""
        uut1.execute(cmd)
        
        log.info(f"Creating a vlan {v}")
         
        cmd = """vlan %s"""%(v)
        uut1.configure(cmd)
        
###############################################################################################
    @aetest.test
    def test_L2(self):
      
        log.info(("Configuration of {0} and {1}").format(uut1_intf1,uut1_intf2))
         
        buglib.L2_intf(uut1_intf1,uut1_intf2,uut1)
            
        buglib.SnD_ports(s,uut1_intf1,uut1_intf2,v,uut1)
    
        #buglib.swi_mon(uut1_intf2,uut1)        
    
    @aetest.test
    def run_conf_check_L2(self):
        
        log.info("CHECKING THE RUNNING CONFIGS OF MONITOR SESSION...")
         
        Output = buglib.run_conf(s,uut1)
        
        k = ((f"monitor session {s}"))
        
        if k in Output:
            m = (("source interface Ethernet {0} both").format(uut1_intf1))
            
            if m in Output:
                n = (("destination interface Ethernet {1}").format(uut1_intf2))
                
                if n in Output:
                    l = ((f"filter vlan {v}"))
            
                    if l in Output:
                        
                        if "no shut" in Output:
                            log.info("PASSED")
        else:    
            log.error("##########_____Fail_____##########")
            self.failed()
            
    @aetest.test
    def status_in_L2(self):
        
        log.info("CHECKING THE STATUS OF MONITOR SESSION...")
         
        Output = buglib.mon_sess(uut1_intf1,uut1_intf2,s,uut1)
        if "down" in Output:
            log.error("##########_____Fail_____##########")
            self.failed()
            
    @aetest.test
    def CC_check_L2(self):
        
        log.info("CONSISTENCY CHECKER...")
         
        Output = buglib.consis_check(s,uut1)
        if "FAILED" in Output:
            log.error("##########_____Fail_____##########")
            self.failed()
        else:
            log.info("PASSED")        
###############################################################################################
    
###############################################################################################
# Test case 2 :                                                                               #
###############################################################################################
    @aetest.test
    def test_L3(self):
      
        log.info(("Configuring {0} and {1}").format(uut1_intf1,uut1_intf2))
        
        buglib.L3_intf(uut1_intf1,uut1_intf2,uut1)
        
        buglib.SnD_ports(s,uut1_intf1,uut1_intf2,v,uut1)
        
        # buglib.swi_mon(uut1_intf2,uut1)
                
    @aetest.test
    def run_conf_check_L3(self):
        
        log.info("CHECKING THE RUNNING CONFIGS OF MONITOR SESSION...")
         
        Output = buglib.run_conf(s,uut1)
        
        k = ((f"monitor session {s}"))
        
        if k in Output:
            m = (("source interface Ethernet {0} both").format(uut1_intf1))
            
            if m in Output:
                n = (("destination interface Ethernet {1}").format(uut1_intf2))
                
                if n in Output:
                    l = ((f"filter vlan {v}"))
            
                    if l in Output:
                        
                        if "no shut" in Output:
                            log.info("PASSED")
        else:    
            log.error("##########_____Fail_____##########")
            self.failed()
            
    @aetest.test
    def status_in_L3(self):
        
        log.info("CHECKING THE STATUS OF MONITOR SESSION...")
         
        Output = buglib.mon_sess(uut1_intf1,uut1_intf2,s,uut1)
        if "down" in Output:
            log.error("##########_____Fail_____##########")
            self.failed()
            
    @aetest.test
    def CC_check_L3(self):
        
        log.info("CONSISTENCY CHECKER...")
         
        Output = buglib.consis_check(s,uut1)
        if "FAILED" in Output:
            log.error("##########_____Fail_____##########")
            self.failed()
        else:
            log.info("PASSED")
###############################################################################################            
    @aetest.test
    def removing(self):
        cmd = """no monitor session %s
              """%(s)
        uut1.configure(cmd)
        
        cmd = """no vlan %s
              """%(v)
        uut1.configure(cmd)      
