import cv2
from ultralytics import YOLO
import time

# --- CONFIGURAÇÕES ---
MODEL_PATH = 'best.pt'      
CONFIDENCE = 0.15            
SOURCE = 'video.mp4'        

# Lista de perigo
DANGEROUS_CLASSES = ['knife', 'scissors', 'sharp object', 'blade', 'weapon'] 

def main():
    print("🧠 Carregando o modelo...")
    try:
        model = YOLO(MODEL_PATH)
    except Exception as e:
        print(f"❌ Erro ao carregar best.pt: {e}")
        return

    print(f"📋 Classes que o modelo conhece: {model.names}")
    
    cap = cv2.VideoCapture(SOURCE)
    
    if not cap.isOpened():
        print(f"❌ Erro ao abrir: {SOURCE}")
        return

    print("✅ Sistema iniciado! Olhe o terminal para ver a contagem.")
    
    total_detections_count = 0

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

                # --- DEBUG ---
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
                    cv2.putText(annotated_frame, class_name, (x1, y1 - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        if alert_triggered:
            cv2.putText(annotated_frame, f"PERIGO! Total: {total_detections_count}", (20, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            
            print(f"🚨 ALERTA #{total_detections_count}: Detectado {detected_names_in_frame}")

        cv2.imshow("Monitoramento - Contagem", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"🛑 Fim. Total de detecções de perigo: {total_detections_count}")

if __name__ == "__main__":
    main()