"""
Motor Principal - Multi-Zap
Otimizado para computadores fracos
Exibe múltiplas instâncias do WhatsApp Web com perfis separados
"""
import sys
import os
import psutil  # Para detectar recursos do sistema
from PyQt6.QtWidgets import (QApplication, QMainWindow, QGridLayout, 
                             QVBoxLayout, QWidget, QMessageBox,
                             QPushButton, QLabel, QHBoxLayout)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage, QWebEngineSettings
from PyQt6.QtCore import QUrl, Qt, QTimer
from login import ProfileManager

def detect_system_capabilities():
    """Detecta as capacidades do sistema e retorna configurações otimizadas"""
    try:
        # Detectar RAM disponível
        ram_gb = psutil.virtual_memory().total / (1024**3)
        cpu_count = psutil.cpu_count()
        
        # Perfil BAIXO: < 4GB RAM ou <= 2 CPUs
        if ram_gb < 4 or cpu_count <= 2:
            return {
                'profile': 'LOW',
                'cache_size': 20,  # MB
                'keep_alive_interval': 60000,  # 60 segundos
                'max_heap': 256,  # MB
                'raster_threads': 1
            }
        # Perfil MÉDIO: 4-8GB RAM ou 2-4 CPUs
        elif ram_gb < 8 or cpu_count <= 4:
            return {
                'profile': 'MEDIUM',
                'cache_size': 30,  # MB
                'keep_alive_interval': 45000,  # 45 segundos
                'max_heap': 512,  # MB
                'raster_threads': 2
            }
        # Perfil ALTO: >= 8GB RAM e > 4 CPUs
        else:
            return {
                'profile': 'HIGH',
                'cache_size': 50,  # MB
                'keep_alive_interval': 30000,  # 30 segundos
                'max_heap': 1024,  # MB
                'raster_threads': 4
            }
    except:
        # Fallback para perfil médio se não conseguir detectar
        return {
            'profile': 'MEDIUM',
            'cache_size': 30,
            'keep_alive_interval': 45000,
            'max_heap': 512,
            'raster_threads': 2
        }

# Detectar configurações otimizadas
SYSTEM_CONFIG = detect_system_capabilities()
print(f"[Sistema] Perfil detectado: {SYSTEM_CONFIG['profile']}")
print(f"[Sistema] RAM Total: {psutil.virtual_memory().total / (1024**3):.1f} GB")
print(f"[Sistema] CPUs: {psutil.cpu_count()}")

