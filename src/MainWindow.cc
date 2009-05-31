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

  // Set up the basic layout of the window and its menus
  create_actions();
  create_menus();
  //  create_status_bar();
  
  // Set the window title and add tabs
  std::string window_title = "Phosphor Essence v0.1";
  this->setWindowTitle(window_title.c_str());

  // Set up GraphicsEngine
  m_graphics_engine = new GraphicsEngine(this);
  setCentralWidget(m_graphics_engine);

  // Maximize the main window
  //  this->showMaximized();
  this->showFullScreen();
}

//********************************************************************
//                      MAIN WINDOW SETUP
//********************************************************************

void MainWindow::create_actions() {

  // The About Box
  about_action = new QAction(tr("About VWV"), this);
  about_action->setStatusTip(tr("Show the Vision Workbench Viewere about box."));
  connect(about_action, SIGNAL(triggered()), this, SLOT(about()));

  // Exit or Quit
  exit_action = new QAction(tr("E&xit"), this);
  exit_action->setShortcut(tr("Ctrl+Q"));
  exit_action->setStatusTip(tr("Exit the application"));
  connect(exit_action, SIGNAL(triggered()), this, SLOT(close()));
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

void MainWindow::create_status_bar() {
  status_label = new QLabel("");
  status_label->setAlignment(Qt::AlignHCenter);
  statusBar()->addWidget(status_label);

  // WARNING: Memory leak as currently written.  Fix this somewhow...
  //   GuiProgressCallback *clbk = new GuiProgressCallback(this, "Updating: ");
  //   statusBar()->addWidget(clbk->widget());
}

void MainWindow::update_status_bar(std::string const& s) {
  status_label->setText(QString(s.c_str()));
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
