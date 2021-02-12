function bar() {
  var newDeadline = document.createElement("div");
  newDeadline.className = "deadline";
  var newSubject = document.createElement("div");
  newSubject.className = "subject";
  var newOpen = documet.createElement("a");
  newOpen.className = "open";

  var newlist = document.createElement("li");
  newlist.className = "elem";
  newlist.appendChild(newDeadline);
  newlist.appendChild(newSubject);
  newlist.appendChild(newOpen);

  var board = document.getElementById("left_tasks");
  board.appendChild(newlist)
}
