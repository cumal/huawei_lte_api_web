from nicegui import ui
from huawei_lte_api.Client import Client
from huawei_lte_api.Connection import Connection
import requests
import urllib3
import os
import re

urllib3.disable_warnings()
user = os.getenv('API_USER')
passw = os.getenv('API_PASSW')
router_ip= os.getenv('API_IP')
url = "https://" + user + ":" + passw + "@" + router_ip + "/"

def create_session():
    # with Connection('http://192.168.8.1/') as connection: For limited access, I have valid credentials no need for limited access
    session = requests.Session()
    session.verify = False
    return session

def update_dns():
    session = create_session()
    with Connection(url, requests_session=session) as connection:
        client = Client(connection) # This just simplifies access to separate API groups, you can use device = Device(connection) if you want
        ip1 = "192.168.1.5"
        ip2 = ""
        dnsstatus=False
        was = client.dhcp.set_settings(dhcp_ip_address=router_ip, dhcp_lan_netmask="255.255.255.0", dhcp_status=True, dhcp_start_ip_range=100, dhcp_end_ip_range=200, dhcp_lease_time=86400, dns_status=dnsstatus, primary_dns=ip1, secondary_dns=ip2, show_dns_setting=True)
        ui.notify(str(was))
    session.close()

def restore_dns():
    session = create_session()
    with Connection(url, requests_session=session) as connection:
        client = Client(connection) # This just simplifies access to separate API groups, you can use device = Device(connection) if you want
        ip1="8.8.8.8"
        ip2="8.8.4.4"
        dnsstatus=True
        was = client.dhcp.set_settings(dhcp_ip_address=router_ip, dhcp_lan_netmask="255.255.255.0", dhcp_status=True, dhcp_start_ip_range=100, dhcp_end_ip_range=200, dhcp_lease_time=86400, dns_status=dnsstatus, primary_dns=ip1, secondary_dns=ip2, show_dns_setting=True)
        ui.notify(str(was))
    session.close()

def fix_val(value, regex, best, worst):
    rex = re.search(regex, value)
    val = float(rex.group(1))
    percent = (worst - val) / (worst - best)
    return round(percent, 2)

def get_color(percent):
    if (percent > 0.7):
        color = "green"
    elif (percent > 0.4):
        color = "yellow"
    else:
        color = "red"
    return color

def get_info():
    session = create_session()
    with Connection(url, requests_session=session) as connection:
        client = Client(connection) # This just simplifies access to separate API groups, you can use device = Device(connection) if you want
        signal = client.device.signal()
        ui.notify(str(signal))  # Can be accessed without authorization
        ui.notify(str(client.device.information()))  # Needs valid authorization, will throw exception if invalid credentials are passed in URL
        ui.notify(str(client.dhcp.settings()))
    session.close()

    val = fix_val(signal["rsrq"], "-(\d+\.\d+)dB", 5, 18)
    color = get_color(val)
    i.style('color: ' + color)
    i.props('color=' + color)
    i.set_value(val)
    i.tooltip(str(signal["rsrq"]))

    val = fix_val(signal["rsrp"], "-(\d+)dBm", 95, 65)
    color = get_color(val)
    j.style('color: ' + color)
    j.props('color=' + color)
    j.set_value(val)
    j.tooltip(str(signal["rsrp"]))

def reboot_router():
    session = create_session()
    with Connection(url, requests_session=session) as connection:
        client = Client(connection)
        if client.device.reboot() == ResponseEnum.OK.value:
            ui.notify('Reboot requested successfully')
        else:
            ui.notify('Error requesting reboot')
    session.close()

with ui.column().classes('fixed-center').style('align-items: center;'):
    with ui.card().style('align-items: center;'):
        ui.label("Router configuration")
        ui.link('Router website', 'https://' + router_ip + "/", new_tab=True).style('color: inherit;')
        ui.button('Update DNS', on_click=lambda: [update_dns()])
        ui.button('Restore DNS', on_click=lambda: [restore_dns()])
        ui.button('Get info', on_click=lambda: [get_info()])
        ui.button('Reboot', on_click=lambda: [reboot_router()])
        with ui.row().style('align-items: center;'):
            ui.label("RSRQ")
            ui.label("RSRP")
        with ui.row().style('align-items: center;'):
            i = ui.circular_progress()
            j = ui.circular_progress()

ui.run(port=2233, title="RouterConfig", dark=None, reload=False)