class WhatsAppInstance(QWidget):
    def __init__(self, profile_name, label_title, color_code):
        super().__init__()
        
        # Armazena o título para usar na mensagem de permissão
        self.instance_title = label_title
        self.profile_name = profile_name
        
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
        
        # Criar perfil único para cada instância (evita conflitos e tela preta)
        self.profile = QWebEngineProfile(profile_name, self.browser)
        self.profile.setPersistentStoragePath(storage_path)
        self.profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)
        
        # Limitar tamanho do cache baseado no perfil do sistema
        cache_size = SYSTEM_CONFIG['cache_size'] * 1024 * 1024
        self.profile.setHttpCacheMaximumSize(cache_size)
        
        # Política de cache HTTP agressiva para economizar banda e processamento
        self.profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.DiskHttpCache)
        
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        self.profile.setHttpUserAgent(user_agent)
        
        # Criar página e manter referência forte para evitar garbage collection
        self.page = QWebEnginePage(self.profile, self.browser)
        
        # Conectar o pedido de permissão (microfone/câmera)
        self.page.featurePermissionRequested.connect(self.grant_permission)
        
        # Otimizações de performance agressivas
        settings = self.page.settings()
        
        # Desabilitar recursos pesados não necessários
        settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, False)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PdfViewerEnabled, False)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AutoLoadIconsForPage, False)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows, False)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.ScrollAnimatorEnabled, False)
        
        # Funcionalidades essenciais para WhatsApp
        settings.setAttribute(QWebEngineSettings.WebAttribute.PlaybackRequiresUserGesture, False)
        settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.Accelerated2dCanvasEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, False)
        settings.setAttribute(QWebEngineSettings.WebAttribute.XSSAuditingEnabled, False)
        
        # Otimizações de JavaScript
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        
        self.browser.setPage(self.page)
        
        # Conectar o sinal de carregamento concluído para injetar CSS (apenas uma vez)
        self.browser.loadFinished.connect(self.on_load_finished)
        
        # Timer para manter a view ativa (intervalo baseado no perfil do sistema)
        self.keep_alive_timer = QTimer(self)
        self.keep_alive_timer.timeout.connect(self.keep_view_alive)
        self.keep_alive_timer.start(SYSTEM_CONFIG['keep_alive_interval'])
        
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
    
    def keep_view_alive(self):
        """Mantém a view ativa executando um pequeno script JavaScript periodicamente"""
        if self.browser and self.browser.page():
            # Executa um script simples para manter o contexto de renderização ativo
            self.browser.page().runJavaScript("void(0);")

    def on_load_finished(self):
        # Injeta CSS apenas se ainda não foi injetado (evita re-injeções desnecessárias)
        if not hasattr(self, '_css_injected'):
            # Injeta CSS + otimizações de performance do WhatsApp Web
            js_code = f"""
                (function() {{
                    // CSS personalizado
                    const style = document.createElement('style');
                    style.textContent = `
                        header {{ background-color: {self.header_color} !important; }}
                        #side {{ border-right: 5px solid {self.header_color} !important; }}
                        
                        /* Otimizações de performance */
                        * {{ 
                            -webkit-font-smoothing: antialiased;
                            text-rendering: optimizeSpeed;
                        }}
                        img {{ 
                            image-rendering: -webkit-optimize-contrast;
                        }}
                    `;
                    document.head.appendChild(style);
                    
                    // Liberar memória do garbage collector após 5 segundos
                    setTimeout(() => {{
                        if (window.gc) window.gc();
                    }}, 5000);
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
                "Nenhum perfil habilitado!\n Abra o dashboard.py para configurar."
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

    # Otimizações de ambiente Qt
    os.environ["QT_FONT_DPI"] = "96"
    os.environ["QT_SCALE_FACTOR"] = "1"
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "0"
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
    
    # Flags do Chromium ULTRA otimizadas para computadores fracos
    # Balanceamento entre performance e funcionalidade do WhatsApp
    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = (
        # === Economia de Memória ===
        "--disable-dev-shm-usage "                # Evita problemas com /dev/shm
        "--disable-background-timer-throttling "  # Não throttle timers em background
        "--disable-backgrounding-occluded-windows " # Não desativa janelas ocultas
        "--disable-renderer-backgrounding "       # Mantém renderer ativo
        "--max-old-space-size=512 "              # Limita heap do V8 a 512MB
        
        # === Segurança Relaxada (Performance) ===
        "--no-sandbox "                           # Remove sandbox (reduz overhead)
        "--disable-setuid-sandbox "               # Remove setuid sandbox
        "--disable-web-security "                 # Desativa algumas verificações de segurança
        
        # === JavaScript Otimizado ===
        f"--js-flags=--expose-gc,--max-old-space-size={SYSTEM_CONFIG['max_heap']} " # GC manual + limite heap
        
        # === Modo Dispositivos Fracos ===
        "--enable-low-end-device-mode "           # Modo para dispositivos fracos
        "--enable-low-res-tiling "                # Tiles de baixa resolução
        
        # === Recursos Desabilitados ===
        "--disable-sync "                         # Sem sincronização
        "--disable-breakpad "                     # Desabilita crash reporter
        "--disable-extensions "                   # Sem extensões
        "--disable-plugins "                      # Sem plugins
        "--disable-print-preview "                # Sem preview de impressão
        "--disable-component-update "             # Sem atualizações de componentes
        "--disable-background-networking "        # Reduz networking em background
        "--disable-features=TranslateUI "         # Desabilita tradução
        "--disable-features=MediaRouter "         # Desabilita media router
        "--disable-domain-reliability "           # Desabilita relatórios de confiabilidade
        
        # === GPU e Renderização (Mantém aceleração) ===
        "--enable-accelerated-2d-canvas "         # Mantém aceleração 2D
        "--ignore-gpu-blocklist "                 # Força uso da GPU
        "--enable-gpu-rasterization "             # Rasterização por GPU
        f"--num-raster-threads={SYSTEM_CONFIG['raster_threads']} " # Threads baseadas no sistema
        
        # === Rede e Cache ===
        "--disk-cache-size=31457280 "             # Cache de disco 30MB
        "--media-cache-size=20971520 "            # Cache de mídia 20MB
        
        # === Áudio/Vídeo (Essencial para WhatsApp) ===
        "--autoplay-policy=no-user-gesture-required " # Permite autoplay
        "--use-fake-ui-for-media-stream "         # UI fake para mídia
        "--enable-features=WebRTC-H264WithOpenH264FFmpeg " # Codec H264
        
        # === Performance Geral ===
        "--process-per-site "                     # Um processo por site
        "--in-process-gpu "                       # GPU no mesmo processo
        "--metrics-recording-only "               # Apenas métricas essenciais
        "--disable-software-rasterizer "          # Força rasterização por hardware
        "--v8-cache-options=code "                # Cache de código V8
    )

    # Atributos de performance - DEVE ser definido ANTES de criar QApplication
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts, False)
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseDesktopOpenGL, True)
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_CompressHighFrequencyEvents, True)
    
    # Criar aplicação
    app = QApplication(sys.argv)
    
    # Configurar estilo para melhor performance
    app.setStyle("Fusion")  # Estilo Fusion é mais leve
    
    # Desabilitar efeitos visuais pesados
    app.setEffectEnabled(Qt.UIEffect.UI_AnimateMenu, False)
    app.setEffectEnabled(Qt.UIEffect.UI_AnimateCombo, False)
    app.setEffectEnabled(Qt.UIEffect.UI_AnimateTooltip, False)
    
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
