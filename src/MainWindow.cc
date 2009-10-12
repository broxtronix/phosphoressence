// __BEGIN_LICENSE__
// Copyright (C) 2009 Michael J. Broxton
// All Rights Reserved.
// __END_LICENSE__

/// \file MainWindow.cc
///
#include <pe_config.h>
#include <MainWindow.h>
#include <GraphicsEngine.h>

#include <vw/FileIO/DiskImageView.h>
#include <vw/Image/Statistics.h>
#include <vw/Image/PixelMask.h>

#include <QtGui>

#include <sstream>

MainWindow::MainWindow() {

  
  // Set the window title and add tabs
  std::string window_title = "Phosphor Essence v0.3";
  this->setWindowTitle(window_title.c_str());

  // Set up GraphicsEngine
  QGLFormat gl_frmt = QGLFormat::defaultFormat();
  gl_frmt.setSampleBuffers(true);
  gl_frmt.setDoubleBuffer(true);
  //  gl_frmt.setSamples(16);
  gl_frmt.setSwapInterval(0);
  m_graphics_engine = new GraphicsEngine(this, gl_frmt);
  setCentralWidget(m_graphics_engine);

  // Set up the basic layout of the window and its menus
  create_actions();
  // create_menus();

  // Maximize the main window
  //this->showMaximized();
  this->showFullScreen();
}

//********************************************************************
//                      MAIN WINDOW SETUP
//********************************************************************

void MainWindow::create_actions() {

  // The About Box
  about_action = new QAction(tr("About VWV"), this);
  about_action->setStatusTip(tr("Show the PhosphorEssence about box."));
  connect(about_action, SIGNAL(triggered()), this, SLOT(about()));

  // Exit or Quit
  exit_action = new QAction(tr("E&xit"), this);
  exit_action->setShortcut(tr("Ctrl+Q"));
  exit_action->setStatusTip(tr("Exit the application"));
  connect(exit_action, SIGNAL(triggered()), this, SLOT(close()));

  // A call to close from the inner OpenGLWidget
  connect(m_graphics_engine, SIGNAL(pe_quit()), this, SLOT(close()));
}

void MainWindow::create_menus() {
  
  // File Menu
  file_menu = menuBar()->addMenu(tr("&File"));
  file_menu->addAction(exit_action);

  // Edit Menu
  edit_menu = menuBar()->addMenu(tr("&Edit"));

  // Help menu
  menuBar()->addSeparator();
  help_menu = menuBar()->addMenu(tr("&Help"));
  help_menu->addAction(about_action);
}

void MainWindow::about() {
  std::ostringstream about_text;
  about_text << "<h3>PhosphorEssence</h3>"
             << "<p>Version " << PE_PACKAGE_VERSION << "</p>"
             << "<p>Copyright &copy; 2009 Michael J. Broxton</p>";
  QMessageBox::about(this, tr("About PhosphorEssence"),
                     tr(about_text.str().c_str()));
                       
}

void MainWindow::keyPressEvent(QKeyEvent *event) {

  std::ostringstream s; 
  
  switch (event->key()) {
  case Qt::Key_Escape:  // Quit
    close();
    break;
  }
}
