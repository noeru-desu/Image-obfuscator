# -*- coding: utf-8 -*-

###########################################################################
# Python code generated with wxFormBuilder (version 3.10.1-df7791b)
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
        'autoZoomIn', 'autoZoomOut', 'directExtraction', 'insideFile', 'lsbMode', 'lsbNum', 'lsbRatio', 'm_button1',
        'm_staticText10', 'm_staticText7', 'm_staticText8', 'useAlpha'
    )

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(-1, -1), style=wx.TAB_TRAVERSAL, name=wx.EmptyString):
        wx.Panel.__init__(self, parent, id=id, pos=pos, size=size, style=style, name=name)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        bSizer5 = wx.BoxSizer(wx.HORIZONTAL)

        self.insideFile = wx.FilePickerCtrl(self, wx.ID_ANY, wx.EmptyString, u"选择需隐写文件", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE | wx.FLP_FILE_MUST_EXIST)
        self.insideFile.SetToolTip(u"需要隐写到当前图像内的文件, 可以是任何文件")

        bSizer5.Add(self.insideFile, 1, wx.EXPAND, 0)

        bSizer1.Add(bSizer5, 0, wx.EXPAND, 5)

        bSizer6 = wx.BoxSizer(wx.VERTICAL)

        bSizer12 = wx.BoxSizer(wx.HORIZONTAL)

        lsbModeChoices = [u"写入", u"提取"]
        self.lsbMode = wx.RadioBox(self, wx.ID_ANY, u"处理方式", wx.DefaultPosition, wx.DefaultSize, lsbModeChoices, 1, wx.RA_SPECIFY_ROWS)
        self.lsbMode.SetSelection(0)
        self.lsbMode.SetToolTip(u"图像处理方式")

        bSizer12.Add(self.lsbMode, 0, wx.ALL | wx.EXPAND, 2)

        bSizer16 = wx.BoxSizer(wx.VERTICAL)

        self.m_button1 = wx.Button(self, wx.ID_ANY, u"尝试自动检测\n提取设置", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_button1.SetToolTip(u"自动根据一些可用信息推测提取设置。当前不支持提取不由本程序写入的LSB信息")

        bSizer16.Add(self.m_button1, 1, wx.ALL | wx.EXPAND, 2)

        self.directExtraction = wx.CheckBox(self, wx.ID_ANY, u"直接提取", wx.DefaultPosition, wx.DefaultSize, 0)
        self.directExtraction.Hide()

        bSizer16.Add(self.directExtraction, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

        bSizer12.Add(bSizer16, 1, wx.EXPAND, 5)

        bSizer6.Add(bSizer12, 0, wx.EXPAND, 0)

        bSizer7 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText7 = wx.StaticText(self, wx.ID_ANY, u"使用的LSB位数(1-8)", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText7.Wrap(-1)

        self.m_staticText7.SetToolTip(u"可占用的每个像素最低有效位位数。越低越不明显, 但等量数据需占用的像素越多。不建议设置到4及以上")

        bSizer7.Add(self.m_staticText7, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)

        self.lsbNum = wx.SpinCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL | wx.SP_ARROW_KEYS | wx.TE_PROCESS_ENTER, 1, 8, 1)
        self.lsbNum.SetToolTip(u"可占用的每个像素最低有效位位数。越低越不明显, 但等量数据需占用的像素越多。不建议设置到4及以上")

        bSizer7.Add(self.lsbNum, 1, 0, 0)

        bSizer6.Add(bSizer7, 0, wx.EXPAND, 5)

        bSizer8 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer10 = wx.BoxSizer(wx.VERTICAL)

        self.useAlpha = wx.CheckBox(self, wx.ID_ANY, u"使用透明通道", wx.DefaultPosition, wx.DefaultSize, 0)
        self.useAlpha.SetToolTip(u"是否在透明通道的LSB上也存储信息。启用后等像素量可存储1.33倍的数据, 但会导致每个像素点的透明度出现变化。 具体请根据最终图像效果自行斟酌")

        bSizer10.Add(self.useAlpha, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)

        self.autoZoomIn = wx.CheckBox(self, wx.ID_ANY, u"自动放大", wx.DefaultPosition, wx.DefaultSize, 0)
        self.autoZoomIn.SetValue(True)
        self.autoZoomIn.SetToolTip(u"是否在像素量不足时自动等比放大图像。关闭后，若右侧宽高缩放比超过100%, 将无法生成图像")

        bSizer10.Add(self.autoZoomIn, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)

        self.autoZoomOut = wx.CheckBox(self, wx.ID_ANY, u"自动缩小", wx.DefaultPosition, wx.DefaultSize, 0)
        self.autoZoomOut.SetToolTip(u"是否在像素量超过所需像素量时自动等比缩小图像。自行选择开启或关闭, 启用后将减少无隐写数据的像素量")

        bSizer10.Add(self.autoZoomOut, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)

        bSizer8.Add(bSizer10, 1, wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer9 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText8 = wx.StaticText(self, wx.ID_ANY, u"宽高缩放比:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText8.Wrap(-1)

        self.m_staticText8.SetToolTip(u"写入当前需隐写文件所需的像素量占比，其数值除精度外与宽高自动缩放率相同。可用LSB位数、是否使用透明通道都将影响该值，当该值大于100%时必须启用\"自动放大\", 否则无法生成图像。")

        bSizer9.Add(self.m_staticText8, 0, wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_staticText10 = wx.StaticText(self, wx.ID_ANY, u"(自动缩放比例)", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText10.Wrap(-1)

        self.m_staticText10.SetToolTip(u"写入当前需隐写文件所需的像素量占比，其数值除精度外与宽高自动缩放率相同。可用LSB位数、是否使用透明通道都将影响该值，当该值大于100%时必须启用\"自动放大\", 否则无法生成图像。")

        bSizer9.Add(self.m_staticText10, 0, wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.lsbRatio = wx.StaticText(self, wx.ID_ANY, u"待计算", wx.DefaultPosition, wx.DefaultSize, 0)
        self.lsbRatio.Wrap(-1)

        self.lsbRatio.SetToolTip(u"写入当前需隐写文件所需的像素量占比，其数值除精度外与宽高自动缩放率相同。可用LSB位数、是否使用透明通道都将影响该值，当该值大于100%时必须启用\"自动放大\", 否则无法生成图像。")

        bSizer9.Add(self.lsbRatio, 0, wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer8.Add(bSizer9, 1, wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer6.Add(bSizer8, 0, wx.EXPAND, 5)

        bSizer1.Add(bSizer6, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()
        bSizer1.Fit(self)

        # Connect Events
        self.insideFile.Bind(wx.EVT_FILEPICKER_CHANGED, self.recal_lsb_ratio)
        self.lsbMode.Bind(wx.EVT_RADIOBOX, self.settings_changed)
        self.m_button1.Bind(wx.EVT_BUTTON, self.detect_lsb)
        self.directExtraction.Bind(wx.EVT_CHECKBOX, self.settings_changed)
        self.lsbNum.Bind(wx.EVT_SPINCTRL, self.recal_lsb_ratio)
        self.lsbNum.Bind(wx.EVT_TEXT_ENTER, self.recal_lsb_ratio)
        self.useAlpha.Bind(wx.EVT_CHECKBOX, self.recal_lsb_ratio)
        self.autoZoomIn.Bind(wx.EVT_CHECKBOX, self.auto_zoom_in_changed)
        self.autoZoomOut.Bind(wx.EVT_CHECKBOX, self.settings_changed)

    def __del__(self):
        pass

    # Virtual event handlers, override them in your derived class
    def recal_lsb_ratio(self, event):
        event.Skip()

    def settings_changed(self, event):
        event.Skip()

    def detect_lsb(self, event):
        event.Skip()

    def auto_zoom_in_changed(self, event):
        event.Skip()


###########################################################################
# Class DetectLsbDialog
###########################################################################

class DetectLsbDialog (wx.Dialog):
    __slots__ = (
        'applyBtn', 'gauge', 'info', 'm_button3', 'm_panel2', 'startDetectBtn'
    )

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"LSB探测", pos=wx.DefaultPosition, size=wx.Size(-1, -1), style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.Size(350, -1), wx.DefaultSize)

        bSizer17 = wx.BoxSizer(wx.VERTICAL)

        self.gauge = wx.Gauge(self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL)
        self.gauge.SetValue(0)
        bSizer17.Add(self.gauge, 0, wx.ALL | wx.EXPAND, 2)

        bSizer18 = wx.BoxSizer(wx.HORIZONTAL)

        self.startDetectBtn = wx.Button(self, wx.ID_ANY, u"开始探测", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer18.Add(self.startDetectBtn, 0, wx.ALL, 5)

        self.info = wx.StaticText(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.info.Wrap(-1)

        bSizer18.Add(self.info, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 0)

        bSizer17.Add(bSizer18, 0, wx.EXPAND, 5)

        self.m_panel2 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, -1), wx.TAB_TRAVERSAL)
        self.m_panel2.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DLIGHT))

        bSizer19 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer19.Add((0, 0), 1, 0, 0)

        self.applyBtn = wx.Button(self.m_panel2, wx.ID_ANY, u"应用", wx.DefaultPosition, wx.DefaultSize, 0)
        self.applyBtn.Enable(False)

        bSizer19.Add(self.applyBtn, 0, wx.ALL, 5)

        self.m_button3 = wx.Button(self.m_panel2, wx.ID_ANY, u"取消", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer19.Add(self.m_button3, 0, wx.ALL, 5)

        self.m_panel2.SetSizer(bSizer19)
        self.m_panel2.Layout()
        bSizer19.Fit(self.m_panel2)
        bSizer17.Add(self.m_panel2, 0, wx.EXPAND, 0)

        self.SetSizer(bSizer17)
        self.Layout()
        bSizer17.Fit(self)

        self.Centre(wx.BOTH)

        # Connect Events
        self.Bind(wx.EVT_CLOSE, self.cancel)
        self.startDetectBtn.Bind(wx.EVT_BUTTON, self.start_detect)
        self.applyBtn.Bind(wx.EVT_BUTTON, self.apply)
        self.m_button3.Bind(wx.EVT_BUTTON, self.cancel)

    def __del__(self):
        pass

    # Virtual event handlers, override them in your derived class
    def cancel(self, event):
        event.Skip()

    def start_detect(self, event):
        event.Skip()

    def apply(self, event):
        event.Skip()
