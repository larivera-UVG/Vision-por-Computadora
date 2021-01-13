#############################################################################
# Makefile for building: TomaPose_Robots.app/Contents/MacOS/TomaPose_Robots
# Generated by qmake (3.1) (Qt 5.15.1)
# Project:  TomaPose_Robots.pro
# Template: app
# Command: /usr/local/bin/qmake -o TomaPose_Robots.xcodeproj/project.pbxproj TomaPose_Robots.pro -spec macx-xcode
#############################################################################

MAKEFILE      = project.pbxproj

EQ            = =

MOC       = /usr/local/Cellar/qt/5.15.1/bin/moc
UIC       = /usr/local/Cellar/qt/5.15.1/bin/uic
LEX       = flex
LEXFLAGS  = 
YACC      = yacc
YACCFLAGS = -d
DEFINES       = -DQT_DEPRECATED_WARNINGS -DQT_NO_DEBUG -DQT_WIDGETS_LIB -DQT_GUI_LIB -DQT_CORE_LIB
INCPATH       = -I. -I/usr/local/include/opencv -I/usr/local/include -I/usr/local/Cellar/qt/5.15.1/lib/QtWidgets.framework/Headers -I/usr/local/Cellar/qt/5.15.1/lib/QtGui.framework/Headers -I/usr/local/Cellar/qt/5.15.1/lib/QtCore.framework/Headers -I. -I/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.15.sdk/System/Library/Frameworks/OpenGL.framework/Headers -I/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.15.sdk/System/Library/Frameworks/AGL.framework/Headers -I. -I/usr/local/Cellar/qt/5.15.1/mkspecs/macx-clang -F/usr/local/Cellar/qt/5.15.1/lib
DEL_FILE  = rm -f
MOVE      = mv -f

preprocess: compilers
clean preprocess_clean: compiler_clean

mocclean: compiler_moc_header_clean compiler_moc_objc_header_clean compiler_moc_source_clean

mocables: compiler_moc_header_make_all compiler_moc_objc_header_make_all compiler_moc_source_make_all

check: first

benchmark: first

compilers: moc_predefs.h moc_mainwindow.cpp ui_mainwindow.h
compiler_rcc_make_all:
compiler_rcc_clean:
compiler_moc_predefs_make_all: moc_predefs.h
compiler_moc_predefs_clean:
	-$(DEL_FILE) moc_predefs.h
moc_predefs.h: /usr/local/Cellar/qt/5.15.1/mkspecs/features/data/dummy.cpp
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/clang++ -pipe -stdlib=libc++ -O2 -std=gnu++11 -Wall -Wextra -dM -E -o moc_predefs.h /usr/local/Cellar/qt/5.15.1/mkspecs/features/data/dummy.cpp

compiler_moc_header_make_all: moc_mainwindow.cpp
compiler_moc_header_clean:
	-$(DEL_FILE) moc_mainwindow.cpp
