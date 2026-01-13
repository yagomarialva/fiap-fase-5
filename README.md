# 🛡️ VisionGuard - Sistema de Monitoramento Inteligente (MVP)

> **Projeto desenvolvido para o Hackathon FIAP - Pós Tech em IA para Devs.**

O **VisionGuard** é um MVP (Produto Viável Mínimo) de Visão Computacional projetado para identificar proativamente objetos cortantes e armas em ambientes monitorados por câmeras de segurança (CFTV). Utilizando Inteligência Artificial (YOLOv8), o sistema detecta ameaças em tempo real e envia alertas automáticos para uma central de segurança.

---

## 🎯 Objetivos do Projeto
Este projeto foi desenvolvido para atender aos requisitos técnicos do desafio:
- [x] **Dataset:** Utilização de dataset anotado contendo facas, tesouras e armas (Fonte: Roboflow Universe).
- [x] **Treinamento Supervisionado:** Modelo treinado via Transfer Learning utilizando YOLOv8.
- [x] **Redução de Falsos Positivos:** O sistema diferencia objetos inofensivos (celulares, copos) de ameaças reais.
- [x] **Sistema de Alertas:** Envio automático de e-mail com log da ocorrência ao detectar perigo.

---

## 🚀 Funcionalidades

* **Detecção em Tempo Real:** Processamento de vídeo ou webcam com baixa latência.
* **Filtragem de Classes:** Alerta apenas para objetos específicos (`knife`, `scissors`, `weapon`, etc.), ignorando outras classes.
* **Feedback Visual:**
    * 🟩 **Verde:** Objetos seguros ou não listados como perigo.
    * 🟥 **Vermelho:** Ameaça detectada (desenha bounding box e nome da classe).
* **Cooldown de Alertas:** Sistema inteligente que evita spam, enviando apenas um e-mail a cada X segundos caso a ameaça persista.
* **Log de Console:** Registro detalhado de detecções para auditoria.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.9+
* **Modelo de IA:** YOLOv8 (Ultralytics) - Versão Nano (otimizada para Edge Computing/Mac M1).
* **Processamento de Imagem:** OpenCV.
* **Notificação:** Protocolo SMTP (Gmail).

---

## 📦 Instalação e Configuração

Siga os passos abaixo para rodar o projeto localmente.

### 1. Pré-requisitos
* Python instalado.
* Git instalado.

### 2. Clonar o Repositório
```bash
git clone [https://github.com/SEU-USUARIO/VisionGuard-MVP.git](https://github.com/SEU-USUARIO/VisionGuard-MVP.git)
cd VisionGuard-MVP