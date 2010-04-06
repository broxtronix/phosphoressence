// __BEGIN_LICENSE__
// Copyright (C) 2009 Michael J. Broxton
// All Rights Reserved.
// __END_LICENSE__

/// \file MainWindow.h
///
#ifndef __MAINWINDOW_H__
#define __MAINWINDOW_H__

#include <QMainWindow>
#include <string>

// Boost
#include <boost/program_options.hpp>

class QAction;
class QLabel;
class QTabWidget;
class GraphicsEngine;

class MainWindow : public QMainWindow {
  Q_OBJECT

public:
  MainWindow();
  virtual ~MainWindow() {}

  GraphicsEngine* gl_widget() const { return m_graphics_engine; }

private slots:
  void about();

protected:
  void keyPressEvent(QKeyEvent *event);

private:
  void create_actions();
  void create_menus();

  GraphicsEngine *m_graphics_engine;

  QMenu *file_menu;
  QMenu *edit_menu;
  QMenu *help_menu;

  QAction *about_action;
  QAction *exit_action;
};

#endif // __MAINWINDOW_H__
