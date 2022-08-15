# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-df7791b)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class ProcSettingsPanel
###########################################################################

class ProcSettingsPanel ( wx.Panel ):

    def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
        wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText62 = wx.StaticText( self, wx.ID_ANY, u"当前模式处于测试阶段，性能较低", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText62.Wrap( -1 )

        self.m_staticText62.SetForegroundColour( wx.Colour( 255, 0, 0 ) )

        bSizer1.Add( self.m_staticText62, 0, wx.ALIGN_CENTER, 2 )

        self.outsideImage = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"选择表图", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE|wx.FLP_FILE_MUST_EXIST )
        bSizer1.Add( self.outsideImage, 0, wx.ALL|wx.EXPAND, 2 )

        bSizer5 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer6 = wx.BoxSizer( wx.VERTICAL )

        bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

        resizeMethodChoices = [ u"拉伸以填充", u"缩放以适应" ]
        self.resizeMethod = wx.RadioBox( self, wx.ID_ANY, u"统一图像大小的方式", wx.DefaultPosition, wx.DefaultSize, resizeMethodChoices, 1, wx.RA_SPECIFY_ROWS )
        self.resizeMethod.SetSelection( 1 )
        bSizer2.Add( self.resizeMethod, 1, wx.EXPAND, 2 )

        self.toggleBg = wx.ToggleButton( self, wx.ID_ANY, u"切换至\n黑底预览", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.toggleBg.SetToolTip( u"切换背景颜色以查看表图与里图的显示效果\n注意：该设置为当前模式的全局设置" )

        bSizer2.Add( self.toggleBg, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2 )


        bSizer6.Add( bSizer2, 0, wx.EXPAND, 5 )

        fgSizer1 = wx.FlexGridSizer( 0, 3, 0, 0 )
        fgSizer1.SetFlexibleDirection( wx.BOTH )
        fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )


        fgSizer1.Add( ( 0, 0), 0, 0, 5 )

        self.m_staticText8 = wx.StaticText( self, wx.ID_ANY, u"表图", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText8.Wrap( -1 )

        fgSizer1.Add( self.m_staticText8, 0, wx.ALIGN_CENTER_HORIZONTAL, 2 )

        self.m_staticText9 = wx.StaticText( self, wx.ID_ANY, u"里图", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText9.Wrap( -1 )

        fgSizer1.Add( self.m_staticText9, 0, wx.ALIGN_CENTER_HORIZONTAL, 2 )

        self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, u"亮度百分比", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText6.Wrap( -1 )

        fgSizer1.Add( self.m_staticText6, 0, wx.ALIGN_CENTER, 5 )

        self.outsideBrightnessScale = wx.SpinCtrlDouble( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.SP_ARROW_KEYS|wx.TE_PROCESS_ENTER, 0, 100, 100, 5 )
        self.outsideBrightnessScale.SetDigits( 1 )
        fgSizer1.Add( self.outsideBrightnessScale, 0, wx.ALL, 1 )

        self.insideBrightnessScale = wx.SpinCtrlDouble( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.SP_ARROW_KEYS|wx.TE_PROCESS_ENTER, 0, 100, 18, 5 )
        self.insideBrightnessScale.SetDigits( 1 )
        fgSizer1.Add( self.insideBrightnessScale, 0, wx.ALL, 1 )

        self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"色彩百分比", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText7.Wrap( -1 )

        fgSizer1.Add( self.m_staticText7, 0, wx.ALIGN_CENTER, 5 )

        self.outsideColorScale = wx.SpinCtrlDouble( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.SP_ARROW_KEYS|wx.TE_PROCESS_ENTER, 0, 100, 50, 5 )
        self.outsideColorScale.SetDigits( 1 )
        fgSizer1.Add( self.outsideColorScale, 0, wx.ALL, 1 )

        self.insideColorScale = wx.SpinCtrlDouble( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.SP_ARROW_KEYS|wx.TE_PROCESS_ENTER, 0, 100, 70, 5 )
        self.insideColorScale.SetDigits( 1 )
        fgSizer1.Add( self.insideColorScale, 0, wx.ALL, 1 )

        self.m_staticText61 = wx.StaticText( self, wx.ID_ANY, u"额外处理", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText61.Wrap( -1 )

        fgSizer1.Add( self.m_staticText61, 0, wx.ALIGN_CENTER, 5 )

        self.damierMode = wx.CheckBox( self, wx.ID_ANY, u"棋盘格渲染", wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer1.Add( self.damierMode, 0, 0, 2 )

        self.colorfulMode = wx.CheckBox( self, wx.ID_ANY, u"彩色模式", wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer1.Add( self.colorfulMode, 0, 0, 2 )


        bSizer6.Add( fgSizer1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2 )


        bSizer5.Add( bSizer6, 0, wx.EXPAND, 5 )

        accuracyChoices = [ u"低", u"中", u"高" ]
        self.accuracy = wx.RadioBox( self, wx.ID_ANY, u"计算精度", wx.DefaultPosition, wx.DefaultSize, accuracyChoices, 1, wx.RA_SPECIFY_COLS )
        self.accuracy.SetSelection( 1 )
        self.accuracy.SetToolTip( u"低 - float16\n中 - float32 (C.float)\n高 - float64 (C.double)\n\n由于使用浮点数计算，所以计算精度还将影响计算的速度、内存占用\n\n如何选择？\n请结合RAM性能与CPU性能进行选择。float64意味着更多的内存占用与读写量，CPU计算量也会增大；而float16虽然应该有更小的内存与CPU占用，但大部分消费级CPU并不支持float16硬件加速(一般是转换为float32进行计算)，导致性能低下。一般情况下使用float32性能最佳。" )

        bSizer5.Add( self.accuracy, 0, wx.ALL|wx.EXPAND, 5 )


        bSizer1.Add( bSizer5, 0, wx.EXPAND, 5 )


        self.SetSizer( bSizer1 )
        self.Layout()
        bSizer1.Fit( self )

        # Connect Events
        self.outsideImage.Bind( wx.EVT_FILEPICKER_CHANGED, self.settings_changed )
        self.resizeMethod.Bind( wx.EVT_RADIOBOX, self.settings_changed )
        self.toggleBg.Bind( wx.EVT_TOGGLEBUTTON, self.toggle_bg )
        self.outsideBrightnessScale.Bind( wx.EVT_SPINCTRLDOUBLE, self.settings_changed )
        self.outsideBrightnessScale.Bind( wx.EVT_TEXT_ENTER, self.settings_changed )
        self.insideBrightnessScale.Bind( wx.EVT_SPINCTRLDOUBLE, self.settings_changed )
        self.insideBrightnessScale.Bind( wx.EVT_TEXT_ENTER, self.settings_changed )
        self.outsideColorScale.Bind( wx.EVT_SPINCTRLDOUBLE, self.settings_changed )
        self.outsideColorScale.Bind( wx.EVT_TEXT_ENTER, self.settings_changed )
        self.insideColorScale.Bind( wx.EVT_SPINCTRLDOUBLE, self.settings_changed )
        self.insideColorScale.Bind( wx.EVT_TEXT_ENTER, self.settings_changed )
        self.damierMode.Bind( wx.EVT_CHECKBOX, self.settings_changed )
        self.colorfulMode.Bind( wx.EVT_CHECKBOX, self.toggle_colorful_mode )
        self.accuracy.Bind( wx.EVT_RADIOBOX, self.settings_changed )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def settings_changed( self, event ):
        event.Skip()


    def toggle_bg( self, event ):
        event.Skip()










    def toggle_colorful_mode( self, event ):
        event.Skip()



