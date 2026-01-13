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

1. **Clone ou baixe o repositório:**
```bash
cd "Área de trabalho"
git clone [URL_DO_REPOSITORIO] Multi_Stace_Whats
cd Multi_Stace_Whats
```

2. **Crie e ative o ambiente virtual:**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Instale as dependências:**
```bash
pip install PyQt6 PyQt6-WebEngine
```

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

O sistema foi otimizado especialmente para computadores com recursos limitados:

- **Cache de perfis** - Reutilização de instâncias
- **Limite de cache HTTP** - 50MB por perfil
- **GPU desabilitada** - Reduz uso de VRAM
- **WebGL desabilitado** - Menos processamento gráfico
- **Plugins desabilitados** - Menos overhead
- **Modo low-end-device** - Otimizações do Chromium
- **Áudio desabilitado** - Economia de recursos
- **Sincronização desabilitada** - Sem rede em background

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

### Avisos no terminal
- Avisos sobre `libva`, `Permissions-Policy` são normais e não afetam o funcionamento

## 📄 Licença

Este projeto foi desenvolvido para uso interno da LKA.

## 👨‍💻 Desenvolvimento

Desenvolvido com:
- Python 3
- PyQt6
- QtWebEngine

---

**💡 Dica:** Para melhor performance, feche outros programas pesados enquanto usa o Multi-Zap!
