from pymodbus.client import ModbusSerialClient as ModbusClient


# Sensor specific settings (change these as per your sensor documentation)
SENSOR_MODBUS_ADDRESS = 1  # The Modbus ID of the sensor
PORT = '/dev/ttyUSB0'  # Replace with the correct serial port


temperature_register = 0x0000   
moisture_register = 0x0001     
ec_register = 0x0002           
salinity_register = 0x0003     
n_register = 0x0004          
ph_register = 0x0007
p_register = 0x0005
k_register = 0x0006      
  
# Modbus client setup for RTU (over RS-485)
client = ModbusClient( port=PORT,baudrate=9600, timeout=1, stopbits=1, bytesize=8, parity='N')

# Connect to the sensor
client.connect()


def calibrate_ph():
    # Select pH calibration channel
    client.write_register(0x006F, ph_register)
    
    # Calibrate with pH 4.01 solution
    client.write_register(0x0055, 0x0000)
    
    # Calibrate with pH 6.86 solution
    client.write_register(0x0056, 0x0000)
    
    # Calibrate with pH 9.18 solution
    client.write_register(0x0057, 0x0000)

    # Save the calibration settings
    client.write_register(0x006D, 0x01C2)
    client.write_register(0x006E, 0x0320)

    print("pH calibration completed successfully.")



def calibrate_moisture():
    # Select moisture calibration channel
    client.write_register(0x006F, moisture_register)
    
    # Calibrate moisture in air (0%)
    client.write_register(0x0055, 0x0000)
    
    # Calibrate moisture in water (100%)
    client.write_register(0x0057, 0x0000)
    
    print("Moisture calibration completed successfully.")
    



def calibrate_temperature():
    # Select temperature calibration channel
    client.write_register(0x006F, temperature_register)
    
    # Example: Increase temperature by 1°C
    client.write_register(0x0054, 0x000A)
    
    # Example: Decrease temperature by 1°C (use FF F6 to decrease by 1)
    client.write_register(0x0054, 0xFFF6)

    print("Temperature calibration completed successfully.")





def calibrate_ec():
    # Select EC calibration channel
    client.write_register(0x006F, ec_register)
    
    # Example: Increase EC by 10 units
    client.write_register(0x0054, 0x000A)
    
    # Example: Decrease EC by 10 units
    client.write_register(0x0054, 0xFFF6)

    print("EC calibration completed successfully.")




def calibrate_nitrogen():
    # Select nitrogen calibration channel
    client.write_register(0x006F, n_register)
    
    # Example: Increase nitrogen by 5 mg/kg
    client.write_register(0x0054, 0x0005)
    
    print("Nitrogen calibration completed successfully.")

def calibrate_phosphorus():
    # Select phosphorus calibration channel
    client.write_register(0x006F, p_register)
    
    # Example: Increase phosphorus by 10 mg/kg
    client.write_register(0x0054, 0x000A)
    
    print("Phosphorus calibration completed successfully.")

def calibrate_potassium():
    # Select potassium calibration channel
    client.write_register(0x006F, k_register)
    
    # Example: Increase potassium by 15 mg/kg
    client.write_register(0x0054, 0x000F)
    
    print("Potassium calibration completed successfully.")

def calibrate_salinity():
    # Select salinity calibration channel
    client.write_register(0x006F, salinity_register)
    
    # Example: Increase salinity by 10 units
    client.write_register(0x0054, 0x000A)
    
    print("Salinity calibration completed successfully.")

# Run calibration for each parameter
#calibrate_nitrogen()
#calibrate_phosphorus()
#calibrate_potassium()
#calibrate_salinity()
#calibrate_ec()
#calibrate_temperature()
#calibrate_moisture()
#calibrate_ph()







# Function to read sensor data from the specified register
def read_register(register, count=1):
    try:
        result = client.read_holding_registers(register, count, slave=SENSOR_MODBUS_ADDRESS)
        if result.isError():
            print(f"Error reading register {register}: {result}")
            return None
        return result.registers
    except Exception as e:
        print(f"Exception: {e}")
        return None


def read_sensor_data():  
    # Read temperature
  temp_data = read_register(temperature_register)
  temperature = temp_data[0] / 10.0

    
  p_data = read_register(p_register)
  p = p_data[0]  # Assuming scale of 0.1% RH

    
    # Read CO2 concentration
  k_data = read_register(k_register)
  k = k_data[0]  # Assuming no scaling

    
  moisture_data = read_register(moisture_register)
  moisture = moisture_data[0]/10

  
  ec_data = read_register(ec_register)
  ec = ec_data[0]

  
  salinity_data = read_register(salinity_register)
  salinity = salinity_data[0]

  
  n_data = read_register(n_register)
  n = n_data[0]

  
  Ph_data = read_register(ph_register)
  ph = Ph_data[0] / 100.0
  return {
            "temperature": temperature,
            "n": n,
            "p": p ,
            "moisture": moisture,
            "ec": ec,
            "salinity": salinity,
            "k": k,
            "ph": ph,
        }     


