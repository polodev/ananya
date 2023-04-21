// var random1 = parseInt(Math.random() * 255)
// var random2 = parseInt(Math.random() * 255)
// var random3 = parseInt(Math.random() * 255)
// document.body.style.backgroundColor = `rgb(${random1}, ${random2}, ${random3})`;
var materials = ['#e53935', '#d32f2f', '#c62828', '#b71c1c', '#d81b60', '#c2185b', '#ad1457', '#880e4f', '#8e24aa', '#7b1fa2', '#6a1b9a', '#4a148c', '#5e35b1', '#512da8', '#4527a0', '#311b92', '#3949ab', '#303f9f', '#283593', '#1a237e', '#1e88e5', '#1976d2', '#1565c0', '#0d47a1', '#039be5', '#0288d1', '#0277bd', '#01579b', '#00acc1', '#0097a7', '#00838f', '#006064', '#00897b', '#00796b', '#00695c', '#004d40', '#43a047', '#388e3c', '#2e7d32', '#1b5e20', '#7cb342', '#689f38', '#558b2f', '#33691e', '#c0ca33', '#afb42b', '#9e9d24', '#827717', '#fdd835', '#fbc02d', '#f9a825', '#f57f17', '#ffb300', '#ffa000', '#ff8f00', '#ff6f00', '#fb8c00', '#f57c00', '#ef6c00', '#e65100', '#f4511e', '#e64a19', '#d84315', '#bf360c', '#6d4c41', '#5d4037', '#4e342e', '#3e2723', '#757575', '#616161', '#424242', '#212121', '#546e7a', '#455a64', '#37474f', '#263238',]
var flat = ["#1abc9c", "#2ecc71", "#3498db", "#9b59b6", "#34495e", "#16a085", "#27ae60", "#2980b9", "#8e44ad", "#2c3e50", "#f1c40f", "#e67e22", "#e74c3c", "#95a5a6", "#f39c12", "#d35400", "#c0392b", "#7f8c8d", ];
var matbg = ['#ee6e73'];
var colors = materials.concat(flat, matbg);

function backgroundColor (element) {
  var random_number = parseInt(Math.random() * colors.length)
  console.log(random_number)
  console.log(colors[random_number])
  element.style.backgroundColor = colors[random_number];
}
var colorDiv = document.querySelectorAll('.random_color');
for (var i = 0; i < colorDiv.length; i++) {
  backgroundColor(colorDiv[i]);
}
