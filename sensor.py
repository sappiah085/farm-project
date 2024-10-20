from pymodbus.client import ModbusSerialClient as ModbusClient


# Sensor specific settings (change these as per your sensor documentation)
SENSOR_MODBUS_ADDRESS = 1  # The Modbus ID of the sensor
PORT = '/dev/ttyUSB0'  # Replace with the correct serial port

# Modbus client setup for RTU (over RS-485)
client = ModbusClient( port=PORT,baudrate=9600, timeout=1, stopbits=1, bytesize=8, parity='N')

# Connect to the sensor
client.connect()

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
  temperature_register = 0x0000   
  moisture_register = 0x0001     
  ec_register = 0x0002           
  salinity_register = 0x0007     
  n_register = 0x0004          
  ph_register = 0x0003
  p_register = 0x0005
  k_register = 0x0006      
    
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


