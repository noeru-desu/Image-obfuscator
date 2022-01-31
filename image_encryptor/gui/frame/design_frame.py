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
# Class MainFrame
###########################################################################


class MainFrame (wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Image Encryptor", pos=wx.DefaultPosition, size=wx.Size(770, 900), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL, name=u"Image Encryptor")

        self.SetSizeHints(wx.Size(770, 640), wx.DefaultSize)
        self.SetFont(wx.Font(9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Segoe UI"))
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        bSizer26 = wx.BoxSizer(wx.VERTICAL)

        self.loadingPrograssPanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.loadingPrograssPanel.Hide()

        bSizer263 = wx.BoxSizer(wx.HORIZONTAL)

        self.stopLoadingBtn = wx.Button(self.loadingPrograssPanel, wx.ID_ANY, u"停止载入", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer263.Add(self.stopLoadingBtn, 0, wx.ALL, 5)

        self.loadingPrograss = wx.Gauge(self.loadingPrograssPanel, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL)
        self.loadingPrograss.SetValue(0)
        bSizer263.Add(self.loadingPrograss, 1, wx.ALIGN_CENTER | wx.ALL, 5)

        self.loadingPrograssInfo = wx.StaticText(self.loadingPrograssPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.loadingPrograssInfo.Wrap(-1)

        bSizer263.Add(self.loadingPrograssInfo, 1, wx.ALIGN_CENTER | wx.ALIGN_LEFT | wx.ALL, 5)

        self.loadingPrograssPanel.SetSizer(bSizer263)
        self.loadingPrograssPanel.Layout()
        bSizer263.Fit(self.loadingPrograssPanel)
        bSizer26.Add(self.loadingPrograssPanel, 0, wx.ALL | wx.EXPAND, 5)

        self.loadingPanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, -1), wx.TAB_TRAVERSAL)
        bSizer91 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_button5 = wx.Button(self.loadingPanel, wx.ID_ANY, u"载入文件", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer91.Add(self.m_button5, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.m_button6 = wx.Button(self.loadingPanel, wx.ID_ANY, u"载入文件夹", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer91.Add(self.m_button6, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.imageInfo = wx.StaticText(self.loadingPanel, wx.ID_ANY, u"图像信息：未选择图片", wx.DefaultPosition, wx.DefaultSize, 0)
        self.imageInfo.Wrap(-1)

        bSizer91.Add(self.imageInfo, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.loadingPanel.SetSizer(bSizer91)
        self.loadingPanel.Layout()
        bSizer91.Fit(self.loadingPanel)
        bSizer26.Add(self.loadingPanel, 0, wx.ALL | wx.EXPAND, 5)

        bSizer281 = wx.BoxSizer(wx.HORIZONTAL)

        self.imageTreePanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer262 = wx.BoxSizer(wx.VERTICAL)

        self.imageTreeSearchCtrl = wx.SearchCtrl(self.imageTreePanel, wx.ID_ANY, u"文件树搜索功能尚不可用", wx.DefaultPosition, wx.DefaultSize, wx.TE_CENTER)
        self.imageTreeSearchCtrl.ShowSearchButton(True)
        self.imageTreeSearchCtrl.ShowCancelButton(True)
        self.imageTreeSearchCtrl.Enable(False)

        bSizer262.Add(self.imageTreeSearchCtrl, 0, wx.ALL | wx.EXPAND, 5)

        bSizer40 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_button10 = wx.Button(self.imageTreePanel, wx.ID_ANY, u"删除此项", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer40.Add(self.m_button10, 1, 0, 5)

        self.m_button11 = wx.Button(self.imageTreePanel, wx.ID_ANY, u"重载此项", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer40.Add(self.m_button11, 1, 0, 5)

        bSizer262.Add(bSizer40, 0, wx.EXPAND, 5)

        self.imageTreeCtrl = wx.TreeCtrl(self.imageTreePanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE | wx.TR_FULL_ROW_HIGHLIGHT |
                                         wx.TR_HAS_BUTTONS | wx.TR_HAS_VARIABLE_ROW_HEIGHT | wx.TR_HIDE_ROOT | wx.TR_ROW_LINES | wx.TR_SINGLE | wx.TR_TWIST_BUTTONS)
        bSizer262.Add(self.imageTreeCtrl, 1, wx.EXPAND, 5)

        self.imageTreePanel.SetSizer(bSizer262)
        self.imageTreePanel.Layout()
        bSizer262.Fit(self.imageTreePanel)
        bSizer281.Add(self.imageTreePanel, 2, wx.EXPAND | wx.ALL, 5)

        self.imagePanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        gSizer1 = wx.GridSizer(0, 1, 0, 0)

        sbSizer2 = wx.StaticBoxSizer(wx.StaticBox(self.imagePanel, wx.ID_ANY, u"导入图片-预览图"), wx.VERTICAL)

        self.importedBitmapPlanel = wx.Panel(sbSizer2.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer261 = wx.BoxSizer(wx.VERTICAL)

        self.importedBitmap = wx.StaticBitmap(self.importedBitmapPlanel, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer261.Add(self.importedBitmap, 1, wx.ALL | wx.EXPAND, 0)

        self.importedBitmapPlanel.SetSizer(bSizer261)
        self.importedBitmapPlanel.Layout()
        bSizer261.Fit(self.importedBitmapPlanel)
        sbSizer2.Add(self.importedBitmapPlanel, 1, wx.EXPAND | wx.ALL, 5)

        gSizer1.Add(sbSizer2, 1, wx.EXPAND, 5)

        sbSizer3 = wx.StaticBoxSizer(wx.StaticBox(self.imagePanel, wx.ID_ANY, u"处理结果-预览图"), wx.VERTICAL)

        self.previewedBitmapPlanel = wx.Panel(sbSizer3.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer27 = wx.BoxSizer(wx.VERTICAL)

        self.previewedBitmap = wx.StaticBitmap(self.previewedBitmapPlanel, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer27.Add(self.previewedBitmap, 1, wx.ALL | wx.EXPAND, 0)

        self.previewedBitmapPlanel.SetSizer(bSizer27)
        self.previewedBitmapPlanel.Layout()
        bSizer27.Fit(self.previewedBitmapPlanel)
        sbSizer3.Add(self.previewedBitmapPlanel, 1, wx.EXPAND | wx.ALL, 5)

        gSizer1.Add(sbSizer3, 1, wx.EXPAND, 5)

        self.imagePanel.SetSizer(gSizer1)
        self.imagePanel.Layout()
        gSizer1.Fit(self.imagePanel)
        bSizer281.Add(self.imagePanel, 5, wx.ALL | wx.EXPAND, 2)

        bSizer26.Add(bSizer281, 1, wx.EXPAND, 5)

        bSizer43 = wx.BoxSizer(wx.HORIZONTAL)

        self.settingsPanel = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.NB_FIXEDWIDTH)
        self.processingOptions = wx.Panel(self.settingsPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer12 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer282 = wx.BoxSizer(wx.VERTICAL)

        procModeChoices = [u"加密模式", u"解密模式", u"QQ反屏蔽"]
        self.procMode = wx.RadioBox(self.processingOptions, wx.ID_ANY, u"处理模式", wx.DefaultPosition, wx.DefaultSize, procModeChoices, 1, wx.RA_SPECIFY_COLS)
        self.procMode.SetSelection(0)
        bSizer282.Add(self.procMode, 0, wx.ALIGN_CENTER | wx.ALL, 3)

        self.m_staticText12 = wx.StaticText(self.processingOptions, wx.ID_ANY, u"添加密码到密码字典", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText12.Wrap(-1)

        bSizer282.Add(self.m_staticText12, 0, wx.ALL, 2)

        self.passwordCtrl = wx.TextCtrl(self.processingOptions, wx.ID_ANY, u"none", wx.DefaultPosition, wx.DefaultSize, wx.TE_CENTER | wx.TE_PROCESS_ENTER)
        self.passwordCtrl.SetMaxLength(32)
        bSizer282.Add(self.passwordCtrl, 0, wx.ALL, 0)

        bSizer12.Add(bSizer282, 0, wx.EXPAND, 5)

        bSizer12.Add((0, 0), 1, wx.EXPAND, 5)

        self.processingSettingsPanel1 = wx.Panel(self.processingOptions, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer33 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer13 = wx.BoxSizer(wx.VERTICAL)

        bSizer131 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText8 = wx.StaticText(self.processingSettingsPanel1, wx.ID_ANY, u"切割行数", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText8.Wrap(-1)

        bSizer131.Add(self.m_staticText8, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.cuttingRow = wx.SpinCtrl(self.processingSettingsPanel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(60, -1), wx.ALIGN_CENTER_HORIZONTAL | wx.SP_ARROW_KEYS | wx.TE_PROCESS_ENTER, 1, 100000000, 25)
        bSizer131.Add(self.cuttingRow, 0, wx.ALL, 3)

        bSizer13.Add(bSizer131, 0, wx.EXPAND, 5)

        bSizer15 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText9 = wx.StaticText(self.processingSettingsPanel1, wx.ID_ANY, u"切割列数", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText9.Wrap(-1)

        bSizer15.Add(self.m_staticText9, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.cuttingCol = wx.SpinCtrl(self.processingSettingsPanel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(60, -1), wx.ALIGN_CENTER_HORIZONTAL | wx.SP_ARROW_KEYS | wx.TE_PROCESS_ENTER, 1, 100000000, 25)
        bSizer15.Add(self.cuttingCol, 0, wx.ALL | wx.EXPAND, 3)

        bSizer13.Add(bSizer15, 0, wx.EXPAND, 5)

        self.shuffleChunks = wx.CheckBox(self.processingSettingsPanel1, wx.ID_ANY, u"随机打乱分块", wx.DefaultPosition, wx.DefaultSize, 0)
        self.shuffleChunks.SetValue(True)
        bSizer13.Add(self.shuffleChunks, 0, wx.ALL, 3)

        self.flipChunks = wx.CheckBox(self.processingSettingsPanel1, wx.ID_ANY, u"随机翻转分块", wx.DefaultPosition, wx.DefaultSize, 0)
        self.flipChunks.SetValue(True)
        bSizer13.Add(self.flipChunks, 0, wx.ALL, 3)

        self.rgbMapping = wx.CheckBox(self.processingSettingsPanel1, wx.ID_ANY, u"分块随机RGB映射", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer13.Add(self.rgbMapping, 0, wx.ALL, 3)

        self.XOREncryption = wx.CheckBox(self.processingSettingsPanel1, wx.ID_ANY, u"使用异或加密", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer13.Add(self.XOREncryption, 0, wx.ALL, 3)

        bSizer33.Add(bSizer13, 0, wx.EXPAND, 5)

        xorSizer = wx.StaticBoxSizer(wx.StaticBox(self.processingSettingsPanel1, wx.ID_ANY, u"异或加密"), wx.HORIZONTAL)

        self.xorPanel = wx.Panel(xorSizer.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer47 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer42 = wx.BoxSizer(wx.VERTICAL)

        self.XORR = wx.CheckBox(self.xorPanel, wx.ID_ANY, u"R", wx.DefaultPosition, wx.Size(-1, -1), 0)
        self.XORR.SetValue(True)
        bSizer42.Add(self.XORR, 0, wx.ALL, 0)

        self.XORG = wx.CheckBox(self.xorPanel, wx.ID_ANY, u"G", wx.DefaultPosition, wx.Size(-1, -1), 0)
        self.XORG.SetValue(True)
        bSizer42.Add(self.XORG, 0, wx.ALL, 0)

        self.XORB = wx.CheckBox(self.xorPanel, wx.ID_ANY, u"B", wx.DefaultPosition, wx.Size(-1, -1), 0)
        self.XORB.SetValue(True)
        bSizer42.Add(self.XORB, 0, wx.ALL, 0)

        self.XORA = wx.CheckBox(self.xorPanel, wx.ID_ANY, u"A", wx.DefaultPosition, wx.Size(-1, -1), 0)
        bSizer42.Add(self.XORA, 0, wx.ALL, 0)

        bSizer47.Add(bSizer42, 0, 0, 0)

        bSizer44 = wx.BoxSizer(wx.VERTICAL)

        self.noiseXor = wx.CheckBox(self.xorPanel, wx.ID_ANY, u"噪音", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT)
        bSizer44.Add(self.noiseXor, 0, wx.ALIGN_RIGHT | wx.ALL, 0)

        bSizer331 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText141 = wx.StaticText(self.xorPanel, wx.ID_ANY, u"系数:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText141.Wrap(-1)

        bSizer331.Add(self.m_staticText141, 0, wx.ALIGN_CENTER | wx.ALL, 0)

        self.noiseFactorNum = wx.StaticText(self.xorPanel, wx.ID_ANY, u"128", wx.DefaultPosition, wx.DefaultSize, 0)
        self.noiseFactorNum.Wrap(-1)

        bSizer331.Add(self.noiseFactorNum, 0, wx.ALIGN_CENTER | wx.ALL, 0)

        bSizer44.Add(bSizer331, 0, wx.EXPAND, 0)

        self.noiseFactor = wx.Slider(self.xorPanel, wx.ID_ANY, 128, 1, 255, wx.DefaultPosition, wx.Size(-1, 90), wx.SL_BOTH | wx.SL_INVERSE | wx.SL_VERTICAL)
        self.noiseFactor.Enable(False)

        bSizer44.Add(self.noiseFactor, 1, wx.ALIGN_CENTER | wx.ALL, 0)

        bSizer47.Add(bSizer44, 0, wx.EXPAND, 0)

        self.xorPanel.SetSizer(bSizer47)
        self.xorPanel.Layout()
        bSizer47.Fit(self.xorPanel)
        xorSizer.Add(self.xorPanel, 0, wx.ALL | wx.EXPAND, 0)

        bSizer33.Add(xorSizer, 0, wx.ALL | wx.EXPAND, 3)

        self.processingSettingsPanel1.SetSizer(bSizer33)
        self.processingSettingsPanel1.Layout()
        bSizer33.Fit(self.processingSettingsPanel1)
        bSizer12.Add(self.processingSettingsPanel1, 0, wx.ALL, 5)

        bSizer12.Add((0, 0), 1, 0, 5)

        self.previewOptions = wx.Panel(self.processingOptions, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer19 = wx.BoxSizer(wx.VERTICAL)

        bSizer28 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer32 = wx.BoxSizer(wx.VERTICAL)

        bSizer31 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticline31 = wx.StaticLine(self.previewOptions, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL)
        bSizer31.Add(self.m_staticline31, 0, wx.EXPAND | wx.ALL, 2)

        bSizer29 = wx.BoxSizer(wx.VERTICAL)

        bSizer29.Add((0, 0), 1, wx.EXPAND, 5)

        self.m_staticText14 = wx.StaticText(self.previewOptions, wx.ID_ANY, u"同步加密设置", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText14.Wrap(-1)

        bSizer29.Add(self.m_staticText14, 0, wx.ALIGN_CENTER | wx.ALL, 2)

        self.m_button31 = wx.Button(self.previewOptions, wx.ID_ANY, u"应用到全部", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer29.Add(self.m_button31, 0, wx.ALIGN_CENTER | wx.ALL, 2)

        self.m_button311 = wx.Button(self.previewOptions, wx.ID_ANY, u"设置为默认", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer29.Add(self.m_button311, 0, wx.ALIGN_CENTER | wx.ALL, 2)

        bSizer29.Add((0, 0), 1, wx.EXPAND, 5)

        bSizer31.Add(bSizer29, 0, wx.ALL | wx.EXPAND, 2)

        self.m_staticline4 = wx.StaticLine(self.previewOptions, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL)
        bSizer31.Add(self.m_staticline4, 0, wx.EXPAND | wx.ALL, 2)

        bSizer32.Add(bSizer31, 1, wx.EXPAND, 5)

        self.previewProgressInfo = wx.StaticText(self.previewOptions, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.previewProgressInfo.Wrap(-1)

        bSizer32.Add(self.previewProgressInfo, 0, wx.ALL | wx.EXPAND, 5)

        bSizer28.Add(bSizer32, 0, wx.EXPAND, 5)

        bSizer30 = wx.BoxSizer(wx.VERTICAL)

        previewModeChoices = [u"不显示", u"手动刷新", u"自动刷新"]
        self.previewMode = wx.RadioBox(self.previewOptions, wx.ID_ANY, u"预览图", wx.DefaultPosition, wx.DefaultSize, previewModeChoices, 1, wx.RA_SPECIFY_COLS)
        self.previewMode.SetSelection(2)
        bSizer30.Add(self.previewMode, 0, wx.ALL, 3)

        self.m_button3 = wx.Button(self.previewOptions, wx.ID_ANY, u"刷新预览图", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer30.Add(self.m_button3, 0, wx.ALIGN_CENTER, 5)

        bSizer28.Add(bSizer30, 0, 0, 5)

        bSizer19.Add(bSizer28, 0, wx.EXPAND, 5)

        self.previewProgress = wx.Gauge(self.previewOptions, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size(160, -1), wx.GA_HORIZONTAL)
        self.previewProgress.SetValue(0)
        bSizer19.Add(self.previewProgress, 0, wx.ALL, 5)

        self.previewOptions.SetSizer(bSizer19)
        self.previewOptions.Layout()
        bSizer19.Fit(self.previewOptions)
        bSizer12.Add(self.previewOptions, 0, 0, 0)

        self.processingOptions.SetSizer(bSizer12)
        self.processingOptions.Layout()
        bSizer12.Fit(self.processingOptions)
        self.settingsPanel.AddPage(self.processingOptions, u"处理方式", True)
        self.savingOptions = wx.Panel(self.settingsPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer264 = wx.BoxSizer(wx.VERTICAL)

        bSizer23 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer191 = wx.BoxSizer(wx.VERTICAL)

        bSizer265 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText81 = wx.StaticText(self.savingOptions, wx.ID_ANY, u"保存位置", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText81.Wrap(-1)

        bSizer265.Add(self.m_staticText81, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.selectSavingPath = wx.DirPickerCtrl(self.savingOptions, wx.ID_ANY, wx.EmptyString, u"选择保存位置", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE | wx.DIRP_DIR_MUST_EXIST)
        bSizer265.Add(self.selectSavingPath, 1, wx.ALL | wx.EXPAND, 3)

        savingFormatChoices = [u"blp", u"bmp", u"dib", u"bufr", u"cur", u"pcx", u"dcx", u"dds", u"ps", u"eps", u"fit", u"fits", u"fli", u"flc", u"ftc", u"ftu", u"gbr", u"gif", u"grib", u"h5", u"hdf", u"png", u"apng", u"jp2", u"j2k", u"jpc", u"jpf", u"jpx", u"j2c", u"icns", u"ico", u"im",
                               u"iim", u"tif", u"tiff", u"jfif", u"jpe", u"jpg", u"jpeg", u"mpg", u"mpeg", u"mpo", u"msp", u"palm", u"pcd", u"pdf", u"pxr", u"pbm", u"pgm", u"ppm", u"pnm", u"psd", u"bw", u"rgb", u"rgba", u"sgi", u"ras", u"tga", u"icb", u"vda", u"vst", u"webp", u"wmf", u"emf", u"xbm", u"xpm"]
        self.savingFormat = wx.Choice(self.savingOptions, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, savingFormatChoices, 0)
        self.savingFormat.SetSelection(21)
        bSizer265.Add(self.savingFormat, 0, wx.ALIGN_CENTER | wx.ALL, 3)

        bSizer191.Add(bSizer265, 0, wx.EXPAND, 0)

        sbSizer61 = wx.StaticBoxSizer(wx.StaticBox(self.savingOptions, wx.ID_ANY, u"高级设置"), wx.HORIZONTAL)

        bSizer44 = wx.BoxSizer(wx.VERTICAL)

        bSizer451 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText8212 = wx.StaticText(sbSizer61.GetStaticBox(), wx.ID_ANY, u"有损保存质量:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText8212.Wrap(-1)

        self.m_staticText8212.SetToolTip(u"(1-100)保存为有损格式时，值越大保存的文件越大，质量越好")

        bSizer451.Add(self.m_staticText8212, 0, wx.ALIGN_CENTER | wx.ALL, 2)

        self.qualityInfo = wx.StaticText(sbSizer61.GetStaticBox(), wx.ID_ANY, u"98", wx.DefaultPosition, wx.DefaultSize, 0)
        self.qualityInfo.Wrap(-1)

        bSizer451.Add(self.qualityInfo, 0, wx.ALIGN_CENTER | wx.ALL, 2)

        bSizer44.Add(bSizer451, 0, wx.ALIGN_CENTER, 0)

        self.savingQuality = wx.Slider(sbSizer61.GetStaticBox(), wx.ID_ANY, 98, 1, 100, wx.DefaultPosition, wx.Size(-1, 25), wx.SL_BOTH | wx.SL_HORIZONTAL)
        bSizer44.Add(self.savingQuality, 0, wx.ALL | wx.EXPAND, 0)

        sbSizer61.Add(bSizer44, 1, wx.EXPAND, 5)

        bSizer45 = wx.BoxSizer(wx.VERTICAL)

        bSizer461 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText82111 = wx.StaticText(sbSizer61.GetStaticBox(), wx.ID_ANY, u"有损色度抽样等级:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText82111.Wrap(-1)

        self.m_staticText82111.SetToolTip(u"(0-2) 0表示不使用，等级越高，保存有损格式时获得的文件大小越小，但会导致图片出现噪点，使图片解密后失真")

        bSizer461.Add(self.m_staticText82111, 0, wx.ALL, 2)

        self.subsamplingInfo = wx.StaticText(sbSizer61.GetStaticBox(), wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0)
        self.subsamplingInfo.Wrap(-1)

        bSizer461.Add(self.subsamplingInfo, 0, wx.ALL, 2)

        bSizer45.Add(bSizer461, 0, wx.ALIGN_CENTER, 0)

        self.subsamplingLevel = wx.Slider(sbSizer61.GetStaticBox(), wx.ID_ANY, 0, 0, 2, wx.DefaultPosition, wx.Size(-1, 25), wx.SL_BOTH | wx.SL_HORIZONTAL)
        bSizer45.Add(self.subsamplingLevel, 0, wx.ALL | wx.EXPAND, 0)

        sbSizer61.Add(bSizer45, 1, wx.EXPAND, 5)

        bSizer191.Add(sbSizer61, 1, wx.ALL | wx.EXPAND, 3)

        bSizer23.Add(bSizer191, 1, wx.EXPAND, 5)

        self.savingFilters = wx.Panel(self.savingOptions, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer311 = wx.BoxSizer(wx.HORIZONTAL)

        sbSizer4 = wx.StaticBoxSizer(wx.StaticBox(self.savingFilters, wx.ID_ANY, u"[过滤器]模式"), wx.VERTICAL)

        self.encryptionFilter = wx.CheckBox(sbSizer4.GetStaticBox(), wx.ID_ANY, u"加密模式", wx.DefaultPosition, wx.DefaultSize, 0)
        self.encryptionFilter.SetValue(True)
        sbSizer4.Add(self.encryptionFilter, 0, wx.ALL, 5)

        sbSizer4.Add((0, 0), 1, wx.EXPAND, 5)

        self.decryptionFilter = wx.CheckBox(sbSizer4.GetStaticBox(), wx.ID_ANY, u"解密模式", wx.DefaultPosition, wx.DefaultSize, 0)
        self.decryptionFilter.SetValue(True)
        sbSizer4.Add(self.decryptionFilter, 0, wx.ALL, 5)

        sbSizer4.Add((0, 0), 1, wx.EXPAND, 5)

        self.qqFilter = wx.CheckBox(sbSizer4.GetStaticBox(), wx.ID_ANY, u"QQ反屏蔽", wx.DefaultPosition, wx.DefaultSize, 0)
        self.qqFilter.SetValue(True)
        sbSizer4.Add(self.qqFilter, 0, wx.ALL, 5)

        bSizer311.Add(sbSizer4, 0, wx.ALL | wx.EXPAND, 2)

        sbSizer41 = wx.StaticBoxSizer(wx.StaticBox(self.savingFilters, wx.ID_ANY, u"[过滤器]操作"), wx.HORIZONTAL)

        bSizer35 = wx.BoxSizer(wx.VERTICAL)

        self.passwordFilter = wx.CheckBox(sbSizer41.GetStaticBox(), wx.ID_ANY, u"使用密码", wx.DefaultPosition, wx.DefaultSize, wx.CHK_3STATE | wx.CHK_ALLOW_3RD_STATE_FOR_USER)
        self.passwordFilter.SetValue(True)
        bSizer35.Add(self.passwordFilter, 0, wx.ALL, 5)

        bSizer35.Add((0, 0), 1, wx.EXPAND, 5)

        self.shuffleFilter = wx.CheckBox(sbSizer41.GetStaticBox(), wx.ID_ANY, u"顺序打乱", wx.DefaultPosition, wx.DefaultSize, wx.CHK_3STATE | wx.CHK_ALLOW_3RD_STATE_FOR_USER)
        self.shuffleFilter.SetValue(True)
        bSizer35.Add(self.shuffleFilter, 0, wx.ALL, 5)

        bSizer35.Add((0, 0), 1, wx.EXPAND, 5)

        self.flipFilter = wx.CheckBox(sbSizer41.GetStaticBox(), wx.ID_ANY, u"随机翻转", wx.DefaultPosition, wx.DefaultSize, wx.CHK_3STATE | wx.CHK_ALLOW_3RD_STATE_FOR_USER)
        self.flipFilter.SetValue(True)
        bSizer35.Add(self.flipFilter, 0, wx.ALL, 5)

        sbSizer41.Add(bSizer35, 0, wx.EXPAND, 5)

        bSizer351 = wx.BoxSizer(wx.VERTICAL)

        self.mappingFilter = wx.CheckBox(sbSizer41.GetStaticBox(), wx.ID_ANY, u"通道映射", wx.DefaultPosition, wx.DefaultSize, wx.CHK_3STATE | wx.CHK_ALLOW_3RD_STATE_FOR_USER)
        self.mappingFilter.SetValue(True)
        bSizer351.Add(self.mappingFilter, 0, wx.ALL, 5)

        bSizer351.Add((0, 0), 1, wx.EXPAND, 5)

        self.XorFilter = wx.CheckBox(sbSizer41.GetStaticBox(), wx.ID_ANY, u"异或加密", wx.DefaultPosition, wx.DefaultSize, wx.CHK_3STATE | wx.CHK_ALLOW_3RD_STATE_FOR_USER)
        self.XorFilter.SetValue(True)
        bSizer351.Add(self.XorFilter, 0, wx.ALL, 5)

        sbSizer41.Add(bSizer351, 0, wx.EXPAND, 5)

        bSizer311.Add(sbSizer41, 0, wx.ALL | wx.EXPAND, 2)

        self.savingFilters.SetSizer(bSizer311)
        self.savingFilters.Layout()
        bSizer311.Fit(self.savingFilters)
        bSizer23.Add(self.savingFilters, 0, wx.EXPAND | wx.ALL, 5)

        bSizer264.Add(bSizer23, 0, wx.EXPAND, 5)

        self.savingBtnPanel = wx.Panel(self.savingOptions, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer20 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_button7 = wx.Button(self.savingBtnPanel, wx.ID_ANY, u"保存当前选中的图片", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer20.Add(self.m_button7, 0, wx.ALL, 5)

        self.m_button8 = wx.Button(self.savingBtnPanel, wx.ID_ANY, u"保存所有符合过滤条件的图片", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer20.Add(self.m_button8, 0, wx.ALL, 5)

        self.savingBtnPanel.SetSizer(bSizer20)
        self.savingBtnPanel.Layout()
        bSizer20.Fit(self.savingBtnPanel)
        bSizer264.Add(self.savingBtnPanel, 0, wx.EXPAND | wx.ALL, 0)

        self.savingPrograssPanel = wx.Panel(self.savingOptions, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.savingPrograssPanel.Hide()

        bSizer231 = wx.BoxSizer(wx.HORIZONTAL)

        self.stopSavingBtn = wx.Button(self.savingPrograssPanel, wx.ID_ANY, u"取消尚未进行的任务", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer231.Add(self.stopSavingBtn, 0, wx.ALL, 5)

        self.savingProgress = wx.Gauge(self.savingPrograssPanel, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL | wx.GA_SMOOTH)
        self.savingProgress.SetValue(0)
        bSizer231.Add(self.savingProgress, 2, wx.ALIGN_CENTER | wx.ALL, 5)

        self.savingProgressInfo = wx.StaticText(self.savingPrograssPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.savingProgressInfo.Wrap(-1)

        bSizer231.Add(self.savingProgressInfo, 1, wx.ALIGN_CENTER | wx.ALIGN_LEFT | wx.ALL, 5)

        self.savingPrograssPanel.SetSizer(bSizer231)
        self.savingPrograssPanel.Layout()
        bSizer231.Fit(self.savingPrograssPanel)
        bSizer264.Add(self.savingPrograssPanel, 0, wx.EXPAND | wx.ALL, 0)

        self.savingOptions.SetSizer(bSizer264)
        self.savingOptions.Layout()
        bSizer264.Fit(self.savingOptions)
        self.settingsPanel.AddPage(self.savingOptions, u"保存图片", False)

        bSizer43.Add(self.settingsPanel, 1, wx.ALL | wx.EXPAND, 5)

        sbSizer6 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"高级导入设置"), wx.VERTICAL)

        self.m_staticText82 = wx.StaticText(sbSizer6.GetStaticBox(), wx.ID_ANY, u"允许最大像素量", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText82.Wrap(-1)

        self.m_staticText82.SetToolTip(u"允许载入的最大图片像素量，0为禁用(谨防DOS压缩炸弹图片)")

        sbSizer6.Add(self.m_staticText82, 0, wx.ALIGN_CENTER | wx.ALL, 2)

        self.maxImagePixels = wx.SpinCtrl(sbSizer6.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL | wx.SP_ARROW_KEYS | wx.TE_PROCESS_ENTER, 0, 1000000000, 89478485)
        self.maxImagePixels.SetToolTip(u"允许载入的最大图片像素量，0为禁用(谨防DOS压缩炸弹图片)")

        sbSizer6.Add(self.maxImagePixels, 0, wx.ALL | wx.EXPAND, 0)

        bSizer43.Add(sbSizer6, 0, wx.ALL | wx.EXPAND, 5)

        bSizer26.Add(bSizer43, 0, wx.EXPAND, 5)

        self.SetSizer(bSizer26)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.Bind(wx.EVT_CLOSE, self.exit)
        self.Bind(wx.EVT_MOVE_END, self.on_move_end)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.stopLoadingBtn.Bind(wx.EVT_BUTTON, self.stop_loading_event)
        self.m_button5.Bind(wx.EVT_BUTTON, self.load_file)
        self.m_button6.Bind(wx.EVT_BUTTON, self.load_dir)
        self.m_button10.Bind(wx.EVT_BUTTON, self.del_item)
        self.imageTreeCtrl.Bind(wx.EVT_TREE_SEL_CHANGED, self.switch_image)
        self.procMode.Bind(wx.EVT_RADIOBOX, self.processing_mode_change)
        self.passwordCtrl.Bind(wx.EVT_TEXT_ENTER, self.update_password_dict)
        self.cuttingRow.Bind(wx.EVT_SPINCTRL, self.refresh_preview)
        self.cuttingRow.Bind(wx.EVT_TEXT_ENTER, self.refresh_preview)
        self.cuttingCol.Bind(wx.EVT_SPINCTRL, self.refresh_preview)
        self.cuttingCol.Bind(wx.EVT_TEXT_ENTER, self.refresh_preview)
        self.shuffleChunks.Bind(wx.EVT_CHECKBOX, self.refresh_preview)
        self.flipChunks.Bind(wx.EVT_CHECKBOX, self.refresh_preview)
        self.rgbMapping.Bind(wx.EVT_CHECKBOX, self.refresh_preview)
        self.XOREncryption.Bind(wx.EVT_CHECKBOX, self.toggle_xor_panel_switch)
        self.XORR.Bind(wx.EVT_CHECKBOX, self.refresh_preview)
        self.XORG.Bind(wx.EVT_CHECKBOX, self.refresh_preview)
        self.XORB.Bind(wx.EVT_CHECKBOX, self.refresh_preview)
        self.XORA.Bind(wx.EVT_CHECKBOX, self.refresh_preview)
        self.noiseXor.Bind(wx.EVT_CHECKBOX, self.toggle_factor_slider_switch)
        self.noiseFactor.Bind(wx.EVT_SCROLL, self.update_noise_factor_num)
        self.noiseFactor.Bind(wx.EVT_SCROLL_CHANGED, self.refresh_preview)
        self.m_button31.Bind(wx.EVT_BUTTON, self.apply_to_all)
        self.m_button311.Bind(wx.EVT_BUTTON, self.set_settings_as_default)
        self.previewMode.Bind(wx.EVT_RADIOBOX, self.preview_mode_change)
        self.m_button3.Bind(wx.EVT_BUTTON, self.manual_refresh)
        self.selectSavingPath.Bind(wx.EVT_DIRPICKER_CHANGED, self.sync_saving_settings)
        self.savingFormat.Bind(wx.EVT_CHOICE, self.sync_saving_settings)
        self.savingQuality.Bind(wx.EVT_SCROLL, self.update_quality_num)
        self.subsamplingLevel.Bind(wx.EVT_SCROLL, self.update_subsampling_num)
        self.m_button7.Bind(wx.EVT_BUTTON, self.save_selected_image)
        self.m_button8.Bind(wx.EVT_BUTTON, self.bulk_save)
        self.stopSavingBtn.Bind(wx.EVT_BUTTON, self.stop_saving_event)

    def __del__(self):
        pass

    # Virtual event handlers, override them in your derived class
    def exit(self, event):
        event.Skip()

    def on_move_end(self, event):
        event.Skip()

    def on_size(self, event):
        event.Skip()

    def stop_loading_event(self, event):
        event.Skip()

    def load_file(self, event):
        event.Skip()

    def load_dir(self, event):
        event.Skip()

    def del_item(self, event):
        event.Skip()

    def switch_image(self, event):
        event.Skip()

    def processing_mode_change(self, event):
        event.Skip()

    def update_password_dict(self, event):
        event.Skip()

    def refresh_preview(self, event):
        event.Skip()

    def toggle_xor_panel_switch(self, event):
        event.Skip()

    def toggle_factor_slider_switch(self, event):
        event.Skip()

    def update_noise_factor_num(self, event):
        event.Skip()

    def apply_to_all(self, event):
        event.Skip()

    def set_settings_as_default(self, event):
        event.Skip()

    def preview_mode_change(self, event):
        event.Skip()

    def manual_refresh(self, event):
        event.Skip()

    def sync_saving_settings(self, event):
        event.Skip()

    def update_quality_num(self, event):
        event.Skip()

    def update_subsampling_num(self, event):
        event.Skip()

    def save_selected_image(self, event):
        event.Skip()

    def bulk_save(self, event):
        event.Skip()

    def stop_saving_event(self, event):
        event.Skip()
