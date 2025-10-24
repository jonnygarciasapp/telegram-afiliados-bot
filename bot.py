#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bot de Afiliados para Telegram
Posta ofertas automaticamente no canal com links de afiliados
COM SUPORTE A FOTOS!
"""

import os
import asyncio
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from datetime import datetime

# ========== CONFIGURAÇÃO ==========
# Adicione suas credenciais aqui ou use variáveis de ambiente
BOT_TOKEN = os.getenv('BOT_TOKEN', '7956930899:AAFHLdd-K5rIlhmwS8w6C-plw4-cu00EcIE')
CHANNEL_ID = os.getenv('CHANNEL_ID', '@oreidoachado')  # Pode ser @username ou ID numérico

# ========== CONFIGURAÇÃO DE AFILIADOS ==========
# IMPORTANTE: Adicione seus IDs de afiliado aqui!
AFFILIATE_IDS = {
    'mercadolivre': 'SEU_ID_MERCADOLIVRE',  # Ex: MLB-123456
    'amazon': 'SEU_ID_AMAZON',              # Ex: tag=seuafiliado-20
    'shopee': 'SEU_ID_SHOPEE',              # Ex: affiliate_id=123456
    'magalu': 'SEU_ID_MAGALU',
    'americanas': 'SEU_ID_AMERICANAS',
}

# ========== TEMPLATES DE POSTS ==========
class PostTemplates:
    @staticmethod
    def oferta_relampago(produto, preco_antigo, preco_novo, desconto_pct, cupom, link_afiliado, foto_url=None, frete="GRÁTIS"):
        """Template para ofertas relâmpago"""
        texto = f"""🚨 <b>OFERTA RELÂMPAGO</b> 🔥

📦 <b>{produto}</b>
💰 De R$ {preco_antigo} por <b>R$ {preco_novo}</b>
🟩 {desconto_pct}% OFF | Frete {frete}

🎫 <b>Cupom: {cupom}</b>

🔥 Corre! Estoque limitado
⚠️ Ative as notificações para não perder"""
        
        keyboard = [[InlineKeyboardButton("🛍️ COMPRAR AGORA", url=link_afiliado)]]
        if foto_url:
            keyboard.append([InlineKeyboardButton("👀 VER FOTO", url=foto_url)])
        
        return texto, InlineKeyboardMarkup(keyboard), foto_url

    @staticmethod
    def achado_do_dia(titulo, produto, preco_unitario, preco_final, cupom, link_afiliado, foto_url=None, link_vip=None, validade=None):
        """Template para achados do dia"""
        texto = f"""💎 <b>ACHADO DO DIA</b> 💎

🏷️ <b>{titulo}</b>
{produto}

💵 Valor: R$ {preco_unitario}
💰 Com cupom: <b>R$ {preco_final}</b>

🎫 <b>Cupom: {cupom}</b>
"""
        
        if validade:
            texto += f"\n⏰ Válido até {validade}\n"
        
        texto += "\n📢 R$ (preço) em até (parcelas)x sem juros\n"
        texto += "\n✨ <b>Por que vale a pena?</b>\n{beneficios_texto}"
        
        keyboard = [[InlineKeyboardButton("🛒 GARANTA O SEU", url=link_afiliado)]]
        if link_vip:
            keyboard.append([InlineKeyboardButton("👑 GRUPO VIP", url=link_vip)])
        
        return texto, InlineKeyboardMarkup(keyboard), foto_url

    @staticmethod
    def cupom_exclusivo(titulo, produto, preco_unitario, preco_final, cupom, link_afiliado, foto_url=None, link_vip=None, validade=None):
        """Template para cupons exclusivos"""
        texto = f"""🎯 <b>CUPOM EXCLUSIVO</b> 🔥

🏷️ <b>{titulo}</b>
{produto}

💵 Valor: R$ {preco_unitario}
💰 Com cupom: <b>R$ {preco_final}</b>

