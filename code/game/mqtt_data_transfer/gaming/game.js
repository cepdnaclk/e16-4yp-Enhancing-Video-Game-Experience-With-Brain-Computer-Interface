var myGamePiece;

var target;

// Function to generate random number
function randomNumber(min, max) {
  return Math.random() * (max - min) + min;
}

var game_piece_x = randomNumber(50, 450);
var game_piece_y = randomNumber(50, 350);

var target_piece_x = randomNumber(50, 450);
var target_piece_y = randomNumber(50, 350);

// function myFunction(event) {
//   var x = event.key;
//   document.getElementById("demo").innerHTML = "The pressed key was: " + x;

//   if (x == "ArrowUp") {
//     moveup();
//   } else if (x == "ArrowDown") {
//     movedown();
//   } else if (x == "ArrowLeft") {
//     moveleft();
//   } else if (x == "ArrowRight") {
//     moveright();
//   }
// }

function startGame() {
  myGamePiece = new component(40, 40, "red", game_piece_x, game_piece_y);
  target = new component(
    40,
    40,
    "blue",
    target_piece_x + 20,
    target_piece_y - 20
  );

  myGameArea.start();
}

var myGameArea = {
  canvas: document.createElement("canvas"),
  start: function () {
    this.canvas.width = 480;
    this.canvas.height = 480;
    this.context = this.canvas.getContext("2d");
    document.body.insertBefore(this.canvas, document.body.childNodes[0]);
    this.interval = setInterval(updateGameArea, 1000);
  },
  clear: function () {
    this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
  },
};

function component(width, height, color, x, y) {
  this.width = width;
  this.height = height;
  this.speedX = 0;
  this.speedY = 0;
  this.x = x;
  this.y = y;
  this.update = function () {
    ctx = myGameArea.context;
    ctx.fillStyle = color;
    ctx.fillRect(this.x, this.y, this.width, this.height);
  };
  this.newPos = function () {
    this.x += this.speedX;
    this.y += this.speedY;
  };
}

function updateGameArea() {
  myGameArea.clear();

  target.update();
  myGamePiece.newPos();
  myGamePiece.update();
}

function moveup() {
  myGamePiece.speedY = -25;
}

function movedown() {
  myGamePiece.speedY = 25;
}

function moveleft() {
  myGamePiece.speedX = -25;
}

function moveright() {
  myGamePiece.speedX = 25;
}

function clearmove() {
  myGamePiece.speedX = 0;
  myGamePiece.speedY = 0;
}
