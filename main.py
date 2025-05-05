import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.graph_objects as go
from database import init_db, salvar_comentario, carregar_comentarios
import easyocr
import cv2
import numpy as np
import re

# Chama a função de banco de dados
init_db()

# Nome do App
st.set_page_config(page_title="FURIA App", layout="wide")
st.title("FURIA - KNOW YOUR FÃ")

# Menu de Navegação
abas = st.tabs(["HOME","CADASTRO", "FURIA CS2", "LOJA", "CONTATO"])

# HOME
with abas[0]:
    st.subheader("")
    st.markdown("## 🐾 Bem-vindo, fã da FURIA!")
    st.write("""
    Ser fã da organização FURIA é admirar mais do que apenas uma equipe de CS2 - é apoiar um projeto que representa garra, inovação e brasilidade no cenário mundial dos esports. A FURIA é sinônimo de atitude dentro e fora dos servidores, com uma identidade forte e uma visão de futuro que inspira seus fãs. A organização valoriza não só os resultados, mas também a cultura, o estilo e a comunidade que construiu. Ser fã da FURIA é sentir orgulho ao ver a Pantera estampada em produtos, arenas e transmissões. É reconhecer o trabalho sério nos bastidores, com investimentos em estrutura, talentos e formação de base. É acompanhar não só o CS, mas também os outros projetos da organização, como conteúdo, moda e ações sociais. A FURIA vai além do jogo — ela constrói um movimento. E quem é fã, vive isso no dia a dia, com paixão e pertencimento. Ser FURIA é fazer parte de uma revolução nos esports brasileiros.
    """)
    st.divider()
    # Seção da enquete
    st.subheader("Enquete - O quanto você é fã da FURIA?")
    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        comprou_produto = st.radio(
            "🛍️ Você já comprou algum produto da FURIA?",
            ["Sim", "Não"]
        )

    with col2:
        acompanha_jogos = st.radio(
            "🎮 Você acompanha os jogos dos times da FURIA?",
            ["Sim, sempre", "Às vezes", "Raramente", "Nunca"]
        )

    colone, coltwo = st.columns(2)
    with colone:
        time_ganhar = st.radio(
            "🎮 Você acha que o time da FURIA vai ser campeão com essa nova line?",
            ["Sim", "Talvez", "Não", "Nunca"]
        )

    with coltwo:
         rede_social = st.radio(
             "Onde você assiste os jogos da FURIA?",
             ["Twitch", "Youtube"]
         )
    jogo_torce = st.selectbox(
        "📺 Você sempre torce para o time da FURIA?",
        ["Sim", "Não", "Algumas vezes"]
    )

    # Pergunta 4
    redes_sociais = st.multiselect(
        "📲 Em quais redes sociais você mais posta ou vê conteúdos sobre a FURIA?",
        ["Twitter/X", "Instagram", "TikTok", "Facebook", "Reddit", "Discord"]
    )

    # Pergunta 5
    jogadores_favoritos = st.multiselect(
        "🌟 Quem são seus jogadores favoritos da FURIA?",
        ["FalleN", "Kscerato", "Yuurih", "Molodoy", "Yekindar", "Outro"]
    )

    # Pergunta 6
    nota_fan = st.slider(
        "🔥 De 0 a 10, quanto você se considera fã da FURIA?",
        0, 10, 5
    )

    # Resultado opcional ao clicar no botão
    if st.button("📩 Enviar respostas"):
        st.success("Obrigado por participar da pesquisa! 💥")

        st.markdown("### ✅ Suas respostas:")
        st.write(f"🛍️ Já comprou produto? **{comprou_produto}**")
        st.write(f"🎮 Acompanha os jogos? **{acompanha_jogos}**")
        st.write(f"📺 Onde assiste? **{jogo_torce}**")
        st.write(f"📲 Redes que usa para FURIA: **{', '.join(redes_sociais)}**")
        st.write(f"🌟 Jogadores favoritos: **{', '.join(jogadores_favoritos)}**")
        st.write(f"🔥 Nível de fã: **{nota_fan}/10**")

    st.subheader("")

    # Botões para seguir na rede sociais
    st.markdown("### 📲 Siga a FURIA nas redes sociais e participe dos nossos sorteios!!")

    # Função para exibir os botões das redes sociais
    def social_buttons():
        st.markdown("""
                <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                    <a href="https://x.com/furia" target="_blank">
                        <button style="background-color:#000000;color:white;padding:10px 20px;border:none;border-radius:5px;cursor:pointer;">
                            Twitter
                        </button>
                    </a>
                    <a href="https://www.instagram.com/furiagg/" target="_blank">
                        <button style="background-color:#8134AF;color:white;padding:10px 20px;border:none;border-radius:5px;cursor:pointer;">
                            Instagram
                        </button>
                    </a>
                    <a href="https://www.twitch.tv/furiatv" target="_blank">
                        <button style="background-color:#9146FF;color:white;padding:10px 20px;border:none;border-radius:5px;cursor:pointer;">
                            Twitch
                        </button>
                    </a>
                    <a href="https://www.tiktok.com/@furia" target="_blank">
                        <button style="background-color:#FE2C55;color:white;padding:10px 20px;border:none;border-radius:5px;cursor:pointer;">
                            TikTok
                        </button>
                    </a>
                    <a href="https://www.facebook.com/furiagg" target="_blank">
                        <button style="background-color:#1877F2;color:white;padding:10px 20px;border:none;border-radius:5px;cursor:pointer;">
                            Facebook
                        </button>
                    </a>
                </div>
            """, unsafe_allow_html=True)

    # Chama a função para exibir os botões
    social_buttons()

    st.write("")
    # Sorteio para os fãns
    st.subheader("🎁 Sorteio da FURIA - 10/05/2025")

    st.write("Confira os itens que serão sorteados:")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("https://furiagg.fbitsstatic.net/img/p/moletom-careca-furia-classic-2-preto-150186/337164-1.jpg?w=468&h=468&v=202501231555", caption="Moletom FURIA Black")
    with col2:
        st.image("https://furiagg.fbitsstatic.net/img/p/camiseta-furia-oficial-24-preta-150177/336897-1.jpg?w=468&h=468&v=202502121640", caption="Camisa FURIA")
    with col3:
        st.image("https://furiagg.fbitsstatic.net/img/p/bone-59fifty-furia-x-new-era-preto-e-branco-150193/336989-1.jpg?w=468&h=468&v=no-value", caption="Boné FURIA")

    st.markdown("""
    No dia **10/05/2025**, a FURIA vai realizar um super sorteio para a torcida!  
    Serão três prêmios exclusivos: um moletom preto, uma camisa e um boné — todos oficiais da coleção FURIA.  
    Para participar, é simples: segue as redes sociais da FURIA. Essa é a chance perfeita de representar a Pantera com estilo e ainda fortalecer sua conexão com a organização.  
    Fique ligado nas redes sociais da FURIA para mais informações e boa sorte! 🐾🔥  
    """)
    # Videos sobre os jogos da FURIA

    st.subheader("Highlights FURIA")
    st.write("")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.video("https://www.youtube.com/watch?v=vFPo6WiBrXw")

    with col2:
        st.video("https://www.youtube.com/watch?v=-DPTntPa_Ig")

    with col3:
        st.video("https://www.youtube.com/watch?v=6YY6AkHOm14")

    # Videos sobre os vlogs da FURIA

    st.subheader("Vlogs FURIA")
    st.write("")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.video("https://www.youtube.com/watch?v=Dee2b9p8POE")

    with col2:
        st.video("https://www.youtube.com/watch?v=eGXP599-GXc")

    with col3:
        st.video("https://www.youtube.com/watch?v=54ESQcaVxXE")

    # Uma aba com a stream FURIA da twitch para os fã se entreterem

    st.title("STREAM FURIA")
    components.html("""
        <div style="display: flex; justify-content: center;">
            <iframe
                src="https://player.twitch.tv/?channel=furiatv&parent=localhost"
                height="500"
                width="850"
                allowfullscreen="true">
            </iframe>
        </div>
    """, height=500)

    # Footer FURIA
    st.markdown("""
        <hr style="margin-top: 50px;"/>
        <div style="text-align: center; color: gray; font-size: 14px;">
            © 2025 FURIA Fansite. Todos os direitos reservados. <br>
            Feito com 💙 por fãs da FURIA.
        </div>
    """, unsafe_allow_html=True)

