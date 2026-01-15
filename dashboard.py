"""
Dashboard - Interface gráfica para gerenciamento de perfis
Permite criar, editar e selecionar quais perfis serão exibidos
"""
import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QLineEdit,
                             QListWidget, QListWidgetItem, QDialog, QColorDialog,
                             QMessageBox, QCheckBox, QGridLayout, QGroupBox,
                             QSpinBox, QDialogButtonBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor
from login import ProfileManager
import subprocess

def show_message(parent, title, text, icon_type="info"):
    """Exibe uma mensagem estilizada que funciona no Windows 10"""
    msg = QMessageBox(parent)
    msg.setWindowTitle(title)
    msg.setText(text)
    
    # Forçar o texto a aparecer usando stylesheet
    msg.setStyleSheet("""
        QMessageBox {
            background-color: #2b2b2b;
        }
        QMessageBox QLabel {
            color: white;
            font-size: 9pt;
            min-width: 150px;
            min-height: 20px;
            qproperty-alignment: AlignCenter;
            padding-left: 10px;
        }
        QMessageBox QLabel#qt_msgbox_label {
            padding-left: 0px;
            margin-left: -20px;
        }
        QPushButton {
            background-color: #0d7377;
            color: white;
            padding: 5px 14px;
            border: none;
            border-radius: 4px;
            font-weight: bold;
            font-size: 9pt;
        }
        QPushButton:hover {
            background-color: #14a085;
        }
    """)
    
    if icon_type == "info":
        msg.setIcon(QMessageBox.Icon.Information)
    elif icon_type == "warning":
        msg.setIcon(QMessageBox.Icon.Warning)
    elif icon_type == "error":
        msg.setIcon(QMessageBox.Icon.Critical)
    
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg.exec()

