import cv2
from ultralytics import YOLO
import time
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

# 1. Carrega as variáveis do arquivo .env
load_dotenv()

# --- CONFIGURAÇÕES CARREGADAS DO ENV ---
EMAIL_SENDER = os.getenv('EMAIL_SENDER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_RECEIVER = os.getenv('EMAIL_RECEIVER')
MODEL_PATH = os.getenv('MODEL_PATH', 'best.pt') # Usa 'best.pt' se não achar no env
CONFIDENCE = float(os.getenv('CONFIDENCE', 0.25))

# --- OUTRAS CONFIGURAÇÕES ---
# 0 para Webcam ou nome do arquivo 'video.mp4'
SOURCE = 'video.mp4' 
EMAIL_COOLDOWN = 20 
DANGEROUS_CLASSES = ['knife', 'scissors', 'sharp object', 'blade', 'weapon', 'senjata_api'] 

def enviar_email(detected_list):
    """Função que conecta no Gmail e manda o alerta"""
    # Verificação de segurança antes de tentar enviar
    if not EMAIL_SENDER or not EMAIL_PASSWORD or not EMAIL_RECEIVER:
        print("❌ ERRO: Credenciais de e-mail não configuradas no arquivo .env")
        return False

    print(f"📧 Iniciando envio de e-mail para {EMAIL_RECEIVER}...")
    try:
        msg = MIMEText(f"ALERTA DE SEGURANÇA VISIONGUARD.\n\nO sistema detectou os seguintes objetos perigosos: {detected_list}.\n\nPor favor, verifique as câmeras imediatamente.")
        msg['Subject'] = f"🚨 PERIGO DETECTADO: {detected_list[0]}"
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        
        print("✅ E-MAIL ENVIADO COM SUCESSO!")
        return True
    except Exception as e:
        print(f"❌ FALHA AO ENVIAR E-MAIL: {e}")
        return False

def main():
    print("🧠 Carregando o modelo...")
    try:
        model = YOLO(MODEL_PATH)
    except Exception as e:
        print(f"❌ Erro ao carregar modelo ({MODEL_PATH}): {e}")
        return

    cap = cv2.VideoCapture(SOURCE)
    
    if not cap.isOpened():
        print(f"❌ Erro ao abrir: {SOURCE}")
        return

    print("✅ Sistema iniciado! Leitura de variáveis de ambiente OK.")
    
    total_detections_count = 0
    last_email_time = 0

    while True:
        success, frame = cap.read()
        if not success:
            break

        results = model(frame, conf=CONFIDENCE, verbose=False)
        annotated_frame = frame.copy() 

        alert_triggered = False
        detected_names_in_frame = []

        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                class_name = model.names[cls_id]
                confidence = float(box.conf[0])
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                is_dangerous = False
                if class_name.lower() in DANGEROUS_CLASSES or 'knife' in class_name.lower():
                    is_dangerous = True
                
                if is_dangerous:
                    total_detections_count += 1
                    alert_triggered = True
                    detected_names_in_frame.append(class_name)

                    cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
                    cv2.putText(annotated_frame, f"{class_name} ({confidence:.2f})", (x1, y1 - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                else:
                    cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        if alert_triggered:
            cv2.putText(annotated_frame, f"PERIGO! Total: {total_detections_count}", (20, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            
            current_time = time.time()
            if (current_time - last_email_time) > EMAIL_COOLDOWN:
                cv2.putText(annotated_frame, "ENVIANDO EMAIL...", (20, 100), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)
                
                email_sent = enviar_email(detected_names_in_frame)
                
                if email_sent:
                    last_email_time = current_time
            else:
                tempo_restante = int(EMAIL_COOLDOWN - (current_time - last_email_time))
                print(f"⏳ Aguardando cooldown ({tempo_restante}s)...")

        cv2.imshow("VisionGuard MVP", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"🛑 Fim. Total de detecções: {total_detections_count}")

if __name__ == "__main__":
    main()