with abas[1]:
    st.title("CADASTRO")

    st.subheader("Faça seu cadastro e entre para nossa família furioso(a)")
    with st.form("cadastro_fan"):
        nome = st.text_input("Nome")
        email = st.text_input("E-mail")
        endereco = st.text_input("Endereço")
        cidade = st.text_input("Cidade")
        cpf = st.text_input("CPF")
        instagram = st.text_input("Instagram (opcional)")
        interesse = st.multiselect("Do que você mais gosta na FURIA?",
                                   ["Jogadores", "Times", "História", "Eventos", "Loja"])
        uploaded_file = st.file_uploader("Envie a imagem do CPF(frente) para validação dos dados", type=["jpg", "jpeg", "png"])

        if uploaded_file:
            # Lê e mostra a imagem
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            image = cv2.imdecode(file_bytes, 1)
            st.image(image, channels="BGR", caption="Imagem enviada")

            # OCR com EasyOCR
            with st.spinner("🔍 Extraindo texto..."):
                reader = easyocr.Reader(['pt'])
                results = reader.readtext(image, detail=0)
                texto = " ".join(results)
                st.subheader("📝 Texto extraído:")
                st.text(texto)

            # === Validações ===
            st.subheader("✅ Validações:")

            # CPF
            cpf = re.search(r"\d{3}\.\d{3}\.\d{3}-\d{2}", texto)
            if cpf:
                st.success(f"CPF encontrado: {cpf.group()}")
            else:
                st.warning("CPF não encontrado.")

            # Data de validade
            validade = re.search(r"\d{2}/\d{2}/\d{4}", texto)
            if validade:
                st.success(f"Data de validade: {validade.group()}")
            else:
                st.warning("Data de validade não identificada.")

            # Nome (pega palavra após "Nome" ou "Nome:")
            nome = ""
            for i, word in enumerate(results):
                if "nome" in word.lower():
                    if i + 1 < len(results):
                        nome = results[i + 1]
                    break
            if nome:
                st.success(f"Nome identificado: {nome}")
            else:
                st.warning("Nome não identificado.")
        consent = st.checkbox("Autorizo o uso dos meus dados para melhorar minha experiência")
        if st.form_submit_button("Enviar"):
            if consent:
                st.success("Perfil feito com sucesso!")
                st.balloons()
            else:
                st.warning("Você precisa autorizar o uso dos dados para continuar.")


    # FURIA CS2
