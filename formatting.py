empty_data = 'N/A'

def format_data(temp, humidity):
    temp_string = '{:.1f}C'.format(temp) if temp is not None else empty_data
    hum_string = '{:.1f}%'.format(humidity) if humidity is not None else empty_data
    
    return (temp_string, hum_string)