"""
Módulo de gerenciamento de perfis do WhatsApp
Responsável por criar, salvar e carregar perfis de usuário
"""
import os
import json

PROFILES_DIR = "profiles"
PROFILES_CONFIG = "profiles_config.json"

class ProfileManager:
    def __init__(self):
        self.profiles_dir = PROFILES_DIR
        self.config_file = PROFILES_CONFIG
        self.profiles = self.load_profiles()
    
    def load_profiles(self):
        """Carrega a lista de perfis salvos"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Erro ao carregar perfis: {e}")
                return []
        return []
    
    def save_profiles(self):
        """Salva a lista de perfis no arquivo de configuração"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.profiles, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erro ao salvar perfis: {e}")
            return False
    
    def add_profile(self, name, profile_id, color):
        """
        Adiciona um novo perfil
        
        Args:
            name (str): Nome de exibição do perfil
            profile_id (str): ID único do perfil (usado como nome da pasta)
            color (str): Cor em hexadecimal (#RRGGBB)
        
        Returns:
            bool: True se adicionado com sucesso
        """
        # Verificar se o profile_id já existe
        if any(p['profile_id'] == profile_id for p in self.profiles):
            return False
        
        # Criar diretório do perfil se não existir
        profile_path = os.path.join(self.profiles_dir, profile_id)
        if not os.path.exists(profile_path):
            os.makedirs(profile_path)
        
        # Adicionar perfil à lista
        profile = {
            'name': name,
            'profile_id': profile_id,
            'color': color,
            'enabled': True
        }
        self.profiles.append(profile)
        self.save_profiles()
        return True
    
    def remove_profile(self, profile_id):
        """Remove um perfil da lista (não remove a pasta)"""
        self.profiles = [p for p in self.profiles if p['profile_id'] != profile_id]
        self.save_profiles()
    
    def update_profile(self, profile_id, name=None, color=None, enabled=None):
        """Atualiza informações de um perfil"""
        for profile in self.profiles:
            if profile['profile_id'] == profile_id:
                if name is not None:
                    profile['name'] = name
                if color is not None:
                    profile['color'] = color
                if enabled is not None:
                    profile['enabled'] = enabled
                self.save_profiles()
                return True
        return False
    
    def get_profile(self, profile_id):
        """Retorna um perfil específico"""
        for profile in self.profiles:
            if profile['profile_id'] == profile_id:
                return profile
        return None
    
    def get_enabled_profiles(self):
        """Retorna apenas os perfis habilitados"""
        return [p for p in self.profiles if p.get('enabled', True)]
    
    def get_all_profiles(self):
        """Retorna todos os perfis"""
        return self.profiles
    
    @staticmethod
    def ensure_profiles_directory():
        """Garante que o diretório de perfis existe"""
        if not os.path.exists(PROFILES_DIR):
            os.makedirs(PROFILES_DIR)