with abas[2]:
    st.title("Equipe FURIA CS2")

    # Informações dos jogadores

    st.subheader("Jogadores Atuais")
    st.markdown("""
    - **FalleN** (IGL / Rifler / Suport)  
    - **Yuurih** (Rifler)  
    - **Kscerato** (Rifler)  
    - **Molodoy** (AWP)  
    - **Yekindar** (Entry)  
    """)
    st.divider()


    # Estatísticas dos jogadores

    st.subheader("⭐ Estatísticas dos Jogadores")

    jogadores = pd.DataFrame({
        "Jogador": ["FalleN", "Yuurih", "Kscerato", "Molodoy", "Yekindar"],
        "Rating 2.0": [1.12, 1.18, 1.20, 1.05, 1.03],
        "K/D": [1.10, 1.22, 1.25, 0.98, 1.00],
        "Entry %": [10, 15, 8, 20, 12]
    })

    st.dataframe(jogadores.set_index("Jogador"), height=220)
    st.divider()

    # Desempenho por mapa
    st.subheader("🗺️ Winrate por Mapa")

    mapas = pd.DataFrame({
        "Mapa": ["Mirage", "Inferno", "Nuke", "Ancient", "Overpass"],
        "Winrate (%)": [60, 75, 50, 40, 55]
    })

    fig_mapas = go.Figure(data=[
        go.Bar(x=mapas["Mapa"], y=mapas["Winrate (%)"], marker_color="purple")
    ])
    fig_mapas.update_layout(title="Vitórias por mapa (últimos jogos)", yaxis=dict(range=[0, 100]))
    st.plotly_chart(fig_mapas, use_container_width=True)
    st.divider()

    # Resultados recentes

    st.subheader("📅 Resultados Recentes")

    resultados = pd.DataFrame({
        "Data": ["22/03/2025", "06/04/2025", "07/04/2025","08/04/2025", "09/04/2025" ],
        "Adversário": ["M80", "Betclic", "Complexity", "Virtus.pro", "The MongolZ"],
        "Resultado": ["2-1", "2-0", "2-1", "2-0", "2-0"],
        "Vitória": ["❌", "✅", "❌", "❌", "❌"]
    })

    st.table(resultados)

    # Tabela de desempenho
    st.subheader("📈 Estatísticas em Torneios")

    stats_torneios = pd.DataFrame({
        "Torneio": ["PGL Astana", "IEM Dallas", "BLAST Austin"],
        "Vitórias": [4, 2, 3],
        "Derrotas": [1, 2, 1],
        "KD médio": [1.15, 1.05, 1.10]
    })
    st.dataframe(stats_torneios.set_index("Torneio"))

    # Destaque individual
    st.subheader("🏅 Destaque da Semana")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.write("FalleN")
    with col2:
        st.write(
            "**FalleN** foi o destaque da semana com média de **1.12 de rating**, clutchs decisivos e impacto tático nos rounds de CT.")

    st.subheader("Vote no percentual de vitória nos próximos jogos")
    percentual = st.slider("Qual a chance da FURIA ganhar o próximo jogo?", 0, 100, 70)
    st.write(f"Você votou: {percentual}%")

    # Secão de comentários para os fã darem um feedback

    st.subheader("Faça seu comentário e interaja com nossa comunidade!")
    with st.form("comentario_form"):
        nome = st.text_input("Seu nome")
        comentario = st.text_area("Deixe seu comentário sobre a equipe")
        enviar = st.form_submit_button("Enviar comentário")

        if enviar:
            if nome and comentario:
                salvar_comentario(nome, comentario)
                st.success("Comentário enviado! Go FURIA! 💪")
            else:
                st.error("Por favor, preencha seu nome e comentário.")

    st.markdown("---")
    st.subheader("Comentários anteriores:")
    comentarios = carregar_comentarios()
    if comentarios:
        for nome, texto in comentarios:
            st.markdown(f"**{nome}** disse:")
            st.write(f"> {texto}")
            st.markdown("---")
    else:
        st.write("Ainda não há comentários. Seja o primeiro a comentar! 🎉")

