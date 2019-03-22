# -*- coding: utf-8 -*-

# mui network utility class
# when using this utility, user must be root/admin.

from threading import Thread
from threading import Timer
from multiping import MultiPing

import subprocess


class MuiNetworkUtil(object):
    """
    net work utility class
    """

    def check_internet_access(self):
        """
        check internet access via Ping
        Pingでインターネット接続を確認する
        """
        connect = False

        try:
            mp = MultiPing(['google.com'])
            mp.send()
            responses, no_responses = mp.receive(1)
            if len(responses) > 0:
                connect = True
        except Exception as e:
            print(e)

        return connect

    def set_new_wpa_config(self, key: str, value: str, file_path: str='/etc/wpa_supplicant/wpa_supplicant.conf'):
        """
        re-write target key of wpa_supplicant.conf
        if you want to delete target key line, please set None to value.

        wpa_supplicant.confの指定キーを更新する.
        valueにNoneを設定することで指定キー行を削除できる

        Parameters
        -----------
        key : str
            target key
        value : str
            value
        file_path : str
            path of wpa_supplicant.conf
        """

        with open(file_path,'r') as f:
            in_file = f.readlines()
            f.close()
            
        out_file = []
        exist_target_line = False
        for line in in_file:
            skip_line = False

            if line.lstrip().startswith(key):
                if value is not None:
                    line = '    ' + key + '=' + value + '\n'
                else:
                    # 対象のキーを削除したいとき
                    skip_line = True

                exist_target_line = True

            elif line.startswith('}'):
                # 対象のキーがなかったら}の前に新規で追加
                if (exist_target_line is False) and (value is not None):
                    new_line = '    ' + key + '=' + value + '\n'
                    out_file.append(new_line)

            if skip_line is False:
                out_file.append(line)

                
        with open(file_path,'w') as f:
            for line in out_file:
                f.write(line)

            f.close()

    def get_ip_address(self):
        """
        get current IP address of Wi-Fi module
        Wi-Fiモジュールの現在のIPアドレスを取得する
        """
        ssid = '0.0.0.0'
        wlan0 = subprocess.Popen(['ifconfig', 'wlan0'], stdout=subprocess.PIPE)
        try:
            out, err = wlan0.communicate()
            s = out.decode()
            for line in s.split('\n'):
                line = line.lstrip()
                if line.startswith('inet '):
                    l2 = line.split(' ')[1]
                    ssid = l2

        except subprocess.CalledProcessError as e:
            pass

        return ssid

    def get_wifi_ssid(self):
        """
        get current connected access point ssid of Wi-Fi module
        Wi-Fiモジュールが接続しているアクセスポイントのSSIDを取得する
        """
        ps = subprocess.Popen(['iwconfig'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        ssid = None
        try:
            o = subprocess.check_output(('grep', 'ESSID'), stdin=ps.stdout)
            s0 = o.decode('utf-8')
            s1 = s0.split()
            s2 = [s for s in s1 if s.startswith('ESSID')]
            ssid = s2[0].split(':')[1][1:-1]
            if ssid == 'ff/an':
                # when do not connect to any access point / 未接続の時、[off/any]がff/anになる
                ssid = None
        except subprocess.CalledProcessError as e:
            print(e)

        return ssid

    def get_wifi_rssi(self):
        """
        get current connected access posint rssi of Wi-Fi module
        Wi-Fiモジュールが接続しているアクセスポイントの電波強度(rssi)を取得する
        """
        ps = subprocess.Popen(['iwconfig'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        rssi = None
        try:
            o = subprocess.check_output(('grep', 'Signal level'), stdin=ps.stdout)
            s0 = o.decode('utf-8')
            s1 = s0.split()
            s2 = [s for s in s1 if s.startswith('level')]
            rssi = s2[0].split('=')[1]
        except subprocess.CalledProcessError as e:
            print(e)

        return rssi

