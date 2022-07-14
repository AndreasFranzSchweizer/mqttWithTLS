#import the client library
import paho.mqtt.client as mqtt 

#set brocker adress
broker_address="r023-01"
#set brocker port 1883 for unsecure 8883 for tls connections
broker_port=8883
#create new instance with ClientID = ClientID (should be unique for production environment)
print("creating new instance")
client = mqtt.Client("ClientID")
#client.tls_set('/home/sca/media/sca_auf_server/certs/ca.crt',tls_version=2)
client.tls_set('/home/sca/media/sca_auf_server/certs/ca.crt','/home/sca/media/sca_auf_server/certs/client.crt','/home/sca/media/sca_auf_server/certs/client.key',tls_version=2)

#connect to broker with procker_address
print("connecting to broker")
client.connect(broker_address,broker_port) 

#publich a message
print("Publishing message to topic","house/bulbs/bulb1")
client.publish("house/bulbs/bulb1","OFF")