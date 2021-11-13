# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.0-4761b0c)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Image Encryptor", pos = wx.DefaultPosition, size = wx.Size( 1170,640 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.Size( 745,640 ), wx.DefaultSize )
        self.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

        self.m_menubar1 = wx.MenuBar( 0 )
        self.m_menu1 = wx.Menu()
        self.loadFileMenuItem = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"载入文件", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu1.Append( self.loadFileMenuItem )

        self.m_menuItem51 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"载入文件夹", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu1.Append( self.m_menuItem51 )

        self.m_menu1.AppendSeparator()

        self.m_menuItem5 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"保存", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu1.Append( self.m_menuItem5 )

        self.m_menubar1.Append( self.m_menu1, u"文件(File)" )

        self.m_menu2 = wx.Menu()
        self.aboutMenuItem = wx.MenuItem( self.m_menu2, wx.ID_ANY, u"关于", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu2.Append( self.aboutMenuItem )

        self.m_menu2.AppendSeparator()

        self.m_menuItem4 = wx.MenuItem( self.m_menu2, wx.ID_ANY, u"退出", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu2.Append( self.m_menuItem4 )

        self.m_menubar1.Append( self.m_menu2, u"关于(About)" )

        self.SetMenuBar( self.m_menubar1 )

        bSizer26 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer251 = wx.BoxSizer( wx.VERTICAL )

        self.imageTreePanel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer262 = wx.BoxSizer( wx.VERTICAL )

        self.imageTreeSearchCtrl = wx.SearchCtrl( self.imageTreePanel, wx.ID_ANY, u"文件树搜索功能尚不可用", wx.DefaultPosition, wx.DefaultSize, wx.TE_CENTER )
        self.imageTreeSearchCtrl.ShowSearchButton( True )
        self.imageTreeSearchCtrl.ShowCancelButton( True )
        self.imageTreeSearchCtrl.Enable( False )

        bSizer262.Add( self.imageTreeSearchCtrl, 0, wx.ALL|wx.EXPAND, 5 )

        self.imageTreeCtrl = wx.TreeCtrl( self.imageTreePanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE|wx.TR_FULL_ROW_HIGHLIGHT|wx.TR_HAS_BUTTONS|wx.TR_HAS_VARIABLE_ROW_HEIGHT|wx.TR_HIDE_ROOT|wx.TR_ROW_LINES|wx.TR_SINGLE|wx.TR_TWIST_BUTTONS )
        bSizer262.Add( self.imageTreeCtrl, 1, wx.EXPAND, 5 )


        self.imageTreePanel.SetSizer( bSizer262 )
        self.imageTreePanel.Layout()
        bSizer262.Fit( self.imageTreePanel )
        bSizer251.Add( self.imageTreePanel, 1, wx.EXPAND |wx.ALL, 5 )


        bSizer26.Add( bSizer251, 1, wx.EXPAND, 5 )

        self.settingsPanel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer10 = wx.BoxSizer( wx.VERTICAL )

        self.loadingPrograssPanel = wx.Panel( self.settingsPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.loadingPrograssPanel.Hide()

        bSizer263 = wx.BoxSizer( wx.VERTICAL )

        bSizer263.SetMinSize( wx.Size( -1,45 ) )
        bSizer271 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_button8 = wx.Button( self.loadingPrograssPanel, wx.ID_ANY, u"停止载入", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer271.Add( self.m_button8, 0, wx.ALL, 0 )

        self.loadingPrograss = wx.Gauge( self.loadingPrograssPanel, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
        self.loadingPrograss.SetValue( 0 )
        bSizer271.Add( self.loadingPrograss, 1, wx.ALL, 4 )

        self.stopLoadingBtn = wx.Button( self.loadingPrograssPanel, wx.ID_ANY, u"强制终止载入", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer271.Add( self.stopLoadingBtn, 0, wx.ALL, 0 )


        bSizer263.Add( bSizer271, 1, wx.EXPAND, 5 )

        self.loadingPrograssText = wx.StaticText( self.loadingPrograssPanel, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.loadingPrograssText.Wrap( -1 )

        bSizer263.Add( self.loadingPrograssText, 0, wx.ALIGN_CENTER|wx.ALL, 1 )


        self.loadingPrograssPanel.SetSizer( bSizer263 )
        self.loadingPrograssPanel.Layout()
        bSizer263.Fit( self.loadingPrograssPanel )
        bSizer10.Add( self.loadingPrograssPanel, 0, wx.ALL|wx.EXPAND, 5 )

        self.loadingPanel = wx.Panel( self.settingsPanel, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
        bSizer91 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer91.SetMinSize( wx.Size( -1,45 ) )
        self.m_button5 = wx.Button( self.loadingPanel, wx.ID_ANY, u"载入文件", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer91.Add( self.m_button5, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.m_button6 = wx.Button( self.loadingPanel, wx.ID_ANY, u"载入文件夹", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer91.Add( self.m_button6, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.imageInfo = wx.StaticText( self.loadingPanel, wx.ID_ANY, u"图像信息：未选择图片", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.imageInfo.Wrap( -1 )

        self.imageInfo.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )

        bSizer91.Add( self.imageInfo, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


        self.loadingPanel.SetSizer( bSizer91 )
        self.loadingPanel.Layout()
        bSizer91.Fit( self.loadingPanel )
        bSizer10.Add( self.loadingPanel, 0, wx.ALL, 5 )

        self.m_staticline3 = wx.StaticLine( self.settingsPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer10.Add( self.m_staticline3, 0, wx.EXPAND |wx.ALL, 5 )

        self.processingOptions = wx.Panel( self.settingsPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.processingOptions.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

        bSizer11 = wx.BoxSizer( wx.VERTICAL )

        bSizer12 = wx.BoxSizer( wx.HORIZONTAL )

        modeChoices = [ u"加密模式", u"解密模式", u"QQ反屏蔽" ]
        self.mode = wx.RadioBox( self.processingOptions, wx.ID_ANY, u"处理模式", wx.DefaultPosition, wx.DefaultSize, modeChoices, 1, wx.RA_SPECIFY_COLS )
        self.mode.SetSelection( 0 )
        bSizer12.Add( self.mode, 0, wx.ALL|wx.EXPAND, 5 )

        self.processingSettingsPanel1 = wx.Panel( self.processingOptions, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer13 = wx.BoxSizer( wx.VERTICAL )

        bSizer131 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText8 = wx.StaticText( self.processingSettingsPanel1, wx.ID_ANY, u"切割行数", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText8.Wrap( -1 )

        self.m_staticText8.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )

        bSizer131.Add( self.m_staticText8, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.row = wx.SpinCtrl( self.processingSettingsPanel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.SP_ARROW_KEYS|wx.TE_PROCESS_ENTER, 1, 100000000, 25 )
        bSizer131.Add( self.row, 0, wx.ALL, 5 )


        bSizer13.Add( bSizer131, 0, wx.EXPAND, 5 )

        bSizer15 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText9 = wx.StaticText( self.processingSettingsPanel1, wx.ID_ANY, u"切割列数", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText9.Wrap( -1 )

        bSizer15.Add( self.m_staticText9, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.col = wx.SpinCtrl( self.processingSettingsPanel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.SP_ARROW_KEYS|wx.TE_PROCESS_ENTER, 1, 100000000, 25 )
        bSizer15.Add( self.col, 0, wx.ALL|wx.EXPAND, 5 )


        bSizer13.Add( bSizer15, 0, wx.EXPAND, 5 )

        self.upset = wx.CheckBox( self.processingSettingsPanel1, wx.ID_ANY, u"随机打乱分块", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.upset.SetValue(True)
        self.upset.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )

        bSizer13.Add( self.upset, 0, wx.ALL, 5 )

        self.flip = wx.CheckBox( self.processingSettingsPanel1, wx.ID_ANY, u"随机翻转分块", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.flip.SetValue(True)
        self.flip.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )

        bSizer13.Add( self.flip, 0, wx.ALL, 5 )

        self.rgbMapping = wx.CheckBox( self.processingSettingsPanel1, wx.ID_ANY, u"分块随机RGB映射", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer13.Add( self.rgbMapping, 0, wx.ALL, 5 )


        self.processingSettingsPanel1.SetSizer( bSizer13 )
        self.processingSettingsPanel1.Layout()
        bSizer13.Fit( self.processingSettingsPanel1 )
        bSizer12.Add( self.processingSettingsPanel1, 1, wx.EXPAND |wx.ALL, 5 )

        bSizer17 = wx.BoxSizer( wx.VERTICAL )

        xorRgbChoices = [ u"不启用", u"RGB通道", u"RGBA通道" ]
        self.xorRgb = wx.RadioBox( self.processingOptions, wx.ID_ANY, u"异或加密", wx.DefaultPosition, wx.DefaultSize, xorRgbChoices, 1, wx.RA_SPECIFY_COLS )
        self.xorRgb.SetSelection( 0 )
        bSizer17.Add( self.xorRgb, 0, wx.ALL, 5 )

        self.m_staticText12 = wx.StaticText( self.processingOptions, wx.ID_ANY, u"添加密码到密码字典", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText12.Wrap( -1 )

        bSizer17.Add( self.m_staticText12, 0, wx.ALL, 5 )

        self.password = wx.TextCtrl( self.processingOptions, wx.ID_ANY, u"none", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        bSizer17.Add( self.password, 0, wx.ALL, 5 )


        bSizer12.Add( bSizer17, 0, wx.EXPAND, 5 )


        bSizer11.Add( bSizer12, 0, wx.EXPAND, 5 )

        bSizer9 = wx.BoxSizer( wx.HORIZONTAL )

        self.previewOptions = wx.Panel( self.processingOptions, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer19 = wx.BoxSizer( wx.VERTICAL )

        bSizer28 = wx.BoxSizer( wx.HORIZONTAL )

        previewModeChoices = [ u"不显示", u"手动刷新", u"自动刷新" ]
        self.previewMode = wx.RadioBox( self.previewOptions, wx.ID_ANY, u"预览图", wx.DefaultPosition, wx.DefaultSize, previewModeChoices, 1, wx.RA_SPECIFY_COLS )
        self.previewMode.SetSelection( 1 )
        bSizer28.Add( self.previewMode, 0, wx.ALL, 5 )

        self.m_staticline31 = wx.StaticLine( self.previewOptions, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
        bSizer28.Add( self.m_staticline31, 0, wx.EXPAND |wx.ALL, 5 )

        bSizer29 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText14 = wx.StaticText( self.previewOptions, wx.ID_ANY, u"同步设置", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText14.Wrap( -1 )

        bSizer29.Add( self.m_staticText14, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.m_button31 = wx.Button( self.previewOptions, wx.ID_ANY, u"应用到全部", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer29.Add( self.m_button31, 0, wx.ALL, 5 )

        self.m_button311 = wx.Button( self.previewOptions, wx.ID_ANY, u"设置为默认", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer29.Add( self.m_button311, 0, wx.ALL, 5 )


        bSizer28.Add( bSizer29, 1, wx.EXPAND, 5 )

        self.m_staticline4 = wx.StaticLine( self.previewOptions, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
        bSizer28.Add( self.m_staticline4, 0, wx.EXPAND |wx.ALL, 5 )


        bSizer19.Add( bSizer28, 1, wx.EXPAND, 5 )

        bSizer18 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_button3 = wx.Button( self.previewOptions, wx.ID_ANY, u"刷新预览图", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer18.Add( self.m_button3, 0, wx.ALL, 5 )

        self.previewProgressPrompt = wx.StaticText( self.previewOptions, wx.ID_ANY, u"等待载入图片", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.previewProgressPrompt.Wrap( -1 )

        bSizer18.Add( self.previewProgressPrompt, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


        bSizer19.Add( bSizer18, 0, wx.EXPAND, 5 )

        self.previewProgress = wx.Gauge( self.previewOptions, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
        self.previewProgress.SetValue( 0 )
        bSizer19.Add( self.previewProgress, 0, wx.ALL, 5 )


        self.previewOptions.SetSizer( bSizer19 )
        self.previewOptions.Layout()
        bSizer19.Fit( self.previewOptions )
        bSizer9.Add( self.previewOptions, 1, wx.EXPAND |wx.ALL, 5 )

        sbSizer6 = wx.StaticBoxSizer( wx.StaticBox( self.processingOptions, wx.ID_ANY, u"高级设置" ), wx.VERTICAL )

        self.m_staticText82 = wx.StaticText( sbSizer6.GetStaticBox(), wx.ID_ANY, u"允许载入最大像素量", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText82.Wrap( -1 )

        self.m_staticText82.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
        self.m_staticText82.SetToolTip( u"允许载入的最大图片像素量，0为禁用(谨防DOS压缩炸弹图片)" )

        sbSizer6.Add( self.m_staticText82, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.maxImagePixels = wx.SpinCtrl( sbSizer6.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.SP_ARROW_KEYS|wx.TE_PROCESS_ENTER, 0, 1000000000, 89478485 )
        self.maxImagePixels.SetToolTip( u"允许载入的最大图片像素量，0为禁用(谨防DOS压缩炸弹图片)" )

        sbSizer6.Add( self.maxImagePixels, 0, wx.ALL|wx.EXPAND, 0 )

        self.m_staticText821 = wx.StaticText( sbSizer6.GetStaticBox(), wx.ID_ANY, u"有损格式保存质量", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText821.Wrap( -1 )

        self.m_staticText821.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
        self.m_staticText821.SetToolTip( u"(1-100)保存为有损格式时，值越大保存的文件越大，质量越好" )

        sbSizer6.Add( self.m_staticText821, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.saveQuality = wx.SpinCtrl( sbSizer6.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.SP_ARROW_KEYS|wx.TE_PROCESS_ENTER, 1, 100, 95 )
        self.saveQuality.SetToolTip( u"(1-100)保存为有损格式时，值越大保存的文件越大，质量越好" )

        sbSizer6.Add( self.saveQuality, 1, wx.ALL|wx.EXPAND, 0 )

        self.m_staticText8211 = wx.StaticText( sbSizer6.GetStaticBox(), wx.ID_ANY, u"有损格式色度抽样等级", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText8211.Wrap( -1 )

        self.m_staticText8211.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
        self.m_staticText8211.SetToolTip( u"(0-2) 0表示不使用，等级越高，保存有损格式时获得的文件大小越小，但会导致图片出现噪点，使图片解密后失真" )

        sbSizer6.Add( self.m_staticText8211, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.subsamplingLevel = wx.SpinCtrl( sbSizer6.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.SP_ARROW_KEYS|wx.TE_PROCESS_ENTER, 0, 2, 0 )
        self.subsamplingLevel.SetToolTip( u"(0-2) 0表示不使用，等级越高，保存有损格式时获得的文件大小越小，但会导致图片出现噪点，使图片解密后失真" )

        sbSizer6.Add( self.subsamplingLevel, 1, wx.ALL|wx.EXPAND, 0 )


        bSizer9.Add( sbSizer6, 1, wx.ALL|wx.EXPAND, 0 )


        bSizer11.Add( bSizer9, 0, wx.EXPAND, 5 )


        self.processingOptions.SetSizer( bSizer11 )
        self.processingOptions.Layout()
        bSizer11.Fit( self.processingOptions )
        bSizer10.Add( self.processingOptions, 1, wx.EXPAND |wx.ALL, 5 )

        self.m_staticline21 = wx.StaticLine( self.settingsPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer10.Add( self.m_staticline21, 0, wx.EXPAND |wx.ALL, 5 )

        self.saveOptions = wx.Panel( self.settingsPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.saveOptions.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

        bSizer23 = wx.BoxSizer( wx.VERTICAL )

        bSizer20 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer22 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText81 = wx.StaticText( self.saveOptions, wx.ID_ANY, u"保存位置", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText81.Wrap( -1 )

        bSizer22.Add( self.m_staticText81, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.selectSavePath = wx.DirPickerCtrl( self.saveOptions, wx.ID_ANY, wx.EmptyString, u"选择保存位置", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
        bSizer22.Add( self.selectSavePath, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


        bSizer20.Add( bSizer22, 0, wx.EXPAND, 5 )

        bSizer21 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText22 = wx.StaticText( self.saveOptions, wx.ID_ANY, u"保存格式", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText22.Wrap( -1 )

        self.m_staticText22.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )

        bSizer21.Add( self.m_staticText22, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

        selectFormatChoices = [ u"blp", u"bmp", u"dib", u"bufr", u"cur", u"pcx", u"dcx", u"dds", u"ps", u"eps", u"fit", u"fits", u"fli", u"flc", u"ftc", u"ftu", u"gbr", u"gif", u"grib", u"h5", u"hdf", u"png", u"apng", u"jp2", u"j2k", u"jpc", u"jpf", u"jpx", u"j2c", u"icns", u"ico", u"im", u"iim", u"tif", u"tiff", u"jfif", u"jpe", u"jpg", u"jpeg", u"mpg", u"mpeg", u"mpo", u"msp", u"palm", u"pcd", u"pdf", u"pxr", u"pbm", u"pgm", u"ppm", u"pnm", u"psd", u"bw", u"rgb", u"rgba", u"sgi", u"ras", u"tga", u"icb", u"vda", u"vst", u"webp", u"wmf", u"emf", u"xbm", u"xpm" ]
        self.selectFormat = wx.Choice( self.saveOptions, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, selectFormatChoices, 0 )
        self.selectFormat.SetSelection( 21 )
        bSizer21.Add( self.selectFormat, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )


        bSizer20.Add( bSizer21, 0, wx.EXPAND, 5 )


        bSizer23.Add( bSizer20, 0, wx.EXPAND, 5 )

        bSizer25 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_button7 = wx.Button( self.saveOptions, wx.ID_ANY, u"保存文件", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button7.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )

        bSizer25.Add( self.m_button7, 0, wx.ALL, 5 )

        self.saveProgressPrompt = wx.StaticText( self.saveOptions, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.saveProgressPrompt.Wrap( -1 )

        bSizer25.Add( self.saveProgressPrompt, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


        bSizer23.Add( bSizer25, 0, wx.EXPAND, 5 )

        self.saveProgress = wx.Gauge( self.saveOptions, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL|wx.GA_SMOOTH )
        self.saveProgress.SetValue( 0 )
        bSizer23.Add( self.saveProgress, 0, wx.ALL, 5 )


        self.saveOptions.SetSizer( bSizer23 )
        self.saveOptions.Layout()
        bSizer23.Fit( self.saveOptions )
        bSizer10.Add( self.saveOptions, 1, wx.EXPAND |wx.ALL, 5 )


        self.settingsPanel.SetSizer( bSizer10 )
        self.settingsPanel.Layout()
        bSizer10.Fit( self.settingsPanel )
        bSizer26.Add( self.settingsPanel, 0, wx.EXPAND |wx.ALL, 0 )

        self.imagePanel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        gSizer1 = wx.GridSizer( 0, 1, 0, 0 )

        sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self.imagePanel, wx.ID_ANY, u"导入图片-预览图" ), wx.VERTICAL )

        self.importedImagePlanel = wx.Panel( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer261 = wx.BoxSizer( wx.VERTICAL )

        self.importedImage = wx.StaticBitmap( self.importedImagePlanel, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer261.Add( self.importedImage, 1, wx.ALL|wx.EXPAND, 0 )


        self.importedImagePlanel.SetSizer( bSizer261 )
        self.importedImagePlanel.Layout()
        bSizer261.Fit( self.importedImagePlanel )
        sbSizer2.Add( self.importedImagePlanel, 1, wx.EXPAND |wx.ALL, 5 )


        gSizer1.Add( sbSizer2, 1, wx.EXPAND, 5 )

        sbSizer3 = wx.StaticBoxSizer( wx.StaticBox( self.imagePanel, wx.ID_ANY, u"处理结果-预览图" ), wx.VERTICAL )

        self.previewedImagePlanel = wx.Panel( sbSizer3.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer27 = wx.BoxSizer( wx.VERTICAL )

        self.previewedImage = wx.StaticBitmap( self.previewedImagePlanel, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer27.Add( self.previewedImage, 1, wx.ALL|wx.EXPAND, 0 )


        self.previewedImagePlanel.SetSizer( bSizer27 )
        self.previewedImagePlanel.Layout()
        bSizer27.Fit( self.previewedImagePlanel )
        sbSizer3.Add( self.previewedImagePlanel, 1, wx.EXPAND |wx.ALL, 5 )


        gSizer1.Add( sbSizer3, 1, wx.EXPAND, 5 )


        self.imagePanel.SetSizer( gSizer1 )
        self.imagePanel.Layout()
        gSizer1.Fit( self.imagePanel )
        bSizer26.Add( self.imagePanel, 2, wx.ALL|wx.EXPAND, 2 )


        self.SetSizer( bSizer26 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.Bind( wx.EVT_CLOSE, self.exit )
        self.Bind( wx.EVT_MOVE_END, self.refresh_preview )
        self.Bind( wx.EVT_SIZE, self.resize_image )
        self.Bind( wx.EVT_MENU, self.load_file, id = self.loadFileMenuItem.GetId() )
        self.Bind( wx.EVT_MENU, self.load_dir, id = self.m_menuItem51.GetId() )
        self.Bind( wx.EVT_MENU, self.save_image, id = self.m_menuItem5.GetId() )
        self.Bind( wx.EVT_MENU, self.exit, id = self.m_menuItem4.GetId() )
        self.imageTreeCtrl.Bind( wx.EVT_TREE_SEL_CHANGED, self.switch_image )
        self.m_button8.Bind( wx.EVT_BUTTON, self.set_stop_loading_signal )
        self.stopLoadingBtn.Bind( wx.EVT_BUTTON, self.stop_loading )
        self.m_button5.Bind( wx.EVT_BUTTON, self.load_file )
        self.m_button6.Bind( wx.EVT_BUTTON, self.load_dir )
        self.mode.Bind( wx.EVT_RADIOBOX, self.processing_mode_change )
        self.row.Bind( wx.EVT_SPINCTRL, self.refresh_preview )
        self.row.Bind( wx.EVT_TEXT_ENTER, self.refresh_preview )
        self.col.Bind( wx.EVT_SPINCTRL, self.refresh_preview )
        self.col.Bind( wx.EVT_TEXT_ENTER, self.refresh_preview )
        self.upset.Bind( wx.EVT_CHECKBOX, self.refresh_preview )
        self.flip.Bind( wx.EVT_CHECKBOX, self.refresh_preview )
        self.rgbMapping.Bind( wx.EVT_CHECKBOX, self.refresh_preview )
        self.xorRgb.Bind( wx.EVT_RADIOBOX, self.refresh_preview )
        self.password.Bind( wx.EVT_TEXT_ENTER, self.update_password_dict )
        self.previewMode.Bind( wx.EVT_RADIOBOX, self.preview_mode_change )
        self.m_button31.Bind( wx.EVT_BUTTON, self.apply_settings_to_all )
        self.m_button311.Bind( wx.EVT_BUTTON, self.set_settings_as_default )
        self.m_button3.Bind( wx.EVT_BUTTON, self.manual_refresh )
        self.m_button7.Bind( wx.EVT_BUTTON, self.save_image )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def exit( self, event ):
        event.Skip()

    def refresh_preview( self, event ):
        event.Skip()

    def resize_image( self, event ):
        event.Skip()

    def load_file( self, event ):
        event.Skip()

    def load_dir( self, event ):
        event.Skip()

    def save_image( self, event ):
        event.Skip()


    def switch_image( self, event ):
        event.Skip()

    def set_stop_loading_signal( self, event ):
        event.Skip()

    def stop_loading( self, event ):
        event.Skip()



    def processing_mode_change( self, event ):
        event.Skip()









    def update_password_dict( self, event ):
        event.Skip()

    def preview_mode_change( self, event ):
        event.Skip()

    def apply_settings_to_all( self, event ):
        event.Skip()

    def set_settings_as_default( self, event ):
        event.Skip()

    def manual_refresh( self, event ):
        event.Skip()



###########################################################################
## Class AboutFrame
###########################################################################

class AboutFrame ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"关于", pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.Size( 500,300 ), wx.Size( 500,300 ) )
        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

        bSizer57 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel12 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.m_panel12.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

        bSizer58 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText17 = wx.StaticText( self.m_panel12, wx.ID_ANY, u"Image encryptor 1.0.0-beta.1\n", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText17.Wrap( -1 )

        self.m_staticText17.SetFont( wx.Font( 20, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        bSizer58.Add( self.m_staticText17, 0, wx.ALIGN_CENTER|wx.ALL, 20 )

        self.m_staticText18 = wx.StaticText( self.m_panel12, wx.ID_ANY, u"GUI版正在开发中", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText18.Wrap( -1 )

        self.m_staticText18.SetFont( wx.Font( 20, wx.FONTFAMILY_DECORATIVE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer58.Add( self.m_staticText18, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


        self.m_panel12.SetSizer( bSizer58 )
        self.m_panel12.Layout()
        bSizer58.Fit( self.m_panel12 )
        bSizer57.Add( self.m_panel12, 1, wx.EXPAND |wx.ALL, 5 )


        self.SetSizer( bSizer57 )
        self.Layout()

        self.Centre( wx.BOTH )

    def __del__( self ):
        pass