class ProfileDialog(QDialog):
    """Diálogo para adicionar/editar perfil"""
    def __init__(self, parent=None, profile=None):
        super().__init__(parent)
        self.profile = profile
        self.selected_color = profile['color'] if profile else "#b71c1c"
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Adicionar Perfil" if not self.profile else "Editar Perfil")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        
        # Nome do perfil
        layout.addWidget(QLabel("Nome do Perfil:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Ex: Suporte, Vendas, Financeiro")
        if self.profile:
            self.name_input.setText(self.profile['name'])
        layout.addWidget(self.name_input)
        
        # ID do perfil (apenas para novos perfis)
        if not self.profile:
            layout.addWidget(QLabel("ID do Perfil (único):"))
            self.id_input = QLineEdit()
            self.id_input.setPlaceholderText("Ex: zap_suporte, zap_vendas")
            layout.addWidget(self.id_input)
        
        # Seletor de cor
        color_layout = QHBoxLayout()
        color_layout.addWidget(QLabel("Cor:"))
        self.color_button = QPushButton("Escolher Cor")
        self.color_button.clicked.connect(self.choose_color)
        self.update_color_button()
        color_layout.addWidget(self.color_button)
        color_layout.addStretch()
        layout.addLayout(color_layout)
        
        # Botões
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.validate_and_accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
    
    def choose_color(self):
        color = QColorDialog.getColor(QColor(self.selected_color), self)
        if color.isValid():
            self.selected_color = color.name()
            self.update_color_button()
    
    def update_color_button(self):
        self.color_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.selected_color};
                color: white;
                font-weight: bold;
                padding: 10px;
                border: 2px solid #333;
            }}
        """)
    
    def validate_and_accept(self):
        name = self.name_input.text().strip()
        if not name:
            show_message(self, "Aviso", "O nome do perfil é obrigatório!", "warning")
            return
        
        if not self.profile:
            profile_id = self.id_input.text().strip()
            if not profile_id:
                show_message(self, "Aviso", "O ID do perfil é obrigatório!", "warning")
                return
        
        self.accept()
    
    def get_data(self):
        data = {
            'name': self.name_input.text().strip(),
            'color': self.selected_color
        }
        if not self.profile:
            data['profile_id'] = self.id_input.text().strip()
        return data


class DashboardWindow(QMainWindow):
    """Janela principal do dashboard"""
    def __init__(self):
        super().__init__()
        self.profile_manager = ProfileManager()
        ProfileManager.ensure_profiles_directory()
        self.setup_ui()
        self.load_profiles_list()
    
    def setup_ui(self):
        self.setWindowTitle("Multi-Zap Dashboard | LKA - Gerenciador")
        self.setMinimumSize(800, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QLabel {
                color: white;
                font-size: 12pt;
            }
            QPushButton {
                background-color: #0d7377;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #14a085;
            }
            QPushButton:disabled {
                background-color: #555;
            }
            QListWidget {
                background-color: #2b2b2b;
                color: white;
                border: 1px solid #444;
            }
            QGroupBox {
                color: white;
                border: 2px solid #0d7377;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Título
        title = QLabel("Gerenciador de Perfis WhatsApp")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18pt; font-weight: bold; margin: 20px;")
        main_layout.addWidget(title)
        
        # Container principal com dois grupos
        content_layout = QHBoxLayout()
        
        # Grupo de perfis
        profiles_group = QGroupBox("Perfis Disponíveis")
        profiles_layout = QVBoxLayout()
        
        self.profiles_list = QListWidget()
        self.profiles_list.itemChanged.connect(self.on_profile_checked)
        profiles_layout.addWidget(self.profiles_list)
        
        # Botões de gerenciamento
        buttons_layout = QHBoxLayout()
        self.add_btn = QPushButton("➕ Adicionar")
        self.edit_btn = QPushButton("✏️ Editar")
        self.remove_btn = QPushButton("🗑️ Remover")
        
        self.add_btn.clicked.connect(self.add_profile)
        self.edit_btn.clicked.connect(self.edit_profile)
        self.remove_btn.clicked.connect(self.remove_profile)
        
        buttons_layout.addWidget(self.add_btn)
        buttons_layout.addWidget(self.edit_btn)
        buttons_layout.addWidget(self.remove_btn)
        profiles_layout.addLayout(buttons_layout)
        
        profiles_group.setLayout(profiles_layout)
        content_layout.addWidget(profiles_group, 2)
        
        # Grupo de layout
        layout_group = QGroupBox("Configuração de Layout")
        layout_config = QVBoxLayout()
        
        layout_config.addWidget(QLabel("Disposição das telas:"))
        
        grid_layout = QGridLayout()
        self.grid_spin = QSpinBox()
        self.grid_spin.setMinimum(1)
        self.grid_spin.setMaximum(4)
        self.grid_spin.setValue(2)
        self.grid_spin.setPrefix("Grade: ")
        self.grid_spin.setSuffix(" x 2")
        grid_layout.addWidget(QLabel("Colunas:"), 0, 0)
        grid_layout.addWidget(self.grid_spin, 0, 1)
        
        layout_config.addLayout(grid_layout)
        layout_config.addStretch()
        
        layout_group.setLayout(layout_config)
        content_layout.addWidget(layout_group, 1)
        
        main_layout.addLayout(content_layout)
        
        # Botão de iniciar
        self.start_btn = QPushButton("🚀 Iniciar Multi-Zap")
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #1b5e20;
                font-size: 14pt;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #2e7d32;
            }
        """)
        self.start_btn.clicked.connect(self.start_multizap)
        main_layout.addWidget(self.start_btn)
        
        # Info
        info_label = QLabel("✓ Marque os perfis que deseja exibir e clique em Iniciar")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setStyleSheet("color: #aaa; font-size: 10pt; margin: 10px;")
        main_layout.addWidget(info_label)
    
    def load_profiles_list(self):
        """Carrega a lista de perfis no widget"""
        self.profiles_list.clear()
        profiles = self.profile_manager.get_all_profiles()
        
        for profile in profiles:
            item = QListWidgetItem(f"● {profile['name']} ({profile['profile_id']})")
            item.setData(Qt.ItemDataRole.UserRole, profile)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(
                Qt.CheckState.Checked if profile.get('enabled', True) 
                else Qt.CheckState.Unchecked
            )
            
            # Aplicar cor
            item.setForeground(QColor(profile['color']))
            self.profiles_list.addItem(item)
    
    def on_profile_checked(self, item):
        """Atualiza o estado habilitado do perfil"""
        profile = item.data(Qt.ItemDataRole.UserRole)
        enabled = item.checkState() == Qt.CheckState.Checked
        self.profile_manager.update_profile(profile['profile_id'], enabled=enabled)
    
    def add_profile(self):
        """Adiciona um novo perfil"""
        dialog = ProfileDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if self.profile_manager.add_profile(data['name'], data['profile_id'], data['color']):
                show_message(self, "Sucesso", "Perfil adicionado com sucesso!", "info")
                self.load_profiles_list()
            else:
                show_message(self, "Erro", "Perfil com este ID já existe!", "warning")
    
    def edit_profile(self):
        """Edita o perfil selecionado"""
        current_item = self.profiles_list.currentItem()
        if not current_item:
            show_message(self, "Aviso", "Selecione um perfil para editar!", "warning")
            return
        
        profile = current_item.data(Qt.ItemDataRole.UserRole)
        dialog = ProfileDialog(self, profile)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if self.profile_manager.update_profile(
                profile['profile_id'], 
                name=data['name'], 
                color=data['color']
            ):
                show_message(self, "Sucesso", "Perfil atualizado com sucesso!", "info")
                self.load_profiles_list()
    
    def remove_profile(self):
        """Remove o perfil selecionado"""
        current_item = self.profiles_list.currentItem()
        if not current_item:
            show_message(self, "Aviso", "Selecione um perfil para remover!", "warning")
            return
        
        profile = current_item.data(Qt.ItemDataRole.UserRole)
        reply = QMessageBox.question(
            self, 
            "Confirmar Remoção",
            f"Deseja remover o perfil '{profile['name']}'?\n(Os dados não serão apagados)",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.profile_manager.remove_profile(profile['profile_id'])
            show_message(self, "Sucesso", "Perfil removido com sucesso!", "info")
            self.load_profiles_list()
    
    def start_multizap(self):
        """Inicia o Multi-Zap com os perfis selecionados"""
        enabled_profiles = self.profile_manager.get_enabled_profiles()
        
        if not enabled_profiles:
            show_message(self, "Aviso", "Selecione pelo menos um perfil!", "warning")
            return
        
        # Fechar dashboard e iniciar main
        try:
            if getattr(sys, 'frozen', False):
                # SE ESTIVER RODANDO COMO EXE (PyInstaller)
                application_path = os.path.dirname(sys.executable)
                main_exe_path = os.path.join(application_path, "main.exe")
                subprocess.Popen([main_exe_path])
            else:
                # SE ESTIVER RODANDO NO PYTHON (VS Code)
                subprocess.Popen([sys.executable, "main.py"])
                
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao iniciar Multi-Zap: {e}")

# ==========================================
# BLOCO PRINCIPAL (FORA DA CLASSE)
# ==========================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DashboardWindow()
    window.show()
    sys.exit(app.exec())