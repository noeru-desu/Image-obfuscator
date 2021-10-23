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
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Image Encryptor 1.0.0 alpha1", pos = wx.DefaultPosition, size = wx.Size( 1269,824 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.Size( 950,550 ), wx.DefaultSize )
        self.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHTTEXT ) )
        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

        gSizer7 = wx.GridSizer( 0, 2, 0, 0 )

        fgSizer6 = wx.FlexGridSizer( 0, 1, 0, 0 )
        fgSizer6.SetFlexibleDirection( wx.BOTH )
        fgSizer6.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.m_panel3 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        gSizer9 = wx.GridSizer( 0, 2, 0, 0 )

        self.selectFile = wx.FilePickerCtrl( self.m_panel3, wx.ID_ANY, wx.EmptyString, u"选择图像", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
        gSizer9.Add( self.selectFile, 0, wx.ALIGN_RIGHT|wx.ALL, 10 )

        self.imageInfo = wx.StaticText( self.m_panel3, wx.ID_ANY, u"图像信息：未载入图片", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.imageInfo.Wrap( -1 )

        self.imageInfo.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )

        gSizer9.Add( self.imageInfo, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


        self.m_panel3.SetSizer( gSizer9 )
        self.m_panel3.Layout()
        gSizer9.Fit( self.m_panel3 )
        fgSizer6.Add( self.m_panel3, 1, wx.EXPAND |wx.ALL, 5 )

        self.m_staticline3 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        fgSizer6.Add( self.m_staticline3, 0, wx.EXPAND |wx.ALL, 5 )

        self.processingOptions = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.processingOptions.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        self.processingOptions.Enable( False )

        gSizer10 = wx.GridSizer( 0, 5, 0, 0 )

        modeChoices = [ u"加密模式", u"解密模式", u"QQ反屏蔽" ]
        self.mode = wx.RadioBox( self.processingOptions, wx.ID_ANY, u"处理模式", wx.DefaultPosition, wx.DefaultSize, modeChoices, 1, wx.RA_SPECIFY_COLS )
        self.mode.SetSelection( 0 )
        gSizer10.Add( self.mode, 0, wx.ALIGN_RIGHT|wx.ALL|wx.EXPAND, 5 )

        bSizer8 = wx.BoxSizer( wx.VERTICAL )

        self.normalEncryption = wx.CheckBox( self.processingOptions, wx.ID_ANY, u"常规加密", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.normalEncryption.SetValue(True)
        self.normalEncryption.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )

        bSizer8.Add( self.normalEncryption, 0, wx.ALL, 5 )

        self.rgbMapping = wx.CheckBox( self.processingOptions, wx.ID_ANY, u"RGB映射", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer8.Add( self.rgbMapping, 0, wx.ALL, 5 )


        gSizer10.Add( bSizer8, 0, wx.ALL|wx.EXPAND, 5 )

        xorRgbChoices = [ u"不启用", u"RGB通道", u"RGBA通道" ]
        self.xorRgb = wx.RadioBox( self.processingOptions, wx.ID_ANY, u"异或加密", wx.DefaultPosition, wx.DefaultSize, xorRgbChoices, 1, wx.RA_SPECIFY_COLS )
        self.xorRgb.SetSelection( 0 )
        gSizer10.Add( self.xorRgb, 0, wx.ALL, 5 )

        bSizer13 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText8 = wx.StaticText( self.processingOptions, wx.ID_ANY, u"切割行数", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText8.Wrap( -1 )

        self.m_staticText8.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )

        bSizer13.Add( self.m_staticText8, 0, wx.ALL, 5 )

        self.row = wx.SpinCtrl( self.processingOptions, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.SP_ARROW_KEYS|wx.TE_PROCESS_ENTER, 1, 100000000, 25 )
        bSizer13.Add( self.row, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText9 = wx.StaticText( self.processingOptions, wx.ID_ANY, u"切割列数", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText9.Wrap( -1 )

        bSizer13.Add( self.m_staticText9, 0, wx.ALL, 5 )

        self.col = wx.SpinCtrl( self.processingOptions, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.SP_ARROW_KEYS|wx.TE_PROCESS_ENTER, 1, 100000000, 25 )
        bSizer13.Add( self.col, 0, wx.ALL|wx.EXPAND, 5 )


        gSizer10.Add( bSizer13, 1, wx.EXPAND, 5 )

        bSizer14 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText12 = wx.StaticText( self.processingOptions, wx.ID_ANY, u"添加密码到密码字典", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText12.Wrap( -1 )

        bSizer14.Add( self.m_staticText12, 0, wx.ALL, 5 )

        self.password = wx.TextCtrl( self.processingOptions, wx.ID_ANY, u"none", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        bSizer14.Add( self.password, 0, wx.ALL, 5 )

        self.m_staticText13 = wx.StaticText( self.processingOptions, wx.ID_ANY, u"进程池大小", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText13.Wrap( -1 )

        bSizer14.Add( self.m_staticText13, 0, wx.ALL, 5 )

        self.processPool = wx.SpinCtrl( self.processingOptions, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.SP_ARROW_KEYS|wx.TE_PROCESS_ENTER, 1, 10, 1 )
        bSizer14.Add( self.processPool, 0, wx.ALL, 5 )


        gSizer10.Add( bSizer14, 1, wx.EXPAND, 5 )

        bSizer18 = wx.BoxSizer( wx.VERTICAL )

        bSizer9 = wx.BoxSizer( wx.VERTICAL )

        previewModeChoices = [ u"不显示", u"手动刷新", u"自动刷新" ]
        self.previewMode = wx.RadioBox( self.processingOptions, wx.ID_ANY, u"预览图", wx.DefaultPosition, wx.DefaultSize, previewModeChoices, 1, wx.RA_SPECIFY_COLS )
        self.previewMode.SetSelection( 2 )
        bSizer9.Add( self.previewMode, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )

        self.m_button3 = wx.Button( self.processingOptions, wx.ID_ANY, u"刷新预览图", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer9.Add( self.m_button3, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )


        bSizer18.Add( bSizer9, 1, wx.EXPAND, 5 )


        gSizer10.Add( bSizer18, 1, wx.EXPAND, 5 )

        self.previewProgress = wx.Gauge( self.processingOptions, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL|wx.GA_SMOOTH )
        self.previewProgress.SetValue( 0 )
        gSizer10.Add( self.previewProgress, 0, wx.ALIGN_BOTTOM|wx.ALL|wx.EXPAND, 10 )

        self.previewProgressPrompt = wx.StaticText( self.processingOptions, wx.ID_ANY, u"等待载入图片", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.previewProgressPrompt.Wrap( -1 )

        gSizer10.Add( self.previewProgressPrompt, 0, wx.ALIGN_BOTTOM|wx.ALL, 10 )


        self.processingOptions.SetSizer( gSizer10 )
        self.processingOptions.Layout()
        gSizer10.Fit( self.processingOptions )
        fgSizer6.Add( self.processingOptions, 1, wx.EXPAND |wx.ALL, 5 )

        self.m_staticline21 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        fgSizer6.Add( self.m_staticline21, 0, wx.EXPAND |wx.ALL, 5 )

        self.saveOptions = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.saveOptions.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        self.saveOptions.Enable( False )

        gSizer101 = wx.GridSizer( 0, 1, 0, 0 )

        gSizer71 = wx.GridSizer( 0, 2, 0, 0 )

        self.m_staticText22 = wx.StaticText( self.saveOptions, wx.ID_ANY, u"保存格式", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText22.Wrap( -1 )

        self.m_staticText22.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )

        gSizer71.Add( self.m_staticText22, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

        selectFormatChoices = [ u"blp", u"bmp", u"dib", u"bufr", u"cur", u"pcx", u"dcx", u"dds", u"ps", u"eps", u"fit", u"fits", u"fli", u"flc", u"ftc", u"ftu", u"gbr", u"gif", u"grib", u"h5", u"hdf", u"png", u"apng", u"jp2", u"j2k", u"jpc", u"jpf", u"jpx", u"j2c", u"icns", u"ico", u"im", u"iim", u"tif", u"tiff", u"jfif", u"jpe", u"jpg", u"jpeg", u"mpg", u"mpeg", u"mpo", u"msp", u"palm", u"pcd", u"pdf", u"pxr", u"pbm", u"pgm", u"ppm", u"pnm", u"psd", u"bw", u"rgb", u"rgba", u"sgi", u"ras", u"tga", u"icb", u"vda", u"vst", u"webp", u"wmf", u"emf", u"xbm", u"xpm" ]
        self.selectFormat = wx.Choice( self.saveOptions, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, selectFormatChoices, 0 )
        self.selectFormat.SetSelection( 21 )
        gSizer71.Add( self.selectFormat, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 0 )


        gSizer101.Add( gSizer71, 1, wx.ALIGN_CENTER|wx.ALL, 5 )

        gSizer91 = wx.GridSizer( 0, 1, 0, 0 )

        self.m_staticText81 = wx.StaticText( self.saveOptions, wx.ID_ANY, u"保存位置", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText81.Wrap( -1 )

        gSizer91.Add( self.m_staticText81, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.selectSavePath = wx.DirPickerCtrl( self.saveOptions, wx.ID_ANY, wx.EmptyString, u"选择保存位置", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
        gSizer91.Add( self.selectSavePath, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.m_button7 = wx.Button( self.saveOptions, wx.ID_ANY, u"保存文件", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button7.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )

        gSizer91.Add( self.m_button7, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )


        gSizer101.Add( gSizer91, 1, wx.EXPAND, 5 )

        gSizer8 = wx.GridSizer( 0, 2, 0, 0 )

        self.saveProgressPrompt = wx.StaticText( self.saveOptions, wx.ID_ANY, u"进度", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.saveProgressPrompt.Wrap( -1 )

        gSizer8.Add( self.saveProgressPrompt, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )

        self.saveProgress = wx.Gauge( self.saveOptions, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL|wx.GA_SMOOTH )
        self.saveProgress.SetValue( 0 )
        gSizer8.Add( self.saveProgress, 0, wx.ALL, 5 )


        gSizer101.Add( gSizer8, 1, wx.ALIGN_RIGHT|wx.ALL, 5 )


        self.saveOptions.SetSizer( gSizer101 )
        self.saveOptions.Layout()
        gSizer101.Fit( self.saveOptions )
        fgSizer6.Add( self.saveOptions, 1, wx.EXPAND |wx.ALL, 5 )


        gSizer7.Add( fgSizer6, 1, wx.EXPAND, 5 )

        bSizer3 = wx.BoxSizer( wx.VERTICAL )

        self.importedImageScrolled = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
        self.importedImageScrolled.SetScrollRate( 0, 5 )
        bSizer28 = wx.BoxSizer( wx.VERTICAL )

        self.importedImage = wx.StaticBitmap( self.importedImageScrolled, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer28.Add( self.importedImage, 1, wx.ALL|wx.EXPAND, 5 )


        self.importedImageScrolled.SetSizer( bSizer28 )
        self.importedImageScrolled.Layout()
        bSizer28.Fit( self.importedImageScrolled )
        bSizer3.Add( self.importedImageScrolled, 1, wx.EXPAND |wx.ALL, 5 )

        self.m_staticline2 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer3.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )

        self.previewedImageScrolled = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
        self.previewedImageScrolled.SetScrollRate( 5, 5 )
        bSizer30 = wx.BoxSizer( wx.VERTICAL )

        self.previewedImage = wx.StaticBitmap( self.previewedImageScrolled, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer30.Add( self.previewedImage, 1, wx.ALL|wx.EXPAND, 5 )


        self.previewedImageScrolled.SetSizer( bSizer30 )
        self.previewedImageScrolled.Layout()
        bSizer30.Fit( self.previewedImageScrolled )
        bSizer3.Add( self.previewedImageScrolled, 1, wx.EXPAND |wx.ALL, 5 )


        gSizer7.Add( bSizer3, 1, wx.EXPAND, 5 )


        self.SetSizer( gSizer7 )
        self.Layout()
        self.m_menubar1 = wx.MenuBar( 0 )
        self.m_menu1 = wx.Menu()
        self.loadFileMenuItem = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"载入文件", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu1.Append( self.loadFileMenuItem )

        self.m_menubar1.Append( self.m_menu1, u"文件(File)" )

        self.m_menu2 = wx.Menu()
        self.aboutMenuItem = wx.MenuItem( self.m_menu2, wx.ID_ANY, u"关于", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu2.Append( self.aboutMenuItem )

        self.m_menubar1.Append( self.m_menu2, u"关于(About)" )

        self.SetMenuBar( self.m_menubar1 )


        self.Centre( wx.BOTH )

        # Connect Events
        self.Bind( wx.EVT_MAXIMIZE, self.refresh_preview )
        self.Bind( wx.EVT_MOVE_END, self.refresh_preview )
        self.selectFile.Bind( wx.EVT_FILEPICKER_CHANGED, self.load_select_file )
        self.mode.Bind( wx.EVT_RADIOBOX, self.refresh_preview )
        self.normalEncryption.Bind( wx.EVT_CHECKBOX, self.refresh_preview )
        self.rgbMapping.Bind( wx.EVT_CHECKBOX, self.refresh_preview )
        self.xorRgb.Bind( wx.EVT_RADIOBOX, self.refresh_preview )
        self.row.Bind( wx.EVT_SPINCTRL, self.refresh_preview )
        self.row.Bind( wx.EVT_TEXT_ENTER, self.refresh_preview )
        self.col.Bind( wx.EVT_SPINCTRL, self.refresh_preview )
        self.col.Bind( wx.EVT_TEXT_ENTER, self.refresh_preview )
        self.password.Bind( wx.EVT_TEXT_ENTER, self.update_password_dict )
        self.previewMode.Bind( wx.EVT_RADIOBOX, self.preview_mode_change )
        self.m_button3.Bind( wx.EVT_BUTTON, self.manual_refresh )
        self.m_button7.Bind( wx.EVT_BUTTON, self.save_image )
        self.Bind( wx.EVT_MENU, self.load_file, id = self.loadFileMenuItem.GetId() )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def refresh_preview( self, event ):
        event.Skip()


    def load_select_file( self, event ):
        event.Skip()









    def update_password_dict( self, event ):
        event.Skip()

    def preview_mode_change( self, event ):
        event.Skip()

    def manual_refresh( self, event ):
        event.Skip()

    def save_image( self, event ):
        event.Skip()

    def load_file( self, event ):
        event.Skip()


###########################################################################
## Class PasswordInputFrame
###########################################################################

class PasswordInputFrame ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"批量处理", pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        gSizer8 = wx.GridSizer( 0, 2, 0, 0 )


        self.SetSizer( gSizer8 )
        self.Layout()

        self.Centre( wx.BOTH )

    def __del__( self ):
        pass


