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
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Image Encryptor 1.0.0 -alpha.4", pos = wx.DefaultPosition, size = wx.Size( 915,640 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.Size( 400,640 ), wx.DefaultSize )
        self.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHTTEXT ) )
        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

        self.m_menubar1 = wx.MenuBar( 0 )
        self.m_menu1 = wx.Menu()
        self.loadFileMenuItem = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"载入文件", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu1.Append( self.loadFileMenuItem )

        self.m_menuItem5 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"保存", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu1.Append( self.m_menuItem5 )

        self.m_menubar1.Append( self.m_menu1, u"文件(File)" )

        self.m_menu2 = wx.Menu()
        self.aboutMenuItem = wx.MenuItem( self.m_menu2, wx.ID_ANY, u"关于", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu2.Append( self.aboutMenuItem )

        self.m_menuItem4 = wx.MenuItem( self.m_menu2, wx.ID_ANY, u"退出", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu2.Append( self.m_menuItem4 )

        self.m_menubar1.Append( self.m_menu2, u"关于(About)" )

        self.SetMenuBar( self.m_menubar1 )

        bSizer26 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer10 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel3 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer91 = wx.BoxSizer( wx.HORIZONTAL )

        self.selectFile = wx.FilePickerCtrl( self.m_panel3, wx.ID_ANY, wx.EmptyString, u"选择图像", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
        bSizer91.Add( self.selectFile, 0, wx.ALL, 5 )

        self.imageInfo = wx.StaticText( self.m_panel3, wx.ID_ANY, u"图像信息：未载入图片", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.imageInfo.Wrap( -1 )

        self.imageInfo.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )

        bSizer91.Add( self.imageInfo, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


        self.m_panel3.SetSizer( bSizer91 )
        self.m_panel3.Layout()
        bSizer91.Fit( self.m_panel3 )
        bSizer10.Add( self.m_panel3, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticline3 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer10.Add( self.m_staticline3, 0, wx.EXPAND |wx.ALL, 5 )

        self.processingOptions = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.processingOptions.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

        bSizer11 = wx.BoxSizer( wx.VERTICAL )

        bSizer12 = wx.BoxSizer( wx.HORIZONTAL )

        modeChoices = [ u"加密模式", u"解密模式", u"QQ反屏蔽" ]
        self.mode = wx.RadioBox( self.processingOptions, wx.ID_ANY, u"处理模式", wx.DefaultPosition, wx.DefaultSize, modeChoices, 1, wx.RA_SPECIFY_COLS )
        self.mode.SetSelection( 0 )
        bSizer12.Add( self.mode, 0, wx.ALL|wx.EXPAND, 5 )

        bSizer13 = wx.BoxSizer( wx.VERTICAL )

        bSizer131 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText8 = wx.StaticText( self.processingOptions, wx.ID_ANY, u"切割行数", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText8.Wrap( -1 )

        self.m_staticText8.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )

        bSizer131.Add( self.m_staticText8, 0, wx.ALL, 5 )

        self.row = wx.SpinCtrl( self.processingOptions, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.SP_ARROW_KEYS|wx.TE_PROCESS_ENTER, 1, 100000000, 25 )
        bSizer131.Add( self.row, 0, wx.ALL|wx.EXPAND, 5 )


        bSizer13.Add( bSizer131, 1, wx.EXPAND, 5 )

        bSizer15 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText9 = wx.StaticText( self.processingOptions, wx.ID_ANY, u"切割列数", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText9.Wrap( -1 )

        bSizer15.Add( self.m_staticText9, 0, wx.ALL, 5 )

        self.col = wx.SpinCtrl( self.processingOptions, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.SP_ARROW_KEYS|wx.TE_PROCESS_ENTER, 1, 100000000, 25 )
        bSizer15.Add( self.col, 0, wx.ALL|wx.EXPAND, 5 )


        bSizer13.Add( bSizer15, 1, wx.EXPAND, 5 )

        self.normalEncryption = wx.CheckBox( self.processingOptions, wx.ID_ANY, u"常规加密", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.normalEncryption.SetValue(True)
        self.normalEncryption.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )

        bSizer13.Add( self.normalEncryption, 0, wx.ALL, 5 )

        self.rgbMapping = wx.CheckBox( self.processingOptions, wx.ID_ANY, u"RGB映射", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer13.Add( self.rgbMapping, 0, wx.ALL, 5 )


        bSizer12.Add( bSizer13, 0, 0, 5 )

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


        bSizer12.Add( bSizer17, 1, wx.EXPAND, 5 )


        bSizer11.Add( bSizer12, 0, wx.EXPAND, 5 )

        bSizer9 = wx.BoxSizer( wx.HORIZONTAL )

        self.previewOptions = wx.Panel( self.processingOptions, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.previewOptions.Enable( False )

        bSizer19 = wx.BoxSizer( wx.VERTICAL )

        previewModeChoices = [ u"不显示", u"手动刷新", u"自动刷新" ]
        self.previewMode = wx.RadioBox( self.previewOptions, wx.ID_ANY, u"预览图", wx.DefaultPosition, wx.DefaultSize, previewModeChoices, 1, wx.RA_SPECIFY_COLS )
        self.previewMode.SetSelection( 1 )
        bSizer19.Add( self.previewMode, 0, wx.ALL, 5 )

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
        bSizer9.Add( self.previewOptions, 0, wx.EXPAND |wx.ALL, 5 )

        sbSizer6 = wx.StaticBoxSizer( wx.StaticBox( self.processingOptions, wx.ID_ANY, u"高级设置" ), wx.VERTICAL )

        bSizer1311 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText82 = wx.StaticText( sbSizer6.GetStaticBox(), wx.ID_ANY, u"允许载入最大像素量", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText82.Wrap( -1 )

        self.m_staticText82.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
        self.m_staticText82.SetToolTip( u"允许载入的最大图片像素量，0为禁用(谨防DOS压缩炸弹图片)" )

        bSizer1311.Add( self.m_staticText82, 0, wx.ALL, 5 )

        self.maxImagePixels = wx.SpinCtrl( sbSizer6.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.SP_ARROW_KEYS|wx.TE_PROCESS_ENTER, 0, 1000000000, 89478485 )
        self.maxImagePixels.SetToolTip( u"允许载入的最大图片像素量，0为禁用(谨防DOS压缩炸弹图片)" )

        bSizer1311.Add( self.maxImagePixels, 0, wx.ALL|wx.EXPAND, 0 )


        sbSizer6.Add( bSizer1311, 0, wx.ALL|wx.EXPAND, 0 )

        bSizer1312 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText821 = wx.StaticText( sbSizer6.GetStaticBox(), wx.ID_ANY, u"有损格式保存质量", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText821.Wrap( -1 )

        self.m_staticText821.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
        self.m_staticText821.SetToolTip( u"(1-100)保存为有损格式时，值越大保存的文件越大，质量越好" )

        bSizer1312.Add( self.m_staticText821, 0, wx.ALL, 5 )

        self.saveQuality = wx.SpinCtrl( sbSizer6.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.SP_ARROW_KEYS|wx.TE_PROCESS_ENTER, 1, 100, 95 )
        self.saveQuality.SetToolTip( u"(1-100)保存为有损格式时，值越大保存的文件越大，质量越好" )

        bSizer1312.Add( self.saveQuality, 1, wx.ALL|wx.EXPAND, 0 )


        sbSizer6.Add( bSizer1312, 0, wx.EXPAND, 5 )

        bSizer13121 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText8211 = wx.StaticText( sbSizer6.GetStaticBox(), wx.ID_ANY, u"有损格式色度抽样等级", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText8211.Wrap( -1 )

        self.m_staticText8211.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
        self.m_staticText8211.SetToolTip( u"(0-2) 0表示不使用，等级越高，保存有损格式时获得的文件大小越小，但会导致图片出现噪点，使图片解密后失真" )

        bSizer13121.Add( self.m_staticText8211, 0, wx.ALL, 5 )

        self.subsamplingLevel = wx.SpinCtrl( sbSizer6.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.SP_ARROW_KEYS|wx.TE_PROCESS_ENTER, 0, 2, 0 )
        self.subsamplingLevel.SetToolTip( u"(0-2) 0表示不使用，等级越高，保存有损格式时获得的文件大小越小，但会导致图片出现噪点，使图片解密后失真" )

        bSizer13121.Add( self.subsamplingLevel, 1, wx.ALL|wx.EXPAND, 0 )


        sbSizer6.Add( bSizer13121, 0, wx.EXPAND, 5 )


        bSizer9.Add( sbSizer6, 1, wx.ALL|wx.EXPAND, 0 )


        bSizer11.Add( bSizer9, 0, wx.EXPAND, 5 )


        self.processingOptions.SetSizer( bSizer11 )
        self.processingOptions.Layout()
        bSizer11.Fit( self.processingOptions )
        bSizer10.Add( self.processingOptions, 1, wx.EXPAND |wx.ALL, 5 )

        self.m_staticline21 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer10.Add( self.m_staticline21, 0, wx.EXPAND |wx.ALL, 5 )

        self.saveOptions = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.saveOptions.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        self.saveOptions.Enable( False )

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


        bSizer26.Add( bSizer10, 0, wx.EXPAND, 5 )

        self.m_staticline5 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
        bSizer26.Add( self.m_staticline5, 0, wx.EXPAND |wx.ALL, 5 )

        self.imagePanel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer3 = wx.BoxSizer( wx.VERTICAL )

        self.importedImagePanel = wx.ScrolledWindow( self.imagePanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
        self.importedImagePanel.SetScrollRate( 0, 0 )
        bSizer43 = wx.BoxSizer( wx.VERTICAL )

        self.importedImage = wx.StaticBitmap( self.importedImagePanel, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer43.Add( self.importedImage, 1, wx.ALL|wx.EXPAND, 0 )


        self.importedImagePanel.SetSizer( bSizer43 )
        self.importedImagePanel.Layout()
        bSizer43.Fit( self.importedImagePanel )
        bSizer3.Add( self.importedImagePanel, 1, wx.EXPAND |wx.ALL, 0 )

        self.imageStaticline = wx.StaticLine( self.imagePanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer3.Add( self.imageStaticline, 0, wx.EXPAND |wx.ALL, 5 )

        self.previewedImagePanel = wx.ScrolledWindow( self.imagePanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
        self.previewedImagePanel.SetScrollRate( 0, 1000 )
        bSizer44 = wx.BoxSizer( wx.VERTICAL )

        self.previewedImage = wx.StaticBitmap( self.previewedImagePanel, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer44.Add( self.previewedImage, 1, wx.ALL|wx.EXPAND, 0 )


        self.previewedImagePanel.SetSizer( bSizer44 )
        self.previewedImagePanel.Layout()
        bSizer44.Fit( self.previewedImagePanel )
        bSizer3.Add( self.previewedImagePanel, 1, wx.EXPAND |wx.ALL, 0 )


        self.imagePanel.SetSizer( bSizer3 )
        self.imagePanel.Layout()
        bSizer3.Fit( self.imagePanel )
        bSizer26.Add( self.imagePanel, 1, wx.EXPAND |wx.ALL, 5 )


        self.SetSizer( bSizer26 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.Bind( wx.EVT_CLOSE, self.exit )
        self.Bind( wx.EVT_MOVE_END, self.refresh_preview )
        self.Bind( wx.EVT_SIZE, self.resize_image )
        self.Bind( wx.EVT_MENU, self.load_file, id = self.loadFileMenuItem.GetId() )
        self.Bind( wx.EVT_MENU, self.save_image, id = self.m_menuItem5.GetId() )
        self.Bind( wx.EVT_MENU, self.exit, id = self.m_menuItem4.GetId() )
        self.selectFile.Bind( wx.EVT_FILEPICKER_CHANGED, self.load_select_file )
        self.mode.Bind( wx.EVT_RADIOBOX, self.refresh_preview )
        self.row.Bind( wx.EVT_SPINCTRL, self.refresh_preview )
        self.row.Bind( wx.EVT_TEXT_ENTER, self.refresh_preview )
        self.col.Bind( wx.EVT_SPINCTRL, self.refresh_preview )
        self.col.Bind( wx.EVT_TEXT_ENTER, self.refresh_preview )
        self.normalEncryption.Bind( wx.EVT_CHECKBOX, self.refresh_preview )
        self.rgbMapping.Bind( wx.EVT_CHECKBOX, self.refresh_preview )
        self.xorRgb.Bind( wx.EVT_RADIOBOX, self.refresh_preview )
        self.password.Bind( wx.EVT_TEXT_ENTER, self.update_password_dict )
        self.previewMode.Bind( wx.EVT_RADIOBOX, self.preview_mode_change )
        self.m_button3.Bind( wx.EVT_BUTTON, self.manual_refresh )
        self.maxImagePixels.Bind( wx.EVT_SPINCTRL, self.refresh_preview )
        self.maxImagePixels.Bind( wx.EVT_TEXT_ENTER, self.refresh_preview )
        self.saveQuality.Bind( wx.EVT_SPINCTRL, self.refresh_preview )
        self.saveQuality.Bind( wx.EVT_TEXT_ENTER, self.refresh_preview )
        self.subsamplingLevel.Bind( wx.EVT_SPINCTRL, self.refresh_preview )
        self.subsamplingLevel.Bind( wx.EVT_TEXT_ENTER, self.refresh_preview )
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

    def save_image( self, event ):
        event.Skip()


    def load_select_file( self, event ):
        event.Skip()









    def update_password_dict( self, event ):
        event.Skip()

    def preview_mode_change( self, event ):
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

        self.m_staticText17 = wx.StaticText( self.m_panel12, wx.ID_ANY, u"Image encryptor 1.0.0-alpha.4", wx.DefaultPosition, wx.DefaultSize, 0 )
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


