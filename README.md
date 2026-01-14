# Multi-Zap Dashboard | LKA

Sistema otimizado para gerenciar múltiplas instâncias do WhatsApp Web simultaneamente, com perfis separados e interface gráfica intuitiva.

## 📋 Características

- ✅ **Múltiplas contas** do WhatsApp simultaneamente
- 🎨 **Identificação visual** por cores personalizadas
- 💾 **Perfis persistentes** - mantém sessões salvas
- ⚡ **Otimizado para PCs fracos** - baixo consumo de RAM e CPU
- 🖥️ **Interface gráfica** moderna e intuitiva
- 🔄 **Botão de recarregar** para cada instância
- 📊 **Dashboard** para gerenciar perfis facilmente

## 🚀 Requisitos

- Python 3.8 ou superior
- Linux (testado no Ubuntu/Debian)
- PyQt6 e PyQt6-WebEngine

## 📦 Instalação

1- **Clone ou baixe o repositório:**

```bash
cd "Área de trabalho"
git clone [URL_DO_REPOSITORIO] Multi_Stace_Whats
cd Multi_Stace_Whats
```

2- **Crie e ative o ambiente virtual:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**

```powershell
python -m venv venv
.\venv\Scripts\Activate
```

3- **Instale as dependências:**

```bash
pip install -r requirements.txt
```

ou manualmente:

```bash
pip install PyQt6 PyQt6-WebEngine psutil
```

## ⚙️ Auto-Otimização por Hardware

O Multi-Zap **detecta automaticamente** as capacidades do seu computador e ajusta as configurações:

### 🔴 Perfil BAIXO (< 4GB RAM ou ≤ 2 CPUs)
- Cache reduzido: 20MB
- Heap JavaScript: 256MB
- Keep-alive: 60 segundos
- Ideal para: Netbooks, PCs antigos

### 🟡 Perfil MÉDIO (4-8GB RAM ou 2-4 CPUs)
- Cache padrão: 30MB
- Heap JavaScript: 512MB
- Keep-alive: 45 segundos
- Ideal para: PCs de entrada, notebooks básicos

### 🟢 Perfil ALTO (≥ 8GB RAM e > 4 CPUs)
- Cache expandido: 50MB
- Heap JavaScript: 1024MB
- Keep-alive: 30 segundos
- Ideal para: Desktops modernos, workstations

**O sistema ajusta automaticamente sem necessidade de configuração manual!**

## 🎯 Como Usar

### 1️⃣ Configurar Perfis (Primeira vez)

Execute o dashboard para criar seus perfis:

```bash
python dashboard.py
```

No dashboard você pode:

- **➕ Adicionar** novos perfis (nome, ID único e cor)
- **✏️ Editar** perfis existentes
- **🗑️ Remover** perfis
- **☑️ Marcar/Desmarcar** quais perfis deseja exibir

**Exemplo de perfis:**

- Nome: "Suporte" | ID: `zap_suporte` | Cor: Vermelho
- Nome: "Vendas" | ID: `zap_vendas` | Cor: Verde
- Nome: "Financeiro" | ID: `zap_financeiro` | Cor: Azul
- Nome: "Pessoal" | ID: `zap_pessoal` | Cor: Roxo

### 2️⃣ Iniciar Multi-Zap

Após configurar os perfis, clique em **"🚀 Iniciar Multi-Zap"** no dashboard, ou execute diretamente:

```bash
python main.py
```

### 3️⃣ Login no WhatsApp

- Cada instância abrirá o WhatsApp Web
- Faça o login com o QR Code em cada uma
- As sessões ficarão salvas nos perfis

## 📁 Estrutura do Projeto

```
Multi_Stace_Whats/
├── dashboard.py          # Interface para gerenciar perfis
├── login.py              # Gerenciador de perfis (backend)
├── main.py               # Motor principal otimizado
├── profiles/             # Pasta com dados dos perfis (cookies, sessões)
│   ├── zap_suporte/
│   ├── zap_vendas/
│   └── ...
├── profiles_config.json  # Configuração dos perfis
├── venv/                 # Ambiente virtual Python
├── .gitignore
└── README.md
```

## ⚙️ Arquivos e Funções

### `dashboard.py`

Interface gráfica para:

- Criar, editar e remover perfis
- Selecionar quais perfis exibir
- Iniciar o Multi-Zap

### `login.py`

Gerenciador de perfis (classe `ProfileManager`):

