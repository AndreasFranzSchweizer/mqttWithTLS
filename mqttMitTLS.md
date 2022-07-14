# Mosquitto MQTT mit TLS
Eine kleine Beschreibung wie ein MQTT Brocker mit TLS abgesichert werden kann. Es wird der Mosquitto Brocker verwendet.
## Mosquitto Brocker einrichten (es werden root-Rechte benötigt)
1. ```sudo apt-add-repository ppa:mosquitto-dev/mosquitto-ppa```
2. ```sudo apt-get update```
3. ```sudo apt-get install mosquitto```
4. /etc/mosquitto/mosquitto.conf bearbeiten und die folgenden Zeilen hinzufügen

    ```
    listener 1883
    allow_anonymous true
    ```
5. Server neustarten mit 
* ```sudo service mosquitto stop```
* ```sudo service  mosquitto start```
6. Server installation mit ```ss -lt``` prüfen, ob auf Port 1883 gehört wird

## CA einrichten und Zertifikate erstellen
1. In das Verzeichnis etc/mosquitto/certs wechseln
2. Mit ```sudo openssl genrsa -des3 -out ca.key 2048``` eine Schlüsselpaar für die CA erstellen

    ---
    Info: Hier kann ein beliebiges Passwort gesetzt werden

    ---

3. Mit ```sudo openssl req -new -x509 -days 1826 -key ca.key -out ca.crt``` ein neues Zertifikat für die CA erstellen.

    ---
    Wichtig: Der Common Name muss dem Hostnamen des Brockers 
    entsprechen.

    ---

4. Ein Schlüsselpaar für Brocker erstellen mit 'sudo openssl genrsa -out server.key 2048'
5. Wir erzeugen eine Zertifizierungsanfrage für das eben erstellte Schlüsselpaar. ```sudo openssl req -new -out server.csr -key server.key```

    ---

    Wichtig die Angaben bei der Erzeugung der Zertifizierungsanfrage müssen leicht unterschiedlich sein. z.B. im Feld Organizational Unit Name, sonst denkt der Client es ist ein self signed Zertifikat. Der Common Name muss aber dem Hostnamen des Brockers entsprechen
    
    ---

    ---
    
    Zur CA müssen wir das natürlich nicht senden, das wir die CA sind.

    ---

6. Die Anfrage von 5. können wir mit dem Befehl ```sudo openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 360``` beglaubigen.
7. Nun solten wir im Verzeichnis etc/mosquitto/certs neben anderen die folgenden drei Dateien finden:
* ca.crt
* server.crt
* server.key
8. Der Eigentümer dieser Dateien muss noch auf mosquitto:mosquoitto geändert werden.
```sudo chown mosquitto:mosquitto ca.crt server.*```

## Zertifikat in Mosquitto Brocker einbinden
1. /etc/mosquitto/mosquitto.conf bearbeiten und die folgenden Zeilen ändern bzw. hinzufügen
    ```
    listener 8883
    cafile /etc/mosquitto/certs/ca.crt
    keyfile /etc/mosquitto/certs/server.key
    certfile /etc/mosquitto/certs/server.crt
    tls_version tlsv1.2
    ```
2. Server neustarten mit 
    ```
    sudo service mosquitto stop'
    sudo service  mosquitto start'
    ```
## Optional: Client Zertifikat erzeugen
1. Mit ```sudo openssl genrsa -out client.key 2048``` ein Schlüsselpaar für den Client erzeugen.
2. Nun mit dem Schlüsselpaar mit ```sudo openssl req -new -out client.csr -key client.key``` eine Zertifizierungsanfrage stellen.

    ---

    Wichtig: Der Common Name ist für Später der Benutzername um Berechtigen zu können.

    ---

3. Das Zertifikat mit der CA signieren. ```sudo openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out client.crt -days 360```
4. Nun solten wir im Verzeichnis etc/mosquitto/certs neben anderen die folgenden zwei Dateien finden:
* client.crt
* client.key