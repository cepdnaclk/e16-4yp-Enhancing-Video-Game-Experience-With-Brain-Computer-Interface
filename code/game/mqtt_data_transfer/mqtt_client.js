var move;
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
  message = new Paho.MQTT.Message("Hello");
  message.destinationName = "World";
  client.send(message);
}

// called when the client loses its connection
function onConnectionLost(responseObject) {
  if (responseObject.errorCode !== 0) {
    console.log("onConnectionLost:" + responseObject.errorMessage);
  }
}

// called when a message arrives
function onMessageArrived(message) {
  console.log("onMessageArrived:" + message.payloadString);
  move = message.payloadString;
  move = move.split(" ")[1];
  console.log("move " + move);

  if (move == "ArrowUp") {
    moveup();
    setTimeout(() => {
      clearmove();
    }, 1000);
  } else if (move == "ArrowDown") {
    movedown();
    setTimeout(() => {
      clearmove();
    }, 1000);
  } else if (move == "ArrowLeft") {
    moveleft();
    setTimeout(() => {
      clearmove();
    }, 1000);
  } else if (move == "ArrowRight") {
    moveright();
    setTimeout(() => {
      clearmove();
    }, 1000);
  }
}
