# 🤖 Bot de Afiliados para Telegram

Bot automatizado para postar ofertas e produtos com links de afiliados no seu canal do Telegram. Ideal para canais de promoções, cupons e ofertas.

## ✨ Funcionalidades

- 📝 **3 Templates Prontos**: Oferta Relâmpago, Achado do Dia e Cupom Exclusivo
- 🎯 **Botões com Links**: Adicione botões clicáveis com seus links de afiliado
- 🎨 **Formatação HTML**: Posts bonitos com negrito, emojis e destaque
- ⚡ **Fácil de Usar**: Configure e poste em minutos
- 🔄 **Extensível**: Adicione seus próprios templates facilmente

## 📦 O que está incluído?

```
telegram-afiliados-bot/
├── bot.py              # Script principal com templates
├── requirements.txt    # Dependências Python
└── README.md           # Este arquivo
```

## 🚀 Primeiros Passos

### 1️⃣ Pré-requisitos

- Python 3.8 ou superior
- Um bot do Telegram (crie com @BotFather)
- Um canal no Telegram

### 2️⃣ Criar o Bot no Telegram

1. Abra o Telegram e procure por **@BotFather**
2. Envie `/newbot` e siga as instruções
3. Escolha um nome e username para seu bot
4. **Copie o token** que o BotFather te enviar (algo como `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 3️⃣ Adicionar o Bot ao Canal

1. Vá ao seu canal no Telegram
2. Clique no nome do canal > **Administradores**
3. Clique em **Adicionar Administrador**
4. Procure pelo username do seu bot (ex: `@seu_bot`)
5. Dê permissão de **Postar Mensagens**
6. Salve

### 4️⃣ Instalar Dependências

```bash
# Clone o repositório
git clone https://github.com/jonnygarciasapp/telegram-afiliados-bot.git
cd telegram-afiliados-bot

# Instale as dependências
pip install -r requirements.txt
```

### 5️⃣ Configurar o Bot

Abra o arquivo `bot.py` e edite estas linhas:

```python
BOT_TOKEN = 'SEU_TOKEN_AQUI'  # Cole o token do BotFather
CHANNEL_ID = '@seu_canal'      # Username do seu canal (com @)
```

**Alternativa (mais seguro):** Use variáveis de ambiente:

```bash
export BOT_TOKEN="seu_token_aqui"
export CHANNEL_ID="@seu_canal"
```

## 📝 Como Usar

### Método 1: Editar e Executar o Exemplo

O arquivo `bot.py` já vem com um exemplo pronto. Edite os dados do produto e execute:

```python
# No arquivo bot.py, edite este trecho:
texto, keyboard = PostTemplates.oferta_relampago(
    produto="Seu Produto Aqui",
    preco_antigo="199,00",
    preco_novo="99,00",
    desconto_pct=50,
    cupom="MEUCUPOM",
    link_afiliado="https://seu-link-de-afiliado.com",
    frete="GRÁTIS"
)

# Descomente esta linha:
asyncio.run(postar_no_canal(texto, keyboard))
```

Depois execute:

```bash
python bot.py
```

### Método 2: Criar um Script Personalizado

Crie um arquivo novo (ex: `meu_post.py`):

```python
import asyncio
from bot import PostTemplates, postar_no_canal

# Template 1: Oferta Relâmpago
texto, keyboard = PostTemplates.oferta_relampago(
    produto="Xiaomi Redmi 13C 128GB",
    preco_antigo="1.299,00",
    preco_novo="899,00",
    desconto_pct=31,
    cupom="MEUOFERTA",
    link_afiliado="https://mercadolivre.com/seu-link",
    frete="GRÁTIS"
)

asyncio.run(postar_no_canal(texto, keyboard))
```

Execute:

```bash
python meu_post.py
```

## 🎨 Templates Disponíveis

### 1. Oferta Relâmpago

Para produtos com desconto alto e prazo limitado:

```python
texto, keyboard = PostTemplates.oferta_relampago(
    produto="Nome do Produto",
    preco_antigo="199,00",
    preco_novo="99,00",
    desconto_pct=50,
    cupom="CUPOM10",
    link_afiliado="https://seu-link.com",
    frete="GRÁTIS"  # ou "R$ 15,00"
)
```

### 2. Achado do Dia

Para produtos curados com avaliações:

```python
texto, keyboard = PostTemplates.achado_do_dia(
    produto="Air Fryer 5L",
    preco="299,00",
    parcelas="12",
    avaliacoes="2.547",
    nota="4.8",
    beneficios=[
        "Capacidade de 5 litros",
        "7 programas pré-definidos",
        "Cozinha sem óleo"
    ],
    link_afiliado="https://seu-link.com",
    link_vip="https://t.me/seu_grupo"  # Opcional
)
```

### 3. Cupom Exclusivo

Para promoções com cupom:

```python
texto, keyboard = PostTemplates.cupom_exclusivo(
    titulo="LEVE 3 PAGUE 2",
    produto="Cosméticos Selecionados",
    preco_unitario="49,90",
    preco_final="99,80",  # Preço de 3 produtos
    cupom="LEVE3",
    link_afiliado="https://seu-link.com",
    validade="31/10/2025",
    link_vip="https://t.me/seu_grupo"  # Opcional
)
```

## ⚙️ Personalizações Avançadas

### Adicionar Novo Template

Edite `bot.py` e adicione na classe `PostTemplates`:

```python
@staticmethod
def meu_template_customizado(titulo, descricao, link):
    texto = f"""
🎉 <b>{titulo}</b>

{descricao}
    """
    
    keyboard = [[InlineKeyboardButton("🛍️ COMPRAR", url=link)]]
    return texto, keyboard
```

### Agendar Posts Automáticos

Instale a biblioteca `apscheduler` (já está no `requirements.txt`):

```python
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio

async def postar_automatico():
    # Seu código de post aqui
    texto, keyboard = PostTemplates.oferta_relampago(...)
    await postar_no_canal(texto, keyboard)

scheduler = AsyncIOScheduler()

# Postar todos os dias às 9h e 18h
scheduler.add_job(postar_automatico, 'cron', hour='9,18')

scheduler.start()
print("🔄 Bot rodando... Pressione Ctrl+C para parar")

# Mantém o bot rodando
asyncio.get_event_loop().run_forever()
```

## 🛠️ Troubleshooting

### Erro: "Chat not found"

- Verifique se o bot é administrador do canal
- Use `@` antes do username: `@seu_canal`
- Ou use o ID numérico do canal (ex: `-1001234567890`)

### Erro: "Unauthorized"

- Verifique se o token está correto
- Gere um novo token com @BotFather se necessário

### Bot não posta

1. Verifique as permissões do bot no canal
2. Teste com um grupo privado primeiro
3. Verifique os logs de erro no terminal

### Como pegar o ID numérico do canal?

1. Adicione o bot @userinfobot ao seu canal
2. Ele enviará o ID do canal
3. Use esse ID no lugar de `@username`

## 📚 Links Úteis

- [Documentação python-telegram-bot](https://docs.python-telegram-bot.org/)
- [Como criar um bot no Telegram](https://core.telegram.org/bots/tutorial)
- [Formatação de mensagens](https://core.telegram.org/bots/api#formatting-options)

## 👥 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

- Reportar bugs
- Sugerir novos templates
- Enviar pull requests
- Melhorar a documentação

## ⚠️ Aviso Legal

Este bot é fornecido "como está" para fins educacionais. Certifique-se de:

- Respeitar os termos de serviço do Telegram
- Seguir as regras dos programas de afiliados que usar
- Divulgar claramente que usa links de afiliados
- Não fazer spam ou enviar mensagens não solicitadas

## 💬 Suporte

Teve problemas? Abra uma [issue](https://github.com/jonnygarciasapp/telegram-afiliados-bot/issues) no GitHub!

---

Feito com ❤️ para ajudar afiliados a automatizar seus canais no Telegram
