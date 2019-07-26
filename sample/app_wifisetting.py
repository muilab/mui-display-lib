# -*- coding: utf-8 -*-

# mui wifi setting application class

from threading import Thread
from threading import Timer

import subprocess
import sys
import asyncio
import time
import logging

from mui_ui import Text, Image, Widget, AbsApp, Dialog, DialogListener
from mui_ui import TextAlignment, MotionEvent, OnTouchEventListener, AppEventListener, OnUpdateRequestListener  
from mui_ui import Keyboard, KeyboardListener
from mui_ui import MuiNetworkUtil

import os
dir = os.path.dirname(os.path.abspath(__file__))


class WiFiSetting(AbsApp, OnTouchEventListener, OnUpdateRequestListener, KeyboardListener, DialogListener):
    """
    Wi-Fi setting app

    this application is helper for wpa_supplicant.conf edit.
    user can input ssid and security key on mui.
    """

    def __init__(self, appEventListener: AppEventListener, lang='en-US'):
        super().__init__(appEventListener)

        self._lang = lang

        # create display current Wi-Fi setting panel
        def createCurrentSettingPanel():
            showCurrentSetting = Widget(200, 32)

            wifiCaption = Text('Wi-Fi')
            wifiCaption.setSize(0, 0, 30, 8)
            showCurrentSetting.addParts(wifiCaption)

            self._icon_wifi_enable = os.path.normpath(os.path.join(dir, './assets/icon_wifi_enable.png'))
            self._icon_wifi_disable = os.path.normpath(os.path.join(dir, './assets/icon_wifi_disable.png'))
            connectionStatus = Image(self._icon_wifi_disable)
            connectionStatus.setSize(36, 0, 11, 11)
            connectionStatus.offset_y = 2
            showCurrentSetting.addParts(connectionStatus)
            self.setView(connectionStatus, 'connectionStatus')

            currentIP = Text('')
            currentIP.setTextAlignment(TextAlignment.RIGHT)
            currentIP.setSize(65, 0, 168 - 65, 8)
            showCurrentSetting.addParts(currentIP)
            self.setView(currentIP, 'IPAddress')

            currentSSID = Text('')
            currentSSID.setSize(0, 24, 130, 8)
            showCurrentSetting.addParts(currentSSID)
            self.setView(currentSSID, 'SSID')

            btnNext = Text('>>')
            btnNext.setSize(158, 24, 10, 8)
            btnNext.addOnTouchViewListener(self)
            showCurrentSetting.addParts(btnNext)
            self.setView(btnNext, 'btnNext')

            self.addView(showCurrentSetting)
            self.setView(showCurrentSetting, 'panelShowWiFi')

        # create SSID input panel
        def createInputSSIDPanel():
            inputSSIDPanel = Widget(200, 32)
            inputSSIDPanel.visible = False

            inputSSIDCaption = Text('ssid: ')
            inputSSIDCaption.setSize(0, 0, 32, 8)
            inputSSIDPanel.addParts(inputSSIDCaption)

            inputSSIDArea = Text('')
            inputSSIDArea.setSize(36, 0, 168 - 36, 8)
            inputSSIDPanel.addParts(inputSSIDArea)
            self.setView(inputSSIDArea, 'inputSSIDArea')

            keyboardSSID = Keyboard(listener=self)
            keyboardSSID.setSize(0, 11, keyboardSSID.width, keyboardSSID.height)
            keyboardSSID.addOnUpdateViewListener(self)
            inputSSIDPanel.addParts(keyboardSSID)

            btnInputSSIDOk = Text('>>')
            btnInputSSIDOk.setSize(158, 24, 10, 8)
            btnInputSSIDOk.addOnTouchViewListener(self)
            inputSSIDPanel.addParts(btnInputSSIDOk)
            self.setView(btnInputSSIDOk, 'btnInputSSIDOk')

            btnInputSSIDBack = Text('<<')
            btnInputSSIDBack.setSize(140, 24, 10, 8)
            btnInputSSIDBack.addOnTouchViewListener(self)
            inputSSIDPanel.addParts(btnInputSSIDBack)
            self.setView(btnInputSSIDBack, 'btnInputSSIDBack')

            self.addView(inputSSIDPanel)
            self.setView(inputSSIDPanel, 'panelInputSSID')

        # create Security Type select panel
        def createSelectSecurityTypePanel():
            selectSecurityPanel = Widget(200, 32)
            selectSecurityPanel.visible = False

            securityCaption = Text('security type')
            securityCaption.setSize(0, 0, 120, 8)
            selectSecurityPanel.addParts(securityCaption)

            securityArea = Text('WPA-PSK')
            securityArea.setSize(20, 18, 140, 10)
            selectSecurityPanel.addParts(securityArea)
            self.setView(securityArea, 'securityArea')

            btnUpSec = Text('↑')
            btnUpSec.setSize(10, 12, 8, 8)
            btnUpSec.addOnTouchViewListener(self)
            btnUpSec.visible = False
            selectSecurityPanel.addParts(btnUpSec)
            self.setView(btnUpSec, 'btnUpSec')

            btnDownSec = Text('↓')
            btnDownSec.setSize(10, 23, 8, 8)
            btnDownSec.addOnTouchViewListener(self)
            selectSecurityPanel.addParts(btnDownSec)
            self.setView(btnDownSec, 'btnDownSec')

            btnSecurityOk = Text('>>')
            btnSecurityOk.setSize(158, 24, 10, 8)
            btnSecurityOk.addOnTouchViewListener(self)
            selectSecurityPanel.addParts(btnSecurityOk)
            self.setView(btnSecurityOk, 'btnSecurityOk')

            btnSecurityBack = Text('<<')
            btnSecurityBack.setSize(140, 24, 10, 8)
            btnSecurityBack.addOnTouchViewListener(self)
            selectSecurityPanel.addParts(btnSecurityBack)
            self.setView(btnSecurityBack, 'btnSecurityBack')

            self.addView(selectSecurityPanel)
            self.setView(selectSecurityPanel, 'panelSecurity')

        # create Security Key input panel
        def createSecurityKeyInputPanel():
            inputPassPanel = Widget(200, 32)
            inputPassPanel.visible = False

            inputPassCaption = Text('pw: ')
            inputPassCaption.setSize(0, 0, 18, 8)
            inputPassPanel.addParts(inputPassCaption)

            passArea = Text('')
            passArea.setSize(22, 0, 140, 8)
            inputPassPanel.addParts(passArea)
            self.setView(passArea, 'passArea')

            keyboardPass = Keyboard(listener=self)
            keyboardPass.setSize(0, 11, keyboardPass.width, keyboardPass.height)
            keyboardPass.addOnUpdateViewListener(self)
            inputPassPanel.addParts(keyboardPass)

            btnConnectWiFi = Text('>>')
            btnConnectWiFi.setSize(158, 24, 10, 8)
            btnConnectWiFi.addOnTouchViewListener(self)
            inputPassPanel.addParts(btnConnectWiFi)
            self.setView(btnConnectWiFi, 'btnConnectWiFi')

            btnConnectWiFiBack = Text('<<')
            btnConnectWiFiBack.setSize(140, 24, 10, 8)
            btnConnectWiFiBack.addOnTouchViewListener(self)
            inputPassPanel.addParts(btnConnectWiFiBack)
            self.setView(btnConnectWiFiBack, 'btnConnectWiFiBack')

            self.addView(inputPassPanel)
            self.setView(inputPassPanel, 'panelInputPass')

        # create confirm dialog
        def createConfirmDialog():
            panelConfirm = Dialog(
                listener = self, 
                pos_text = 'yes' if self._lang == 'en-US' else 'はい',
                nega_text = 'no' if self._lang == 'en-US' else 'いいえ'         
            )
            panelConfirm.visible = False
            self.addView(panelConfirm)
            self.setView(panelConfirm, 'panelConfirm')

        createCurrentSettingPanel()
        createInputSSIDPanel()
        createSelectSecurityTypePanel()
        createSecurityKeyInputPanel()
        createConfirmDialog()

        self._changeWiFiConfirm = False
        self._rebootConfirm = False
        self._inputSSID = False
        self._inputKey = False

        self._selectedSecIndex = 0
        self._selectedSSID = ''
        self._selectedSecType = ''
        self._selectedPass = ''

        self._network = MuiNetworkUtil()
        self._wifi_enable = False


    # ------------------------
    # override AbsApp methods

    def startTask(self):
        self.showCurrentWiFiConfig()

    def stopTask(self):
        pass

    def dispatchFlingEvent(self, e1, e2, x, y):
        panelShowWiFi = self.getView('panelShowWiFi')
        if panelShowWiFi.visible is True:
            self.close()

    def dispatchLongPressEvent(self, e):
        pass    

    def onTurnOffDisplay(self):
        # always do not allow turn off duaring this application
        return False

    # ------------------------
    # OnUpdateRequestListener implementation

    def onUpdateView(self, view):
        self.updateRequest(0)


    # ------------------------
    # KeyboardListener implementation

    def onInput(self, char):
        if self._inputSSID is True:
            self.getView('inputSSIDArea').addText(char)
        elif self._inputKey is True:
            self.getView('passArea').addText(char)

        self.updateRequest(0)

    def onDelete(self):
        if self._inputSSID is True:
            self.getView('inputSSIDArea').deleteLastChar()
        elif self._inputKey is True:
            self.getView('passArea').deleteLastChar()

        self.updateRequest(0)

    # ------------------------
    # OnTouchEventListener implementation

    def onTouch(self, view, e):
        btnNext = self.getView('btnNext')
        btnInputSSIDOk = self.getView('btnInputSSIDOk')
        btnInputSSIDBack = self.getView('btnInputSSIDBack')
        btnUpSec = self.getView('btnUpSec')
        btnDownSec = self.getView('btnDownSec')
        btnSecurityOk = self.getView('btnSecurityOk')
        btnSecurityBack = self.getView('btnSecurityBack')
        btnConnectWiFi = self.getView('btnConnectWiFi')
        btnConnectWiFiBack = self.getView('btnConnectWiFiBack')

        panelShowWiFi = self.getView('panelShowWiFi')
        panelInputSSID = self.getView('panelInputSSID')
        panelSecurity = self.getView('panelSecurity')
        panelInputPass = self.getView('panelInputPass')
        panelConfirm = self.getView('panelConfirm')

        if view == btnNext:
            panelShowWiFi.visible = False
            if self._wifi_enable is True:
                # when enable Wi-Fi connection 
                panelConfirm.visible = True
                panelConfirm.setMessage(
                    'Are you sure to change Wi-Fi access point?' if self._lang == 'en-US' else 'Wi-Fiアクセスポイントを変更しますか？'
                    )
                self._changeWiFiConfirm = True
            else:
                # when disable Wi-Fi connection
                panelInputSSID.visible = True
                self._inputSSID = True

            self.updateRequest(2)

        elif view == btnInputSSIDOk:
            self._inputSSID = False
            panelInputSSID.visible = False
            panelSecurity.visible = True
            self._selectedSSID = self.getView('inputSSIDArea')._text
            self.updateRequest(2)

        elif view == btnInputSSIDBack:
            panelInputSSID.visible = False
            panelShowWiFi.visible = True
            self._inputSSID = False
            self.updateRequest(2)        

        elif view == btnUpSec:
            self._selectedSecIndex -= 1
            if self._selectedSecIndex <= 0:
                self._selectedSecIndex = 0
                btnUpSec.visible = False
            btnDownSec.visible = True

            securityArea = self.getView('securityArea')
            if self._selectedSecIndex == 0:
                securityArea.setText('WPA-PSK')
            elif self._selectedSecIndex == 1:
                securityArea.setText('WEP')
            else:
                securityArea.setText('NONE')
            self.updateRequest(0)

        elif view == btnDownSec:
            self._selectedSecIndex += 1
            if self._selectedSecIndex >= 2:
                self._selectedSecIndex = 2
                btnDownSec.visible = False
            btnUpSec.visible = True

            securityArea = self.getView('securityArea')
            if self._selectedSecIndex == 0:
                securityArea.setText('WPA-PSK')
            elif self._selectedSecIndex == 1:
                securityArea.setText('WEP')
            else:
                securityArea.setText('NONE')
            self.updateRequest(0)

        elif view == btnSecurityOk:
            panelSecurity.visible = False
            panelInputPass.visible = True
            self._inputKey = True
            self._selectedSecType = self.getView('securityArea')._text
            self.updateRequest(2)

        elif view == btnSecurityBack:
            panelSecurity.visible = False
            panelInputSSID.visible = True
            self._inputSSID = True
            self.updateRequest(2)

        elif view == btnConnectWiFi:
            panelInputPass.visible = False
            panelConfirm.visible = True
            panelConfirm.setMessage(
                'Are you sure to try connect to access point? If you select [yes], mui reboot to connect.' if self._lang == 'en-US' else '指定したアクセスポイントに接続します。\n接続のために再起動します'
            )
            self._rebootConfirm = True
            self._selectedPass = self.getView('passArea')._text
            self.updateRequest(2)

        elif view == btnConnectWiFiBack:
            panelInputPass.visible = False
            panelSecurity.visible = True
            self._inputKey = False
            self.updateRequest(2)

    # ------------------------
    # DialogListener implementation

    def onPositive(self):
        panelConfirm =  self.getView('panelConfirm')

        if self._changeWiFiConfirm is True:
            self._changeWiFiConfirm = False
            self.getView('panelInputSSID').visible = True
            self._inputSSID = True
            panelConfirm.visible = False

        elif self._rebootConfirm is True:
            # rewrite wpa_supplicant.conf and reboot device.
            self._rebootConfirm = False
            self._updateWPASupplicant()

            panelConfirm.visible = False
            self.updateRequest(2)

            self._do_reboot()
            pass

        self.updateRequest(2)

    def onNegative(self):
        self.getView('panelConfirm').visible = False

        if self._changeWiFiConfirm is True:
            self._changeWiFiConfirm = False
            self.getView('panelShowWiFi').visible = True

        elif self._rebootConfirm is True:
            self._rebootConfirm = False
            self.getView('panelInputPass').visible = True

        self.updateRequest(2)
        
    # ------------------------

    def showCurrentWiFiConfig(self):
        ipAddress = self._get_ip_address()
        ssid = self._get_wifi_ssid()

        ipArea = self.getView('IPAddress')
        ipArea.setText(ipAddress)

        ssidArea = self.getView('SSID')
        if ssid is None:
            self._wifi_enable = False
            ssidArea.setText('offline')
        else:
            self._wifi_enable = True
            ssidArea.setText(ssid)

        connect_to_internet = self._network.check_internet_access()
        if connect_to_internet is True:
            self.getView('connectionStatus').setImage(self._icon_wifi_enable)
        else:
            self.getView('connectionStatus').setImage(self._icon_wifi_disable)

        # set current ssid to input ssid area
        if ssid is not None:
            self.getView('inputSSIDArea').setText(ssid)

        self.updateRequest(0)

    def _updateWPASupplicant(self):
        print('ssid : ', self._selectedSSID)
        print('sec type : ', self._selectedSecType)
        print('pass : ', self._selectedPass)

        self._set_new_wpa_config('ssid', '"' + self._selectedSSID + '"')
        self._set_new_wpa_config('key_mgmt', self._get_key_mgmt(self._selectedSecType))

        if self._selectedSecType == 'WPA-PSK':
            self._set_new_wpa_config('psk', '"' + self._selectedPass + '"')
            self._set_new_wpa_config('wep_key0', None) # clear
            self._set_new_wpa_config('wep_tx_keyidx', None) # clear
        
        elif self._selectedSecType == 'WEP':
            self._set_new_wpa_config('wep_key0', '"' + self._selectedPass + '"')
            self._set_new_wpa_config('wep_tx_keyidx', '0')
            self._set_new_wpa_config('psk', None)
            
        elif self._selectedSecType == 'NONE':
            self._set_new_wpa_config('wep_key0', None) # clear
            self._set_new_wpa_config('wep_tx_keyidx', None) # clear
            self._set_new_wpa_config('psk', None) # clear


    def _get_key_mgmt(self, secType):
        if self._selectedSecType == 'WPA-PSK':
            return 'WPA-PSK'

        elif self._selectedSecType == 'WEP':
            return 'NONE'

        elif self._selectedSecType == 'NONE':
            return 'NONE'

    def _set_new_wpa_config(self, key: str, value: str):
        file_path = '/etc/wpa_supplicant/wpa_supplicant.conf'
        self._network.set_new_wpa_config(key, value, file_path)

    def _get_ip_address(self):
        return self._network.get_ip_address()

    def _get_wifi_ssid(self):
        return self._network.get_wifi_ssid()

    def _do_reboot(self):
        sb = subprocess.Popen(['reboot'], stdout=subprocess.PIPE)
        
