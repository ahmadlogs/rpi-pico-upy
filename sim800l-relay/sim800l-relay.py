from machine import UART, Pin

#import time

#Issue: uart.readline() doesn't read line properly
#Solution: increase the timeout value to 3000ms or 4000ms
gsm_module = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5), timeout=2000)
gsm_buffer = ''

########################################################################
#this phone number is used to send commands
# and receive response from the project
#Note: Don't enter the SIM800L phone number here
destination_phone = 'ENTER_YOUR_PHONE_NUMBER'
########################################################################

relay1 = Pin(2, Pin.OUT)
relay2 = Pin(3, Pin.OUT)

########################################################################
def convert_to_string(buf):
    tt =  buf.decode('utf-8').strip()
    return tt
########################################################################

########################################################################
def do_action(msg):
    msg = msg.lower()
    #print('do_action: '+msg)
    if(msg.strip() == 'relay1 off'):
        relay1(0)
        send_sms('Relay1 is OFF')
    elif(msg.strip() == "relay1 on"):
        relay1(1)
        send_sms('Relay1 is ON')
    elif(msg.strip() == 'relay2 off'):
        relay2(0)
        send_sms('Relay2 is OFF')
    elif(msg.strip() == 'relay2 on'):
        print('do_action1: '+msg)
        relay2(1)
        send_sms('Relay2 is ON')
########################################################################

########################################################################
def send_command(cmdstr, lines=1, msgtext=None):
    global gsm_buffer
    #___________________________________________________________________
    print(cmdstr)
    cmdstr = cmdstr+'\r\n'
    #___________________________________________________________________
    #Empty the serial buffer
    while gsm_module.any():
        gsm_module.read()
    #___________________________________________________________________
    #Send command to sim800l
    gsm_module.write(cmdstr)
    #___________________________________________________________________
    #Only used while sending sms
    if msgtext:
        print(msgtext)
        gsm_module.write(msgtext)
    #___________________________________________________________________        
    #while gsm_module.any():
    #pass
    #___________________________________________________________________
    #read data comming from sim800l line by line
    buf=gsm_module.readline() #discard linefeed etc
    #print('discard linefeed:{}'.format(buf))
    buf=gsm_module.readline()
    #print('next linefeed:{}'.format(buf))
    #___________________________________________________________________
    if not buf:
        return None
    result = convert_to_string(buf)
    #___________________________________________________________________
    #if there are multiple lines of data comming from sim800l
    if lines>1:
        gsm_buffer = ''
        for i in range(lines-1):
            buf=gsm_module.readline()
            if not buf:
                return result
            #print(buf)
            buf = convert_to_string(buf)
            if not buf == '' and not buf == 'OK':
                gsm_buffer += buf+'\n'
    #___________________________________________________________________
    return result
########################################################################

########################################################################
def read_sms(sms_id):
    result = send_command('AT+CMGR={}\n'.format(sms_id),99)
    print(result)
    #___________________________________________________________________
    if result:
        #NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
        #+CMGR: "REC READ","+923001234567","","21/04/18,11:15:53+20"
        params=result.split(',')
        if params[0] == '':
           return None
        #NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
        params2 = params[0].split(':')
        if not params2[0]=='+CMGR':
            return None
        #NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
        number = params[1].replace('"',' ').strip()
        date   = params[3].replace('"',' ').strip()
        time   = params[4].replace('"',' ').strip()
        #print('gsm_buffer:'+gsm_buffer)
        return  [number,date,time,gsm_buffer]
        #NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
########################################################################

########################################################################
def send_sms(msgtext):
    global gsm_buffer
    result = send_command('AT+CMGS="{}"\n'.format(destination_phone),99,msgtext+'\x1A')
    if result and result=='>' and gsm_buffer:
        params = gsm_buffer.split(':')
        if params[0]=='+CUSD' or params[0] == '+CMGS':
            print('OK')
            return 'OK'
    print('ERROR')
    return 'ERROR'
########################################################################    
print(send_command('AT'))
print(send_command('AT+CMGF=1'))
#______________________________________________________
#delete all sms from sim800l memory
#print(send_command('AT+CMGD=1,4'))
#______________________________________________________
#send ussd code
#print(send_command('AT+CUSD=1,"*ENTER_YOUR_USSD_CODE#"'))
#______________________________________________________
#read_sms(1)
#send_sms('ddddd')

########################################################################
while True:
    if gsm_module.any():
        buf=gsm_module.readline()
        buf = convert_to_string(buf)
        print(buf)
        
        params=buf.split(',')
        #if params[0] == "RING":
        #elif params[0][0:5] == "+CLIP":
        #elif params[0][0:5] == "+CUSD":
        #elif params[0] == "NO CARRIER":
        #NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
        if params[0][0:5] == "+CMTI":
            msgid = int(params[1])
            msg_data = read_sms(msgid)
            #______________________________________________________
            if not msg_data:
                print("No sms data found.")
                break
            #______________________________________________________
            #print(msg_data[0]) #Sender Phone Number
            #print(msg_data[1]) #Received SMS Date
            #print(msg_data[2]) #Received SMS Time
            print(msg_data[3]) #Received SMS Text
            #______________________________________________________
            if not msg_data[0] == destination_phone:
                print("Destination phone pumber not matching")
                break
            #______________________________________________________
            #function to turn ON or OFF relays
            do_action(msg_data[3])
            #______________________________________________________
        #NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
########################################################################