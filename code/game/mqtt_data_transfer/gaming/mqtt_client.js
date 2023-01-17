var move;
const moves = ["Up", "Down", "Left", "Right"];
// Create a client instance
client = new Paho.MQTT.Client("ws://broker.emqx.io:8083/mqtt", "clientId1");

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

// function publishStartMessage(direction) {
//   // Publish a Message
//   var message = new Paho.MQTT.Message(direction + "_Start!");
//   message.destinationName = "bci/game/start/" + direction;
//   message.qos = 0;

//   client.send(message);
// }

// called when a message arrives
function onMessageArrived(message) {
  console.log("onMessageArrived:" + message.payloadString);
  msg = message.payloadString;
  msg = msg.split(" ")[1];

  if (moves.indexOf(msg) !== -1) {
    move = msg;
    if (move == "Up") {
      moveup();
      setTimeout(() => {
        clearmove();
      }, 1000);
    } else if (move == "Down") {
      movedown();
      setTimeout(() => {
        clearmove();
      }, 1000);
    } else if (move == "Left") {
      moveleft();
      setTimeout(() => {
        clearmove();
      }, 1000);
    } else if (move == "Right") {
      moveright();
      setTimeout(() => {
        clearmove();
      }, 1000);
    }
  }
}
