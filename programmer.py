import time
import serial.tools.list_ports
import os

# Definicja kodów kolorów ANSI
RED = '\033[91m'
GREEN = '\033[92m'
END = '\033[0m'

from termcolor import colored



   


#ramka na gorze

def print_mega_in_yellow_frame():
    #print("\n" * 1)
    
    text1 = "Programator Megaelektronik v1.0"
    text2 = "      powered by gramszu"
    
    max_len = max(len(text1), len(text2))
    
    framed_text = f"{'*' * (max_len + 4)}\n"
    
    framed_text += f"* {colored(text1, 'blue')}{' ' * (max_len - len(text1))} *\n"
    framed_text += f"* {colored(text2, 'blue')}{' ' * (max_len - len(text2))} *\n"
    
    framed_text += f"{'*' * (max_len + 4)}"

    print(framed_text)






    

def program_device(software_choice):
    # Zdefiniuj VID i PID urządzenia, które chcesz znaleźć
    VENDOR_ID = 0x067b
    PRODUCT_ID = 0x2303

    # Szukaj urządzeń z określonym VID i PID
    urzadzenie = next((d for d in serial.tools.list_ports.comports() if d.vid == VENDOR_ID and d.pid == PRODUCT_ID), None)

    if urzadzenie is None:
        print(RED + '*** error connect the programmer ***' + END)  # Wyświetlenie w czerwonym kolorze
        print("\n" * 2)
        return
    else:
        print(f'Find programmer {urzadzenie.device}')
        port = urzadzenie.device

    programmer = 'avrispmkII'
    avr_type = 'atmega328pb'
    files_dir = ""

    if software_choice == 1:
        files_dir = os.path.expanduser('~/Desktop/megaelektronik/programator/bramster')
        software_name = "Sim Ster +"
    elif software_choice == 2:
        files_dir = os.path.expanduser('~/Desktop/bram_ster_plus')
        software_name = "Bram Ster +"
    elif software_choice == 3:
        files_dir = os.path.expanduser('~/Desktop/sim_eco_plus')
        software_name = "Sim Eco +"
    else:
        print("Incorrect selection. Try again.")
        return

    print(f'starting to program the device with software: {software_name}...')

    if os.system(f'avrdude -F -c {programmer} -p {avr_type} -P {port}') != 0:
        #print('Error : no connection microcontroller')
        print(RED + '*** error connection microcontroller ***' + END)  # Wyświetlenie w czerwonym kolorze
        print("\n" * 2)
        return

    if os.system(f'avrdude -c {programmer} -p {avr_type} -P {port} -e') != 0:
        print('error : comunication')
        print(RED + 'ERROR*' + END)  # Wyświetlenie w czerwonym kolorze
        print("\n" * 2)
        return

    time.sleep(2)

    if os.system(f'avrdude -c {programmer} -p {avr_type} -P {port} -V -u -U flash:w:"{files_dir}/FH_BS_125.hex":i') != 0:
        #print('Błąd: Błąd zapisu do flash')
        print(RED + '*** Error  write to flash ***' + END)  # Wyświetlenie w czerwonym kolorze
        print("\n" * 2)
        return

    if os.system(f'avrdude -c {programmer} -p {avr_type} -P {port} -V -u -U eeprom:w:"{files_dir}/EE_BS_125.hex":i') != 0:
        print("\n" * 2)
        print('Błąd: Error EEPROM')
        print(RED + '** error write EEPROM *' + END)  # Wyświetlenie w czerwonym kolorze
        return

    # Programowanie bitów fuse i lock
    if os.system(f'avrdude -p {avr_type} -c {programmer} -P {port} -V -u -U lfuse:w:0xFD:m -U hfuse:w:0xC9:m -U efuse:w:0xFD:m -U lock:w:0x3C:m') != 0:
        print(RED + 'Błąd: Komenda avrdude zwróciła niezerowy status wyjścia *' + END)  # Wyświetlenie w czerwonym kolorze
        print("\n" * 2)
        return

  
    colored_text = colored(f'The device has been programmed correctly: {software_name}.', 'green')
    print(colored_text)
    print("\n" * 1)
    

if __name__ == "__main__":
    while True:
        print_mega_in_yellow_frame()

        software_choice = int(input("Select software:\n1. Sim Ster +\n2. Bram Ster +\n3. Sim Eco +\n4. Exit\n"))
        print("\n" * 2)
        if software_choice == 4:
            break
        elif 1 <= software_choice <= 3:
            program_device(software_choice)
        else:
            print("Error selection, please try again")
            print("\n" * 2)
