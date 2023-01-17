var shared_move;

// Create a client instance
client = new Paho.MQTT.Client("ws://broker.emqx.io:8083/mqtt", "clientId1");

// set callback handlers
client.onConnectionLost = onConnectionLost;

client.onMessageDelivered = onMessageDelivered;

// connect the client
client.connect({ onSuccess: onConnect });

// called when the client connects
function onConnect() {
  // Once a connection has been made, make a subscription and send a message.
  console.log("onConnect");
  client.subscribe("bci/game/training");

  message = new Paho.MQTT.Message("Hello");
  message.destinationName = "bci/game/training";
  client.send(message);

  shared_move = move_used;

  setInterval(function () {
    publishMessage();
  }, 5000);
}

// called when the client loses its connection
function onConnectionLost(responseObject) {
  if (responseObject.errorCode !== 0) {
    console.log("onConnectionLost:" + responseObject.errorMessage);
  }
}

function publishMessage() {
  shared_move = move_used;
  console.log("shared_move " + shared_move);
  var d = new Date();
  var n = d.toLocaleTimeString();
  console.log("shared_move " + n);
  // Publish a Message
  var message = new Paho.MQTT.Message(shared_move + "_Start!");
  message.destinationName = "bci/game/training/start/" + shared_move;
  message.qos = 0;

  client.send(message);
  var d = new Date();
  var n = d.toLocaleTimeString();

  console.log("start " + n);

  setTimeout(function () {
    var message = new Paho.MQTT.Message(shared_move + "_Stop!");
    message.destinationName = "bci/game/training/stop/" + shared_move;
    message.qos = 0;

    client.send(message);
    var d = new Date();
    var n = d.toLocaleTimeString();

    console.log("stop " + n);
  }, 3000);
}

// function publishStopMessage(direction) {
//   // Publish a Message
//   var message = new Paho.MQTT.Message(direction + "_Stop!");
//   message.destinationName = "bci/game/training/stop/" + direction;
//   message.qos = 0;

//   client.send(message);
// }

function onMessageDelivered(msg) {
  console.log(
    "onMessageDelivered: " +
      msg.payloadString +
      " has been successfully delivered."
  );
}

// // called when a message arrives
// function onMessageArrived(message) {
//   console.log("onMessageArrived:" + message.payloadString);
//   msg = message.payloadString;
//   msg = msg.split(" ")[1];

//   if (moves.indexOf(msg) !== -1) {
//     move = msg;
//     if (move == "ArrowUp") {
//       moveup();
//       setTimeout(() => {
//         clearmove();
//       }, 1000);
//     } else if (move == "ArrowDown") {
//       movedown();
//       setTimeout(() => {
//         clearmove();
//       }, 1000);
//     } else if (move == "ArrowLeft") {
//       moveleft();
//       setTimeout(() => {
//         clearmove();
//       }, 1000);
//     } else if (move == "ArrowRight") {
//       moveright();
//       setTimeout(() => {
//         clearmove();
//       }, 1000);
//     }
//   }
// }
