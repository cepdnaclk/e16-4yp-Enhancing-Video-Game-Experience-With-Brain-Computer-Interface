var myGamePiece;
var target;
var move_used = "";
var key = "";

const all_moves = ["Up", "Down", "Left", "Right"];

var d = new Date();
var n = d.toLocaleTimeString();
console.log("complete game " + n);

// Function to generate random number
function randomNumber(min, max) {
  return Math.floor(Math.random() * (max - min)) + min;
}

function select_shift() {
  shift = randomNumber(80, 150);
  var d = new Date();
  var n = d.toLocaleTimeString();
  console.log("shift " + n);

  console.log("shift " + shift);

  all_shifts = {
    Right: [shift, 0],
    Down: [0, shift],
    Left: [-1 * shift, 0],
    Up: [0, -1 * shift],
  };

  // get random index value
  const randomIndex = Math.floor(Math.random() * all_moves.length);

  // get random item
  key = all_moves[randomIndex];

  move_used = key;

  const item = all_shifts[key];
  console.log("item " + item + " move " + move_used);
  var d = new Date();
  var n = d.toLocaleTimeString();
  console.log("item shift " + n);

  return item;
}

var game_piece_x = randomNumber(100, 350);
var game_piece_y = randomNumber(100, 300);

var shift_val;

var target_x_shift = 0;
var target_y_shift = 0;

// console.log("x " + game_piece_x + " " + game_piece_x + target_x_shift);
// console.log("y " + game_piece_y + " " + game_piece_y + target_y_shift);

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
    game_piece_x + target_x_shift,
    game_piece_y + target_y_shift
  );

  setTimeout(function () {
    myGameArea.start();
  }, 1000);
}

var myGameArea = {
  canvas: document.createElement("canvas"),
  start: function () {
    this.canvas.width = 480;
    this.canvas.height = 480;
    this.context = this.canvas.getContext("2d");
    document.body.insertBefore(this.canvas, document.body.childNodes[0]);
    this.frameNo = 0;
    this.interval = setInterval(function () {
      updateGameArea();

      var d = new Date();
      var n = d.toLocaleTimeString();
      console.log("game " + n);
    }, 5000);
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
  myGameArea.frameNo += 1;

  shift_val = select_shift();

  target_x_shift = shift_val[0];
  target_y_shift = shift_val[1];
  // console.log("Target changed!");

  target.x = game_piece_x + target_x_shift;
  target.y = game_piece_y + target_y_shift;
  target.update();
  myGamePiece.newPos();
  myGamePiece.update();
}

function everyinterval(n) {
  if ((myGameArea.frameNo / n) % 1 == 0) {
    return true;
  }
  return false;
}

function moveup() {
  myGamePiece.speedY = -10;
}

function movedown() {
  myGamePiece.speedY = 10;
}

function moveleft() {
  myGamePiece.speedX = -10;
}

function moveright() {
  myGamePiece.speedX = 10;
}

function clearmove() {
  myGamePiece.speedX = 0;
  myGamePiece.speedY = 0;
}
