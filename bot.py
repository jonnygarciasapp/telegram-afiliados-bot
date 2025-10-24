#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bot de Afiliados para Telegram
Posta ofertas automaticamente no canal com links de afiliados
"""

import os
import asyncio
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from datetime import datetime

# ========== CONFIGURAÇÃO ==========
# Adicione suas credenciais aqui ou use variáveis de ambiente
BOT_TOKEN = os.getenv('BOT_TOKEN', 'SEU_TOKEN_AQUI')
CHANNEL_ID = os.getenv('CHANNEL_ID', '@oreidoachado')  # Pode ser @username ou ID numérico

# ========== TEMPLATES DE POSTS ==========

class PostTemplates:
    @staticmethod
    def oferta_relampago(produto, preco_antigo, preco_novo, desconto_pct, cupom, link_afiliado, frete="GRÁTIS"):
        """Template para ofertas relâmpago"""
        texto = f"""🚨 <b>OFERTA RELÂMPAGO</b> 🔥

📦 <b>{produto}</b>
💰 De R$ {preco_antigo} por <b>R$ {preco_novo}</b>
📊 {desconto_pct}% OFF | Frete {frete}

🏟️ <b>Cupom: {cupom}</b>

⏰ Corre! Estoque limitado
🔔 Ative as notificações para não perder
"""
        
        keyboard = [[InlineKeyboardButton("🛍️ COMPRAR AGORA", url=link_afiliado)]]
        return texto, keyboard
    
    @staticmethod
    def achado_do_dia(produto, preco, parcelas, avaliacoes, nota, beneficios, link_afiliado, link_vip=None):
        """Template para curadoria do dia"""
        beneficios_texto = "\n".join([f"• {b}" for b in beneficios])
        
        texto = f"""💎 <b>ACHADO DO DIA</b>

📦 <b>{produto}</b>
⭐ Avaliação: {nota}/5 ({avaliacoes} avaliações)

💵 R$ {preco} em até {parcelas}x sem juros

✅ <b>Por que vale a pena?</b>
{beneficios_texto}
"""
        
        keyboard = [[InlineKeyboardButton("🛍️ GARANTA O SEU", url=link_afiliado)]]
        if link_vip:
            keyboard.append([InlineKeyboardButton("👥 GRUPO VIP", url=link_vip)])
        
        return texto, keyboard
    
    @staticmethod
    def cupom_exclusivo(titulo, produto, preco_unitario, preco_final, cupom, link_afiliado, validade, link_vip=None):
        """Template para cupons exclusivos"""
        texto = f"""🏆 <b>CUPOM EXCLUSIVO</b>

🎁 <b>{titulo}</b>
{produto}

💰 Valor: R$ {preco_unitario}
🏟️ Com cupom: <b>R$ {preco_final}</b>

📌 <b>CUPOM: {cupom}</b>

⚡ Válido até {validade}
"""
        
        keyboard = [[InlineKeyboardButton("🛍️ APROVEITE AGORA", url=link_afiliado)]]
        if link_vip:
            keyboard.append([InlineKeyboardButton("👥 GRUPO VIP", url=link_vip)])
        
        return texto, keyboard

# ========== FUNÇÕES DO BOT ==========

async def postar_no_canal(texto, keyboard=None):
    """
    Posta uma mensagem no canal
    
    Args:
        texto: Texto da mensagem (pode usar HTML)
        keyboard: Lista de botões inline (opcional)
    """
    bot = Bot(token=BOT_TOKEN)
    
    try:
        reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None
        
        message = await bot.send_message(
            chat_id=CHANNEL_ID,
            text=texto,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup,
            disable_web_page_preview=False
        )
        
        print(f"✅ Post publicado com sucesso! ID: {message.message_id}")
        print(f"🔗 Link: https://t.me/{CHANNEL_ID.replace('@', '')}/{message.message_id}")
        return message
        
    except Exception as e:
        print(f"❌ Erro ao postar: {e}")
        return None

# ========== EXEMPLO DE USO ==========

if __name__ == "__main__":
    # Exemplo 1: Oferta Relâmpago
    texto, keyboard = PostTemplates.oferta_relampago(
        produto="Xiaomi Redmi 13C 128GB",
        preco_antigo="1.299,00",
        preco_novo="899,00",
        desconto_pct=31,
        cupom="MEUOFERTA",
        link_afiliado="https://mercadolivre.com/seu-link-afiliado",
        frete="GRÁTIS"
    )
    
    # Para postar, descomente a linha abaixo:
    # asyncio.run(postar_no_canal(texto, keyboard))
    
    print("📝 Preview do post:\n")
    print(texto)
    print("\n🔗 Botões:", [btn[0].text for btn in keyboard])