moc_mainwindow.cpp: mainwindow.h \
		/usr/local/Cellar/qt/5.15.1/lib/QtWidgets.framework/Headers/QMainWindow \
		/usr/local/Cellar/qt/5.15.1/lib/QtWidgets.framework/Headers/qmainwindow.h \
		/usr/local/include/QtWidgets/qtwidgetsglobal.h \
		/usr/local/include/QtGui/qtguiglobal.h \
		/usr/local/include/QtCore/qglobal.h \
		/usr/local/include/QtCore/qconfig-bootstrapped.h \
		/usr/local/include/QtCore/qconfig.h \
		/usr/local/include/QtCore/qtcore-config.h \
		/usr/local/include/QtCore/qsystemdetection.h \
		/usr/local/include/QtCore/qprocessordetection.h \
		/usr/local/include/QtCore/qcompilerdetection.h \
		/usr/local/include/QtCore/qtypeinfo.h \
		/usr/local/include/QtCore/qsysinfo.h \
		/usr/local/include/QtCore/qlogging.h \
		/usr/local/include/QtCore/qflags.h \
		/usr/local/include/QtCore/qatomic.h \
		/usr/local/include/QtCore/qbasicatomic.h \
		/usr/local/include/QtCore/qatomic_bootstrap.h \
		/usr/local/include/QtCore/qgenericatomic.h \
		/usr/local/include/QtCore/qatomic_cxx11.h \
		/usr/local/include/QtCore/qatomic_msvc.h \
		/usr/local/include/QtCore/qglobalstatic.h \
		/usr/local/include/QtCore/qmutex.h \
		/usr/local/include/QtCore/qnumeric.h \
		/usr/local/include/QtCore/qversiontagging.h \
		/usr/local/include/QtGui/qtgui-config.h \
		/usr/local/include/QtWidgets/qtwidgets-config.h \
		/usr/local/include/QtWidgets/qwidget.h \
		/usr/local/include/QtGui/qwindowdefs.h \
		/usr/local/include/QtCore/qobjectdefs.h \
		/usr/local/include/QtCore/qnamespace.h \
		/usr/local/include/QtCore/qobjectdefs_impl.h \
		/usr/local/include/QtGui/qwindowdefs_win.h \
		/usr/local/include/QtCore/qobject.h \
		/usr/local/include/QtCore/qstring.h \
		/usr/local/include/QtCore/qchar.h \
		/usr/local/include/QtCore/qbytearray.h \
		/usr/local/include/QtCore/qrefcount.h \
		/usr/local/include/QtCore/qarraydata.h \
		/usr/local/include/QtCore/qstringliteral.h \
		/usr/local/include/QtCore/qstringalgorithms.h \
		/usr/local/include/QtCore/qstringview.h \
		/usr/local/include/QtCore/qstringbuilder.h \
		/usr/local/include/QtCore/qlist.h \
		/usr/local/include/QtCore/qalgorithms.h \
		/usr/local/include/QtCore/qiterator.h \
		/usr/local/include/QtCore/qhashfunctions.h \
		/usr/local/include/QtCore/qpair.h \
		/usr/local/include/QtCore/qvector.h \
		/usr/local/include/QtCore/qcontainertools_impl.h \
		/usr/local/include/QtCore/qpoint.h \
		/usr/local/include/QtCore/qbytearraylist.h \
		/usr/local/include/QtCore/qstringlist.h \
		/usr/local/include/QtCore/qregexp.h \
		/usr/local/include/QtCore/qstringmatcher.h \
		/usr/local/include/QtCore/qcoreevent.h \
		/usr/local/include/QtCore/qscopedpointer.h \
		/usr/local/include/QtCore/qmetatype.h \
		/usr/local/include/QtCore/qvarlengtharray.h \
		/usr/local/include/QtCore/qcontainerfwd.h \
		/usr/local/include/QtCore/qobject_impl.h \
		/usr/local/include/QtCore/qmargins.h \
		/usr/local/include/QtGui/qpaintdevice.h \
		/usr/local/include/QtCore/qrect.h \
		/usr/local/include/QtCore/qsize.h \
		/usr/local/include/QtGui/qpalette.h \
		/usr/local/include/QtGui/qcolor.h \
		/usr/local/include/QtGui/qrgb.h \
		/usr/local/include/QtGui/qrgba64.h \
		/usr/local/include/QtGui/qbrush.h \
		/usr/local/include/QtGui/qmatrix.h \
		/usr/local/include/QtGui/qpolygon.h \
		/usr/local/include/QtGui/qregion.h \
		/usr/local/include/QtCore/qdatastream.h \
		/usr/local/include/QtCore/qiodevice.h \
		/usr/local/include/QtCore/qline.h \
		/usr/local/include/QtGui/qtransform.h \
		/usr/local/include/QtGui/qimage.h \
		/usr/local/include/QtGui/qpixelformat.h \
		/usr/local/include/QtGui/qpixmap.h \
		/usr/local/include/QtCore/qsharedpointer.h \
		/usr/local/include/QtCore/qshareddata.h \
		/usr/local/include/QtCore/qhash.h \
		/usr/local/include/QtCore/qsharedpointer_impl.h \
		/usr/local/include/QtGui/qfont.h \
		/usr/local/include/QtGui/qfontmetrics.h \
		/usr/local/include/QtGui/qfontinfo.h \
		/usr/local/include/QtWidgets/qsizepolicy.h \
		/usr/local/include/QtGui/qcursor.h \
		/usr/local/include/QtGui/qkeysequence.h \
		/usr/local/include/QtGui/qevent.h \
		/usr/local/include/QtCore/qvariant.h \
		/usr/local/include/QtCore/qmap.h \
		/usr/local/include/QtCore/qdebug.h \
		/usr/local/include/QtCore/qtextstream.h \
		/usr/local/include/QtCore/qlocale.h \
		/usr/local/include/QtCore/qset.h \
		/usr/local/include/QtCore/qcontiguouscache.h \
		/usr/local/include/QtCore/qurl.h \
		/usr/local/include/QtCore/qurlquery.h \
		/usr/local/include/QtCore/qfile.h \
		/usr/local/include/QtCore/qfiledevice.h \
		/usr/local/include/QtGui/qvector2d.h \
		/usr/local/include/QtGui/qtouchdevice.h \
		/usr/local/include/QtWidgets/qtabwidget.h \
		/usr/local/include/QtGui/qicon.h \
		/usr/local/Cellar/qt/5.15.1/lib/QtWidgets.framework/Headers/QFileDialog \
		/usr/local/Cellar/qt/5.15.1/lib/QtWidgets.framework/Headers/qfiledialog.h \
		/usr/local/include/QtCore/qdir.h \
		/usr/local/include/QtCore/qfileinfo.h \
		/usr/local/include/QtWidgets/qdialog.h \
		/usr/local/Cellar/qt/5.15.1/lib/QtCore.framework/Headers/QDir \
		/usr/local/Cellar/qt/5.15.1/lib/QtCore.framework/Headers/qdir.h \
		/usr/local/Cellar/qt/5.15.1/lib/QtCore.framework/Headers/QFile \
		/usr/local/Cellar/qt/5.15.1/lib/QtCore.framework/Headers/qfile.h \
		/usr/local/Cellar/qt/5.15.1/lib/QtGui.framework/Headers/QCloseEvent \
		/usr/local/Cellar/qt/5.15.1/lib/QtGui.framework/Headers/qevent.h \
		/usr/local/Cellar/qt/5.15.1/lib/QtWidgets.framework/Headers/QMessageBox \
		/usr/local/Cellar/qt/5.15.1/lib/QtWidgets.framework/Headers/qmessagebox.h \
		/usr/local/Cellar/qt/5.15.1/lib/QtCore.framework/Headers/QSettings \
		/usr/local/Cellar/qt/5.15.1/lib/QtCore.framework/Headers/qsettings.h \
		moc_predefs.h \
		/usr/local/Cellar/qt/5.15.1/bin/moc
	/usr/local/Cellar/qt/5.15.1/bin/moc $(DEFINES) --include /Users/joseguerra/Desktop/Toma2/moc_predefs.h -I/usr/local/Cellar/qt/5.15.1/mkspecs/macx-clang -I/Users/joseguerra/Desktop/Toma2 -I/usr/local/include/opencv -I/usr/local/include -I/usr/local/Cellar/qt/5.15.1/lib/QtWidgets.framework/Headers -I/usr/local/Cellar/qt/5.15.1/lib/QtGui.framework/Headers -I/usr/local/Cellar/qt/5.15.1/lib/QtCore.framework/Headers -I/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/include/c++/v1 -I/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/clang/12.0.0/include -I/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.15.sdk/usr/include -I/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/include -F/usr/local/Cellar/qt/5.15.1/lib mainwindow.h -o moc_mainwindow.cpp

compiler_moc_objc_header_make_all:
compiler_moc_objc_header_clean:
compiler_moc_source_make_all:
compiler_moc_source_clean:
compiler_uic_make_all: ui_mainwindow.h
compiler_uic_clean:
	-$(DEL_FILE) ui_mainwindow.h
ui_mainwindow.h: mainwindow.ui \
		/usr/local/Cellar/qt/5.15.1/bin/uic
	/usr/local/Cellar/qt/5.15.1/bin/uic mainwindow.ui -o ui_mainwindow.h

compiler_rez_source_make_all:
compiler_rez_source_clean:
compiler_yacc_decl_make_all:
compiler_yacc_decl_clean:
compiler_yacc_impl_make_all:
compiler_yacc_impl_clean:
compiler_lex_make_all:
compiler_lex_clean:
compiler_clean: compiler_moc_predefs_clean compiler_moc_header_clean compiler_uic_clean 

