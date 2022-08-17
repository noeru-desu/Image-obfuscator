# -*- coding: utf-8 -*-

###########################################################################
# Python code generated with wxFormBuilder (version 3.10.1-df7791b)
# http://www.wxformbuilder.org/
##
# PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.adv
import wx.stc

###########################################################################
# Class MainFrame
###########################################################################


class MainFrame (wx.Frame):
    __slots__ = (
        'SettingsSourceUsed', 'advancedSaveSettingsPanel', 'collapseAllBtn', 'delBtn', 'disableCache', 'displayedPreview',
        'expandAllBtn', 'finalLayoutWidgets', 'imageInfo', 'imagePanel', 'imageTreeCtrl', 'imageTreePanel', 'imageTreeSearchCtrl',
        'importedBitmap', 'importedBitmapPanel', 'importedBitmapSizerPanel', 'loadingClipboardBtn', 'loadingFileBtn',
        'loadingPanel', 'loadingProgress', 'loadingProgressInfo', 'loadingProgressPanel', 'lowMemoryMode', 'm_button18',
        'm_button23', 'm_button24', 'm_button31', 'm_button311', 'm_button312', 'm_button6', 'm_button8', 'm_panel25',
        'm_staticText12', 'm_staticText14', 'm_staticText23', 'm_staticText29', 'm_staticText34', 'm_staticText81',
        'm_staticText82', 'm_staticText82111', 'm_staticText821111', 'm_staticText8212', 'm_staticline3', 'm_staticline31',
        'm_staticline4', 'manuallyRefreshBtn', 'maxImagePixels', 'otherOptions', 'passwordCtrl', 'previewLayout', 'previewMode',
        'previewOptions', 'previewProgress', 'previewProgressInfo', 'previewSource', 'previewedBitmap', 'previewedBitmapPanel',
        'previewedBitmapSizerPanel', 'procMode', 'procSettingsPanelContainer', 'processingOptions', 'qualityInfo',
        'recordInterfaceSettings', 'recordPasswordDict', 'redundantCacheLength', 'reloadingBtn', 'resamplingFilter', 'saveBtn',
        'saveBtnPanel', 'saveCompression', 'saveExif', 'saveFormat', 'saveKwdsJson', 'saveLossless', 'saveOptimize', 'saveOptions',
        'saveProgress', 'saveProgressInfo', 'saveProgressPanel', 'saveQuality', 'selectSavePath', 'settingsPanel',
        'stopLoadingBtn', 'stopSaveBtn', 'subsamplingInfo', 'subsamplingLevel'
    )

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Image Obfuscator", pos=wx.DefaultPosition, size=wx.Size(790, 900), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL, name=u"Image Obfuscator")

        self.SetSizeHints(wx.Size(590, 640), wx.DefaultSize)
        self.SetFont(wx.Font(9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Segoe UI"))
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        bSizer26 = wx.BoxSizer(wx.VERTICAL)

        self.loadingProgressPanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.loadingProgressPanel.Hide()

        bSizer263 = wx.BoxSizer(wx.HORIZONTAL)

        self.stopLoadingBtn = wx.Button(self.loadingProgressPanel, wx.ID_ANY, u"停止载入", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer263.Add(self.stopLoadingBtn, 0, wx.ALL, 5)

        self.loadingProgress = wx.Gauge(self.loadingProgressPanel, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL | wx.GA_SMOOTH)
        self.loadingProgress.SetValue(0)
        bSizer263.Add(self.loadingProgress, 1, wx.ALIGN_CENTER | wx.ALL, 5)

        self.loadingProgressInfo = wx.StaticText(self.loadingProgressPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.loadingProgressInfo.Wrap(-1)

        bSizer263.Add(self.loadingProgressInfo, 1, wx.ALIGN_CENTER | wx.ALIGN_LEFT | wx.ALL, 5)

        self.loadingProgressPanel.SetSizer(bSizer263)
        self.loadingProgressPanel.Layout()
        bSizer263.Fit(self.loadingProgressPanel)
        bSizer26.Add(self.loadingProgressPanel, 0, wx.ALL | wx.EXPAND, 5)

        self.loadingPanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, -1), wx.TAB_TRAVERSAL)
        bSizer91 = wx.BoxSizer(wx.HORIZONTAL)

        self.loadingFileBtn = wx.Button(self.loadingPanel, wx.ID_ANY, u"载入文件", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer91.Add(self.loadingFileBtn, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.m_button6 = wx.Button(self.loadingPanel, wx.ID_ANY, u"载入文件夹", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer91.Add(self.m_button6, 0, wx.ALIGN_CENTER_VERTICAL, 5)

        self.loadingClipboardBtn = wx.Button(self.loadingPanel, wx.ID_ANY, u"从剪贴板载入", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer91.Add(self.loadingClipboardBtn, 0, wx.ALL, 5)

        self.imageInfo = wx.StaticText(self.loadingPanel, wx.ID_ANY, u"未选择图像", wx.DefaultPosition, wx.DefaultSize, 0)
        self.imageInfo.Wrap(-1)

        bSizer91.Add(self.imageInfo, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.loadingPanel.SetSizer(bSizer91)
        self.loadingPanel.Layout()
        bSizer91.Fit(self.loadingPanel)
        bSizer26.Add(self.loadingPanel, 0, wx.ALL | wx.EXPAND, 5)

        bSizer281 = wx.BoxSizer(wx.HORIZONTAL)

        self.imageTreePanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.imageTreePanel.SetMaxSize(wx.Size(280, -1))

        bSizer262 = wx.BoxSizer(wx.VERTICAL)

        self.imageTreeSearchCtrl = wx.SearchCtrl(self.imageTreePanel, wx.ID_ANY, u"文件树搜索功能尚不可用", wx.DefaultPosition, wx.DefaultSize, wx.TE_CENTER)
        self.imageTreeSearchCtrl.ShowSearchButton(True)
        self.imageTreeSearchCtrl.ShowCancelButton(True)
        self.imageTreeSearchCtrl.Enable(False)
        self.imageTreeSearchCtrl.Hide()

        bSizer262.Add(self.imageTreeSearchCtrl, 0, wx.ALL | wx.EXPAND, 2)

        bSizer40 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer50 = wx.BoxSizer(wx.VERTICAL)

        self.delBtn = wx.Button(self.imageTreePanel, wx.ID_ANY, u"删除此项", wx.DefaultPosition, wx.DefaultSize, 0)
        self.delBtn.SetToolTip(u"卸载选中的项目")

        bSizer50.Add(self.delBtn, 0, wx.EXPAND, 5)

        self.reloadingBtn = wx.Button(self.imageTreePanel, wx.ID_ANY, u"重载此项", wx.DefaultPosition, wx.DefaultSize, 0)
        self.reloadingBtn.SetToolTip(u"重新加载选中项目的图像文件")

        bSizer50.Add(self.reloadingBtn, 0, wx.EXPAND, 5)

        bSizer40.Add(bSizer50, 1, wx.EXPAND, 5)

        bSizer51 = wx.BoxSizer(wx.VERTICAL)

        self.expandAllBtn = wx.Button(self.imageTreePanel, wx.ID_ANY, u"全部展开", wx.DefaultPosition, wx.DefaultSize, 0)
        self.expandAllBtn.SetToolTip(u"重新加载选中项目的图像文件")

        bSizer51.Add(self.expandAllBtn, 0, wx.EXPAND, 5)

        self.collapseAllBtn = wx.Button(self.imageTreePanel, wx.ID_ANY, u"全部收起", wx.DefaultPosition, wx.DefaultSize, 0)
        self.collapseAllBtn.SetToolTip(u"重新加载选中项目的图像文件")

        bSizer51.Add(self.collapseAllBtn, 0, wx.EXPAND, 5)

        bSizer40.Add(bSizer51, 1, wx.EXPAND, 5)

        bSizer262.Add(bSizer40, 0, wx.EXPAND, 5)

        bSizer262.Add((0, 0), 0, wx.ALL | wx.EXPAND, 3)

        self.imageTreeCtrl = wx.TreeCtrl(self.imageTreePanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE | wx.TR_FULL_ROW_HIGHLIGHT |
                                         wx.TR_HAS_VARIABLE_ROW_HEIGHT | wx.TR_HIDE_ROOT | wx.TR_NO_BUTTONS | wx.TR_ROW_LINES | wx.TR_SINGLE | wx.TR_TWIST_BUTTONS)
        bSizer262.Add(self.imageTreeCtrl, 1, wx.EXPAND, 5)

        self.imageTreePanel.SetSizer(bSizer262)
        self.imageTreePanel.Layout()
        bSizer262.Fit(self.imageTreePanel)
        bSizer281.Add(self.imageTreePanel, 2, wx.EXPAND | wx.ALL, 5)

        self.imagePanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer44 = wx.BoxSizer(wx.VERTICAL)

        self.importedBitmapPanel = wx.Panel(self.imagePanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        sbSizer2 = wx.StaticBoxSizer(wx.StaticBox(self.importedBitmapPanel, wx.ID_ANY, u"导入图像-预览图"), wx.VERTICAL)

        self.importedBitmapSizerPanel = wx.Panel(sbSizer2.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        importedBitmapSizer = wx.BoxSizer(wx.VERTICAL)

        self.importedBitmap = wx.StaticBitmap(self.importedBitmapSizerPanel, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0)
        importedBitmapSizer.Add(self.importedBitmap, 1, wx.ALIGN_CENTER, 0)

        self.importedBitmapSizerPanel.SetSizer(importedBitmapSizer)
        self.importedBitmapSizerPanel.Layout()
        importedBitmapSizer.Fit(self.importedBitmapSizerPanel)
        sbSizer2.Add(self.importedBitmapSizerPanel, 1, wx.EXPAND, 5)

        self.importedBitmapPanel.SetSizer(sbSizer2)
        self.importedBitmapPanel.Layout()
        sbSizer2.Fit(self.importedBitmapPanel)
        bSizer44.Add(self.importedBitmapPanel, 1, wx.EXPAND, 5)

        self.previewedBitmapPanel = wx.Panel(self.imagePanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        sbSizer3 = wx.StaticBoxSizer(wx.StaticBox(self.previewedBitmapPanel, wx.ID_ANY, u"处理结果-预览图"), wx.VERTICAL)

        self.previewedBitmapSizerPanel = wx.Panel(sbSizer3.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        previewedBitmapSizer = wx.BoxSizer(wx.VERTICAL)

        self.previewedBitmap = wx.StaticBitmap(self.previewedBitmapSizerPanel, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0)
        previewedBitmapSizer.Add(self.previewedBitmap, 1, wx.ALIGN_CENTER, 0)

        self.previewedBitmapSizerPanel.SetSizer(previewedBitmapSizer)
        self.previewedBitmapSizerPanel.Layout()
        previewedBitmapSizer.Fit(self.previewedBitmapSizerPanel)
        sbSizer3.Add(self.previewedBitmapSizerPanel, 1, wx.EXPAND, 5)

        self.previewedBitmapPanel.SetSizer(sbSizer3)
        self.previewedBitmapPanel.Layout()
        sbSizer3.Fit(self.previewedBitmapPanel)
        bSizer44.Add(self.previewedBitmapPanel, 1, wx.EXPAND, 5)

        self.imagePanel.SetSizer(bSizer44)
        self.imagePanel.Layout()
        bSizer44.Fit(self.imagePanel)
        bSizer281.Add(self.imagePanel, 5, wx.ALL | wx.EXPAND, 2)

        bSizer26.Add(bSizer281, 1, wx.EXPAND, 5)

        bSizer43 = wx.BoxSizer(wx.HORIZONTAL)

        self.settingsPanel = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.NB_FIXEDWIDTH)
        self.processingOptions = wx.Panel(self.settingsPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer12 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer12.Add((0, 0), 1, 0, 5)

        sbSizer10 = wx.StaticBoxSizer(wx.StaticBox(self.processingOptions, wx.ID_ANY, u"处理模式"), wx.VERTICAL)

        procModeChoices = []
        self.procMode = wx.ListBox(sbSizer10.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, procModeChoices, wx.LB_NEEDED_SB | wx.LB_SINGLE)
        self.procMode.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Segoe UI Variable Display Semib"))

        sbSizer10.Add(self.procMode, 1, wx.EXPAND, 5)

        bSizer12.Add(sbSizer10, 0, wx.EXPAND, 5)

        bSizer12.Add((0, 0), 0, wx.ALL, 3)

        bSizer282 = wx.BoxSizer(wx.VERTICAL)

        SettingsSourceUsedChoices = [u"界面设置", u"文件加密参数", u"加密参数字段"]
        self.SettingsSourceUsed = wx.RadioBox(self.processingOptions, wx.ID_ANY, u"使用的设置源", wx.DefaultPosition, wx.DefaultSize, SettingsSourceUsedChoices, 1, wx.RA_SPECIFY_COLS)
        self.SettingsSourceUsed.SetSelection(0)
        self.SettingsSourceUsed.SetToolTip(u"处理图像时使用的设置来源\n界面设置: 每个模式在右侧(如果有)提供的设置选项\n文件加密参数: 来自于每个被加密文件末尾的加密参数\n加密参数字段: base85编码的加密参数(手动指定)\n选项呈灰色表明当前模式不需要此选项")

        bSizer282.Add(self.SettingsSourceUsed, 1, wx.EXPAND, 5)

        self.m_staticText12 = wx.StaticText(self.processingOptions, wx.ID_ANY, u"密码", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText12.Wrap(-1)

        bSizer282.Add(self.m_staticText12, 0, wx.ALIGN_CENTER | wx.ALL, 2)

        self.passwordCtrl = wx.TextCtrl(self.processingOptions, wx.ID_ANY, u"none", wx.DefaultPosition, wx.DefaultSize, wx.TE_CENTER | wx.TE_NO_VSCROLL | wx.TE_PROCESS_ENTER)
        self.passwordCtrl.SetMaxLength(32)
        self.passwordCtrl.SetToolTip(u"none表示不使用密码，密码长度不可超过32字节")

        bSizer282.Add(self.passwordCtrl, 0, 0, 0)

        bSizer12.Add(bSizer282, 0, wx.EXPAND, 5)

        bSizer12.Add((0, 0), 1, 0, 3)

        self.procSettingsPanelContainer = wx.Panel(self.processingOptions, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.procSettingsPanelContainer.SetMinSize(wx.Size(-1, 180))

        bSizer12.Add(self.procSettingsPanelContainer, 5, wx.EXPAND, 0)

        bSizer31 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticline31 = wx.StaticLine(self.processingOptions, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL)
        bSizer31.Add(self.m_staticline31, 0, wx.EXPAND | wx.ALL, 3)

        bSizer29 = wx.BoxSizer(wx.VERTICAL)

        bSizer29.Add((0, 0), 1, wx.EXPAND, 5)

        self.m_staticText14 = wx.StaticText(self.processingOptions, wx.ID_ANY, u"设置管理", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText14.Wrap(-1)

        bSizer29.Add(self.m_staticText14, 0, wx.ALIGN_CENTER | wx.ALL, 2)

        self.m_button31 = wx.Button(self.processingOptions, wx.ID_ANY, u"应用到全部", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_button31.SetToolTip(u"将当前的处理设置应用到所有已加载的项目中")

        bSizer29.Add(self.m_button31, 0, wx.ALIGN_CENTER | wx.ALL, 2)

        self.m_button311 = wx.Button(self.processingOptions, wx.ID_ANY, u"设置为默认", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_button311.SetToolTip(u"将当前的处理设置设置为默认设置，新加载的项目将会使用默认设置")

        bSizer29.Add(self.m_button311, 0, wx.ALIGN_CENTER | wx.ALL, 2)

        self.m_button312 = wx.Button(self.processingOptions, wx.ID_ANY, u"恢复为默认", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_button312.SetToolTip(u"将默认处理设置应用到当前的项目中")

        bSizer29.Add(self.m_button312, 0, wx.ALL, 2)

        self.m_staticline3 = wx.StaticLine(self.processingOptions, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        bSizer29.Add(self.m_staticline3, 0, wx.EXPAND, 5)

        self.m_staticText23 = wx.StaticText(self.processingOptions, wx.ID_ANY, u"获取加密参数", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText23.Wrap(-1)

        bSizer29.Add(self.m_staticText23, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)

        self.m_button24 = wx.Button(self.processingOptions, wx.ID_ANY, u"序列化数据", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer29.Add(self.m_button24, 0, wx.ALL, 2)

        bSizer29.Add((0, 0), 1, wx.EXPAND, 5)

        bSizer31.Add(bSizer29, 0, wx.ALL | wx.EXPAND, 2)

        self.m_staticline4 = wx.StaticLine(self.processingOptions, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL)
        bSizer31.Add(self.m_staticline4, 0, wx.ALL | wx.EXPAND, 3)

        bSizer12.Add(bSizer31, 0, wx.EXPAND, 5)

        bSizer12.Add((0, 0), 1, 0, 0)

        self.processingOptions.SetSizer(bSizer12)
        self.processingOptions.Layout()
        bSizer12.Fit(self.processingOptions)
        self.settingsPanel.AddPage(self.processingOptions, u"图像加密设置", True)
        self.previewOptions = wx.Panel(self.settingsPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer401 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer401.Add((0, 0), 1, 0, 5)

        bSizer19 = wx.BoxSizer(wx.VERTICAL)

        bSizer28 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer30 = wx.BoxSizer(wx.VERTICAL)

        bSizer40 = wx.BoxSizer(wx.HORIZONTAL)

        previewModeChoices = [u"不显示", u"手动刷新", u"自动刷新"]
        self.previewMode = wx.RadioBox(self.previewOptions, wx.ID_ANY, u"预览图", wx.DefaultPosition, wx.DefaultSize, previewModeChoices, 1, wx.RA_SPECIFY_COLS)
        self.previewMode.SetSelection(2)
        bSizer40.Add(self.previewMode, 0, wx.ALL | wx.EXPAND, 3)

        displayedPreviewChoices = [u"仅导入图像", u"仅处理结果", u"同时显示"]
        self.displayedPreview = wx.RadioBox(self.previewOptions, wx.ID_ANY, u"显示预览图", wx.DefaultPosition, wx.DefaultSize, displayedPreviewChoices, 1, wx.RA_SPECIFY_COLS)
        self.displayedPreview.SetSelection(2)
        bSizer40.Add(self.displayedPreview, 0, wx.ALL | wx.EXPAND, 3)

        previewLayoutChoices = [u"竖向", u"横向", u"自动"]
        self.previewLayout = wx.RadioBox(self.previewOptions, wx.ID_ANY, u"预览图排版", wx.DefaultPosition, wx.DefaultSize, previewLayoutChoices, 1, wx.RA_SPECIFY_COLS)
        self.previewLayout.SetSelection(2)
        bSizer40.Add(self.previewLayout, 0, wx.ALL | wx.EXPAND, 3)

        previewSourceChoices = [u"预览图", u"原图"]
        self.previewSource = wx.RadioBox(self.previewOptions, wx.ID_ANY, u"加密时使用图源", wx.DefaultPosition, wx.DefaultSize, previewSourceChoices, 1, wx.RA_SPECIFY_COLS)
        self.previewSource.SetSelection(0)
        self.previewSource.SetToolTip(u"生成\"处理结果-预览图\"时使用的图源\n选择\"预览图\"可获得更好的性能，但结果会有所偏差\n选择\"原图\"将不会出现偏差，但性能低于\"预览图\"选项")

        bSizer40.Add(self.previewSource, 0, wx.ALL | wx.EXPAND, 3)

        bSizer30.Add(bSizer40, 1, wx.EXPAND, 5)

        bSizer40 = wx.BoxSizer(wx.HORIZONTAL)

        self.previewProgressInfo = wx.StaticText(self.previewOptions, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.previewProgressInfo.Wrap(-1)

        bSizer40.Add(self.previewProgressInfo, 3, wx.ALL, 5)

        self.manuallyRefreshBtn = wx.Button(self.previewOptions, wx.ID_ANY, u"刷新预览图", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer40.Add(self.manuallyRefreshBtn, 1, wx.ALIGN_CENTER | wx.ALL, 1)

        bSizer30.Add(bSizer40, 0, wx.EXPAND, 5)

        bSizer28.Add(bSizer30, 1, wx.EXPAND, 5)

        bSizer19.Add(bSizer28, 1, wx.EXPAND, 5)

        self.previewProgress = wx.Gauge(self.previewOptions, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size(160, -1), wx.GA_HORIZONTAL)
        self.previewProgress.SetValue(0)
        bSizer19.Add(self.previewProgress, 0, wx.ALL | wx.EXPAND, 3)

        bSizer401.Add(bSizer19, 0, wx.EXPAND, 5)

        resamplingFilterChoices = [u"最邻近", u"单线性", u"双线性", u"Hamming", u"双三次", u"Lanczos"]
        self.resamplingFilter = wx.RadioBox(self.previewOptions, wx.ID_ANY, u"重采样方式", wx.DefaultPosition, wx.DefaultSize, resamplingFilterChoices, 1, 0)
        self.resamplingFilter.SetSelection(4)
        self.resamplingFilter.SetToolTip(u"缩放预览图使用的重采样方式，自上而下质量依次递增，性能依次递减，默认为双三次(Bicubic)")

        bSizer401.Add(self.resamplingFilter, 0, wx.ALL, 3)

        bSizer401.Add((0, 0), 1, 0, 5)

        self.previewOptions.SetSizer(bSizer401)
        self.previewOptions.Layout()
        bSizer401.Fit(self.previewOptions)
        self.settingsPanel.AddPage(self.previewOptions, u"预览图相关设置", False)
        self.saveOptions = wx.Panel(self.settingsPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer264 = wx.BoxSizer(wx.VERTICAL)

        bSizer23 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer265 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText81 = wx.StaticText(self.saveOptions, wx.ID_ANY, u"保存位置", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText81.Wrap(-1)

        bSizer265.Add(self.m_staticText81, 0, wx.ALIGN_CENTER | wx.ALL, 2)

        self.selectSavePath = wx.DirPickerCtrl(self.saveOptions, wx.ID_ANY, wx.EmptyString, u"选择保存位置", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE | wx.DIRP_DIR_MUST_EXIST)
        bSizer265.Add(self.selectSavePath, 1, wx.ALL | wx.EXPAND, 2)

        saveFormatChoices = [u"bmp", u"gif", u"png", u"ico", u"tif", u"tiff", u"jpg", u"jpeg", u"pdf", u"psd", u"tga", u"webp"]
        self.saveFormat = wx.ComboBox(self.saveOptions, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, saveFormatChoices, wx.TE_PROCESS_ENTER)
        self.saveFormat.SetSelection(2)
        self.saveFormat.SetToolTip(u"如果下拉框中不存在所需的保存格式，可直接输入后缀名，将自动进行检查。支持的保存格式如下\n")

        bSizer265.Add(self.saveFormat, 0, wx.ALIGN_CENTER | wx.ALL, 4)

        bSizer23.Add(bSizer265, 0, 0, 0)

        self.saveBtnPanel = wx.Panel(self.saveOptions, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer20 = wx.BoxSizer(wx.HORIZONTAL)

        self.saveBtn = wx.Button(self.saveBtnPanel, wx.ID_ANY, u"保存当前选中的图像/文件夹", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer20.Add(self.saveBtn, 0, wx.ALL, 5)

        self.m_button8 = wx.Button(self.saveBtnPanel, wx.ID_ANY, u"保存全部图像", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer20.Add(self.m_button8, 0, wx.ALL, 5)

        self.saveBtnPanel.SetSizer(bSizer20)
        self.saveBtnPanel.Layout()
        bSizer20.Fit(self.saveBtnPanel)
        bSizer23.Add(self.saveBtnPanel, 1, 0, 0)

        self.saveProgressPanel = wx.Panel(self.saveOptions, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.saveProgressPanel.Hide()

        bSizer231 = wx.BoxSizer(wx.HORIZONTAL)

        self.stopSaveBtn = wx.Button(self.saveProgressPanel, wx.ID_ANY, u"取消所有保存任务", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer231.Add(self.stopSaveBtn, 0, wx.ALL, 5)

        self.saveProgress = wx.Gauge(self.saveProgressPanel, wx.ID_ANY, 200, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL)
        self.saveProgress.SetValue(0)
        bSizer231.Add(self.saveProgress, 2, wx.ALIGN_CENTER | wx.ALL, 5)

        self.saveProgressInfo = wx.StaticText(self.saveProgressPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.saveProgressInfo.Wrap(-1)

        bSizer231.Add(self.saveProgressInfo, 1, wx.ALIGN_CENTER | wx.ALIGN_LEFT | wx.ALL, 5)

        self.saveProgressPanel.SetSizer(bSizer231)
        self.saveProgressPanel.Layout()
        bSizer231.Fit(self.saveProgressPanel)
        bSizer23.Add(self.saveProgressPanel, 0, 0, 1)

        bSizer264.Add(bSizer23, 0, wx.EXPAND, 5)

        self.advancedSaveSettingsPanel = wx.Panel(self.saveOptions, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.advancedSaveSettingsPanel.SetToolTip(u"传递给PIL.Image.save的额外参数\n不是所有参数都会被使用，不同格式会使用不同个数/类别的参数\n所有可用参数请查看：https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html")

        sbSizer61 = wx.StaticBoxSizer(wx.StaticBox(self.advancedSaveSettingsPanel, wx.ID_ANY, u"高级保存设置(保存不同格式时会按需使用)"), wx.VERTICAL)

        bSizer47 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer49 = wx.BoxSizer(wx.VERTICAL)

        self.saveOptimize = wx.CheckBox(sbSizer61.GetStaticBox(), wx.ID_ANY, u"优化文件大小", wx.DefaultPosition, wx.DefaultSize, 0)
        self.saveOptimize.SetToolTip(u"部分格式启用后将保持图像质量无损并一定程度减小文件大小，但是会增加保存耗时")

        bSizer49.Add(self.saveOptimize, 0, wx.ALL, 3)

        self.saveExif = wx.CheckBox(sbSizer61.GetStaticBox(), wx.ID_ANY, u"保留Exif信息", wx.DefaultPosition, wx.DefaultSize, 0)
        self.saveExif.SetToolTip(u"部分图像在保存时将从添原始图像中添加Exif信息")

        bSizer49.Add(self.saveExif, 0, wx.ALL, 3)

        bSizer47.Add(bSizer49, 0, wx.EXPAND, 5)

        bSizer491 = wx.BoxSizer(wx.VERTICAL)

        self.saveLossless = wx.CheckBox(sbSizer61.GetStaticBox(), wx.ID_ANY, u"无损Webp", wx.DefaultPosition, wx.DefaultSize, 0)
        self.saveLossless.SetToolTip(u"部分格式启用后将保持图像质量无损并一定程度减小文件大小，但是会增加保存耗时")
        self.saveLossless.SetHelpText(u"保存webp时无损保存")

        bSizer491.Add(self.saveLossless, 0, wx.ALL, 3)

        bSizer47.Add(bSizer491, 1, wx.EXPAND, 5)

        bSizer441 = wx.BoxSizer(wx.VERTICAL)

        bSizer451 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText8212 = wx.StaticText(sbSizer61.GetStaticBox(), wx.ID_ANY, u"保存质量:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText8212.Wrap(-1)

        self.m_staticText8212.SetToolTip(u"保存部分有损格式时，值越大保存的文件越大，质量越好")

        bSizer451.Add(self.m_staticText8212, 0, wx.ALIGN_CENTER | wx.ALL, 2)

        self.qualityInfo = wx.StaticText(sbSizer61.GetStaticBox(), wx.ID_ANY, u"98", wx.DefaultPosition, wx.DefaultSize, 0)
        self.qualityInfo.Wrap(-1)

        bSizer451.Add(self.qualityInfo, 0, wx.ALIGN_CENTER | wx.ALL, 2)

        bSizer441.Add(bSizer451, 0, wx.ALIGN_CENTER, 0)

        self.saveQuality = wx.Slider(sbSizer61.GetStaticBox(), wx.ID_ANY, 98, 1, 100, wx.DefaultPosition, wx.Size(-1, 25), wx.SL_BOTH | wx.SL_HORIZONTAL)
        bSizer441.Add(self.saveQuality, 0, wx.ALL | wx.EXPAND, 0)

        bSizer47.Add(bSizer441, 0, 0, 5)

        bSizer452 = wx.BoxSizer(wx.VERTICAL)

        bSizer461 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText82111 = wx.StaticText(sbSizer61.GetStaticBox(), wx.ID_ANY, u"色度抽样等级:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText82111.Wrap(-1)

        self.m_staticText82111.SetToolTip(u"保存部分有损格式时，0表示不使用，等级越高，保存有损格式时获得的文件大小越小，但会导致图像出现噪点，使图像解密后失真")

        bSizer461.Add(self.m_staticText82111, 0, wx.ALL, 2)

        self.subsamplingInfo = wx.StaticText(sbSizer61.GetStaticBox(), wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0)
        self.subsamplingInfo.Wrap(-1)

        bSizer461.Add(self.subsamplingInfo, 0, wx.ALL, 2)

        bSizer452.Add(bSizer461, 0, wx.ALIGN_CENTER, 0)

        self.subsamplingLevel = wx.Slider(sbSizer61.GetStaticBox(), wx.ID_ANY, 0, 0, 2, wx.DefaultPosition, wx.Size(-1, 25), wx.SL_BOTH | wx.SL_HORIZONTAL)
        bSizer452.Add(self.subsamplingLevel, 0, wx.ALL | wx.EXPAND, 0)

        bSizer47.Add(bSizer452, 0, 0, 5)

        bSizer4521 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText821111 = wx.StaticText(sbSizer61.GetStaticBox(), wx.ID_ANY, u"压缩算法", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText821111.Wrap(-1)

        self.m_staticText821111.SetToolTip(u"保存部分格式时使用的图像有损或无损压缩算法(tiff开头的算法只能用于tiff类文件)")

        bSizer4521.Add(self.m_staticText821111, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)

        saveCompressionChoices = [u"none", u"group3", u"group4", u"jpeg", u"lzma", u"packbits", u"tiff_adobe_deflate", u"tiff_ccitt", u"tiff_lzw", u"tiff_raw_16", u"tiff_sgilog", u"tiff_sgilog24", u"tiff_thunderscan", u"webp", u"zstd"]
        self.saveCompression = wx.Choice(sbSizer61.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, saveCompressionChoices, 0)
        self.saveCompression.SetSelection(0)
        self.saveCompression.SetToolTip(u"保存部分格式时使用的图像有损或无损压缩算法(tiff开头的算法只能用于tiff类文件)")

        bSizer4521.Add(self.saveCompression, 0, 0, 5)

        bSizer47.Add(bSizer4521, 0, wx.EXPAND, 5)

        sbSizer61.Add(bSizer47, 0, 0, 0)

        sbSizer61.Add((0, 0), 1, 0, 5)

        bSizer48 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText29 = wx.StaticText(sbSizer61.GetStaticBox(), wx.ID_ANY, u"其他参数(具有最高优先级)", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText29.Wrap(-1)

        self.m_staticText29.SetToolTip(u"自定义键值对以使用支持的任意保存参数(若与上方的交互式参数重复，重复部分将始终使用自定义参数)")

        bSizer48.Add(self.m_staticText29, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)

        self.m_button18 = wx.Button(sbSizer61.GetStaticBox(), wx.ID_ANY, u"编辑", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_button18.SetToolTip(u"自定义键值对以使用支持的任意保存参数(若与上方的交互式参数重复，重复部分将始终使用自定义参数)")

        bSizer48.Add(self.m_button18, 0, 0, 5)

        self.saveKwdsJson = wx.TextCtrl(sbSizer61.GetStaticBox(), wx.ID_ANY, u"{}", wx.DefaultPosition, wx.DefaultSize, wx.TE_CENTER | wx.TE_NO_VSCROLL | wx.TE_READONLY)
        self.saveKwdsJson.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        self.saveKwdsJson.SetToolTip(u"自定义键值对以使用支持的任意保存参数(若与上方的交互式参数重复，重复部分将始终使用自定义参数)")

        bSizer48.Add(self.saveKwdsJson, 1, 0, 5)

        sbSizer61.Add(bSizer48, 0, wx.EXPAND, 5)

        self.advancedSaveSettingsPanel.SetSizer(sbSizer61)
        self.advancedSaveSettingsPanel.Layout()
        sbSizer61.Fit(self.advancedSaveSettingsPanel)
        bSizer264.Add(self.advancedSaveSettingsPanel, 1, wx.EXPAND | wx.ALL, 5)

        self.saveOptions.SetSizer(bSizer264)
        self.saveOptions.Layout()
        bSizer264.Fit(self.saveOptions)
        self.settingsPanel.AddPage(self.saveOptions, u"保存图像", False)
        self.otherOptions = wx.Panel(self.settingsPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer74 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer47 = wx.BoxSizer(wx.VERTICAL)

        sbSizer6 = wx.StaticBoxSizer(wx.StaticBox(self.otherOptions, wx.ID_ANY, u"高级导入设置"), wx.HORIZONTAL)

        self.m_staticText82 = wx.StaticText(sbSizer6.GetStaticBox(), wx.ID_ANY, u"允许最大像素量", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText82.Wrap(-1)

        self.m_staticText82.SetToolTip(u"允许载入的最大图像像素量，0为禁用(谨防DOS压缩炸弹图像)")

        sbSizer6.Add(self.m_staticText82, 0, wx.ALIGN_CENTER | wx.ALL, 2)

        self.maxImagePixels = wx.SpinCtrl(sbSizer6.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL | wx.SP_ARROW_KEYS | wx.TE_PROCESS_ENTER, 0, 1000000000, 89478485)
        self.maxImagePixels.SetToolTip(u"允许载入的最大图像像素量，0为禁用(谨防DOS压缩炸弹图像)")

        sbSizer6.Add(self.maxImagePixels, 1, wx.ALL, 0)

        bSizer47.Add(sbSizer6, 0, wx.ALL | wx.EXPAND, 5)

        sbSizer7 = wx.StaticBoxSizer(wx.StaticBox(self.otherOptions, wx.ID_ANY, u"其他操作"), wx.VERTICAL)

        bSizer481 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_button23 = wx.Button(sbSizer7.GetStaticBox(), wx.ID_ANY, u"打开配置保存文件夹", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer481.Add(self.m_button23, 0, wx.ALIGN_CENTER_VERTICAL, 5)

        sbSizer7.Add(bSizer481, 0, wx.EXPAND, 5)

        bSizer47.Add(sbSizer7, 1, wx.ALL | wx.EXPAND, 5)

        bSizer74.Add(bSizer47, 0, wx.EXPAND, 5)

        self.m_panel25 = wx.Panel(self.otherOptions, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.m_panel25.SetToolTip(u"热更改启动参数注意事项：\n热更改时不会立即将更改应用到所有已加载项目\n - 如开关低内存占用模式时，不会立即对所有已加载项目创建/清除缓存，而是在切换各项目时进行")

        sbSizer17 = wx.StaticBoxSizer(wx.StaticBox(self.m_panel25, wx.ID_ANY, u"启动参数"), wx.HORIZONTAL)

        bSizer45 = wx.BoxSizer(wx.VERTICAL)

        bSizer75 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText34 = wx.StaticText(sbSizer17.GetStaticBox(), wx.ID_ANY, u"预览图冗余缓存量", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText34.Wrap(-1)

        self.m_staticText34.SetToolTip(u"热更改启动参数注意事项：\n热更改时不会立即将更改应用到所有已加载项目\n - 如开关低内存占用模式时，不会立即对所有已加载项目创建/清除缓存，而是在切换各项目时进行\n\n预览图冗余缓存量: 使用加密模式时缓存多个不同加密设置下的处理结果，在取消选中时会仅保留最新的结果，其余结果将从缓存中删除")

        bSizer75.Add(self.m_staticText34, 0, wx.ALL, 5)

        self.redundantCacheLength = wx.SpinCtrl(sbSizer17.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS | wx.TE_PROCESS_ENTER, 1, 20, 5)
        self.redundantCacheLength.SetToolTip(u"热更改启动参数注意事项：\n热更改时不会立即将更改应用到所有已加载项目\n - 如开关低内存占用模式时，不会立即对所有已加载项目创建/清除缓存，而是在切换各项目时进行\n\n预览图冗余缓存量: 使用加密模式时缓存多个不同加密设置下的处理结果，在取消选中时会仅保留最新的结果，其余结果将从缓存中删除")

        bSizer75.Add(self.redundantCacheLength, 0, wx.ALL | wx.EXPAND, 0)

        bSizer45.Add(bSizer75, 0, wx.EXPAND, 5)

        self.lowMemoryMode = wx.CheckBox(sbSizer17.GetStaticBox(), wx.ID_ANY, u"低内存占用模式", wx.DefaultPosition, wx.DefaultSize, 0)
        self.lowMemoryMode.SetToolTip(u"热更改启动参数注意事项：\n热更改时不会立即将更改应用到所有已加载项目\n - 如开关低内存占用模式时，不会立即对所有已加载项目创建/清除缓存，而是在切换各项目时进行\n\n低内存占用模式: 取消选中时，不缓存原始图像数据(在需要时重新加载)、不缓存图像处理结果(在需要时重新生成)")

        bSizer45.Add(self.lowMemoryMode, 0, wx.ALL, 5)

        self.recordInterfaceSettings = wx.CheckBox(sbSizer17.GetStaticBox(), wx.ID_ANY, u"记录界面设置", wx.DefaultPosition, wx.DefaultSize, 0)
        self.recordInterfaceSettings.SetValue(True)
        self.recordInterfaceSettings.SetToolTip(u"热更改启动参数注意事项：\n热更改时不会立即将更改应用到所有已加载项目\n - 如开关低内存占用模式时，不会立即对所有已加载项目创建/清除缓存，而是在切换各项目时进行\n\n记录界面设置: 在退出时记录界面设置, 并在下次启动时回溯界面")

        bSizer45.Add(self.recordInterfaceSettings, 0, wx.ALL, 5)

        self.recordPasswordDict = wx.CheckBox(sbSizer17.GetStaticBox(), wx.ID_ANY, u"记录密码字典", wx.DefaultPosition, wx.DefaultSize, 0)
        self.recordPasswordDict.SetValue(True)
        self.recordPasswordDict.SetToolTip(u"热更改启动参数注意事项：\n热更改时不会立即将更改应用到所有已加载项目\n - 如开关低内存占用模式时，不会立即对所有已加载项目创建/清除缓存，而是在切换各项目时进行\n\n记录密码字典: 在退出时保存密码字典, 并在下次启动时重新载入")

        bSizer45.Add(self.recordPasswordDict, 0, wx.ALL, 5)

        self.disableCache = wx.CheckBox(sbSizer17.GetStaticBox(), wx.ID_ANY, u"禁止使用缓存", wx.DefaultPosition, wx.DefaultSize, 0)
        self.disableCache.SetToolTip(u"热更改启动参数注意事项：\n热更改时不会立即将更改应用到所有已加载项目\n - 如开关低内存占用模式时，不会立即对所有已加载项目创建/清除缓存，而是在切换各项目时进行\n\n禁止使用缓存: 与低内存占用模式不同，开启此选项后仍会保存缓存，但会在请求处理结果缓存时忽略缓存")

        bSizer45.Add(self.disableCache, 0, wx.ALL, 5)

        sbSizer17.Add(bSizer45, 0, wx.EXPAND, 5)

        bSizer46 = wx.BoxSizer(wx.VERTICAL)

        self.finalLayoutWidgets = wx.CheckBox(sbSizer17.GetStaticBox(), wx.ID_ANY, u"不实时刷新部件大小", wx.DefaultPosition, wx.DefaultSize, 0)
        self.finalLayoutWidgets.SetToolTip(u"热更改启动参数注意事项：\n热更改时不会立即将更改应用到所有已加载项目\n - 如开关低内存占用模式时，不会立即对所有已加载项目创建/清除缓存，而是在切换各项目时进行\n\n不实时刷新部件大小: 在拖动更改窗口大小时不实时刷新部件大小，而是在拖动结束后刷新")

        bSizer46.Add(self.finalLayoutWidgets, 0, wx.ALL, 5)

        sbSizer17.Add(bSizer46, 0, wx.EXPAND, 5)

        self.m_panel25.SetSizer(sbSizer17)
        self.m_panel25.Layout()
        sbSizer17.Fit(self.m_panel25)
        bSizer74.Add(self.m_panel25, 0, wx.ALL, 5)

        self.otherOptions.SetSizer(bSizer74)
        self.otherOptions.Layout()
        bSizer74.Fit(self.otherOptions)
        self.settingsPanel.AddPage(self.otherOptions, u"其他设置", False)

        bSizer43.Add(self.settingsPanel, 1, wx.ALL | wx.EXPAND, 5)

        bSizer26.Add(bSizer43, 0, wx.EXPAND, 5)

        self.SetSizer(bSizer26)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.Bind(wx.EVT_CLOSE, self.exit)
        self.Bind(wx.EVT_MAXIMIZE, self.on_maximize)
        self.Bind(wx.EVT_MOVE_END, self.on_move_end)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.stopLoadingBtn.Bind(wx.EVT_BUTTON, self.stop_loading_event)
        self.loadingFileBtn.Bind(wx.EVT_BUTTON, self.load_file)
        self.m_button6.Bind(wx.EVT_BUTTON, self.load_dir)
        self.loadingClipboardBtn.Bind(wx.EVT_BUTTON, self.load_image_from_clipboard)
        self.delBtn.Bind(wx.EVT_BUTTON, self.del_item)
        self.reloadingBtn.Bind(wx.EVT_BUTTON, self.reload_item)
        self.expandAllBtn.Bind(wx.EVT_BUTTON, self.expand_all_item)
        self.collapseAllBtn.Bind(wx.EVT_BUTTON, self.collapse_all_item)
        self.imageTreeCtrl.Bind(wx.EVT_TREE_SEL_CHANGED, self.switched_image)
        self.imageTreeCtrl.Bind(wx.EVT_TREE_SEL_CHANGING, self.switching_image)
        self.procMode.Bind(wx.EVT_LISTBOX, self.processing_mode_changed)
        self.SettingsSourceUsed.Bind(wx.EVT_RADIOBOX, self.settings_source_changed)
        self.passwordCtrl.Bind(wx.EVT_TEXT_ENTER, self.update_password_dict)
        self.m_button31.Bind(wx.EVT_BUTTON, self.apply_to_all)
        self.m_button311.Bind(wx.EVT_BUTTON, self.set_settings_as_default)
        self.m_button312.Bind(wx.EVT_BUTTON, self.revert_to_default)
        self.m_button24.Bind(wx.EVT_BUTTON, self.get_serialized_encryption_parameters)
        self.previewMode.Bind(wx.EVT_RADIOBOX, self.preview_mode_change)
        self.displayedPreview.Bind(wx.EVT_RADIOBOX, self.change_displayed_preview)
        self.previewLayout.Bind(wx.EVT_RADIOBOX, self.change_preview_layout)
        self.previewSource.Bind(wx.EVT_RADIOBOX, self.force_refresh_preview)
        self.manuallyRefreshBtn.Bind(wx.EVT_BUTTON, self.manually_refresh)
        self.resamplingFilter.Bind(wx.EVT_RADIOBOX, self.force_refresh_preview)
        self.saveFormat.Bind(wx.EVT_COMBOBOX, self.record_save_format)
        self.saveFormat.Bind(wx.EVT_TEXT_ENTER, self.check_save_format)
        self.saveBtn.Bind(wx.EVT_BUTTON, self.save_selected_image)
        self.m_button8.Bind(wx.EVT_BUTTON, self.bulk_save)
        self.stopSaveBtn.Bind(wx.EVT_BUTTON, self.stop_save_event)
        self.saveQuality.Bind(wx.EVT_SCROLL, self.update_quality_num)
        self.subsamplingLevel.Bind(wx.EVT_SCROLL, self.update_subsampling_num)
        self.m_button18.Bind(wx.EVT_BUTTON, self.edit_save_args_json)
        self.m_button23.Bind(wx.EVT_BUTTON, self.open_config_folder)
        self.redundantCacheLength.Bind(wx.EVT_TEXT_ENTER, self.change_redundant_cache_length)
        self.lowMemoryMode.Bind(wx.EVT_CHECKBOX, self.toggle_low_memory_usage_mode)
        self.recordInterfaceSettings.Bind(wx.EVT_CHECKBOX, self.toggle_record_interface_settings)
        self.recordPasswordDict.Bind(wx.EVT_CHECKBOX, self.toggle_record_password_dict)
        self.disableCache.Bind(wx.EVT_CHECKBOX, self.toggle_disable_cache)
        self.finalLayoutWidgets.Bind(wx.EVT_CHECKBOX, self.toggle_final_layout_widgets)

    def __del__(self):
        pass

    # Virtual event handlers, override them in your derived class
    def exit(self, event):
        event.Skip()

    def on_maximize(self, event):
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

    def load_image_from_clipboard(self, event):
        event.Skip()

    def del_item(self, event):
        event.Skip()

    def reload_item(self, event):
        event.Skip()

    def expand_all_item(self, event):
        event.Skip()

    def collapse_all_item(self, event):
        event.Skip()

    def switched_image(self, event):
        event.Skip()

    def switching_image(self, event):
        event.Skip()

    def processing_mode_changed(self, event):
        event.Skip()

    def settings_source_changed(self, event):
        event.Skip()

    def update_password_dict(self, event):
        event.Skip()

    def apply_to_all(self, event):
        event.Skip()

    def set_settings_as_default(self, event):
        event.Skip()

    def revert_to_default(self, event):
        event.Skip()

    def get_serialized_encryption_parameters(self, event):
        event.Skip()

    def preview_mode_change(self, event):
        event.Skip()

    def change_displayed_preview(self, event):
        event.Skip()

    def change_preview_layout(self, event):
        event.Skip()

    def force_refresh_preview(self, event):
        event.Skip()

    def manually_refresh(self, event):
        event.Skip()

    def record_save_format(self, event):
        event.Skip()

    def check_save_format(self, event):
        event.Skip()

    def save_selected_image(self, event):
        event.Skip()

    def bulk_save(self, event):
        event.Skip()

    def stop_save_event(self, event):
        event.Skip()

    def update_quality_num(self, event):
        event.Skip()

    def update_subsampling_num(self, event):
        event.Skip()

    def edit_save_args_json(self, event):
        event.Skip()

    def open_config_folder(self, event):
        event.Skip()

    def change_redundant_cache_length(self, event):
        event.Skip()

    def toggle_low_memory_usage_mode(self, event):
        event.Skip()

    def toggle_record_interface_settings(self, event):
        event.Skip()

    def toggle_record_password_dict(self, event):
        event.Skip()

    def toggle_disable_cache(self, event):
        event.Skip()

    def toggle_final_layout_widgets(self, event):
        event.Skip()


###########################################################################
# Class PasswordDialog
###########################################################################

class PasswordDialog (wx.Dialog):
    __slots__ = (
        'passwordTextCtrl', 'm_staticText20', 'm_staticText22', 'fileNameText', 'tipText', 'mainPanel', 'm_button13',
        'm_staticText18''m_button131'
    )

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"请输入密码", pos=wx.DefaultPosition, size=wx.Size(320, 180), style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetFont(wx.Font(9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Segoe UI"))
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        bSizer43 = wx.BoxSizer(wx.VERTICAL)

        bSizer43.Add((0, 0), 1, wx.EXPAND, 5)

        bSizer46 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer46.Add((0, 0), 0, wx.ALL, 20)

        self.mainPanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer52 = wx.BoxSizer(wx.VERTICAL)

        bSizer51 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText20 = wx.StaticText(self.mainPanel, wx.ID_ANY, u"图像", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText20.Wrap(-1)

        self.m_staticText20.SetFont(wx.Font(9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Segoe UI"))

        bSizer51.Add(self.m_staticText20, 0, 0, 3)

        bSizer54 = wx.BoxSizer(wx.VERTICAL)

        self.fileNameText = wx.StaticText(self.mainPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ST_ELLIPSIZE_END)
        self.fileNameText.Wrap(-1)

        self.fileNameText.SetFont(wx.Font(9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Segoe UI"))

        bSizer54.Add(self.fileNameText, 0, wx.ALIGN_CENTER, 0)

        bSizer51.Add(bSizer54, 1, wx.EXPAND, 5)

        self.m_staticText22 = wx.StaticText(self.mainPanel, wx.ID_ANY, u"被加密", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText22.Wrap(-1)

        self.m_staticText22.SetFont(wx.Font(9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Segoe UI"))

        bSizer51.Add(self.m_staticText22, 0, 0, 3)

        bSizer52.Add(bSizer51, 0, wx.ALIGN_CENTER, 5)

        bSizer45 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText18 = wx.StaticText(self.mainPanel, wx.ID_ANY, u"请输入密码", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText18.Wrap(-1)

        self.m_staticText18.SetFont(wx.Font(9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Segoe UI"))

        bSizer45.Add(self.m_staticText18, 0, wx.ALIGN_CENTER | wx.ALL, 3)

        self.tipText = wx.StaticText(self.mainPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.tipText.Wrap(-1)

        bSizer45.Add(self.tipText, 0, wx.ALIGN_CENTER | wx.ALL, 3)

        self.passwordTextCtrl = wx.TextCtrl(self.mainPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_CENTER | wx.TE_PROCESS_ENTER)
        self.passwordTextCtrl.SetMaxLength(32)
        bSizer45.Add(self.passwordTextCtrl, 1, wx.ALL | wx.EXPAND, 0)

        bSizer52.Add(bSizer45, 1, wx.EXPAND, 5)

        self.mainPanel.SetSizer(bSizer52)
        self.mainPanel.Layout()
        bSizer52.Fit(self.mainPanel)
        bSizer46.Add(self.mainPanel, 1, wx.EXPAND, 5)

        bSizer46.Add((0, 0), 0, wx.ALL, 20)

        bSizer43.Add(bSizer46, 1, wx.EXPAND, 5)

        bSizer43.Add((0, 0), 1, wx.EXPAND, 5)

        bSizer48 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer48.Add((0, 0), 1, wx.EXPAND, 5)

        self.m_button13 = wx.Button(self, wx.ID_ANY, u"确认", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer48.Add(self.m_button13, 0, wx.ALL, 5)

        self.m_button131 = wx.Button(self, wx.ID_ANY, u"取消", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer48.Add(self.m_button131, 0, wx.ALL, 5)

        bSizer43.Add(bSizer48, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer43)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.passwordTextCtrl.Bind(wx.EVT_TEXT_ENTER, self.user_confirm)
        self.m_button13.Bind(wx.EVT_BUTTON, self.user_confirm)
        self.m_button131.Bind(wx.EVT_BUTTON, self.user_cancel)

    def __del__(self):
        pass

    # Virtual event handlers, override them in your derived class
    def user_confirm(self, event):
        event.Skip()

    def user_cancel(self, event):
        event.Skip()


###########################################################################
# Class JsonEditorDialog
###########################################################################

class JsonEditorDialog (wx.Dialog):
    __slots__ = (
        'extraInfoText', 'extraLink', 'font', 'm_button19', 'm_button20', 'm_button21', 'm_button22', 'textEditor', 'titleText'
    )

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"Json编辑器", pos=wx.DefaultPosition, size=wx.Size(702, 450), style=wx.DEFAULT_DIALOG_STYLE | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER)

        self.SetSizeHints(wx.Size(400, 450), wx.DefaultSize)

        bSizer49 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer50 = wx.BoxSizer(wx.VERTICAL)

        self.titleText = wx.StaticText(self, wx.ID_ANY, u"编辑文本", wx.DefaultPosition, wx.DefaultSize, 0)
        self.titleText.Wrap(-1)

        self.titleText.SetMaxSize(wx.Size(200, -1))

        bSizer50.Add(self.titleText, 0, wx.ALL, 5)

        self.extraLink = wx.adv.HyperlinkCtrl(self, wx.ID_ANY, wx.EmptyString, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.adv.HL_DEFAULT_STYLE)
        bSizer50.Add(self.extraLink, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        self.extraInfoText = wx.StaticText(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.extraInfoText.Wrap(-1)

        self.extraInfoText.SetMaxSize(wx.Size(200, -1))

        bSizer50.Add(self.extraInfoText, 1, wx.ALL, 5)

        self.m_button19 = wx.Button(self, wx.ID_ANY, u"检查Json格式", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer50.Add(self.m_button19, 0, wx.ALL | wx.EXPAND, 5)

        self.m_button20 = wx.Button(self, wx.ID_ANY, u"自动格式化Json格式", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer50.Add(self.m_button20, 0, wx.ALL | wx.EXPAND, 5)

        self.m_button21 = wx.Button(self, wx.ID_ANY, u"应用当前Json文本", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer50.Add(self.m_button21, 0, wx.ALL | wx.EXPAND, 5)

        self.m_button22 = wx.Button(self, wx.ID_ANY, u"清空Json文本", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer50.Add(self.m_button22, 0, wx.ALL | wx.EXPAND, 5)

        bSizer49.Add(bSizer50, 0, wx.EXPAND, 5)

        self.textEditor = wx.stc.StyledTextCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.textEditor.SetUseTabs(True)
        self.textEditor.SetTabWidth(2)
        self.textEditor.SetIndent(2)
        self.textEditor.SetTabIndents(True)
        self.textEditor.SetBackSpaceUnIndents(True)
        self.textEditor.SetViewEOL(False)
        self.textEditor.SetViewWhiteSpace(True)
        self.textEditor.SetMarginWidth(2, 0)
        self.textEditor.SetIndentationGuides(True)
        self.textEditor.SetReadOnly(False)
        self.textEditor.SetMarginType(1, wx.stc.STC_MARGIN_SYMBOL)
        self.textEditor.SetMarginMask(1, wx.stc.STC_MASK_FOLDERS)
        self.textEditor.SetMarginWidth(1, 16)
        self.textEditor.SetMarginSensitive(1, True)
        self.textEditor.SetProperty("fold", "1")
        self.textEditor.SetFoldFlags(wx.stc.STC_FOLDFLAG_LINEBEFORE_CONTRACTED | wx.stc.STC_FOLDFLAG_LINEAFTER_CONTRACTED)
        self.textEditor.SetMarginType(0, wx.stc.STC_MARGIN_NUMBER)
        self.textEditor.SetMarginWidth(0, self.textEditor.TextWidth(wx.stc.STC_STYLE_LINENUMBER, "_99999"))
        self.font = wx.Font(14, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Consolas")
        self.textEditor.StyleSetFont(wx.stc.STC_STYLE_DEFAULT, self.font)
        self.textEditor.MarkerDefine(wx.stc.STC_MARKNUM_FOLDER, wx.stc.STC_MARK_BOXPLUS)
        self.textEditor.MarkerSetBackground(wx.stc.STC_MARKNUM_FOLDER, wx.BLACK)
        self.textEditor.MarkerSetForeground(wx.stc.STC_MARKNUM_FOLDER, wx.WHITE)
        self.textEditor.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEROPEN, wx.stc.STC_MARK_BOXMINUS)
        self.textEditor.MarkerSetBackground(wx.stc.STC_MARKNUM_FOLDEROPEN, wx.BLACK)
        self.textEditor.MarkerSetForeground(wx.stc.STC_MARKNUM_FOLDEROPEN, wx.WHITE)
        self.textEditor.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERSUB, wx.stc.STC_MARK_EMPTY)
        self.textEditor.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEREND, wx.stc.STC_MARK_BOXPLUS)
        self.textEditor.MarkerSetBackground(wx.stc.STC_MARKNUM_FOLDEREND, wx.BLACK)
        self.textEditor.MarkerSetForeground(wx.stc.STC_MARKNUM_FOLDEREND, wx.WHITE)
        self.textEditor.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.stc.STC_MARK_BOXMINUS)
        self.textEditor.MarkerSetBackground(wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.BLACK)
        self.textEditor.MarkerSetForeground(wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.WHITE)
        self.textEditor.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERMIDTAIL, wx.stc.STC_MARK_EMPTY)
        self.textEditor.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERTAIL, wx.stc.STC_MARK_EMPTY)
        self.textEditor.SetSelBackground(True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        self.textEditor.SetSelForeground(True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        self.textEditor.SetFont(wx.Font(14, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Consolas"))

        bSizer49.Add(self.textEditor, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(bSizer49)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.Bind(wx.EVT_CLOSE, self.close_dialog)
        self.m_button19.Bind(wx.EVT_BUTTON, self.check_json_format)
        self.m_button20.Bind(wx.EVT_BUTTON, self.format_json)
        self.m_button21.Bind(wx.EVT_BUTTON, self.apply_json)
        self.m_button22.Bind(wx.EVT_BUTTON, self.clear_json)

    def __del__(self):
        pass

    # Virtual event handlers, override them in your derived class
    def close_dialog(self, event):
        event.Skip()

    def check_json_format(self, event):
        event.Skip()

    def format_json(self, event):
        event.Skip()

    def apply_json(self, event):
        event.Skip()

    def clear_json(self, event):
        event.Skip()


###########################################################################
# Class TextDisplayDialog
###########################################################################

class TextDisplayDialog (wx.Dialog):
    __slots__ = (
        'actionTip', 'extraInfo', 'm_button25', 'text'
    )

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"文本展示", pos=wx.DefaultPosition, size=wx.Size(400, 350), style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer52 = wx.BoxSizer(wx.VERTICAL)

        self.extraInfo = wx.StaticText(self, wx.ID_ANY, u"详细信息", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL)
        self.extraInfo.Wrap(-1)

        bSizer52.Add(self.extraInfo, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.text = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE | wx.TE_NO_VSCROLL | wx.TE_READONLY)
        self.text.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        bSizer52.Add(self.text, 1, wx.ALL | wx.EXPAND, 5)

        bSizer53 = wx.BoxSizer(wx.HORIZONTAL)

        self.actionTip = wx.StaticText(self, wx.ID_ANY, u"已复制到剪贴板", wx.DefaultPosition, wx.DefaultSize, 0)
        self.actionTip.Wrap(-1)

        self.actionTip.Hide()

        bSizer53.Add(self.actionTip, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.m_button25 = wx.Button(self, wx.ID_ANY, u"复制到剪贴板", wx.DefaultPosition, wx.DefaultSize, 0)

        self.m_button25.SetDefault()
        bSizer53.Add(self.m_button25, 0, wx.ALL, 3)

        bSizer52.Add(bSizer53, 0, wx.ALIGN_RIGHT, 5)

        self.SetSizer(bSizer52)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_button25.Bind(wx.EVT_BUTTON, self.copy_text)

    def __del__(self):
        pass

    # Virtual event handlers, override them in your derived class
    def copy_text(self, event):
        event.Skip()


###########################################################################
# Class MultiLineTextEntryDialog
###########################################################################

class MultiLineTextEntryDialog (wx.Dialog):
    __slots__ = (
        'actionTip', 'extraInfo', 'm_button25', 'm_button251', 'text'
    )

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"输入文本", pos=wx.DefaultPosition, size=wx.Size(400, 350), style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer52 = wx.BoxSizer(wx.VERTICAL)

        self.extraInfo = wx.StaticText(self, wx.ID_ANY, u"详细信息", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL)
        self.extraInfo.Wrap(-1)

        bSizer52.Add(self.extraInfo, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.text = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE | wx.TE_NO_VSCROLL)
        self.text.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        bSizer52.Add(self.text, 1, wx.ALL | wx.EXPAND, 5)

        bSizer53 = wx.BoxSizer(wx.HORIZONTAL)

        self.actionTip = wx.StaticText(self, wx.ID_ANY, u"已复制到剪贴板", wx.DefaultPosition, wx.DefaultSize, 0)
        self.actionTip.Wrap(-1)

        self.actionTip.Hide()

        bSizer53.Add(self.actionTip, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.m_button251 = wx.Button(self, wx.ID_ANY, u"取消", wx.DefaultPosition, wx.DefaultSize, 0)

        self.m_button251.SetDefault()
        bSizer53.Add(self.m_button251, 0, wx.ALL, 3)

        self.m_button25 = wx.Button(self, wx.ID_ANY, u"确认", wx.DefaultPosition, wx.DefaultSize, 0)

        self.m_button25.SetDefault()
        bSizer53.Add(self.m_button25, 0, wx.ALL, 3)

        bSizer52.Add(bSizer53, 0, wx.ALIGN_RIGHT, 5)

        self.SetSizer(bSizer52)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.Bind(wx.EVT_CLOSE, self.cancel)
        self.m_button251.Bind(wx.EVT_BUTTON, self.cancel)
        self.m_button25.Bind(wx.EVT_BUTTON, self.confirm)

    def __del__(self):
        pass

    # Virtual event handlers, override them in your derived class
    def cancel(self, event):
        event.Skip()

    def confirm(self, event):
        event.Skip()
