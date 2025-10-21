#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script dedicado para limpeza de imagens corrompidas
Remove caracteres $'\n\n' e outros problemas do N8n
"""
import os
import sys

def clean_corrupted_images():
    """Limpa nomes de arquivos corrompidos na pasta imagens"""
    
    IMGS_DIR = "/home/n8n/files/imagens"
    
    if not os.path.exists(IMGS_DIR):
        print("❌ Pasta imagens não existe!")
        return False
    
    print("🧹 LIMPEZA DE IMAGENS CORROMPIDAS")
    print("=" * 50)
    print(f"📁 Pasta: {IMGS_DIR}")
    
    # Listar arquivos antes
    files_before = os.listdir(IMGS_DIR)
    print(f"📋 Arquivos encontrados: {len(files_before)}")
    for f in files_before:
        print(f"  - {repr(f)}")
    
    cleaned_count = 0
    removed_count = 0
    
    for fname in files_before:
        if not os.path.isfile(os.path.join(IMGS_DIR, fname)):
            continue
            
        old_path = os.path.join(IMGS_DIR, fname)
        
        # Verificar se arquivo está vazio
        if os.path.getsize(old_path) == 0:
            os.remove(old_path)
            print(f"🗑️ Removido arquivo vazio: {repr(fname)}")
            removed_count += 1
            continue
        
        # Limpar nome do arquivo
        clean = fname
        
        # Remover caracteres específicos do N8n
        clean = clean.replace('\n', '').replace('\r', '')
        clean = clean.replace("'", "").replace('"', "")
        clean = clean.replace("$'", "").replace("'", "")
        clean = clean.replace("\\n", "").replace("\\r", "")
        
        # Remover $'\n\n' literal
        clean = clean.replace("$'\\n\\n'", "")
        clean = clean.replace("$'\\n'", "")
        
        # Remover espaços extras e caracteres especiais
        clean = clean.strip()
        clean = clean.replace(" ", "_")
        clean = clean.replace("__", "_")
        
        # Se nome mudou, renomear
        if clean != fname and clean:
            new_path = os.path.join(IMGS_DIR, clean)
            try:
                os.rename(old_path, new_path)
                print(f"✅ Renomeado: {repr(fname)} -> {repr(clean)}")
                cleaned_count += 1
            except Exception as e:
                print(f"❌ Erro ao renomear {repr(fname)}: {e}")
        else:
            print(f"⏭️ Mantido: {repr(fname)}")
    
    print("=" * 50)
    print(f"✅ LIMPEZA CONCLUÍDA!")
    print(f"📊 Arquivos limpos: {cleaned_count}")
    print(f"🗑️ Arquivos removidos: {removed_count}")
    
    # Listar arquivos depois
    files_after = os.listdir(IMGS_DIR)
    print(f"📋 Arquivos finais: {len(files_after)}")
    for f in files_after:
        print(f"  - {repr(f)}")
    
    return True

if __name__ == "__main__":
    print("🚀 INICIANDO LIMPEZA DE IMAGENS...")
    success = clean_corrupted_images()
    if success:
        print("🎉 LIMPEZA FINALIZADA COM SUCESSO!")
    else:
        print("❌ ERRO NA LIMPEZA!")
        sys.exit(1)
