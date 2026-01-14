"""
Motor Principal - Multi-Zap
Otimizado para computadores fracos
Exibe múltiplas instâncias do WhatsApp Web com perfis separados
"""
import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QGridLayout, 
                             QVBoxLayout, QWidget, QMessageBox,
                             QPushButton, QLabel, QHBoxLayout)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage, QWebEngineSettings
from PyQt6.QtCore import QUrl, Qt
from login import ProfileManager

# Cache de perfis para reutilização e economia de RAM
_profile_cache = {}

class WhatsAppInstance(QWidget):
    def __init__(self, profile_name, label_title, color_code):
        super().__init__()
        
        # Armazena o título para usar na mensagem de permissão
        self.instance_title = label_title
        
        # Layout da instância individual
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # Barra de controle compacta (Nome + Reload)
        self.control_bar = QHBoxLayout()
        self.control_bar.setContentsMargins(5, 2, 5, 2)
        self.control_bar.setSpacing(5)
        
        self.label = QLabel(f"{label_title}")
        self.label.setStyleSheet("font-weight: bold; color: white; font-size: 11px;")
        
        self.btn_reload = QPushButton("↻")
        self.btn_reload.setFixedSize(20, 20)
        self.btn_reload.setStyleSheet("background-color: #333; color: white; border: none; font-size: 14px;")
        self.btn_reload.clicked.connect(self.reload_page)
        
        self.control_bar.addWidget(self.label)
        self.control_bar.addStretch()
        self.control_bar.addWidget(self.btn_reload)
        
        # Container da barra superior compacta
        self.bar_widget = QWidget()
        self.bar_widget.setLayout(self.control_bar)
        self.bar_widget.setFixedHeight(24)
        self.bar_widget.setStyleSheet(f"background-color: {color_code};")
        self.layout.addWidget(self.bar_widget)

        # Navegador (WebEngine)
        self.browser = QWebEngineView()
        self.setup_browser(profile_name)
        self.layout.addWidget(self.browser)

        # Cor para injeção CSS posterior
        self.header_color = color_code

    def setup_browser(self, profile_name):
        storage_path = os.path.join(os.getcwd(), "profiles", profile_name)
        
        # Reutilizar perfis do cache para economizar RAM
        if profile_name not in _profile_cache:
            self.profile = QWebEngineProfile(profile_name, self.browser)
            self.profile.setPersistentStoragePath(storage_path)
            self.profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)
            
            # Limitar tamanho do cache para economizar RAM/Disco
            self.profile.setHttpCacheMaximumSize(50 * 1024 * 1024)  # 50MB max
            
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            self.profile.setHttpUserAgent(user_agent)
            
            _profile_cache[profile_name] = self.profile
        else:
            self.profile = _profile_cache[profile_name]
        
        self.page = QWebEnginePage(self.profile, self.browser)
        
        # Conectar o pedido de permissão (microfone/câmera)
        self.page.featurePermissionRequested.connect(self.grant_permission)
        
        # Otimizações de performance
        settings = self.page.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, False)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PdfViewerEnabled, False)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AutoLoadIconsForPage, False)
        # PlaybackRequiresUserGesture False para notificações de áudio funcionarem
        settings.setAttribute(QWebEngineSettings.WebAttribute.PlaybackRequiresUserGesture, False)
        settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, False)
        settings.setAttribute(QWebEngineSettings.WebAttribute.Accelerated2dCanvasEnabled, False)
        
        self.browser.setPage(self.page)
        
        # Conectar o sinal de carregamento concluído para injetar CSS (apenas uma vez)
        self.browser.loadFinished.connect(self.on_load_finished)
        
        self.browser.setUrl(QUrl("https://web.whatsapp.com"))
    
    def grant_permission(self, url, feature):
        """
        Intercepta pedidos de uso de Hardware (Microfone/Câmera) e concede automaticamente
        para o domínio do WhatsApp, ou pede autorização ao usuário para outros domínios.
        """
        # Permissões de mídia (microfone/câmera)
        media_features = (
            QWebEnginePage.Feature.MediaAudioCapture, 
            QWebEnginePage.Feature.MediaVideoCapture,
            QWebEnginePage.Feature.MediaAudioVideoCapture
        )
        
        # Auto-conceder para WhatsApp
        if "whatsapp.com" in url.host():
            if feature in media_features:
                print(f"[DEBUG] Auto-concedendo permissão de mídia para {url.host()}")
                self.page.setFeaturePermission(url, feature, QWebEnginePage.PermissionPolicy.PermissionGrantedByUser)
                return
        
        # Para outros domínios ou funcionalidades, perguntar ao usuário
        if feature in media_features:
            feature_name = "o Microfone"
            if feature == QWebEnginePage.Feature.MediaVideoCapture:
                feature_name = "a Câmera"
            elif feature == QWebEnginePage.Feature.MediaAudioVideoCapture:
                feature_name = "a Câmera e o Microfone"

            # Pop-up de confirmação
            resposta = QMessageBox.question(
                self,
                "Solicitação de Acesso",
                f"A instância '{self.instance_title}' deseja acessar {feature_name}.\n\nVocê autoriza?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if resposta == QMessageBox.StandardButton.Yes:
                self.page.setFeaturePermission(url, feature, QWebEnginePage.PermissionPolicy.PermissionGrantedByUser)
            else:
                self.page.setFeaturePermission(url, feature, QWebEnginePage.PermissionPolicy.PermissionDeniedByUser)
        else:
            # Para outras permissões não tratadas, negar por padrão
            self.page.setFeaturePermission(url, feature, QWebEnginePage.PermissionPolicy.PermissionDeniedByUser)

    def reload_page(self):
        self.browser.reload()

    def on_load_finished(self):
        # Injeta CSS apenas se ainda não foi injetado (evita re-injeções desnecessárias)
        if not hasattr(self, '_css_injected'):
            # Injeta CSS de forma mais eficiente usando um único bloco
            js_code = f"""
                (function() {{
                    const style = document.createElement('style');
                    style.textContent = `
                        header {{ background-color: {self.header_color} !important; }}
                        #side {{ border-right: 5px solid {self.header_color} !important; }}
                    `;
                    document.head.appendChild(style);
                }})();
            """
            self.browser.page().runJavaScript(js_code)
            self._css_injected = True

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multi-Zap | LKA")
        self.resize(1400, 900)
        self.setStyleSheet("background-color: #111b21;")
        
        # Carregar gerenciador de perfis
        self.profile_manager = ProfileManager()
        
        # Widget Central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout em Grade (Grid)
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.grid.setContentsMargins(10, 10, 10, 10)
        central_widget.setLayout(self.grid)
        
        # Carregar perfis habilitados
        self.load_enabled_profiles()

    def load_enabled_profiles(self):
        """Carrega apenas os perfis habilitados do gerenciador"""
        profiles = self.profile_manager.get_enabled_profiles()
        
        if not profiles:
            QMessageBox.warning(
                self, 
                "Aviso", 
                "Nenhum perfil habilitado!\nAbra o dashboard.py para configurar."
            )
            sys.exit(0)
        
        # Distribuir perfis em grid (máximo 2 colunas)
        max_cols = 2
        for idx, profile in enumerate(profiles):
            row = idx // max_cols
            col = idx % max_cols
            self.add_instance(
                profile['name'],
                profile['profile_id'],
                profile['color'],
                row,
                col
            )
    
    def add_instance(self, title, profile_id, color, row, col):
        """Adiciona uma instância do WhatsApp ao grid"""
        try:
            instance = WhatsAppInstance(profile_id, title, color)
            self.grid.addWidget(instance, row, col)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao criar instância: {str(e)}")


def main():
    """Função principal otimizada para computadores fracos"""
    # Garantir que o diretório de perfis existe
    ProfileManager.ensure_profiles_directory()

    # Otimizações de ambiente
    os.environ["QT_FONT_DPI"] = "96"
    
    # Flags do Chromium para reduzir consumo de RAM e CPU
    # Essencial para computadores fracos
    # Removido --mute-audio para o microfone funcionar
    # Removido --disable-background-networking para não atrapalhar chamadas WebRTC
    # Removido --disable-gpu para não afetar codificação de áudio
    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = (
        "--disable-software-rasterizer "          # Desabilita rasterização por software
        "--disable-dev-shm-usage "                # Evita problemas com /dev/shm
        "--no-sandbox "                           # Remove sandbox (reduz overhead)
        "--disable-setuid-sandbox "               # Remove setuid sandbox
        "--js-flags=--expose-gc "                 # Permite coleta de lixo JS
        "--enable-low-end-device-mode "           # Modo para dispositivos fracos
        "--disable-sync "                         # Sem sincronização
        "--metrics-recording-only "               # Apenas métricas essenciais
        "--disable-breakpad "                     # Desabilita crash reporter
        "--disable-extensions "                   # Sem extensões
        "--disable-print-preview "                # Sem preview de impressão
        "--disable-component-update "             # Sem atualizações de componentes
        "--autoplay-policy=no-user-gesture-required " # Permite autoplay de áudio
        "--use-fake-ui-for-media-stream"          # Permite acesso a mídia sem UI fake
    )

    # Atributos de performance - DEVE ser definido ANTES de criar QApplication
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts, False)
    
    # Criar aplicação
    app = QApplication(sys.argv)
    
    # Criar e exibir janela principal
    try:
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        QMessageBox.critical(None, "Erro Fatal", f"Erro ao iniciar aplicação:\n{str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
