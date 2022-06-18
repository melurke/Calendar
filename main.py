import datetime as dt
import PySimpleGUI as sg
import asyncio
import python_weather

temp = ""
sky = ""
city = "" # Type in your city

sg.theme('Black')

# ---------Get Weather Data---------
async def getweather():
    client = python_weather.Client(format=python_weather.METRIC)
    weather = await client.find(city)
    global temp
    global sky
    temp = weather.current.temperature
    sky = weather.current.sky_text
    await client.close()

loop = asyncio.get_event_loop()


# ---------Main Code---------

layout = [[sg.Text('Time: '), sg.Text('', key='_time_', size=(20, 1))],
         [sg.Text('Date: '), sg.Text('', key='_date_', size=(20, 1))],
         [sg.Text('Temperature: '), sg.Text('', key='_temperature_', size=(20, 1))],
         [sg.Text('Weather: '), sg.Text('', key='_weather_', size=(20, 1))],
         [sg.Quit()]]

window = sg.Window('Calendar').Layout(layout)

while True:
    event, values = window.Read(timeout=10)

    loop.run_until_complete(getweather())

    # -----Close window-----
    if event in (None, 'Quit'):
        break

    # -----Update time-----
    window.find_element('_time_').Update(dt.datetime.now().strftime('%H:%M:%S'))
    window.find_element('_date_').Update(dt.datetime.now().strftime('%d.%m.%Y'))

    # -----Update Weather-----
    window.find_element('_temperature_').Update(str(temp)+"°C")
    window.find_element('_weather_').Update(sky)
