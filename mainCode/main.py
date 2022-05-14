import logging
import RPi.GPIO as GPIO
#local imports
from checkBattery import *
from deployAntenna import *
from detumble import *
from hddImagingMode import *
from hddTest import *
from mrwImagingMode import *
from readFile import *
from writeFile import *

#Format follows convention of: Level of Warning, Time (down to the ms), Message
LOG_FORMAT = "%(levelname)s %(asctime)s -> %(message)s"
logging.basicConfig(filename = "logger.txt", level = logging.DEBUG, format = LOG_FORMAT)
logger = logging.getLogger()

def main():

    logger.info("Starting main loop")

    # Check if we need to wait 30 minutes (first time booting up)
    t = open("initialTimer.txt", "r")
    initialTimer = t.readline()
    t.close()
    logging.debug('Succesfully read initialTimer.txt')

    if initialTimer.strip()=='yes':
        # Here it will wait for 30 minutes
        logging.debug('Succesfully waited 30 minutes')
        # Write no to file so it doesn't wait the 30 minutes next time it boots up
        f = open("initialTimer.txt","w")
        f.write("no")
        f.close()
        logging.debug('Succesfully wrote "no" to initialTimer.txt')


    #check if antenna has been deployed
    a = open("antennaDeploy.txt","r")
    ifAntennaDeploy=a.readline()
    a.close()
    if ifAntennaDeploy.strip()=='no':
        #actually deploy the antenna
        deployAntenna()
        #write to text file so antenna doesn't deploy again
        b = open("antennaDeploy.txt","w")
        b.write("yes")
        b.close()
        logging.debug('Succesfully wrote "no" to antennaDeploy.txt')


    #get first line of respective file
    batteryText = readFile("batteryText.txt")
    healthText = readFile("healthFile.txt")
    beaconText = readFile("beacon.txt")

    if batteryText.strip()=='yes':
        logging.info("Battery check said yes")
        print('checking battery')
        #actually check the battery
        checkBattery()
        # write no to file and restart timer
        writeFile("batteryText.txt","no")
    if healthText.strip()=='yes':
        logging.info("Health check said yes")
        writeFile("healthFile.txt","no")
    if beaconText.strip()=='yes':
        logging.info("Beacon check said yes")
        writeFile("beacon.txt","no")

    #check the battery before hitting the schedule so you dont die mid hdd or mrwtest
    checkBattery()

    #this is checking what mode it should be in
    mode = readFile("scheduleTimer.txt")

    if mode == 'detumble':
        logging.debug("Calling detumble function")
        print('calling detumble function')
        #Insert ADCS function call here
        #Main_ADCS(sunsensor_input, mag_inputs, angvel_inputs, epoch_time, mode, TLE)
        #detumble()
    elif mode == 'mrwPointing':
        logging.debug("Calling ADCS MRW Pointing")
        print("Calling ADCS MRW Pointing")
        #Insert ADCS function call here
        #Main_ADCS(sunsensor_input, mag_inputs, angvel_inputs, epoch_time, mode, TLE)
        #hddTest()
    elif mode == 'mrwImaging':
        logging.debug("Calling ADCS MRW Imaging function")
        print("Calling ADCS MRW Imaging function")
        #Insert ADCS function call here
        #Main_ADCS(sunsensor_input, mag_inputs, angvel_inputs, epoch_time, mode, TLE)
        #mrwTest()
    elif mode == 'hddPointing':
        logging.debug("Calling ADCS HDD Pointing function")
        print("Calling ADCS HDD Pointing function")
        #Insert ADCS function call here
        #Main_ADCS(sunsensor_input, mag_inputs, angvel_inputs, epoch_time, mode, TLE)
        #hddImagingMode()
    elif mode == 'hddImaging':
        logging.debug("Calling ADCS HDD Imaging function")
        print("Calling ADCS HDD Imaging function")
        #Insert ADCS function call here
        #Main_ADCS(sunsensor_input, mag_inputs, angvel_inputs, epoch_time, mode, TLE)
        #mrwImagingMode()
    #elif mode == "rotisserie":
        #logging.debug("Calling ADCS Rotisserie function")
        #print("Calling ADCS Rotisserie function")
        #Insert ADCS function call here
        #Main_ADCS(sunsensor_input, mag_inputs, angvel_inputs, epoch_time, mode, TLE)
main()
