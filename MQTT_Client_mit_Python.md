# MQTT Client mit Python
1. package paho-mqtt unter Tools->Manage Package installieren
2. Mit ```import paho.mqtt.client as mqtt``` die Bibliothek bekannt machen
3. Eine Instanz mit ```client = mqtt.Client("ClientID")```erzeugen
4. Mit ```client.connect(broker_address,broker_port)``` wird eine Verbindung hergestellt.
5. Die Methode publish, veröffentliche ine Nachricht auf der Topic. ```client.publish("Topic","Value")```
## Optional TLS mit CA
```client.tls_set('ca.crt',tls_version=2)```
## Optional TLS mit Client Zertifikat
```client.tls_set('ca.crt','client.crt','client.key',tls_version=2)```
