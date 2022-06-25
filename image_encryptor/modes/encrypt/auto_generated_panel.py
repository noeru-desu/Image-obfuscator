# -*- coding: utf-8 -*-

###########################################################################
# Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
# http://www.wxformbuilder.org/
##
# PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
# Class ProcSettingsPanel
###########################################################################


class ProcSettingsPanel (wx.Panel):
    __slots__ = (
        'XORA', 'XORB', 'XOREncryption', 'XORG', 'XORR', 'cuttingCol', 'cuttingRow', 'flipChunks', 'm_staticText1',
        'm_staticText11', 'm_staticText6', 'mappingA', 'mappingB', 'mappingG', 'mappingR', 'noiseFactor', 'noiseFactorNum',
        'noiseXor', 'shuffleChunks', 'xorPanel'
    )

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(-1, -1), style=wx.TAB_TRAVERSAL, name=wx.EmptyString):
        wx.Panel.__init__(self, parent, id=id, pos=pos, size=size, style=style, name=name)

        bSizer1 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        bSizer3 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, u"切割行数", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)

        bSizer3.Add(self.m_staticText1, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.cuttingRow = wx.SpinCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(60, -1), wx.ALIGN_CENTER_HORIZONTAL | wx.SP_ARROW_KEYS | wx.TE_PROCESS_ENTER, 1, 100000000, 25)
        bSizer3.Add(self.cuttingRow, 0, wx.ALL, 3)

        bSizer2.Add(bSizer3, 1, wx.EXPAND, 5)

        bSizer4 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText11 = wx.StaticText(self, wx.ID_ANY, u"切割列数", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText11.Wrap(-1)

        bSizer4.Add(self.m_staticText11, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.cuttingCol = wx.SpinCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(60, -1), wx.ALIGN_CENTER_HORIZONTAL | wx.SP_ARROW_KEYS | wx.TE_PROCESS_ENTER, 1, 100000000, 25)
        bSizer4.Add(self.cuttingCol, 0, wx.ALL, 3)

        bSizer2.Add(bSizer4, 1, wx.EXPAND, 5)

        self.shuffleChunks = wx.CheckBox(self, wx.ID_ANY, u"随机打乱分块", wx.DefaultPosition, wx.DefaultSize, 0)
        self.shuffleChunks.SetValue(True)
        bSizer2.Add(self.shuffleChunks, 0, wx.ALL, 5)

        self.flipChunks = wx.CheckBox(self, wx.ID_ANY, u"随机翻转分块", wx.DefaultPosition, wx.DefaultSize, 0)
        self.flipChunks.SetValue(True)
        bSizer2.Add(self.flipChunks, 0, wx.ALL, 5)

        mappingSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"色彩通道映射"), wx.HORIZONTAL)

        self.mappingR = wx.CheckBox(mappingSizer.GetStaticBox(), wx.ID_ANY, u"R", wx.DefaultPosition, wx.DefaultSize, 0)
        mappingSizer.Add(self.mappingR, 0, 0, 0)

        self.mappingG = wx.CheckBox(mappingSizer.GetStaticBox(), wx.ID_ANY, u"G", wx.DefaultPosition, wx.DefaultSize, 0)
        mappingSizer.Add(self.mappingG, 0, 0, 0)

        self.mappingB = wx.CheckBox(mappingSizer.GetStaticBox(), wx.ID_ANY, u"B", wx.DefaultPosition, wx.DefaultSize, 0)
        mappingSizer.Add(self.mappingB, 0, 0, 0)

        self.mappingA = wx.CheckBox(mappingSizer.GetStaticBox(), wx.ID_ANY, u"A", wx.DefaultPosition, wx.DefaultSize, 0)
        mappingSizer.Add(self.mappingA, 0, 0, 0)

        bSizer2.Add(mappingSizer, 0, wx.ALL, 3)

        self.XOREncryption = wx.CheckBox(self, wx.ID_ANY, u"使用异或加密", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.XOREncryption, 0, wx.ALL, 5)

        bSizer1.Add(bSizer2, 0, wx.EXPAND, 5)

        sbSizer1 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"异或加密"), wx.HORIZONTAL)

        self.xorPanel = wx.Panel(sbSizer1.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer9 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer10 = wx.BoxSizer(wx.VERTICAL)

        self.XORR = wx.CheckBox(self.xorPanel, wx.ID_ANY, u"R", wx.DefaultPosition, wx.DefaultSize, 0)
        self.XORR.SetValue(True)
        bSizer10.Add(self.XORR, 0, 0, 0)

        self.XORG = wx.CheckBox(self.xorPanel, wx.ID_ANY, u"G", wx.DefaultPosition, wx.DefaultSize, 0)
        self.XORG.SetValue(True)
        bSizer10.Add(self.XORG, 0, 0, 5)

        self.XORB = wx.CheckBox(self.xorPanel, wx.ID_ANY, u"B", wx.DefaultPosition, wx.DefaultSize, 0)
        self.XORB.SetValue(True)
        bSizer10.Add(self.XORB, 0, 0, 5)

        self.XORA = wx.CheckBox(self.xorPanel, wx.ID_ANY, u"A", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer10.Add(self.XORA, 0, 0, 5)

        bSizer9.Add(bSizer10, 0, 0, 0)

        bSizer11 = wx.BoxSizer(wx.VERTICAL)

        self.noiseXor = wx.CheckBox(self.xorPanel, wx.ID_ANY, u"噪音", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT)
        bSizer11.Add(self.noiseXor, 0, wx.ALIGN_RIGHT, 0)

        bSizer12 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText6 = wx.StaticText(self.xorPanel, wx.ID_ANY, u"系数:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText6.Wrap(-1)

        bSizer12.Add(self.m_staticText6, 0, wx.ALIGN_CENTER, 0)

        self.noiseFactorNum = wx.StaticText(self.xorPanel, wx.ID_ANY, u"128", wx.DefaultPosition, wx.DefaultSize, 0)
        self.noiseFactorNum.Wrap(-1)

        bSizer12.Add(self.noiseFactorNum, 0, wx.ALIGN_CENTER, 0)

        bSizer11.Add(bSizer12, 0, wx.EXPAND, 0)

        self.noiseFactor = wx.Slider(self.xorPanel, wx.ID_ANY, 128, 1, 255, wx.DefaultPosition, wx.DefaultSize, wx.SL_BOTH | wx.SL_INVERSE | wx.SL_VERTICAL)
        self.noiseFactor.Enable(False)

        bSizer11.Add(self.noiseFactor, 1, wx.ALIGN_CENTER, 0)

        bSizer9.Add(bSizer11, 1, wx.EXPAND, 0)

        self.xorPanel.SetSizer(bSizer9)
        self.xorPanel.Layout()
        bSizer9.Fit(self.xorPanel)
        sbSizer1.Add(self.xorPanel, 1, wx.EXPAND, 0)

        bSizer1.Add(sbSizer1, 0, wx.ALL | wx.EXPAND, 3)

        self.SetSizer(bSizer1)
        self.Layout()
        bSizer1.Fit(self)

        # Connect Events
        self.cuttingRow.Bind(wx.EVT_SPINCTRL, self.settings_changed)
        self.cuttingRow.Bind(wx.EVT_TEXT_ENTER, self.settings_changed)
        self.cuttingCol.Bind(wx.EVT_SPINCTRL, self.settings_changed)
        self.cuttingCol.Bind(wx.EVT_TEXT_ENTER, self.settings_changed)
        self.shuffleChunks.Bind(wx.EVT_CHECKBOX, self.settings_changed)
        self.flipChunks.Bind(wx.EVT_CHECKBOX, self.settings_changed)
        self.mappingR.Bind(wx.EVT_CHECKBOX, self.settings_changed)
        self.mappingG.Bind(wx.EVT_CHECKBOX, self.settings_changed)
        self.mappingB.Bind(wx.EVT_CHECKBOX, self.settings_changed)
        self.mappingA.Bind(wx.EVT_CHECKBOX, self.settings_changed)
        self.XOREncryption.Bind(wx.EVT_CHECKBOX, self.toggle_xor_panel_switch)
        self.XORR.Bind(wx.EVT_CHECKBOX, self.settings_changed)
        self.XORG.Bind(wx.EVT_CHECKBOX, self.settings_changed)
        self.XORB.Bind(wx.EVT_CHECKBOX, self.settings_changed)
        self.XORA.Bind(wx.EVT_CHECKBOX, self.settings_changed)
        self.noiseXor.Bind(wx.EVT_CHECKBOX, self.toggle_factor_slider_switch)
        self.noiseFactor.Bind(wx.EVT_SCROLL, self.update_noise_factor_num)
        self.noiseFactor.Bind(wx.EVT_SCROLL_CHANGED, self.settings_changed)

    def __del__(self):
        pass

    # Virtual event handlers, override them in your derived class
    def settings_changed(self, event):
        event.Skip()

    def toggle_xor_panel_switch(self, event):
        event.Skip()

    def toggle_factor_slider_switch(self, event):
        event.Skip()

    def update_noise_factor_num(self, event):
        event.Skip()
