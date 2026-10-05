import os
import sys
from PyQt6.QtCore import QDir, Qt
from PyQt6.QtGui import QAction, QFileSystemModel
from PyQt6.QtWidgets import (
    QApplication,
    QColorDialog,
    QHBoxLayout,
    QInputDialog,
    QListWidget,
    QLineEdit,
    QMenu,
    QMessageBox,
    QPushButton,
    QSplitter,
    QTableView,
    QTreeView,
    QVBoxLayout,
    QWidget,
)


class AmoledExplorer(QWidget):

  def __init__(self):
    super().__init__()
    self.accent_color = "#00e5ff"  
    self.initUI()

  def initUI(self):
    self.setWindowTitle("H.Explorer - Gerenciador de Arquivos")
    self.resize(1300, 750)

    main_layout = QVBoxLayout(self)
    main_layout.setContentsMargins(12, 12, 12, 12)
    main_layout.setSpacing(10)


    nav_layout = QHBoxLayout()
    nav_layout.setSpacing(6)

    self.btn_back = QPushButton("◀")
    self.btn_forward = QPushButton("▶")
    self.btn_up = QPushButton("▲ Acima")
    self.btn_home = QPushButton("🏠 Início")

    for btn in [self.btn_back, self.btn_forward, self.btn_up, self.btn_home]:
      btn.setFixedWidth(75)

    self.path_bar = QLineEdit()
    self.path_bar.setPlaceholderText("Caminho da pasta atual...")

    self.btn_new_folder = QPushButton("Nova Pasta")
    self.btn_new_file = QPushButton("Novo Arquivo")
    self.btn_color_picker = QPushButton("Cor Personalizada")

    nav_layout.addWidget(self.btn_back)
    nav_layout.addWidget(self.btn_forward)
    nav_layout.addWidget(self.btn_up)
    nav_layout.addWidget(self.btn_home)
    nav_layout.addWidget(self.path_bar)
    nav_layout.addWidget(self.btn_new_folder)
    nav_layout.addWidget(self.btn_new_file)
    nav_layout.addWidget(self.btn_color_picker)

    main_layout.addLayout(nav_layout)


    self.file_model = QFileSystemModel()
    self.file_model.setRootPath("")
    self.file_model.setFilter(
        QDir.Filter.AllDirs
        | QDir.Filter.Files
        | QDir.Filter.NoDotAndDotDot
        | QDir.Filter.Hidden
    )

 
    main_splitter = QSplitter(Qt.Orientation.Horizontal)


    self.quick_access_list = QListWidget()
    self.populate_quick_access()


    sub_splitter = QSplitter(Qt.Orientation.Horizontal)


    self.tree_view = QTreeView()
    self.tree_view.setModel(self.file_model)
    self.tree_view.setRootIndex(self.file_model.index(""))
    self.tree_view.hideColumn(1)
    self.tree_view.hideColumn(2)
    self.tree_view.hideColumn(3)
    self.tree_view.setHeaderHidden(True)


    self.table_view = QTableView()
    self.table_view.setModel(self.file_model)
    self.table_view.setSelectionBehavior(
        QTableView.SelectionBehavior.SelectRows
    )
    self.table_view.setSortingEnabled(True)
    self.table_view.horizontalHeader().setStretchLastSection(True)
    self.table_view.horizontalHeader().resizeSection(0, 320)

    sub_splitter.addWidget(self.tree_view)
    sub_splitter.addWidget(self.table_view)
    sub_splitter.setSizes([250, 750])

    main_splitter.addWidget(self.quick_access_list)
    main_splitter.addWidget(sub_splitter)
    main_splitter.setSizes([200, 1000])

    main_layout.addWidget(main_splitter)


    self.quick_access_list.itemClicked.connect(self.on_quick_access_clicked)
    self.tree_view.clicked.connect(self.on_tree_clicked)
    self.table_view.doubleClicked.connect(self.on_table_double_clicked)
    self.path_bar.returnPressed.connect(self.on_path_entered)
    self.btn_up.clicked.connect(self.go_up)
    self.btn_home.clicked.connect(self.go_home)
    self.btn_new_folder.clicked.connect(self.create_folder_action)
    self.btn_new_file.clicked.connect(self.create_file_action)
    self.btn_color_picker.clicked.connect(self.open_color_picker)


    self.table_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
    self.table_view.customContextMenuRequested.connect(self.show_context_menu)


    home_path = QDir.homePath()
    self.navigate_to(home_path)


    self.apply_stylesheet()

  def populate_quick_access(self):
    home = QDir.homePath()
    shortcuts = [
        ("🏠 Início", home),
        ("🖥 Área de Trabalho", os.path.join(home, "Desktop")),
        ("📂 Documentos", os.path.join(home, "Documents")),
        ("⬇️ Downloads", os.path.join(home, "Downloads")),
        ("🖼 Imagens", os.path.join(home, "Pictures")),
        ("🎵 Músicas", os.path.join(home, "Music")),
        ("🎬 Vídeos", os.path.join(home, "Videos")),
        ("💻 Disco Local (C:)", "C:\\"),
    ]

    for name, path in shortcuts:
      if os.path.exists(path):
        item = self.quick_access_list.addItem(name)

        self.quick_access_list.item(
            self.quick_access_list.count() - 1
        ).setData(Qt.ItemDataRole.UserRole, path)

  def on_quick_access_clicked(self, item):
    path = item.data(Qt.ItemDataRole.UserRole)
    if path and os.path.exists(path):
      self.navigate_to(path)

  def apply_stylesheet(self):
    qss = f"""
            QWidget {{
                background-color: #000000;
                color: #e0e0e0;
                font-family: 'Segoe UI', sans-serif;
                font-size: 13px;
            }}
            QTreeView, QTableView, QListWidget {{
                background-color: #030303;
                color: #e0e0e0;
                border: 1px solid #121212;
                alternate-background-color: #080808;
                selection-background-color: {self.accent_color};
                selection-color: #000000;
                border-radius: 6px;
            }}
            QListWidget::item {{
                padding: 8px 10px;
                border-bottom: 1px solid #0a0a0a;
            }}
            QListWidget::item:hover {{
                background-color: #121212;
                color: #ffffff;
            }}
            QHeaderView::section {{
                background-color: #0a0a0a;
                color: #888888;
                padding: 6px;
                border: none;
                border-bottom: 1px solid #1a1a1a;
                font-weight: bold;
            }}
            QLineEdit {{
                background-color: #080808;
                border: 1px solid #1f1f1f;
                border-radius: 5px;
                padding: 6px 10px;
                color: #ffffff;
            }}
            QLineEdit:focus {{
                border: 1px solid {self.accent_color};
            }}
            QPushButton {{
                background-color: #0c0c0c;
                color: #e0e0e0;
                border: 1px solid #1f1f1f;
                border-radius: 5px;
                padding: 6px 12px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: #161616;
                border-color: {self.accent_color};
                color: #ffffff;
            }}
            QSplitter::handle {{
                background-color: #121212;
            }}
            QMenu {{
                background-color: #0a0a0a;
                color: #e0e0e0;
                border: 1px solid #222222;
                padding: 4px;
            }}
            QMenu::item {{
                padding: 6px 20px;
                border-radius: 3px;
            }}
            QMenu::item:selected {{
                background-color: {self.accent_color};
                color: #000000;
            }}
        """
    self.setStyleSheet(qss)

  def open_color_picker(self):
    color = QColorDialog.getColor()
    if color.isValid():
      self.accent_color = color.name()
      self.apply_stylesheet()

  def get_current_path(self):
    index = self.table_view.rootIndex()
    if index.isValid():
      return self.file_model.filePath(index)
    return QDir.homePath()

  def navigate_to(self, path):
    if os.path.exists(path):
      index = self.file_model.index(path)
      self.tree_view.setCurrentIndex(index)
      self.table_view.setRootIndex(index)
      self.path_bar.setText(path)
      self.tree_view.scrollTo(index)

  def on_tree_clicked(self, index):
    path = self.file_model.fileInfo(index).absoluteFilePath()
    if os.path.isdir(path):
      self.table_view.setRootIndex(index)
      self.path_bar.setText(path)

  def on_table_double_clicked(self, index):
    path = self.file_model.fileInfo(index).absoluteFilePath()
    if os.path.isdir(path):
      self.navigate_to(path)
    else:
      try:
        os.startfile(path)
      except Exception as e:
        QMessageBox.warning(
            self, "Aviso", f"Não foi possível abrir o arquivo: {e}"
        )

  def on_path_entered(self):
    path = self.path_bar.text().strip()
    if os.path.exists(path) and os.path.isdir(path):
      self.navigate_to(path)
    else:
      QMessageBox.warning(
          self, "Erro", "O caminho digitado não existe ou não é uma pasta válida."
      )

  def go_up(self):
    current_path = self.path_bar.text()
    parent_path = os.path.dirname(current_path)
    if parent_path and os.path.exists(parent_path):
      self.navigate_to(parent_path)

  def go_home(self):
    self.navigate_to(QDir.homePath())

  def create_folder_action(self):
    current_dir = self.get_current_path()
    folder_name, ok = QInputDialog.getText(
        self, "Nova Pasta", "Digite o nome da nova pasta:"
    )
    if ok and folder_name.strip():
      new_folder_path = os.path.join(current_dir, folder_name.strip())
      try:
        os.makedirs(new_folder_path, exist_ok=False)
      except Exception as e:
        QMessageBox.critical(self, "Erro", f"Não foi possível criar a pasta: {e}")

  def create_file_action(self):
    current_dir = self.get_current_path()
    file_name, ok = QInputDialog.getText(
        self, "Novo Arquivo", "Digite o nome do arquivo (ex: nota.txt):"
    )
    if ok and file_name.strip():
      new_file_path = os.path.join(current_dir, file_name.strip())
      try:
        with open(new_file_path, "w", encoding="utf-8") as f:
          f.write("")
      except Exception as e:
        QMessageBox.critical(
            self, "Erro", f"Não foi possível criar o arquivo: {e}"
        )

  def show_context_menu(self, position):
    index = self.table_view.indexAt(position)
    if not index.isValid():
      return

    file_info = self.file_model.fileInfo(index)
    path = file_info.absoluteFilePath()

    menu = QMenu(self)
    open_action = QAction(" Abrir", self)
    rename_action = QAction(" Renomear", self)
    delete_action = QAction(" Excluir", self)

    menu.addAction(open_action)
    menu.addAction(rename_action)
    menu.addAction(delete_action)

    action = menu.exec(self.table_view.viewport().mapToGlobal(position))

    if action == open_action:
      if file_info.isDir():
        self.navigate_to(path)
      else:
        os.startfile(path)
    elif action == rename_action:
      new_name, ok = QInputDialog.getText(
          self, "Renomear", "Novo nome:", text=file_info.fileName()
      )
      if ok and new_name.strip():
        new_path = os.path.join(os.path.dirname(path), new_name.strip())
        try:
          os.rename(path, new_path)
        except Exception as e:
          QMessageBox.critical(
              self, "Erro", f"Não foi possível renomear: {e}"
          )
    elif action == delete_action:
      confirm = QMessageBox.question(
          self,
          "Confirmar Exclusão",
          f"Deseja realmente excluir '{file_info.fileName()}'?",
          QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
      )
      if confirm == QMessageBox.StandardButton.Yes:
        try:
          if file_info.isDir():
            os.rmdir(path)
          else:
            os.remove(path)
        except Exception as e:
          QMessageBox.critical(self, "Erro", f"Não foi possível excluir: {e}")


if __name__ == "__main__":
  app = QApplication(sys.argv)
  explorer = AmoledExplorer()
  explorer.show()
  sys.exit(app.exec())