# LOJA
with abas[3]:
    st.title("Lançamentos Furia")
    st.write("🛒 Confira mais no [site oficial da FURIA](https://www.furia.gg/)")
    st.subheader("Camisas, Moletons , Jaqueta , Mochila , Calça")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("https://furiagg.fbitsstatic.net/img/p/camiseta-oficial-furia-adidas-preta-150265/337491-1.jpg?w=468&h=468&v=202503281009", caption="Camiseta Oficial Furia | Adidas Preta")
    with col2:
        st.image("https://furiagg.fbitsstatic.net/img/p/jaqueta-college-my-hero-academia-x-furia-azul-150230/337255-2.jpg?w=468&h=468&v=no-value", caption="Jaqueta College My Hero Academia x Furia Azul")
    with col3:
        st.image("https://furiagg.fbitsstatic.net/img/p/moletom-my-hero-academia-x-furia-bakugo-preto-150232/337269-2.jpg?w=468&h=468&v=no-value", caption="Moletom My Hero Academia x Furia Bakugo Preto")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("https://furiagg.fbitsstatic.net/img/p/camiseta-furia-x-champion-college-off-white-150165/336813-2.jpg?w=468&h=468&v=no-value",caption="Camiseta Furia x Champion College Off White")
    with col2:
        st.image("https://furiagg.fbitsstatic.net/img/p/camiseta-furia-future-is-black-sankofa-amarela-150147/336687-2.jpg?w=468&h=468&v=no-value", caption="Camiseta Furia Future is Black Sankofa Amarela")
    with col3:
        st.image("https://furiagg.fbitsstatic.net/img/p/calca-jogger-furia-preta-150198/337022-2.jpg?w=468&h=468&v=no-value", caption="Calça Jogger Furia Preta")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image(
            "https://furiagg.fbitsstatic.net/img/p/jaqueta-furia-future-is-black-preta-150150/336708-1.jpg?w=468&h=468&v=no-value",caption="Jaqueta Furia Future Is Black Preta")
    with col2:
        st.image(
            "https://furiagg.fbitsstatic.net/img/p/sacochila-furia-fc-preta-150266/337498-1.jpg?w=468&h=468&v=202504101319",caption="Sacochila Furia Preta")
    with col3:
        st.image(
            "https://furiagg.fbitsstatic.net/img/p/moletom-careca-furia-future-is-black-preto-150151/336715-2.jpg?w=468&h=468&v=no-value",caption="Moletom Careca Furia Future is Black Preto")

    # Inicializa os contadores se ainda não existirem
    if 'votos_sim' not in st.session_state:
        st.session_state.votos_sim = 0
    if 'votos_nao' not in st.session_state:
        st.session_state.votos_nao = 0
    if 'votou' not in st.session_state:
        st.session_state.votou = False

    # Mini enquete
    st.subheader("Você gostou do lançamento do drop FURIA x Adidas?")

    # Botões de voto
    if not st.session_state.votou:
            if st.button("Sim"):
                st.session_state.votos_sim += 1
                st.session_state.votou = True
            if st.button("Não"):
                st.session_state.votos_nao += 1
                st.session_state.votou = True
    else:
        st.info("Você já votou! Obrigado pelo seu feedback. 💜")

    # Resultados
    total = st.session_state.votos_sim + st.session_state.votos_nao
    if total > 0:
        st.subheader("Resultado parcial:")
        st.write(f"👍 Sim: {st.session_state.votos_sim} votos")
        st.write(f"👎 Não: {st.session_state.votos_nao} votos")
        st.progress(st.session_state.votos_sim / total)
    else:
        st.write("Nenhum voto registrado ainda.")

# CONTATO
with abas[4]:
    st.subheader("Fale com o suporte da FURIA")
    nome = st.text_input("Nome")
    Assunto = st.text_input("Assunto")
    email = st.text_input("E-mail")
    mensagem = st.text_area("Digite sua mensagem")

    if st.button("Enviar"):
        if nome and email and mensagem:
            st.success("Mensagem enviada com sucesso! ⚡ A FURIA agradece o contato.")
            # Aqui você poderia adicionar lógica para armazenar ou enviar essa mensagem, tipo um envio por e-mail ou salvar em um banco de dados
        else:
            st.warning("Por favor, preencha todos os campos antes de enviar.")

