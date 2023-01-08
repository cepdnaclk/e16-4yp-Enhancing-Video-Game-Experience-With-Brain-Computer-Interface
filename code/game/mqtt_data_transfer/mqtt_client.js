var move;
const moves = ["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"];
// Create a client instance
client = new Paho.MQTT.Client("ws://broker.emqx.io:8083/mqtt", "clientId");

// set callback handlers
client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;

// connect the client
client.connect({ onSuccess: onConnect });

// called when the client connects
function onConnect() {
  // Once a connection has been made, make a subscription and send a message.
  console.log("onConnect");
  client.subscribe("bci/game");
  client.subscribe("bci/game/start/Up");
  client.subscribe("bci/game/start/Down");
  client.subscribe("bci/game/start/Left");
  client.subscribe("bci/game/start/Right");
  client.subscribe("bci/game/stop/Up");
  client.subscribe("bci/game/stop/Down");
  client.subscribe("bci/game/stop/Left");
  client.subscribe("bci/game/stop/Right");
  message = new Paho.MQTT.Message("Hello");
  message.destinationName = "bci/game";
  client.send(message);
}

// called when the client loses its connection
function onConnectionLost(responseObject) {
  if (responseObject.errorCode !== 0) {
    console.log("onConnectionLost:" + responseObject.errorMessage);
  }
}

function publishStartMessage(direction) {
  // Publish a Message
  var message = new Paho.MQTT.Message(direction + "_Start!");
  message.destinationName = "bci/game/start/" + direction;
  message.qos = 0;

  client.send(message);
}

function publishStopMessage(direction) {
  // Publish a Message
  var message = new Paho.MQTT.Message(direction + "_Stop!");
  message.destinationName = "bci/game/stop/" + direction;
  message.qos = 0;

  client.send(message);
}

// called when a message arrives
function onMessageArrived(message) {
  console.log("onMessageArrived:" + message.payloadString);
  msg = message.payloadString;
  msg = msg.split(" ")[1];

  if (moves.indexOf(msg) !== -1) {
    move = msg;
    if (move == "ArrowUp") {
      publishStartMessage("Up");
      moveup();
      setTimeout(() => {
        clearmove();
        publishStopMessage("Up");
      }, 1000);
    } else if (move == "ArrowDown") {
      publishStartMessage("Down");
      movedown();
      setTimeout(() => {
        clearmove();
        publishStopMessage("Down");
      }, 1000);
    } else if (move == "ArrowLeft") {
      publishStartMessage("Left");
      moveleft();
      setTimeout(() => {
        clearmove();
        publishStopMessage("Left");
      }, 1000);
    } else if (move == "ArrowRight") {
      publishStartMessage("Right");
      moveright();
      setTimeout(() => {
        clearmove();
        publishStopMessage("Right");
      }, 1000);
    }
  }
}
