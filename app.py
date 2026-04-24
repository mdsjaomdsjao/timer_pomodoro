import streamlit as st
import streamlit.components.v1 as components
import time
import base64
import uuid 

if "rodando" not in st.session_state:
    st.session_state.rodando = False

titulo = st.markdown("<h1 style='text-align: center; color: white; margin-bottom: 15%;'> Timer Pomodoro </h1>", unsafe_allow_html=True)

def tocar_notificacao(tipo):
    if tipo.lower() == 'estudo':
        arquivo = 'som_estudo_finalizado.mp3'
    else:        
        arquivo = 'som_pausa_finalizada.mp3'
        
    # carrega o arquivo de áudio e converte para Base64
    with open(arquivo, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()

    # injeta JavaScript puro para criar o áudio e forçar o play no navegador.
    # uuid.uuid4() gera uma string única toda vez que a função é chamada.
    # isso evita que o Streamlit ignore o código achando que já o executou antes.
    js_code = f"""
        <script id="{uuid.uuid4()}">
            var audio = new Audio("data:audio/mp3;base64,{b64}");
            audio.play().catch(function(error) {{
                console.log("O navegador bloqueou o áudio: ", error);
            }});
        </script>
    """
    
    # renderizando o script de forma invisível (height=0, width=0)
    components.html(js_code, height=0, width=0)

def pomodoro(tempo_estudo, tempo_intervalo):
    timer = st.empty()
    # pra testes usar velocidade menor ex: 0.005
    velocidade = 1

    # estudo
    total = tempo_estudo * 60
    for restante in range(total, -1, -1):
        if not st.session_state.rodando:
            break
        minutos, segundos = divmod(restante, 60)
        timer.metric("Estudo", f"{minutos:02d}:{segundos:02d}")
        time.sleep(velocidade)

    # verifica se realmente terminou ou se foi interrompido no botão PARAR
    if st.session_state.rodando:
        notif_pausa = st.info('Hora do Intervalo!')
        tocar_notificacao('estudo')
        time.sleep(3)
        notif_pausa.empty()

        # pausa
        total = tempo_intervalo * 60
        for restante in range(total, -1, -1):
            if not st.session_state.rodando:
                break
            minutos, segundos = divmod(restante, 60)
            timer.metric("Pausa", f"{minutos:02d}:{segundos:02d}")
            time.sleep(velocidade)
            
        if st.session_state.rodando:
            pausa_finalizada = st.info('Pausa finalizada.')
            tocar_notificacao('pausa')
            time.sleep(3)
            timer.empty()
            pausa_finalizada.empty()
            st.session_state.rodando = False # reseta o estado ao finalizar o ciclo completo

tempo_estudo = st.slider("Tempo de estudo (em min.)", 5, 60)
tempo_intervalo = st.slider("Intervalo (em min.)", 5, 60)

col1, col2, col3, col4 = st.columns([3, 1, 1, 3]) # cria colunas invisívels pra forçar uma centralização das duas colunas c/ botao visíveis

if col2.button("Iniciar"):
    st.session_state.rodando = True
    pomodoro(tempo_estudo, tempo_intervalo)

if col3.button("Parar"):
    st.session_state.rodando = False 



# algumas estilizações

st.markdown(
        """<style>
    div[class*="stSlider"] > label > div[data-testid="stMarkdownContainer"] > p {
        font-size: 20px;
    }
        </style>
        """, unsafe_allow_html=True)

st.markdown("""
<style>
div.stSlider > div[data-baseweb="slider"] > div > div > div[role="slider"]{
    background-color: #007bff; /* Knob Color */
    box-shadow: 0px 0px 0px 0.3rem rgba(0, 123, 255, 0.2); /* Optional: Colored glow */
}
</style>
""", unsafe_allow_html=True)


st.markdown(
    """
<style>
    /* alterando a cor da alça/thumb do slider */
    div[data-baseweb="slider"] [role="slider"] {
        background-color: #00FF00 !important;
        /* Opcional: tira a bordinha padrão para o verde brilhar mais */
        border: none !important; 
        box-shadow: 0 0 5px #00FF00 !important;
    }

    
    /* tamanho do número (valor) que aparece quando arrasta a bolinha */
    div[data-baseweb="slider"] div {
        font-size: 14px !important; 
    }
</style>
    """,
    unsafe_allow_html=True
)