🎫 <b>Cupom: {cupom}</b>
"""
        
        if validade:
            texto += f"\n⏰ Válido até {validade}\n"
        
        texto += "\n🔥 Corre! Estoque limitado\n"
        texto += "⚠️ Ative as notificações para não perder"
        
        keyboard = [[InlineKeyboardButton("🛍️ APROVEITE AGORA", url=link_afiliado)]]
        if link_vip:
            keyboard.append([InlineKeyboardButton("👑 GRUPO VIP", url=link_vip)])
        
        return texto, InlineKeyboardMarkup(keyboard), foto_url

# ========== FUNÇÃO PARA ADICIONAR ID DE AFILIADO ==========
def adicionar_afiliado(url_produto, plataforma='mercadolivre'):
    """
    Adiciona seu ID de afiliado à URL do produto
    
    Parâmetros:
    - url_produto: URL original do produto
    - plataforma: 'mercadolivre', 'amazon', 'shopee', etc.
    
    Retorna: URL com seu ID de afiliado
    """
    affiliate_id = AFFILIATE_IDS.get(plataforma, '')
    
    if not affiliate_id or affiliate_id.startswith('SEU_ID'):
        print(f"⚠️ AVISO: Configure seu ID de afiliado para {plataforma}!")
        return url_produto
    
    # Adiciona o ID de afiliado conforme a plataforma
    if plataforma == 'mercadolivre':
        separador = '&' if '?' in url_produto else '?'
        return f"{url_produto}{separador}mshops_id={affiliate_id}"
    
    elif plataforma == 'amazon':
        separador = '&' if '?' in url_produto else '?'
        return f"{url_produto}{separador}{affiliate_id}"
    
    elif plataforma == 'shopee':
        separador = '&' if '?' in url_produto else '?'
        return f"{url_produto}{separador}affiliate_id={affiliate_id}"
    
    else:
        # Para outras plataformas, adicione a lógica aqui
        return url_produto

# ========== FUNÇÃO PRINCIPAL PARA POSTAR ==========
async def postar_no_canal(texto, keyboard, foto_url=None):
    """
    Posta no canal do Telegram com ou sem foto
    
    Parâmetros:
    - texto: Texto do post
    - keyboard: Botões inline
    - foto_url: URL da foto do produto (opcional)
    """
    try:
        bot = Bot(token=BOT_TOKEN)
        
        if foto_url:
            # Posta com foto
            message = await bot.send_photo(
                chat_id=CHANNEL_ID,
                photo=foto_url,
                caption=texto,
                parse_mode=ParseMode.HTML,
                reply_markup=keyboard,
            )
            print(f"📸 Post com foto publicado com sucesso! ID: {message.message_id}")
        else:
            # Posta só texto
            message = await bot.send_message(
                chat_id=CHANNEL_ID,
                text=texto,
                parse_mode=ParseMode.HTML,
                reply_markup=keyboard,
            )
            print(f"✅ Post publicado com sucesso! ID: {message.message_id}")
        
        print(f"🔗 Link: https://t.me/{CHANNEL_ID.replace('@', '')}/{message.message_id}")
        print(f"\n📝 Preview do post:")
        print(texto)
        
        return message
    
    except Exception as e:
        print(f"❌ Erro ao postar: {e}")
        return None

# ========== EXEMPLO DE USO ==========
if __name__ == "__main__":
    # Exemplo 1: Oferta Relâmpago COM FOTO
    url_produto = "https://mercadolivre.com.br/produto-exemplo"
    link_com_afiliado = adicionar_afiliado(url_produto, 'mercadolivre')
    
    texto, keyboard, foto = PostTemplates.oferta_relampago(
        produto="Xiaomi Redmi 13C 128GB",
        preco_antigo="1.299,00",
        preco_novo="899,00",
        desconto_pct=31,
        cupom="MEUOFERTA",
        link_afiliado=link_com_afiliado,
        foto_url="https://http2.mlstatic.com/D_NQ_NP_2X_682045-MLU74977522685_032024-F.webp"  # FOTO DO PRODUTO!
    )
    
    # Para postar, descomente a linha abaixo:
    asyncio.run(postar_no_canal(texto, keyboard, foto))
    
    print("\n" + "="*50)
    print("📋 INSTRUÇÕES PARA USO:")
    print("="*50)
    print("\n1. Configure seus IDs de afiliado nas linhas 21-27")
    print("\n2. Para postar, use este padrão:")
    print("\n   url_produto = 'https://...'")
    print("   link_afiliado = adicionar_afiliado(url_produto, 'mercadolivre')")
    print("\n   texto, keyboard, foto = PostTemplates.oferta_relampago(")
    print("       produto='Nome do Produto',")
    print("       preco_antigo='999,00',")
    print("       preco_novo='699,00',")
    print("       desconto_pct=30,")
    print("       cupom='MEUCUPOM',")
    print("       link_afiliado=link_afiliado,")
    print("       foto_url='https://url-da-foto-do-produto.jpg'")
    print("   )")
    print("\n   asyncio.run(postar_no_canal(texto, keyboard, foto))")
    print("\n3. Para encontrar a URL da foto:")
    print("   - Vá na página do produto")
    print("   - Clique com botão direito na imagem")
    print("   - Copiar endereço da imagem")
    print("\n" + "="*50)