- Salvar/carregar perfis em JSON
- CRUD completo de perfis
- Gerenciar pastas de perfis

### `main.py`

Motor principal com otimizações:

- Carrega perfis habilitados automaticamente
- Cache de perfis (economia de RAM)
- Flags otimizadas do Chromium
- Recursos desabilitados para melhor performance

## 🔧 Otimizações Implementadas

O sistema foi **ULTRA otimizado** para rodar em qualquer configuração:

### 🚀 Performance Automática
- **Detecção automática** de hardware (RAM, CPU)
- **Ajuste dinâmico** de cache e memória
- **Perfis adaptativos** LOW/MEDIUM/HIGH

### 💾 Gestão de Memória
- Cache HTTP adaptativo: 20-50MB por perfil
- Heap JavaScript limitado: 256MB-1GB (baseado no sistema)
- Garbage Collection manual ativada
- Threads de rasterização otimizadas

### ⚡ Renderização Otimizada
- GPU rasterization mantida (evita tela preta)
- Aceleração 2D Canvas habilitada
- WebGL ativado para WhatsApp Web
- Software rasterizer desabilitado
- Scroll animations desabilitadas

### 🌐 Chromium Flags Ultra-Otimizadas
- `--enable-low-end-device-mode` - Modo dispositivos fracos
- `--disable-background-networking` - Sem rede em background
- `--process-per-site` - Menos processos
- `--in-process-gpu` - GPU no mesmo processo
- `--disable-extensions` - Sem overhead de extensões
- 30+ flags de otimização ativas

### 🔄 Anti-Tela Preta
- Timer keep-alive adaptativo (30-60s)
- Contexto de renderização mantido ativo
- Perfis únicos por instância (sem conflitos)
- Cache de código V8 ativado

### 🎨 Interface Leve
- Estilo Fusion (mais leve que padrão)
- Animações de UI desabilitadas
- Eventos de alta frequência comprimidos
- High DPI scaling desabilitado

## 📝 Notas Importantes

- ⚠️ Cada perfil é uma **conta separada** do WhatsApp
- 💾 Os dados ficam salvos na pasta `profiles/`
- 🔒 **Não compartilhe** a pasta `profiles/` - contém suas sessões
- 🔄 Use o botão **↻** para recarregar uma instância específica
- 🎨 A **barra colorida** no topo identifica cada perfil

## 🐛 Problemas Comuns

### "Nenhum perfil habilitado"
- Execute `python dashboard.py` e marque os perfis que deseja usar

### "python: command not found"
- Use `python3` ao invés de `python`
- Ou ative o ambiente virtual: `source venv/bin/activate`

### Tela Preta após um tempo
- **JÁ CORRIGIDO!** Sistema keep-alive automático
- GPU rasterization mantida ativa
- Timer adaptativo previne suspensão

### Consumo Alto de RAM
- Sistema detecta automaticamente e limita recursos
- Perfil LOW ativa em PCs com < 4GB RAM
- Cache reduzido automaticamente

### Avisos no terminal
- Avisos sobre `libva`, `Permissions-Policy` são normais e não afetam o funcionamento

## 💡 Dicas de Performance Extras

### Para PCs Muito Fracos (< 2GB RAM)
```bash
# Antes de iniciar, feche navegadores e apps pesados
# Execute apenas 2 instâncias por vez
# Considere usar swap file maior
```

### Para Notebooks
```bash
# Conecte o carregador (melhor performance plugado)
# Desative modo de economia de energia
# Feche apps em background
```

### Para Melhor Estabilidade
```bash
# Reinicie o Multi-Zap a cada 8-12 horas de uso contínuo
# Limpe cache periodicamente: rm -rf profiles/*/GPUCache/*
# Mantenha o sistema operacional atualizado
```

### Monitorar Recursos
```bash
# Ver uso de memória:
htop
# ou
top

# Matar processo se travar:
pkill -f "python.*main.py"
```

## 📄 Licença

Este projeto foi desenvolvido para uso interno da LKA.

## 👨‍💻 Desenvolvimento

Desenvolvido com:
- Python 3.8+
- PyQt6
- QtWebEngine
- psutil (detecção de hardware)

**Tecnologias de Otimização:**
- Chromium flags customizadas
- Adaptive resource management
- GPU acceleration
- Garbage collection otimizada

---

**💡 LEMBRE-SE:** O sistema detecta seu hardware automaticamente e aplica as melhores configurações! Funciona em qualquer PC! 🚀
